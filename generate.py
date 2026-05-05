#!/usr/bin/env python3
"""
ANZO Capital SEO Report Generator
----------------------------------
Converts Google Search Console ZIP exports into a report JSON file
and updates reports/manifest.json automatically.

Usage:
  python generate.py --type monthly --period 2026-05

The script expects GSC export ZIPs in a folder (default: ./gsc-exports/).
Name your ZIPs with the date in the filename, e.g.:
  anzocapital.com-Performance-on-Search-2026-05-31.zip
  anzocapital.com-Coverage-2026-05-31.zip
  anzocapital.com-core-web-vitals-2026-05-31.zip        (desktop)
  anzocapital.com-core-web-vitals-2026-05-31 (1).zip    (mobile)
  anzocapital.com-FAQ-2026-05-31.zip
  anzocapital.com-Breadcrumbs-2026-05-31.zip
"""

import argparse
import csv
import json
import os
import re
import sys
import tempfile
import zipfile
from datetime import date, timedelta
from pathlib import Path

# ── Branded query detection ────────────────────────────────────────
BRANDED_TERMS = ["anzo", "anzocapital", "昂首资本"]

def is_branded(query: str) -> bool:
    q = query.lower()
    return any(t in q for t in BRANDED_TERMS)


# ── CSV readers ───────────────────────────────────────────────────
def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def find_zip(folder: Path, keyword: str, exclude: str = None) -> Path | None:
    """Find a ZIP file in folder whose name contains keyword."""
    candidates = sorted(folder.glob("*.zip"))
    for z in candidates:
        name = z.name.lower()
        if keyword.lower() in name:
            if exclude and exclude.lower() in name:
                continue
            return z
    return None


def extract_zip(zip_path: Path, dest: Path):
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)


# ── Period helpers ────────────────────────────────────────────────
MONTH_NAMES = ["","January","February","March","April","May","June",
               "July","August","September","October","November","December"]
