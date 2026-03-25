#!/usr/bin/env python3
"""Prepare aligned inputs for the national four-factor attributable burden upgrade.

This script builds the analysis-ready table used by the four-factor manuscript
upgrade while leaving the established national burden pipeline unchanged. The
prepared table combines:

1. attributable age-sex burden counts
2. aligned population
3. total underlying burden counts

The output is intended for the later four-factor decomposition:

    D_att = N * sum_a,s(share_a,s * rate_total_a,s * PAF_a,s)

where:

- `rate_total_a,s` comes from total disease burden / population
- `PAF_a,s` is implied by attributable burden / total disease burden
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_READY = PROJECT_ROOT / "data_processed" / "analysis_ready"
LOG_DIR = PROJECT_ROOT / "logs"
MANIFEST_PATH = PROJECT_ROOT / "metadata" / "gbd_download_manifest.csv"

ATTRIBUTABLE_BURDEN_LONG = ANALYSIS_READY / "national_burden_long.csv"
POPULATION_LONG = ANALYSIS_READY / "national_population_long.csv"
TOTAL_BURDEN_LONG = ANALYSIS_READY / "national_total_burden_long.csv"
FOUR_FACTOR_READY = ANALYSIS_READY / "national_four_factor_ready_long.csv"
QC_LOG_PATH = LOG_DIR / "four_factor_input_summary.json"

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


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def normalize_text(value: str | None) -> str:
    return (value or "").strip()


def to_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def normalize_cause(raw: str) -> str:
    key = normalize_text(raw).lower()
    return CAUSE_MAP.get(key, key.replace(" ", "_"))


def normalize_measure(raw: str) -> str:
    key = normalize_text(raw).lower()
    return MEASURE_MAP.get(key, key.replace(" ", "_"))


def normalize_metric(raw: str) -> str:
    key = normalize_text(raw).lower()
    return METRIC_MAP.get(key, key.replace(" ", "_"))


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


def read_manifest(manifest_path: Path) -> list[dict[str, str]]:
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_manifest_paths(
    project_root: Path,
    manifest_rows: list[dict[str, str]],
    modules: set[str],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    existing: list[dict[str, object]] = []
    missing: list[dict[str, object]] = []
    for row in manifest_rows:
        if row.get("analysis_module", "").strip() not in modules:
            continue
        full_path = project_root / row["target_subdir"].strip() / row["output_filename"].strip()
        payload = {
            "export_id": row["export_id"],
            "analysis_module": row["analysis_module"],
            "priority": row["priority"],
            "path": str(full_path),
        }
        if full_path.exists():
            existing.append({**payload, "full_path": full_path})
        else:
            missing.append(payload)
    return existing, missing


def normalize_total_rows(path: Path, source_category: str) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in read_rows(path):
        measure_raw = normalize_text(row.get("measure_name"))
        metric_raw = normalize_text(row.get("metric_name"))
        cause_raw = normalize_text(row.get("cause_name"))
        age_name = normalize_text(row.get("age_name"))
        sex_name = normalize_text(row.get("sex_name"))
        out.append(
            {
                "source_file": path.name,
                "source_category": source_category,
                "domain": "burden",
                "risk": "total",
                "risk_name_raw": "",
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


def build_four_factor_ready(
    attributable_rows: list[dict[str, str]],
    population_rows: list[dict[str, str]],
    total_rows: list[dict[str, object]],
) -> tuple[
    list[dict[str, object]],
    list[tuple[str, str, str, int, str, str]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    attributable_age_sex = [
        row
        for row in attributable_rows
        if row["source_category"] == "age_sex_count" and row["metric"] == "number"
    ]
    total_age_sex = [
        row
        for row in total_rows
        if row["source_category"] == "total_age_sex_count" and row["metric"] == "number"
    ]

    combos = sorted(
        {
            (row["risk"], row["cause"], row["measure"])
            for row in attributable_age_sex
        }
    )
    attributable_lookup = {
        (
            row["risk"],
            row["cause"],
            row["measure"],
            row["location_name"],
            int(row["year"]),
            row["sex_name"],
            row["age_name"],
        ): row
        for row in attributable_age_sex
    }
    total_lookup = {
        (
            str(row["cause"]),
            str(row["measure"]),
            str(row["location_name"]),
            int(row["year"]),
            str(row["sex_name"]),
            str(row["age_name"]),
        ): row
        for row in total_age_sex
    }
    total_age_coverage = {
        (str(row["cause"]), str(row["measure"]), str(row["age_name"]))
        for row in total_age_sex
    }

    missing_total_keys: set[tuple[str, str, str, int, str, str]] = set()
    paf_flags: list[dict[str, object]] = []
    structural_zero_total_fills: list[dict[str, object]] = []
    out: list[dict[str, object]] = []

    for pop in population_rows:
        location_name = pop["location_name"]
        year = int(pop["year"])
        sex_name = pop["sex_name"]
        age_name = pop["age_name"]
        population_val = float(pop["val"]) if pop["val"] not in ("", None) else 0.0

        for risk, cause, measure in combos:
            attr_key = (risk, cause, measure, location_name, year, sex_name, age_name)
            total_key = (cause, measure, location_name, year, sex_name, age_name)
            attr = attributable_lookup.get(attr_key)
            total = total_lookup.get(total_key)
            total_filled_zero = 0
            if total is None:
                if attr is None and (cause, measure, age_name) not in total_age_coverage:
                    total = {
                        "val": 0.0,
                        "lower": 0.0,
                        "upper": 0.0,
                    }
                    total_filled_zero = 1
                    structural_zero_total_fills.append(
                        {
                            "risk": risk,
                            "cause": cause,
                            "measure": measure,
                            "location_name": location_name,
                            "year": year,
                            "sex_name": sex_name,
                            "age_name": age_name,
                        }
                    )
                else:
                    missing_total_keys.add(total_key)
                    continue

            attributable_val = float(attr["val"]) if attr and attr["val"] not in ("", None) else 0.0
            attributable_lower = float(attr["lower"]) if attr and attr["lower"] not in ("", None) else 0.0
            attributable_upper = float(attr["upper"]) if attr and attr["upper"] not in ("", None) else 0.0
            total_val = float(total["val"]) if total["val"] not in ("", None) else 0.0
            total_lower = float(total["lower"]) if total["lower"] not in ("", None) else 0.0
            total_upper = float(total["upper"]) if total["upper"] not in ("", None) else 0.0

            implied_paf_raw: float | str = ""
            implied_paf_capped: float | str = ""
            paf_out_of_bounds_flag = 0
            total_zero_flag = 1 if total_val == 0.0 else 0

            if total_val > 0.0:
                implied_paf_raw = attributable_val / total_val
                implied_paf_capped = min(1.0, max(0.0, implied_paf_raw))
                if implied_paf_raw < 0.0 or implied_paf_raw > 1.0:
                    paf_out_of_bounds_flag = 1
            elif attributable_val == 0.0:
                implied_paf_raw = 0.0
                implied_paf_capped = 0.0

            if paf_out_of_bounds_flag or (total_zero_flag and attributable_val > 0.0):
                paf_flags.append(
                    {
                        "risk": risk,
                        "cause": cause,
                        "measure": measure,
                        "location_name": location_name,
                        "year": year,
                        "sex_name": sex_name,
                        "age_name": age_name,
                        "attributable_value": attributable_val,
                        "total_value": total_val,
                        "implied_paf_raw": implied_paf_raw,
                        "paf_out_of_bounds_flag": paf_out_of_bounds_flag,
                        "total_zero_flag": total_zero_flag,
                    }
                )

            out.append(
                {
                    "risk": risk,
                    "cause": cause,
                    "measure": measure,
                    "location_id": pop["location_id"],
                    "location_name": location_name,
                    "year": year,
                    "sex_id": pop["sex_id"],
                    "sex_name": sex_name,
                    "age_id": pop["age_id"],
                    "age_name": age_name,
                    "age_sort_key": pop["age_sort_key"],
                    "population": population_val,
                    "population_lower": pop["lower"],
                    "population_upper": pop["upper"],
                    "attributable_value": attributable_val,
                    "attributable_lower": attributable_lower,
                    "attributable_upper": attributable_upper,
                    "attributable_filled_zero": 0 if attr else 1,
                    "total_value": total_val,
                    "total_lower": total_lower,
                    "total_upper": total_upper,
                    "total_filled_zero": total_filled_zero,
                    "total_rate_per_person": (total_val / population_val) if population_val else 0.0,
                    "total_rate_per_100000": ((total_val / population_val) * 100000.0) if population_val else 0.0,
                    "attributable_rate_per_person": (attributable_val / population_val) if population_val else 0.0,
                    "attributable_rate_per_100000": ((attributable_val / population_val) * 100000.0) if population_val else 0.0,
                    "implied_paf_raw": implied_paf_raw,
                    "implied_paf_capped": implied_paf_capped,
                    "paf_out_of_bounds_flag": paf_out_of_bounds_flag,
                    "total_zero_flag": total_zero_flag,
                }
            )

    out = sorted(
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
    return out, sorted(missing_total_keys), paf_flags, structural_zero_total_fills


def build_qc_summary(
    total_rows: list[dict[str, object]],
    ready_rows: list[dict[str, object]],
    missing_total_keys: list[tuple[str, str, str, int, str, str]],
    paf_flags: list[dict[str, object]],
    structural_zero_total_fills: list[dict[str, object]],
) -> dict[str, object]:
    raw_pafs = [
        float(row["implied_paf_raw"])
        for row in ready_rows
        if row["implied_paf_raw"] not in ("", None)
    ]
    return {
        "total_burden_row_count": len(total_rows),
        "total_age_sex_row_count": sum(
            1 for row in total_rows if row["source_category"] == "total_age_sex_count"
        ),
        "total_summary_rate_row_count": sum(
            1 for row in total_rows if row["source_category"] == "total_summary_rate"
        ),
        "ready_row_count": len(ready_rows),
        "total_locations": sorted({str(row["location_name"]) for row in total_rows}),
        "total_years": sorted({int(row["year"]) for row in total_rows}),
        "max_implied_paf_raw": max(raw_pafs) if raw_pafs else 0.0,
        "min_implied_paf_raw": min(raw_pafs) if raw_pafs else 0.0,
        "paf_flag_count": len(paf_flags),
        "paf_flag_examples": paf_flags[:10],
        "structural_zero_total_fill_count": len(structural_zero_total_fills),
        "structural_zero_total_fill_examples": structural_zero_total_fills[:10],
        "missing_total_key_count": len(missing_total_keys),
        "missing_total_key_examples": [
            {
                "cause": cause,
                "measure": measure,
                "location_name": location_name,
                "year": year,
                "sex_name": sex_name,
                "age_name": age_name,
            }
            for cause, measure, location_name, year, sex_name, age_name in missing_total_keys[:10]
        ],
        "notes": [
            "national_four_factor_ready_long.csv is intended for the later four-factor decomposition script.",
            "implied_paf_raw is derived from attributable_value / total_value at the age-sex cell level.",
            "implied_paf_capped is provided as a QC-friendly bounded view only; downstream modelling should choose explicitly whether to use capped or raw values.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare four-factor analysis-ready inputs.")
    parser.add_argument(
        "--project-root",
        default=PROJECT_ROOT,
        type=Path,
        help="Project root containing metadata and analysis_ready tables.",
    )
    parser.add_argument(
        "--check-inputs",
        action="store_true",
        help="Only report expected inputs and current availability.",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    analysis_ready = project_root / "data_processed" / "analysis_ready"
    log_dir = project_root / "logs"
    burden_long_path = analysis_ready / ATTRIBUTABLE_BURDEN_LONG.name
    population_long_path = analysis_ready / POPULATION_LONG.name
    total_burden_long_path = analysis_ready / TOTAL_BURDEN_LONG.name
    ready_output_path = analysis_ready / FOUR_FACTOR_READY.name
    qc_log_path = log_dir / QC_LOG_PATH.name

    manifest_rows = read_manifest(project_root / "metadata" / "gbd_download_manifest.csv")
    resolved, missing = resolve_manifest_paths(
        project_root,
        manifest_rows,
        {"four_factor_total_burden_age_sex", "four_factor_total_burden_summary"},
    )

    core_inputs = {
        "national_burden_long": burden_long_path.exists(),
        "national_population_long": population_long_path.exists(),
    }
    input_summary = {
        "core_inputs": core_inputs,
        "resolved_four_factor_inputs": [
            {
                "export_id": row["export_id"],
                "analysis_module": row["analysis_module"],
                "priority": row["priority"],
                "path": str(row["full_path"]),
            }
            for row in resolved
        ],
        "missing_four_factor_inputs": missing,
    }

    if args.check_inputs:
        print(json.dumps(input_summary, indent=2, ensure_ascii=False))
        return 0

    if not core_inputs["national_burden_long"] or not core_inputs["national_population_long"]:
        print(json.dumps(input_summary, indent=2, ensure_ascii=False))
        print("")
        print("Run scripts/20_harmonize_national_gbd.py first so the attributable and population long tables exist.")
        return 1

    if missing:
        print(json.dumps(input_summary, indent=2, ensure_ascii=False))
        print("")
        print("The four-factor raw total burden files are still missing. Download them before building the ready table.")
        return 1

    attributable_rows = read_rows(burden_long_path)
    population_rows = read_rows(population_long_path)

    total_rows: list[dict[str, object]] = []
    for payload in resolved:
        source_category = (
            "total_age_sex_count"
            if payload["analysis_module"] == "four_factor_total_burden_age_sex"
            else "total_summary_rate"
        )
        total_rows.extend(normalize_total_rows(payload["full_path"], source_category))

    total_rows = sort_long_rows(total_rows)
    ready_rows, missing_total_keys, paf_flags, structural_zero_total_fills = build_four_factor_ready(
        attributable_rows,
        population_rows,
        total_rows,
    )

    if missing_total_keys:
        qc_summary = build_qc_summary(
            total_rows,
            ready_rows,
            missing_total_keys,
            paf_flags,
            structural_zero_total_fills,
        )
        print(json.dumps(qc_summary, indent=2, ensure_ascii=False))
        print("")
        print("Total burden age-sex coverage does not align with the attributable mainline. Fix the raw downloads before writing outputs.")
        return 1

    analysis_ready.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    write_csv(
        total_burden_long_path,
        total_rows,
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
        ready_output_path,
        ready_rows,
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
            "attributable_value",
            "attributable_lower",
            "attributable_upper",
            "attributable_filled_zero",
            "total_value",
            "total_lower",
            "total_upper",
            "total_filled_zero",
            "total_rate_per_person",
            "total_rate_per_100000",
            "attributable_rate_per_person",
            "attributable_rate_per_100000",
            "implied_paf_raw",
            "implied_paf_capped",
            "paf_out_of_bounds_flag",
            "total_zero_flag",
        ],
    )

    qc_summary = build_qc_summary(
        total_rows,
        ready_rows,
        missing_total_keys,
        paf_flags,
        structural_zero_total_fills,
    )
    qc_log_path.write_text(json.dumps(qc_summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(qc_summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
