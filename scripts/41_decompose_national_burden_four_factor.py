#!/usr/bin/env python3
"""Four-factor decomposition for national attributable burden change.

This script implements the locked four-factor accounting decomposition used by
the manuscript-facing national upgrade:

    D_att = N * sum_a,s(share_a,s * rate_total_a,s * PAF_a,s)

The default reported estimator is a symmetric permutation-average stepwise
replacement over four factors:

1. population growth
2. aging / age-sex structure
3. underlying total disease rate change
4. PAF change

Mandatory robustness outputs are generated alongside the main results:

- `1990-2019` sensitivity rerun
- capped-PAF comparison
- annual chain decomposition comparison
"""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FOUR_FACTOR_INPUT = (
    PROJECT_ROOT / "data_processed" / "analysis_ready" / "national_four_factor_ready_long.csv"
)
BP_MAIN = PROJECT_ROOT / "outputs" / "main" / "breakpoint_series_summary_1990_2021.csv"
BP_SENS = PROJECT_ROOT / "outputs" / "supp" / "breakpoint_series_summary_1990_2019.csv"
OUTPUT_MAIN = PROJECT_ROOT / "outputs" / "main"
OUTPUT_SUPP = PROJECT_ROOT / "outputs" / "supp"
LOG_DIR = PROJECT_ROOT / "logs"


def _format_missing_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def audit_only_exit(missing_paths: list[Path]) -> int:
    details = "\n".join(f"- {_format_missing_path(path)}" for path in missing_paths)
    raise SystemExit(
        "AUDIT NOTE: scripts/41_decompose_national_burden_four_factor.py is retained for "
        "workflow audit in the distributed journal bundle. Complete rerun requires upstream "
        "analysis-ready decomposition inputs that are not redistributed here.\nMissing required "
        f"inputs:\n{details}"
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def to_float(value: str | None) -> float:
    if value in ("", None):
        return 0.0
    return float(value)


def load_breakpoint_lookup(path: Path) -> dict[tuple[str, str, str, str], int]:
    lookup: dict[tuple[str, str, str, str], int] = {}
    for row in read_rows(path):
        metric_column = row["metric_column"]
        measure = "deaths" if metric_column == "deaths_asr" else "dalys"
        years = row["selected_breakpoint_years"].strip()
        if not years:
            continue
        first_year = int(years.split(";", 1)[0])
        lookup[(row["risk"], row["cause"], measure, row["location_name"])] = first_year
    return lookup


def build_series(
    rows: list[dict[str, str]],
    paf_column: str,
) -> dict[tuple[str, str, str, str, str], dict[int, dict[str, tuple[float, float, float, float]]]]:
    out: dict[
        tuple[str, str, str, str, str],
        dict[int, dict[str, tuple[float, float, float, float]]],
    ] = {}

    for row in rows:
        risk = row["risk"]
        cause = row["cause"]
        measure = row["measure"]
        location = row["location_name"]
        year = int(row["year"])
        sex_name = row["sex_name"]
        age_name = row["age_name"]
        population = to_float(row["population"])
        total_rate = to_float(row["total_rate_per_person"])
        paf_value = to_float(row[paf_column])
        attributable = to_float(row["attributable_value"])

        sex_key = (risk, cause, measure, location, sex_name)
        out.setdefault(sex_key, {}).setdefault(year, {})[age_name] = (
            population,
            total_rate,
            paf_value,
            attributable,
        )

        # The both-sex view retains separate female and male cells so the
        # structure term still reflects age-sex composition rather than a
        # purely age-aggregated profile.
        both_key = (risk, cause, measure, location, "Both")
        both_cell = f"{sex_name}::{age_name}"
        out.setdefault(both_key, {}).setdefault(year, {})[both_cell] = (
            population,
            total_rate,
            paf_value,
            attributable,
        )

    return out


def drop_structural_zero_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row["total_filled_zero"] != "1"]


def state_vectors(
    cell_map: dict[str, tuple[float, float, float, float]]
) -> tuple[list[str], float, list[float], list[float], list[float], float, float]:
    cells = sorted(cell_map)
    populations = [cell_map[cell][0] for cell in cells]
    total_rates = [cell_map[cell][1] for cell in cells]
    pafs = [cell_map[cell][2] for cell in cells]
    attributable_values = [cell_map[cell][3] for cell in cells]
    total_population = sum(populations)
    shares = [
        (population / total_population) if total_population else 0.0
        for population in populations
    ]
    attributable_total_observed = sum(attributable_values)
    attributable_total_identity = burden_from_components(
        total_population, shares, total_rates, pafs
    )
    return (
        cells,
        total_population,
        shares,
        total_rates,
        pafs,
        attributable_total_identity,
        attributable_total_observed,
    )


