#!/usr/bin/env python3
"""Build national-only harmonized GBD tables for the upgraded paper mainline.

This script intentionally uses only the Python standard library so it can run
before a richer analysis environment is provisioned.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data_raw"
NATIONAL_DOWNLOADS = DATA_RAW / "gbd_downloads" / "national"
ANALYSIS_READY = PROJECT_ROOT / "data_processed" / "analysis_ready"
LOG_DIR = PROJECT_ROOT / "logs"


LEGACY_BASELINE_FILES = [
    "gbd2021_pm25_copd_deaths_number_all-ages_both_1990_2021.csv",
    "gbd2021_pm25_copd_deaths_rate_age-standardized_both_1990_2021.csv",
    "gbd2021_pm25_copd_dalys_rate_age-standardized_both_1990_2021.csv",
    "gbd2021_pm25_lri_deaths_number_all-ages_both_1990_2021.csv",
    "gbd2021_pm25_lri_deaths_rate_age-standardized_both_1990_2021.csv",
    "gbd2021_pm25_lri_dalys_rate_age-standardized_both_1990_2021.csv",
    "gbd2021_ozone_copd_deaths_number_all-ages_both_1990_2021.csv",
    "gbd2021_ozone_copd_deaths_rate_age-standardized_both_1990_2021.csv",
    "gbd2021_ozone_copd_dalys_rate_age-standardized_both_1990_2021.csv",
]

RISK_MAP = {
    "ambient particulate matter pollution": "pm25",
    "室外颗粒物污染": "pm25",
    "ambient ozone pollution": "ozone",
    "室外臭氧污染": "ozone",
}

CAUSE_MAP = {
    "chronic obstructive pulmonary disease": "copd",
    "慢性阻塞性肺疾病": "copd",
    "lower respiratory infections": "lri",
    "下呼吸道感染": "lri",
}

MEASURE_MAP = {
    "deaths": "deaths",
    "死亡": "deaths",
    "dalys (disability-adjusted life years)": "dalys",
    "伤残调整生命年": "dalys",
    "population": "population",
}

METRIC_MAP = {
    "number": "number",
    "数量": "number",
    "rate": "rate",
    "率": "rate",
}

LOCATION_MAP = {
    "中国": "China",
    "日本": "Japan",
    "大韩民国": "Republic of Korea",
    "高sdi": "High SDI",
    "高SDI": "High SDI",
    "全球": "Global",
    "东亚": "East Asia",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def normalize_text(value: str | None) -> str:
    return (value or "").strip()


def normalize_measure(raw: str) -> str:
    key = normalize_text(raw).lower()
    return MEASURE_MAP.get(key, key.replace(" ", "_"))


def normalize_metric(raw: str) -> str:
    key = normalize_text(raw).lower()
    return METRIC_MAP.get(key, key.replace(" ", "_"))


def normalize_cause(raw: str) -> str:
    key = normalize_text(raw).lower()
    return CAUSE_MAP.get(key, key.replace(" ", "_"))


def normalize_risk(raw: str) -> str:
    key = normalize_text(raw).lower()
    return RISK_MAP.get(key, key.replace(" ", "_"))


def normalize_location(raw: str) -> str:
    text = normalize_text(raw)
    return LOCATION_MAP.get(text, text)


def derive_age_scope(age_name: str) -> str:
    age_name = normalize_text(age_name).lower()
    if age_name in {"全部", "all ages"}:
        return "all-ages"
    if age_name in {"年龄标准化", "age-standardized"}:
        return "age-standardized"
    return "age-specific"


def derive_sex_scope(sex_name: str) -> str:
    sex_name = normalize_text(sex_name).lower()
    if sex_name in {"合计", "both", "both sexes"}:
        return "both"
    return "mf"


def age_sort_key(age_name: str) -> float:
    age_name = normalize_text(age_name).lower()
    if age_name in {"all ages", "全部"}:
        return 10_000.0
    if age_name in {"age-standardized", "年龄标准化"}:
        return 10_001.0
    if age_name.endswith("+ years"):
        return float(age_name.split("+", 1)[0])
    if "days" in age_name:
        return float(age_name.split("-", 1)[0]) / 365.0
    if "months" in age_name:
        return float(age_name.split("-", 1)[0]) / 12.0
    if "years" in age_name and "-" in age_name:
        return float(age_name.split("-", 1)[0])
    return 9_999.0


def normalize_burden_rows(path: Path, source_category: str) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in read_rows(path):
        measure_raw = normalize_text(row.get("measure_name"))
        metric_raw = normalize_text(row.get("metric_name"))
        cause_raw = normalize_text(row.get("cause_name"))
        risk_raw = normalize_text(row.get("rei_name"))
        age_name = normalize_text(row.get("age_name"))
        sex_name = normalize_text(row.get("sex_name"))
        out.append(
            {
                "source_file": path.name,
                "source_category": source_category,
                "domain": "burden",
                "risk": normalize_risk(risk_raw),
                "risk_name_raw": risk_raw,
                "cause": normalize_cause(cause_raw),
                "cause_name_raw": cause_raw,
                "measure": normalize_measure(measure_raw),
                "measure_name_raw": measure_raw,
                "metric": normalize_metric(metric_raw),
                "metric_name_raw": metric_raw,
                "location_id": normalize_text(row.get("location_id")),
                "location_name": normalize_location(row.get("location_name")),
                "sex_id": normalize_text(row.get("sex_id")),
                "sex_name": sex_name,
                "sex_scope": derive_sex_scope(sex_name),
                "age_id": normalize_text(row.get("age_id")),
                "age_name": age_name,
                "age_scope": derive_age_scope(age_name),
                "age_sort_key": age_sort_key(age_name),
                "year": int(float(row["year"])),
                "val": to_float(row.get("val")),
                "lower": to_float(row.get("lower")),
                "upper": to_float(row.get("upper")),
            }
        )
    return out


def normalize_population_rows(path: Path) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in read_rows(path):
        age_name = normalize_text(row.get("age_name"))
        sex_name = normalize_text(row.get("sex_name"))
        out.append(
            {
                "source_file": path.name,
                "source_category": "population_age_sex",
                "domain": "population",
                "risk": "population",
                "risk_name_raw": "",
                "cause": "population",
                "cause_name_raw": "",
                "measure": "population",
                "measure_name_raw": normalize_text(row.get("measure_name")),
                "metric": "number",
                "metric_name_raw": normalize_text(row.get("metric_name")),
                "location_id": normalize_text(row.get("location_id")),
                "location_name": normalize_location(row.get("location_name")),
                "sex_id": normalize_text(row.get("sex_id")),
                "sex_name": sex_name,
                "sex_scope": derive_sex_scope(sex_name),
                "age_id": normalize_text(row.get("age_id")),
                "age_name": age_name,
                "age_scope": derive_age_scope(age_name),
                "age_sort_key": age_sort_key(age_name),
                "year": int(float(row["year"])),
                "val": to_float(row.get("val")),
                "lower": to_float(row.get("lower")),
                "upper": to_float(row.get("upper")),
            }
        )
    return out


def discover_age_sex_burden_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(NATIONAL_DOWNLOADS.glob("gbd2021_*_number_age-specific_mf_1990_2021.csv")):
        if "population" in path.name:
            continue
        # Keep the established attributable-burden pipeline insulated from the
        # total-burden downloads used by the four-factor upgrade.
        if "_total_" in path.name:
            continue
        files.append(path)
    return files


def discover_population_files() -> list[Path]:
    return sorted(NATIONAL_DOWNLOADS.glob("gbd2021_*population_number_age-specific_mf_1990_2021.csv"))


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sort_long_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(
        rows,
        key=lambda r: (
            str(r["domain"]),
            str(r["risk"]),
            str(r["cause"]),
            str(r["measure"]),
            str(r["metric"]),
            str(r["location_name"]),
            int(r["year"]),
            str(r["sex_name"]),
            float(r["age_sort_key"]),
            str(r["age_name"]),
        ),
    )


def build_decomposition_ready(
    burden_rows: list[dict[str, object]], population_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    burden_age_sex = [
        row
        for row in burden_rows
        if row["source_category"] == "age_sex_count" and row["metric"] == "number"
    ]
    combos = sorted(
        {
            (str(row["risk"]), str(row["cause"]), str(row["measure"]))
            for row in burden_age_sex
        }
    )
    burden_lookup = {
        (
            str(row["risk"]),
            str(row["cause"]),
            str(row["measure"]),
            str(row["location_name"]),
            int(row["year"]),
            str(row["sex_name"]),
            str(row["age_name"]),
        ): row
        for row in burden_age_sex
    }

    out: list[dict[str, object]] = []
    for pop in population_rows:
        for risk, cause, measure in combos:
            key = (
                risk,
                cause,
                measure,
                str(pop["location_name"]),
                int(pop["year"]),
                str(pop["sex_name"]),
                str(pop["age_name"]),
            )
            burden = burden_lookup.get(key)
            burden_val = float(burden["val"]) if burden else 0.0
            burden_lower = float(burden["lower"]) if burden else 0.0
            burden_upper = float(burden["upper"]) if burden else 0.0
            population_val = float(pop["val"]) if pop["val"] is not None else 0.0
            out.append(
                {
                    "risk": risk,
                    "cause": cause,
                    "measure": measure,
                    "location_id": pop["location_id"],
                    "location_name": pop["location_name"],
                    "year": pop["year"],
                    "sex_id": pop["sex_id"],
                    "sex_name": pop["sex_name"],
                    "age_id": pop["age_id"],
                    "age_name": pop["age_name"],
                    "age_sort_key": pop["age_sort_key"],
                    "population": population_val,
                    "population_lower": pop["lower"],
                    "population_upper": pop["upper"],
                    "burden_value": burden_val,
                    "burden_lower": burden_lower,
                    "burden_upper": burden_upper,
                    "burden_filled_zero": 0 if burden else 1,
                    "burden_rate_per_person": (burden_val / population_val) if population_val else 0.0,
                    "burden_rate_per_100000": ((burden_val / population_val) * 100000.0) if population_val else 0.0,
                }
            )
    return sorted(
        out,
        key=lambda r: (
            r["risk"],
            r["cause"],
            r["measure"],
            r["location_name"],
            r["year"],
            r["sex_name"],
            r["age_sort_key"],
        ),
    )


def build_summary_panel(
    burden_rows: list[dict[str, object]], population_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    summary: dict[tuple[str, str, str, int], dict[str, object]] = {}

    def get_record(risk: str, cause: str, location: str, year: int) -> dict[str, object]:
        key = (risk, cause, location, year)
        if key not in summary:
            summary[key] = {
                "risk": risk,
                "cause": cause,
                "location_name": location,
                "year": year,
                "deaths_count_all_age": "",
                "deaths_count_lower": "",
                "deaths_count_upper": "",
                "deaths_asr": "",
                "deaths_asr_lower": "",
                "deaths_asr_upper": "",
                "dalys_asdr": "",
                "dalys_asdr_lower": "",
                "dalys_asdr_upper": "",
                "deaths_count_from_age_sex_sum": 0.0,
                "dalys_count_from_age_sex_sum": 0.0,
                "population_total_from_age_sex": 0.0,
            }
        return summary[key]

    for row in burden_rows:
        risk = str(row["risk"])
        cause = str(row["cause"])
        location = str(row["location_name"])
        year = int(row["year"])
        rec = get_record(risk, cause, location, year)
        if row["source_category"] == "legacy_baseline" and row["sex_scope"] == "both":
            if row["measure"] == "deaths" and row["age_scope"] == "all-ages" and row["metric"] == "number":
                rec["deaths_count_all_age"] = row["val"]
                rec["deaths_count_lower"] = row["lower"]
                rec["deaths_count_upper"] = row["upper"]
            elif row["measure"] == "deaths" and row["age_scope"] == "age-standardized" and row["metric"] == "rate":
                rec["deaths_asr"] = row["val"]
                rec["deaths_asr_lower"] = row["lower"]
                rec["deaths_asr_upper"] = row["upper"]
            elif row["measure"] == "dalys" and row["age_scope"] == "age-standardized" and row["metric"] == "rate":
                rec["dalys_asdr"] = row["val"]
                rec["dalys_asdr_lower"] = row["lower"]
                rec["dalys_asdr_upper"] = row["upper"]
        elif row["source_category"] == "age_sex_count":
            if row["measure"] == "deaths":
                rec["deaths_count_from_age_sex_sum"] += float(row["val"])
            elif row["measure"] == "dalys":
                rec["dalys_count_from_age_sex_sum"] += float(row["val"])

    population_totals: dict[tuple[str, int], float] = defaultdict(float)
    for row in population_rows:
        population_totals[(str(row["location_name"]), int(row["year"]))] += float(row["val"])

    for rec in summary.values():
        rec["population_total_from_age_sex"] = population_totals[(str(rec["location_name"]), int(rec["year"]))]
        deaths_baseline = rec["deaths_count_all_age"]
        deaths_agg = rec["deaths_count_from_age_sex_sum"]
        rec["deaths_count_difference_vs_baseline"] = (
            (float(deaths_agg) - float(deaths_baseline)) if deaths_baseline != "" else ""
        )
        rec["dalys_count_ui_note"] = "point_estimate_sum_from_age_sex_only"

    return sorted(summary.values(), key=lambda r: (r["risk"], r["cause"], r["location_name"], r["year"]))


def build_qc_summary(
    burden_rows: list[dict[str, object]],
    population_rows: list[dict[str, object]],
    summary_panel: list[dict[str, object]],
) -> dict[str, object]:
    baseline_locations = sorted(
        {
            str(row["location_name"])
            for row in burden_rows
            if row["source_category"] == "legacy_baseline"
        }
    )
    age_sex_locations = sorted(
        {
            str(row["location_name"])
            for row in burden_rows
            if row["source_category"] == "age_sex_count"
        }
    )
    population_locations = sorted({str(row["location_name"]) for row in population_rows})

    diff_rows = [
        row
        for row in summary_panel
        if row["deaths_count_difference_vs_baseline"] not in ("", None)
    ]
    max_abs_diff = max(abs(float(row["deaths_count_difference_vs_baseline"])) for row in diff_rows) if diff_rows else 0.0
    top_diff_rows = sorted(
        diff_rows,
        key=lambda row: abs(float(row["deaths_count_difference_vs_baseline"])),
        reverse=True,
    )[:10]

    return {
        "burden_row_count": len(burden_rows),
        "population_row_count": len(population_rows),
        "baseline_locations": baseline_locations,
        "age_sex_locations": age_sex_locations,
        "population_locations": population_locations,
        "baseline_only_locations": sorted(set(baseline_locations) - set(age_sex_locations)),
        "years_burden": sorted({int(row["year"]) for row in burden_rows}),
        "years_population": sorted({int(row["year"]) for row in population_rows}),
        "max_abs_deaths_count_difference_vs_baseline": max_abs_diff,
        "top_deaths_count_differences": top_diff_rows,
        "notes": [
            "East Asia age-sex and population coverage is supplied through dedicated add-on files in data_raw/gbd_downloads/national/.",
            "DALY all-age counts are derived here from summed age-sex point estimates; uncertainty bounds are not formally reconstructed from draws.",
        ],
    }


def main() -> int:
    ANALYSIS_READY.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    burden_rows: list[dict[str, object]] = []
    for filename in LEGACY_BASELINE_FILES:
        burden_rows.extend(normalize_burden_rows(DATA_RAW / filename, "legacy_baseline"))
    for path in discover_age_sex_burden_files():
        burden_rows.extend(normalize_burden_rows(path, "age_sex_count"))

    population_rows: list[dict[str, object]] = []
    for path in discover_population_files():
        population_rows.extend(normalize_population_rows(path))

    burden_rows = sort_long_rows(burden_rows)
    population_rows = sort_long_rows(population_rows)
    decomposition_ready = build_decomposition_ready(burden_rows, population_rows)
    summary_panel = build_summary_panel(burden_rows, population_rows)
    qc_summary = build_qc_summary(burden_rows, population_rows, summary_panel)

    write_csv(
        ANALYSIS_READY / "national_burden_long.csv",
        burden_rows,
        [
            "source_file",
            "source_category",
            "domain",
            "risk",
            "risk_name_raw",
            "cause",
            "cause_name_raw",
            "measure",
            "measure_name_raw",
            "metric",
            "metric_name_raw",
            "location_id",
            "location_name",
            "sex_id",
            "sex_name",
            "sex_scope",
            "age_id",
            "age_name",
            "age_scope",
            "age_sort_key",
            "year",
            "val",
            "lower",
            "upper",
        ],
    )
    write_csv(
        ANALYSIS_READY / "national_population_long.csv",
        population_rows,
        [
            "source_file",
            "source_category",
            "domain",
            "risk",
            "risk_name_raw",
            "cause",
            "cause_name_raw",
            "measure",
            "measure_name_raw",
            "metric",
            "metric_name_raw",
            "location_id",
            "location_name",
            "sex_id",
            "sex_name",
            "sex_scope",
            "age_id",
            "age_name",
            "age_scope",
            "age_sort_key",
            "year",
            "val",
            "lower",
            "upper",
        ],
    )
    write_csv(
        ANALYSIS_READY / "national_decomposition_ready_long.csv",
        decomposition_ready,
        [
            "risk",
            "cause",
            "measure",
            "location_id",
            "location_name",
            "year",
            "sex_id",
            "sex_name",
            "age_id",
            "age_name",
            "age_sort_key",
            "population",
            "population_lower",
            "population_upper",
            "burden_value",
            "burden_lower",
            "burden_upper",
            "burden_filled_zero",
            "burden_rate_per_person",
            "burden_rate_per_100000",
        ],
    )
    write_csv(
        ANALYSIS_READY / "national_summary_panel.csv",
        summary_panel,
        [
            "risk",
            "cause",
            "location_name",
            "year",
            "deaths_count_all_age",
            "deaths_count_lower",
            "deaths_count_upper",
            "deaths_asr",
            "deaths_asr_lower",
            "deaths_asr_upper",
            "dalys_asdr",
            "dalys_asdr_lower",
            "dalys_asdr_upper",
            "deaths_count_from_age_sex_sum",
            "deaths_count_difference_vs_baseline",
            "dalys_count_from_age_sex_sum",
            "dalys_count_ui_note",
            "population_total_from_age_sex",
        ],
    )

    (LOG_DIR / "national_harmonization_summary.json").write_text(
        json.dumps(qc_summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OK: national harmonization complete")
    print(" - data_processed/analysis_ready/national_burden_long.csv")
    print(" - data_processed/analysis_ready/national_population_long.csv")
    print(" - data_processed/analysis_ready/national_decomposition_ready_long.csv")
    print(" - data_processed/analysis_ready/national_summary_panel.csv")
    print(" - logs/national_harmonization_summary.json")

    if qc_summary["baseline_only_locations"]:
        print("")
        print("QC NOTE: baseline-only locations detected:", ", ".join(qc_summary["baseline_only_locations"]))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