MONTH_SHORT = ["","Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]

def period_meta(report_type: str, period_str: str) -> dict:
    """
    period_str formats:
      monthly:   YYYY-MM         e.g. 2026-05
      weekly:    YYYY-WNN        e.g. 2026-W18
      quarterly: YYYY-QN         e.g. 2026-Q2
      yearly:    YYYY            e.g. 2026
    Returns dict with id, label, year, dateStart, dateEnd, comparePeriod, etc.
    """
    if report_type == "monthly":
        year, month = int(period_str[:4]), int(period_str[5:7])
        # first and last day
        d_start = date(year, month, 1)
        if month == 12:
            d_end = date(year, 12, 31)
        else:
            d_end = date(year, month + 1, 1) - timedelta(days=1)
        # compare = previous month
        if month == 1:
            py, pm = year - 1, 12
        else:
            py, pm = year, month - 1
        compare = f"{MONTH_NAMES[pm]} {py}"
        return {
            "id":            f"{year}-{month:02d}-monthly",
            "type":          "monthly",
            "label":         f"{MONTH_NAMES[month]} {year}",
            "year":          year,
            "month":         month,
            "dateStart":     d_start.isoformat(),
            "dateEnd":       d_end.isoformat(),
            "comparePeriod": compare,
        }

    elif report_type == "weekly":
        # period_str = YYYY-WNN
        year = int(period_str[:4])
        week = int(period_str[6:])
        d_start = date.fromisocalendar(year, week, 1)
        d_end   = date.fromisocalendar(year, week, 7)
        prev_start = d_start - timedelta(weeks=1)
        prev_end   = d_end   - timedelta(weeks=1)
        compare = f"W{prev_start.isocalendar().week:02d} {prev_start.year}"
        return {
            "id":            f"{year}-W{week:02d}-weekly",
            "type":          "weekly",
            "label":         f"W{week:02d} {year}  ({d_start} – {d_end})",
            "year":          year,
            "week":          week,
            "dateStart":     d_start.isoformat(),
            "dateEnd":       d_end.isoformat(),
            "comparePeriod": compare,
        }

    elif report_type == "quarterly":
        year = int(period_str[:4])
        quarter = int(period_str[6])
        month_start = (quarter - 1) * 3 + 1
        month_end   = quarter * 3
        d_start = date(year, month_start, 1)
        if month_end == 12:
            d_end = date(year, 12, 31)
        else:
            d_end = date(year, month_end + 1, 1) - timedelta(days=1)
        pq = quarter - 1 if quarter > 1 else 4
        py = year if quarter > 1 else year - 1
        compare = f"Q{pq} {py}"
        return {
            "id":            f"{year}-Q{quarter}-quarterly",
            "type":          "quarterly",
            "label":         f"Q{quarter} {year}",
            "year":          year,
            "quarter":       quarter,
            "dateStart":     d_start.isoformat(),
            "dateEnd":       d_end.isoformat(),
            "comparePeriod": compare,
        }

    elif report_type == "yearly":
        year = int(period_str)
        return {
            "id":            f"{year}-yearly",
            "type":          "yearly",
            "label":         str(year),
            "year":          year,
            "dateStart":     f"{year}-01-01",
            "dateEnd":       f"{year}-12-31",
            "comparePeriod": str(year - 1),
        }
    else:
        raise ValueError(f"Unknown report type: {report_type}")


# ── Data parsers ──────────────────────────────────────────────────
def parse_performance(folder: Path) -> dict:
    """Parse GSC performance export folder into structured data."""

    def to_int(s):   return int(s.replace(",", "")) if s else 0
    def to_float(s): return float(s.replace("%", "").replace(",", "")) if s else 0.0

    # Detect column name patterns (GSC uses date ranges in column headers)
    def get_cols(row):
        keys = list(row.keys())
        cur_clicks  = next((k for k in keys if "Clicks" in k and "4/" in k), None) or \
                      next((k for k in keys if "Clicks" in k), None)
        prev_clicks = next((k for k in keys if "Clicks" in k and k != cur_clicks), None)
        cur_impr    = next((k for k in keys if "Impressions" in k and "4/" in k), None) or \
                      next((k for k in keys if "Impressions" in k), None)
        prev_impr   = next((k for k in keys if "Impressions" in k and k != cur_impr), None)
        cur_ctr     = next((k for k in keys if "CTR" in k and "4/" in k), None) or \
                      next((k for k in keys if "CTR" in k), None)
        cur_pos     = next((k for k in keys if "Position" in k and "4/" in k), None) or \
                      next((k for k in keys if "Position" in k), None)
        prev_pos    = next((k for k in keys if "Position" in k and k != cur_pos), None)
        return cur_clicks, prev_clicks, cur_impr, prev_impr, cur_ctr, cur_pos, prev_pos

    result = {}

    # ── Queries
    queries_file = folder / "Queries.csv"
    if queries_file.exists():
        rows = read_csv(queries_file)
        if rows:
            cc, pc, ci, pi, ctr_col, cp, pp = get_cols(rows[0])
            queries = []
            branded_clicks = branded_clicks_prev = branded_impr = branded_impr_prev = 0
            nb_clicks = nb_clicks_prev = nb_impr = nb_impr_prev = 0
            total_clicks = total_clicks_prev = total_impr = total_impr_prev = 0

            for row in rows:
                q = row.get(list(row.keys())[0], "")
                c   = to_int(row.get(cc, "0"))
                cp_ = to_int(row.get(pc, "0")) if pc else 0
                i   = to_int(row.get(ci, "0"))
                ip  = to_int(row.get(pi, "0")) if pi else 0
                ctr = to_float(row.get(ctr_col, "0"))
                pos = to_float(row.get(cp, "0"))
                pos_p = to_float(row.get(pp, "0")) if pp else None

                total_clicks += c; total_clicks_prev += cp_
                total_impr   += i; total_impr_prev   += ip

                if is_branded(q):
                    branded_clicks += c; branded_clicks_prev += cp_
                    branded_impr   += i; branded_impr_prev   += ip
                else:
                    nb_clicks += c; nb_clicks_prev += cp_
                    nb_impr   += i; nb_impr_prev   += ip

                queries.append({
                    "query": q, "clicks": c, "clicksPrev": cp_,
                    "impressions": i, "ctr": round(ctr, 2),
                    "position": round(pos, 2),
                    "positionPrev": round(pos_p, 2) if pos_p else None
                })

            result["queries"] = queries[:50]
            result["branded"] = {
                "clicks":       {"current": branded_clicks, "previous": branded_clicks_prev},
                "impressions":  {"current": branded_impr,   "previous": branded_impr_prev},
                "ctr":          round(branded_clicks / branded_impr * 100, 1) if branded_impr else 0,
                "shareOfClicks": round(branded_clicks / total_clicks * 100, 1) if total_clicks else 0,
            }
            result["nonBranded"] = {
                "clicks":       {"current": nb_clicks, "previous": nb_clicks_prev},
                "impressions":  {"current": nb_impr,   "previous": nb_impr_prev},
                "ctr":          round(nb_clicks / nb_impr * 100, 2) if nb_impr else 0,
                "shareOfClicks": round(nb_clicks / total_clicks * 100, 1) if total_clicks else 0,
            }

    # ── Pages
    pages_file = folder / "Pages.csv"
    if pages_file.exists():
        rows = read_csv(pages_file)
        if rows:
            cc, pc, ci, pi, ctr_col, cp_col, pp = get_cols(rows[0])
            pages = []
            for row in rows[:30]:
                url = row.get(list(row.keys())[0], "")
                display = url.replace("https://www.anzocapital.com", "") \
                             .replace("https://my.anzocapital.com", "my:") \
                             .replace("https://ai.anzocapital.com", "ai:")
                pages.append({
                    "page": url,
                    "displayPage": display[:70],
                    "clicks":      to_int(row.get(cc, "0")),
                    "clicksPrev":  to_int(row.get(pc, "0")) if pc else 0,
                    "impressions": to_int(row.get(ci, "0")),
                    "ctr":         to_float(row.get(ctr_col, "0")),
                    "position":    to_float(row.get(cp_col, "0")),
                })
            result["pages"] = pages

    # ── Countries
    countries_file = folder / "Countries.csv"
    FLAG_MAP = {
        "nigeria":"🇳🇬","kenya":"🇰🇪","philippines":"🇵🇭","taiwan":"🇹🇼",
        "malaysia":"🇲🇾","hong kong":"🇭🇰","united states":"🇺🇸","india":"🇮🇳",
        "singapore":"🇸🇬","indonesia":"🇮🇩","united kingdom":"🇬🇧","australia":"🇦🇺",
        "japan":"🇯🇵","south africa":"🇿🇦","vietnam":"🇻🇳","thailand":"🇹🇭",
    }
    if countries_file.exists():
        rows = read_csv(countries_file)
        if rows:
            cc, pc, _, _, _, cp_col, _ = get_cols(rows[0])
            ctr_col = next((k for k in rows[0].keys() if "CTR" in k), None)
            countries = []
            for row in rows[:15]:
                name = row.get(list(row.keys())[0], "")
                countries.append({
                    "country":    name,
                    "flag":       FLAG_MAP.get(name.lower(), "🌍"),
                    "clicks":     to_int(row.get(cc, "0")),
                    "clicksPrev": to_int(row.get(pc, "0")) if pc else 0,
                    "ctr":        to_float(row.get(ctr_col, "0")),
                    "position":   to_float(row.get(cp_col, "0")),
                })
            result["countries"] = countries

    # ── Devices
    devices_file = folder / "Devices.csv"
    DEVICE_ICON = {"mobile": "📱", "desktop": "🖥", "tablet": "📟"}
    if devices_file.exists():
        rows = read_csv(devices_file)
        if rows:
            cc, pc, _, _, _, cp_col, _ = get_cols(rows[0])
            ctr_col = next((k for k in rows[0].keys() if "CTR" in k), None)
            impr_col = next((k for k in rows[0].keys() if "Impressions" in k and "4/" in k), None)
            devices = []
            for row in rows:
                name = row.get(list(row.keys())[0], "")
                devices.append({
                    "device":      name,
                    "icon":        DEVICE_ICON.get(name.lower(), ""),
                    "clicks":      to_int(row.get(cc, "0")),
                    "clicksPrev":  to_int(row.get(pc, "0")) if pc else 0,
                    "impressions": to_int(row.get(impr_col, "0")) if impr_col else 0,
                    "ctr":         to_float(row.get(ctr_col, "0")),
                    "position":    to_float(row.get(cp_col, "0")),
                })
            result["devices"] = devices

    return result


def parse_coverage(folder: Path) -> dict:
    result = {"issues": [], "notIndexedTrend": [], "richResults": [], "richResultsTrend": {}}

    issues_file = folder / "Critical issues.csv"
    if issues_file.exists():
        for row in read_csv(issues_file):
            reason = row.get("Reason", "")
            pages  = int(row.get("Pages", "0").replace(",", "") or 0)
            if reason:
                result["issues"].append({
                    "reason":   reason,
                    "source":   row.get("Source", ""),
                    "current":  pages,
                    "previous": 0,  # will be filled from prior report if available
                })

    chart_file = folder / "Chart.csv"
    if chart_file.exists():
        rows = read_csv(chart_file)
        # Sample weekly
        sampled = rows[::7]
        for row in sampled:
            d = row.get("Date", "")
            v = row.get("Not indexed", "0") or "0"
            try:
                result["notIndexedTrend"].append({
                    "date":  d[5:],  # strip year → MM-DD
                    "value": int(v)
                })
            except ValueError:
                pass

    return result


def parse_cwv(mobile_folder: Path, desktop_folder: Path) -> dict:
    STATUS_MAP = {"poor": "poor", "need improvement": "needs", "good": "good"}

    def parse_device(folder: Path, device: str) -> dict:
        result = {
            "lcp": {"status": "good", "label": "No data", "urls": 0, "good": 100, "needs": 0, "poor": 0, "target": "<2.5s"},
            "inp": {"status": "good", "label": "No data", "urls": 0, "good": 100, "needs": 0, "poor": 0, "target": "<200ms"},
            "cls": {"status": "good", "label": "No data", "urls": 0, "good": 100, "needs": 0, "poor": 0, "target": "<0.1"},
        }
        table_file = folder / "Table.csv"
        if not table_file.exists():
            return result
        for row in read_csv(table_file):
            issue = row.get("Issue", "").lower()
            severity = STATUS_MAP.get(row.get("Severity", "").lower(), "good")
            urls = int(row.get("URLs", "0").replace(",", "") or 0)

            metric = None
            if "lcp" in issue: metric = "lcp"
            elif "inp" in issue: metric = "inp"
            elif "cls" in issue: metric = "cls"
            if not metric:
                continue

            if severity in ("poor", "needs"):
                result[metric]["status"] = severity if severity == "poor" else \
                    ("poor" if result[metric]["status"] == "poor" else "needs")
                result[metric]["urls"] = urls
                if metric == "lcp":
                    result[metric]["label"] = ">4s" if severity == "poor" else "2.5–4s"
                elif metric == "inp":
                    result[metric]["label"] = ">500ms" if severity == "poor" else "200–500ms"
                elif metric == "cls":
                    result[metric]["label"] = ">0.25" if severity == "poor" else "0.1–0.25"

                if severity == "poor":
                    result[metric]["poor"] = 100
                    result[metric]["good"] = result[metric]["needs"] = 0
                else:
                    result[metric]["needs"] = 100
                    result[metric]["good"] = result[metric]["poor"] = 0
        return result

    return {
        "mobile":  parse_device(mobile_folder, "mobile"),
        "desktop": parse_device(desktop_folder, "desktop"),
    }


def parse_rich_results(faq_folder: Path, bc_folder: Path, prev_faq=1, prev_bc=1) -> dict:
    rich = []

    def count_valid(folder: Path) -> int:
        chart = folder / "Chart.csv"
        if not chart.exists():
            return 0
        rows = read_csv(chart)
        if not rows:
            return 0
        last = rows[-1]
        return int(last.get("Valid", "0") or 0)

    def build_trend(folder: Path, key="Valid"):
        chart = folder / "Chart.csv"
        if not chart.exists():
            return [], []
        rows = read_csv(chart)
        sampled = rows[::7]
        labels = [r["Date"][5:] for r in sampled]
        vals   = [int(r.get(key, "0") or 0) for r in sampled]
        return labels, vals

    faq_valid = count_valid(faq_folder)
    bc_valid  = count_valid(bc_folder)

    rich.append({"type": "FAQ Schema",  "validCurrent": faq_valid, "validPrevious": prev_faq, "issues": "None", "status": "good"})
    rich.append({"type": "Breadcrumbs", "validCurrent": bc_valid,  "validPrevious": prev_bc,  "issues": "None", "status": "good"})

    labels, faq_trend = build_trend(faq_folder)
    _,      bc_trend  = build_trend(bc_folder)

    return {
        "richResults": rich,
        "richResultsTrend": {"labels": labels, "faq": faq_trend, "breadcrumbs": bc_trend}
    }


def parse_opportunities(pages: list, min_impr=500, max_ctr=2.0) -> list:
    opps = []
    for p in pages:
        if p["impressions"] >= min_impr and p["ctr"] < max_ctr:
            opps.append({
                "page":        p["page"].replace("https://www.anzocapital.com", ""),
                "impressions": p["impressions"],
                "clicks":      p["clicks"],
                "ctr":         p["ctr"],
                "position":    p["position"],
                "opportunity": "Review title tag and meta description. Consider adding FAQ schema.",
            })
    opps.sort(key=lambda x: x["impressions"], reverse=True)
    return opps[:15]


# ── Manifest helpers ──────────────────────────────────────────────
def load_manifest(manifest_path: Path) -> dict:
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return {"reports": []}


def update_manifest(manifest_path: Path, entry: dict):
    data = load_manifest(manifest_path)
    data["reports"] = [r for r in data["reports"] if r["id"] != entry["id"]]
    data["reports"].append(entry)
    data["reports"].sort(key=lambda r: r["dateStart"])
    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Updated manifest: {manifest_path}")


# ── Main ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate an ANZO Capital SEO report JSON from GSC exports.")
    parser.add_argument("--type",    required=True, choices=["monthly","weekly","quarterly","yearly"])
    parser.add_argument("--period",  required=True, help="e.g. 2026-05, 2026-W18, 2026-Q2, 2026")
    parser.add_argument("--exports", default="./gsc-exports", help="Folder containing GSC ZIP files")
    parser.add_argument("--out",     default="./reports",     help="Output folder for report JSON files")
    parser.add_argument("--property", default="anzocapital.com")
    args = parser.parse_args()

    exports = Path(args.exports)
    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)

    if not exports.exists():
        print(f"Error: exports folder not found: {exports}")
        sys.exit(1)

    print(f"\n📊 Generating {args.type} report for {args.period}...")

    meta = period_meta(args.type, args.period)
    meta["property"]    = args.property
    meta["generatedAt"] = date.today().isoformat()
    meta["searchType"]  = "Web"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # ── Extract ZIPs
        zips = {
            "performance": find_zip(exports, "Performance-on-Search"),
            "coverage":    find_zip(exports, "Coverage"),
            "cwv_mobile":  find_zip(exports, "core-web-vitals", exclude="(1)"),
            "cwv_desktop": find_zip(exports, "core-web-vitals (1)"),
            "faq":         find_zip(exports, "FAQ"),
            "breadcrumbs": find_zip(exports, "Breadcrumbs"),
        }
        # Fallback: if both CWV zips look the same, try by metadata
        if zips["cwv_desktop"] is None:
            zips["cwv_desktop"] = find_zip(exports, "core-web-vitals")

        extracted = {}
        for key, z in zips.items():
            if z:
                dest = tmp / key
                dest.mkdir()
                extract_zip(z, dest)
                # Flatten one level if needed
                sub = list(dest.iterdir())
                if len(sub) == 1 and sub[0].is_dir():
                    extracted[key] = sub[0]
                else:
                    extracted[key] = dest
                print(f"  ✓ Extracted {key}: {z.name}")
            else:
                print(f"  ⚠ Missing ZIP for: {key}")
                extracted[key] = None

        # ── Parse data
        report = {"meta": meta}

        # Performance
        if extracted.get("performance"):
            perf = parse_performance(extracted["performance"])
            report.update(perf)
            kpis_q = report.get("queries", [])
            total_c = sum(q["clicks"] for q in kpis_q)
            total_cp = sum(q["clicksPrev"] for q in kpis_q)
            total_i = sum(q["impressions"] for q in kpis_q)
            total_ctrs = [q["ctr"] for q in kpis_q if q["clicks"] > 0]
            total_pos  = [q["position"] for q in kpis_q if q["clicks"] > 0]
            report["kpis"] = {
                "clicks":      {"current": total_c,  "previous": total_cp},
                "impressions": {"current": total_i,  "previous": 0},
                "ctr":         {"current": round(sum(total_ctrs)/len(total_ctrs), 2) if total_ctrs else 0, "previous": 0},
                "position":    {"current": round(sum(total_pos) /len(total_pos),  2) if total_pos  else 0, "previous": 0},
            }

        # Coverage
        if extracted.get("coverage"):
            cov = parse_coverage(extracted["coverage"])
            report["coverage"] = cov
        else:
            report["coverage"] = {"issues": [], "notIndexedTrend": [], "richResults": [], "richResultsTrend": {}}

        # CWV
        cwv_mob  = extracted.get("cwv_mobile")  or Path("/dev/null")
        cwv_desk = extracted.get("cwv_desktop") or Path("/dev/null")
        report["cwv"] = parse_cwv(cwv_mob, cwv_desk)

        # Rich results
        faq_dir = extracted.get("faq")  or Path("/dev/null")
        bc_dir  = extracted.get("breadcrumbs") or Path("/dev/null")
        rr = parse_rich_results(faq_dir, bc_dir)
        report["coverage"]["richResults"]      = rr["richResults"]
        report["coverage"]["richResultsTrend"] = rr["richResultsTrend"]

        # Opportunities
        if "pages" in report:
            report["opportunities"] = parse_opportunities(report["pages"])

        # Placeholder wins/concerns/actions — edit after generation
        report["wins"]     = ["(Auto-generated — review and update wins for this period.)"]
        report["concerns"] = ["(Auto-generated — review and update concerns for this period.)"]
        report["actions"]  = []

    # ── Write report JSON
    report_file = out_dir / f"{meta['id']}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  ✓ Report written: {report_file}")

    # ── Update manifest
    manifest_entry = {
        "id":            meta["id"],
        "type":          meta["type"],
        "label":         meta["label"],
        "year":          meta["year"],
        "dateStart":     meta["dateStart"],
        "dateEnd":       meta["dateEnd"],
        "comparePeriod": meta["comparePeriod"],
        "file":          f"reports/{meta['id']}.json",
        "generatedAt":   meta["generatedAt"],
    }
    for key in ("month", "week", "quarter"):
        if key in meta:
            manifest_entry[key] = meta[key]

    update_manifest(out_dir / "manifest.json", manifest_entry)

    print(f"\n✅ Done! Report ID: {meta['id']}")
    print(f"   Next: edit wins/concerns/actions in {report_file}")
    print(f"   Then: git add reports/ && git commit -m 'Add {meta['label']} {meta['type']} report' && git push\n")


if __name__ == "__main__":
    main()