def burden_from_components(
    total_population: float,
    shares: list[float],
    total_rates: list[float],
    pafs: list[float],
) -> float:
    return total_population * sum(
        share * total_rate * paf
        for share, total_rate, paf in zip(shares, total_rates, pafs)
    )


def decompose_two_states(
    start_map: dict[str, tuple[float, float, float, float]],
    end_map: dict[str, tuple[float, float, float, float]],
) -> dict[str, float]:
    cells = sorted(set(start_map) | set(end_map))
    start_aligned = {cell: start_map.get(cell, (0.0, 0.0, 0.0, 0.0)) for cell in cells}
    end_aligned = {cell: end_map.get(cell, (0.0, 0.0, 0.0, 0.0)) for cell in cells}

    _, n0, s0, r0, p0, d0_identity, d0_observed = state_vectors(start_aligned)
    _, n1, s1, r1, p1, d1_identity, d1_observed = state_vectors(end_aligned)

    source = {"N": n0, "s": s0, "r": r0, "p": p0}
    target = {"N": n1, "s": s1, "r": r1, "p": p1}
    contrib = {
        "population_growth": 0.0,
        "aging": 0.0,
        "underlying_rate_change": 0.0,
        "paf_change": 0.0,
    }
    factor_name = {
        "N": "population_growth",
        "s": "aging",
        "r": "underlying_rate_change",
        "p": "paf_change",
    }

    for order in itertools.permutations(["N", "s", "r", "p"]):
        current = {
            "N": source["N"],
            "s": list(source["s"]),
            "r": list(source["r"]),
            "p": list(source["p"]),
        }
        prev = burden_from_components(current["N"], current["s"], current["r"], current["p"])
        for factor in order:
            current[factor] = target[factor] if factor == "N" else list(target[factor])
            new = burden_from_components(current["N"], current["s"], current["r"], current["p"])
            contrib[factor_name[factor]] += new - prev
            prev = new

    for key in contrib:
        contrib[key] /= 24.0

    delta = d1_identity - d0_identity
    residual = delta - sum(contrib.values())
    return {
        "total_start": d0_identity,
        "total_end": d1_identity,
        "delta_total": delta,
        "population_growth_contribution": contrib["population_growth"],
        "aging_contribution": contrib["aging"],
        "underlying_rate_change_contribution": contrib["underlying_rate_change"],
        "paf_change_contribution": contrib["paf_change"],
        "residual": residual,
        "population_total_start": n0,
        "population_total_end": n1,
        "observed_total_start": d0_observed,
        "observed_total_end": d1_observed,
        "observed_identity_gap_start": d0_observed - d0_identity,
        "observed_identity_gap_end": d1_observed - d1_identity,
    }


def decompose_annual_chain(
    year_map: dict[int, dict[str, tuple[float, float, float, float]]],
    start_year: int,
    end_year: int,
) -> dict[str, float]:
    running = {
        "population_growth_contribution": 0.0,
        "aging_contribution": 0.0,
        "underlying_rate_change_contribution": 0.0,
        "paf_change_contribution": 0.0,
    }
    total_start = 0.0
    total_end = 0.0
    population_total_start = 0.0
    population_total_end = 0.0
    observed_total_start = 0.0
    observed_total_end = 0.0
    observed_identity_gap_start = 0.0
    observed_identity_gap_end = 0.0

    for year in range(start_year, end_year):
        step = decompose_two_states(year_map[year], year_map[year + 1])
        if year == start_year:
            total_start = step["total_start"]
            population_total_start = step["population_total_start"]
            observed_total_start = step["observed_total_start"]
            observed_identity_gap_start = step["observed_identity_gap_start"]
        total_end = step["total_end"]
        population_total_end = step["population_total_end"]
        observed_total_end = step["observed_total_end"]
        observed_identity_gap_end = step["observed_identity_gap_end"]

        for key in running:
            running[key] += step[key]

    delta = total_end - total_start
    residual = delta - sum(running.values())
    return {
        "total_start": total_start,
        "total_end": total_end,
        "delta_total": delta,
        "population_total_start": population_total_start,
        "population_total_end": population_total_end,
        "population_growth_contribution": running["population_growth_contribution"],
        "aging_contribution": running["aging_contribution"],
        "underlying_rate_change_contribution": running["underlying_rate_change_contribution"],
        "paf_change_contribution": running["paf_change_contribution"],
        "residual": residual,
        "observed_total_start": observed_total_start,
        "observed_total_end": observed_total_end,
        "observed_identity_gap_start": observed_identity_gap_start,
        "observed_identity_gap_end": observed_identity_gap_end,
    }


def percent_or_blank(numerator: float, denominator: float) -> str | float:
    if abs(denominator) < 1e-12:
        return ""
    return (numerator / denominator) * 100.0


def period_specs(
    year_map: dict[int, dict[str, tuple[float, float, float, float]]],
    main_bp: int | None,
    sens_bp: int | None,
) -> list[tuple[str, int, int, str | int, str]]:
    if 1990 not in year_map or 2021 not in year_map or 2019 not in year_map:
        return []

    periods: list[tuple[str, int, int, str | int, str]] = [
        ("main_overall_1990_2021", 1990, 2021, "", "main"),
    ]
    if main_bp is not None and 1990 < main_bp < 2021:
        periods.extend(
            [
                ("main_pre_break", 1990, main_bp, main_bp, "main"),
                ("main_post_break", main_bp, 2021, main_bp, "main"),
            ]
        )

    periods.append(("sensitivity_overall_1990_2019", 1990, 2019, "", "sensitivity"))
    if sens_bp is not None and 1990 < sens_bp < 2019:
        periods.extend(
            [
                ("sensitivity_pre_break", 1990, sens_bp, sens_bp, "sensitivity"),
                ("sensitivity_post_break", sens_bp, 2019, sens_bp, "sensitivity"),
            ]
        )
    return periods


def build_period_rows(
    series: dict[tuple[str, str, str, str, str], dict[int, dict[str, tuple[float, float, float, float]]]],
    bp_main: dict[tuple[str, str, str, str], int],
    bp_sens: dict[tuple[str, str, str, str], int],
    paf_variant: str,
    time_path_variant: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for (risk, cause, measure, location, sex_name), year_map in sorted(series.items()):
        main_bp = bp_main.get((risk, cause, measure, location))
        sens_bp = bp_sens.get((risk, cause, measure, location))
        for period_label, start_year, end_year, breakpoint_year, window_type in period_specs(
            year_map, main_bp, sens_bp
        ):
            if time_path_variant == "endpoint_direct":
                result = decompose_two_states(year_map[start_year], year_map[end_year])
            else:
                result = decompose_annual_chain(year_map, start_year, end_year)

            rows.append(
                {
                    "analysis_window": window_type,
                    "period_label": period_label,
                    "risk": risk,
                    "cause": cause,
                    "measure": measure,
                    "location_name": location,
                    "sex_name": sex_name,
                    "start_year": start_year,
                    "end_year": end_year,
                    "breakpoint_year": breakpoint_year,
                    "paf_variant": paf_variant,
                    "time_path_variant": time_path_variant,
                    "total_start": result["total_start"],
                    "total_end": result["total_end"],
                    "delta_total": result["delta_total"],
                    "observed_total_start": result["observed_total_start"],
                    "observed_total_end": result["observed_total_end"],
                    "observed_identity_gap_start": result["observed_identity_gap_start"],
                    "observed_identity_gap_end": result["observed_identity_gap_end"],
                    "population_total_start": result["population_total_start"],
                    "population_total_end": result["population_total_end"],
                    "population_growth_contribution": result["population_growth_contribution"],
                    "aging_contribution": result["aging_contribution"],
                    "underlying_rate_change_contribution": result["underlying_rate_change_contribution"],
                    "paf_change_contribution": result["paf_change_contribution"],
                    "population_growth_percent_of_delta": percent_or_blank(
                        result["population_growth_contribution"], result["delta_total"]
                    ),
                    "aging_percent_of_delta": percent_or_blank(
                        result["aging_contribution"], result["delta_total"]
                    ),
                    "underlying_rate_change_percent_of_delta": percent_or_blank(
                        result["underlying_rate_change_contribution"], result["delta_total"]
                    ),
                    "paf_change_percent_of_delta": percent_or_blank(
                        result["paf_change_contribution"], result["delta_total"]
                    ),
                    "residual": result["residual"],
                }
            )

    return rows


def build_qc(
    input_rows: list[dict[str, str]],
    main_rows: list[dict[str, object]],
    main_both_rows: list[dict[str, object]],
    capped_rows: list[dict[str, object]],
    chain_rows: list[dict[str, object]],
    common_age_rows: list[dict[str, object]],
) -> dict[str, object]:
    input_paf_flags = sum(1 for row in input_rows if row["paf_out_of_bounds_flag"] == "1")
    structural_zero_total_fills = sum(1 for row in input_rows if row["total_filled_zero"] == "1")
    total_zero_rows = sum(1 for row in input_rows if row["total_zero_flag"] == "1")
    attributable_filled_zero_rows = sum(
        1 for row in input_rows if row["attributable_filled_zero"] == "1"
    )
    main_residuals = [abs(float(row["residual"])) for row in main_rows]
    capped_residuals = [abs(float(row["residual"])) for row in capped_rows]
    chain_residuals = [abs(float(row["residual"])) for row in chain_rows]
    identity_gaps = [
        abs(float(row["observed_identity_gap_start"]))
        for row in main_rows
    ] + [
        abs(float(row["observed_identity_gap_end"]))
        for row in main_rows
    ]
    common_age_lookup = {
        (
            row["analysis_window"],
            row["period_label"],
            row["risk"],
            row["cause"],
            row["measure"],
            row["location_name"],
            row["sex_name"],
        ): row
        for row in common_age_rows
    }
    diff_keys = [
        key for key in common_age_lookup
        if key in {
            (
                row["analysis_window"],
                row["period_label"],
                row["risk"],
                row["cause"],
                row["measure"],
                row["location_name"],
                row["sex_name"],
            )
            for row in main_both_rows
        }
    ]
    max_common_age_diff = 0.0
    if diff_keys:
        main_lookup = {
            (
                row["analysis_window"],
                row["period_label"],
                row["risk"],
                row["cause"],
                row["measure"],
                row["location_name"],
                row["sex_name"],
            ): row
            for row in main_both_rows
        }
        compare_columns = [
            "delta_total",
            "population_growth_contribution",
            "aging_contribution",
            "underlying_rate_change_contribution",
            "paf_change_contribution",
        ]
        for key in diff_keys:
            main_row = main_lookup[key]
            common_row = common_age_lookup[key]
            for column in compare_columns:
                max_common_age_diff = max(
                    max_common_age_diff,
                    abs(float(main_row[column]) - float(common_row[column])),
                )
    structural_scope = sorted(
        {
            f"{row['risk']}::{row['cause']}::{row['measure']}"
            for row in input_rows
            if row["total_filled_zero"] == "1"
        }
    )

    return {
        "input_row_count": len(input_rows),
        "input_locations": sorted({row["location_name"] for row in input_rows}),
        "input_structural_zero_total_fill_rows": structural_zero_total_fills,
        "input_total_zero_rows": total_zero_rows,
        "input_attributable_filled_zero_rows": attributable_filled_zero_rows,
        "input_paf_out_of_bounds_rows": input_paf_flags,
        "all_periods_by_sex_row_count": len(main_rows),
        "main_both_row_count": len(main_both_rows),
        "capped_row_count": len(capped_rows),
        "chain_row_count": len(chain_rows),
        "common_age_set_both_row_count": len(common_age_rows),
        "max_abs_residual_main": max(main_residuals) if main_residuals else 0.0,
        "max_abs_residual_capped": max(capped_residuals) if capped_residuals else 0.0,
        "max_abs_residual_chain": max(chain_residuals) if chain_residuals else 0.0,
        "max_abs_observed_identity_gap_main": max(identity_gaps) if identity_gaps else 0.0,
        "max_abs_common_age_set_difference_main_both": max_common_age_diff,
        "input_structural_zero_scope": structural_scope,
        "note": (
            "Both-sex rows use age-sex cells internally, so the structure component "
            "represents age-sex composition change in the combined population. "
            "Sex-specific rows represent within-sex age-structure change."
        ),
    }


def main() -> int:
    required_inputs = [FOUR_FACTOR_INPUT, BP_MAIN, BP_SENS]
    missing_inputs = [path for path in required_inputs if not path.exists()]
    if missing_inputs:
        return audit_only_exit(missing_inputs)

    input_rows = read_rows(FOUR_FACTOR_INPUT)
    bp_main = load_breakpoint_lookup(BP_MAIN)
    bp_sens = load_breakpoint_lookup(BP_SENS)

    main_rows = build_period_rows(
        build_series(input_rows, "implied_paf_raw"),
        bp_main,
        bp_sens,
        paf_variant="raw",
        time_path_variant="endpoint_direct",
    )
    capped_rows = build_period_rows(
        build_series(input_rows, "implied_paf_capped"),
        bp_main,
        bp_sens,
        paf_variant="capped",
        time_path_variant="endpoint_direct",
    )
    chain_rows = build_period_rows(
        build_series(input_rows, "implied_paf_raw"),
        bp_main,
        bp_sens,
        paf_variant="raw",
        time_path_variant="annual_chain",
    )
    common_age_rows = build_period_rows(
        build_series(drop_structural_zero_rows(input_rows), "implied_paf_raw"),
        bp_main,
        bp_sens,
        paf_variant="raw_common_age_set",
        time_path_variant="endpoint_direct",
    )

    fieldnames = [
        "analysis_window",
        "period_label",
        "risk",
        "cause",
        "measure",
        "location_name",
        "sex_name",
        "start_year",
        "end_year",
        "breakpoint_year",
        "paf_variant",
        "time_path_variant",
        "total_start",
        "total_end",
        "delta_total",
        "observed_total_start",
        "observed_total_end",
        "observed_identity_gap_start",
        "observed_identity_gap_end",
        "population_total_start",
        "population_total_end",
        "population_growth_contribution",
        "aging_contribution",
        "underlying_rate_change_contribution",
        "paf_change_contribution",
        "population_growth_percent_of_delta",
        "aging_percent_of_delta",
        "underlying_rate_change_percent_of_delta",
        "paf_change_percent_of_delta",
        "residual",
    ]

    main_both_rows = [
        row
        for row in main_rows
        if row["sex_name"] == "Both" and row["analysis_window"] == "main"
    ]
    sensitivity_both_rows = [
        row
        for row in main_rows
        if row["sex_name"] == "Both" and row["analysis_window"] == "sensitivity"
    ]
    capped_both_rows = [row for row in capped_rows if row["sex_name"] == "Both"]
    chain_both_rows = [row for row in chain_rows if row["sex_name"] == "Both"]
    common_age_both_rows = [row for row in common_age_rows if row["sex_name"] == "Both"]

    write_csv(OUTPUT_MAIN / "four_factor_decomposition_main_both.csv", main_both_rows, fieldnames)
    write_csv(
        OUTPUT_SUPP / "four_factor_decomposition_all_periods_by_sex.csv",
        main_rows,
        fieldnames,
    )
    write_csv(
        OUTPUT_SUPP / "four_factor_decomposition_sensitivity_both.csv",
        sensitivity_both_rows,
        fieldnames,
    )
    write_csv(
        OUTPUT_SUPP / "four_factor_decomposition_capped_paf_both.csv",
        capped_both_rows,
        fieldnames,
    )
    write_csv(
        OUTPUT_SUPP / "four_factor_decomposition_annual_chain_both.csv",
        chain_both_rows,
        fieldnames,
    )
    write_csv(
        OUTPUT_SUPP / "four_factor_decomposition_common_age_set_both.csv",
        common_age_both_rows,
        fieldnames,
    )

    qc = build_qc(
        input_rows,
        main_rows,
        main_both_rows,
        capped_both_rows,
        chain_both_rows,
        common_age_both_rows,
    )
    (LOG_DIR / "four_factor_decomposition_summary.json").write_text(
        json.dumps(qc, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OK: four-factor decomposition analysis complete")
    print(" - outputs/main/four_factor_decomposition_main_both.csv")
    print(" - outputs/supp/four_factor_decomposition_all_periods_by_sex.csv")
    print(" - outputs/supp/four_factor_decomposition_sensitivity_both.csv")
    print(" - outputs/supp/four_factor_decomposition_capped_paf_both.csv")
    print(" - outputs/supp/four_factor_decomposition_annual_chain_both.csv")
    print(" - outputs/supp/four_factor_decomposition_common_age_set_both.csv")
    print(" - logs/four_factor_decomposition_summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
