#!/usr/bin/env python3
"""Run piecewise log-linear breakpoint analysis for national burden trends.

This is a pure-standard-library implementation intended to replace the fixed
2005 segmented trend approach with a data-driven breakpoint search.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PANEL = PROJECT_ROOT / "data_processed" / "analysis_ready" / "national_summary_panel.csv"
OUTPUT_MAIN = PROJECT_ROOT / "outputs" / "main"
OUTPUT_SUPP = PROJECT_ROOT / "outputs" / "supp"
LOG_DIR = PROJECT_ROOT / "logs"

MIN_SEGMENT_LENGTH = 8
MAX_BREAKPOINTS = 1
EPS = 1e-12


@dataclass
class SegmentFit:
    year_start: int
    year_end: int
    n_years: int
    intercept: float
    slope: float
    sse: float
    se_slope: float | None
    p_value: float | None
    apc_percent: float
    apc_lower: float | None
    apc_upper: float | None


@dataclass
class ModelFit:
    breakpoints: tuple[int, ...]
    bic: float
    sse: float
    segments: list[SegmentFit]


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


def normal_two_sided_p(z_score: float) -> float:
    return math.erfc(abs(z_score) / math.sqrt(2.0))


def fit_log_linear_segment(points: list[tuple[int, float]]) -> SegmentFit:
    years = [float(year) for year, _ in points]
    values = [float(value) for _, value in points]
    logs = [math.log(max(value, EPS)) for value in values]
    n = len(years)

    mean_x = sum(years) / n
    mean_y = sum(logs) / n
    sxx = sum((x - mean_x) ** 2 for x in years)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(years, logs))
    slope = sxy / sxx if sxx else 0.0
    intercept = mean_y - slope * mean_x
    residuals = [y - (intercept + slope * x) for x, y in zip(years, logs)]
    sse = sum(res * res for res in residuals)

    se_slope: float | None = None
    p_value: float | None = None
    apc_lower: float | None = None
    apc_upper: float | None = None

    if n > 2 and sxx > 0:
        mse = sse / (n - 2)
        se_slope = math.sqrt(mse / sxx)
        if se_slope > 0:
            z_score = slope / se_slope
            p_value = normal_two_sided_p(z_score)
            apc_lower = 100.0 * (math.exp(slope - 1.96 * se_slope) - 1.0)
            apc_upper = 100.0 * (math.exp(slope + 1.96 * se_slope) - 1.0)

    apc_percent = 100.0 * (math.exp(slope) - 1.0)

    return SegmentFit(
        year_start=int(years[0]),
        year_end=int(years[-1]),
        n_years=n,
        intercept=intercept,
        slope=slope,
        sse=sse,
        se_slope=se_slope,
        p_value=p_value,
        apc_percent=apc_percent,
        apc_lower=apc_lower,
        apc_upper=apc_upper,
    )


def enumerate_breakpoints(n_years: int, min_len: int = MIN_SEGMENT_LENGTH, max_breakpoints: int = MAX_BREAKPOINTS) -> list[tuple[int, ...]]:
    candidates: list[tuple[int, ...]] = [tuple()]

    if n_years < min_len * 2:
        return candidates

    for i in range(min_len, n_years - min_len + 1):
        if i < n_years:
            candidates.append((i,))

    return candidates


def fit_model(points: list[tuple[int, float]], breakpoints: tuple[int, ...]) -> ModelFit:
    boundaries = (0,) + breakpoints + (len(points),)
    segments: list[SegmentFit] = []
    total_sse = 0.0
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        seg = fit_log_linear_segment(points[start:end])
        segments.append(seg)
        total_sse += seg.sse

    n = len(points)
    n_params = 2 + (3 * len(breakpoints))
    bic = n * math.log(max(total_sse / n, EPS)) + n_params * math.log(n)
    breakpoint_years = tuple(points[idx][0] for idx in breakpoints)
    return ModelFit(breakpoints=breakpoint_years, bic=bic, sse=total_sse, segments=segments)


def select_best_model(points: list[tuple[int, float]]) -> ModelFit:
    candidates = enumerate_breakpoints(len(points))
    best: ModelFit | None = None
    for candidate in candidates:
        model = fit_model(points, candidate)
        if best is None or model.bic < best.bic:
            best = model
    assert best is not None
    return best


def weighted_aapc(segments: list[SegmentFit]) -> float:
    total_years = sum(seg.n_years for seg in segments)
    weighted_beta = sum(seg.slope * seg.n_years for seg in segments) / total_years
    return 100.0 * (math.exp(weighted_beta) - 1.0)


def build_series(rows: list[dict[str, str]], metric_column: str, year_end: int) -> dict[tuple[str, str, str], list[tuple[int, float]]]:
    out: dict[tuple[str, str, str], list[tuple[int, float]]] = {}
    grouped: dict[tuple[str, str, str], list[tuple[int, float]]] = {}
    for row in rows:
        year = int(row["year"])
        if year > year_end:
            continue
        value = row[metric_column]
        if value in ("", None):
            continue
        numeric = float(value)
        if numeric <= 0:
            continue
        key = (row["risk"], row["cause"], row["location_name"])
        grouped.setdefault(key, []).append((year, numeric))

    for key, points in grouped.items():
        points = sorted(points, key=lambda item: item[0])
        if len(points) >= MIN_SEGMENT_LENGTH:
            out[key] = points
    return out


def run_window(rows: list[dict[str, str]], analysis_window: str, year_end: int) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    metric_map = {
        "deaths_asr": "Deaths ASR",
        "dalys_asdr": "DALYs ASDR",
    }
    segment_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    model_compare_rows: list[dict[str, object]] = []
    qc = {
        "analysis_window": analysis_window,
        "series_count": 0,
        "metric_counts": {},
        "breakpoint_count_distribution": {},
        "series_without_breakpoints": 0,
        "series_with_breakpoints": 0,
    }

    for metric_column, metric_label in metric_map.items():
        series_map = build_series(rows, metric_column, year_end)
        qc["metric_counts"][metric_column] = len(series_map)

        for (risk, cause, location), points in sorted(series_map.items()):
            candidates = [fit_model(points, candidate) for candidate in enumerate_breakpoints(len(points))]
            candidates = sorted(candidates, key=lambda m: (m.bic, len(m.breakpoints)))
            best = candidates[0]
            no_break = next((m for m in candidates if len(m.breakpoints) == 0), None)
            one_break = next((m for m in candidates if len(m.breakpoints) == 1), None)
            aapc = weighted_aapc(best.segments)
            qc["series_count"] += 1
            n_breaks = len(best.breakpoints)
            qc["breakpoint_count_distribution"][str(n_breaks)] = qc["breakpoint_count_distribution"].get(str(n_breaks), 0) + 1
            if n_breaks == 0:
                qc["series_without_breakpoints"] += 1
            else:
                qc["series_with_breakpoints"] += 1

            summary_rows.append(
                {
                    "analysis_window": analysis_window,
                    "metric_column": metric_column,
                    "metric_label": metric_label,
                    "risk": risk,
                    "cause": cause,
                    "location_name": location,
                    "n_points": len(points),
                    "selected_breakpoint_count": n_breaks,
                    "selected_breakpoint_years": ";".join(str(year) for year in best.breakpoints),
                    "model_bic": best.bic,
                    "model_sse": best.sse,
                    "overall_aapc_percent": aapc,
                }
            )

            model_compare_rows.append(
                {
                    "analysis_window": analysis_window,
                    "metric_column": metric_column,
                    "metric_label": metric_label,
                    "risk": risk,
                    "cause": cause,
                    "location_name": location,
                    "n_points": len(points),
                    "selected_model": f"{len(best.breakpoints)}-break",
                    "selected_breakpoint_years": ";".join(str(year) for year in best.breakpoints),
                    "bic_0_break": no_break.bic if no_break is not None else "",
                    "bic_1_break": one_break.bic if one_break is not None else "",
                    "bic_delta_0_minus_1": (no_break.bic - one_break.bic) if (no_break is not None and one_break is not None) else "",
                }
            )

            for idx, seg in enumerate(best.segments, start=1):
                segment_rows.append(
                    {
                        "analysis_window": analysis_window,
                        "metric_column": metric_column,
                        "metric_label": metric_label,
                        "risk": risk,
                        "cause": cause,
                        "location_name": location,
                        "selected_breakpoint_count": n_breaks,
                        "selected_breakpoint_years": ";".join(str(year) for year in best.breakpoints),
                        "segment_index": idx,
                        "year_start": seg.year_start,
                        "year_end": seg.year_end,
                        "n_years": seg.n_years,
                        "slope_log_linear": seg.slope,
                        "slope_se": seg.se_slope if seg.se_slope is not None else "",
                        "p_value": seg.p_value if seg.p_value is not None else "",
                        "apc_percent": seg.apc_percent,
                        "apc_lower": seg.apc_lower if seg.apc_lower is not None else "",
                        "apc_upper": seg.apc_upper if seg.apc_upper is not None else "",
                        "segment_sse": seg.sse,
                        "model_bic": best.bic,
                    }
                )

    return segment_rows, summary_rows, model_compare_rows, qc


def main() -> int:
    rows = read_rows(SUMMARY_PANEL)

    seg_main, sum_main, cmp_main, qc_main = run_window(rows, "1990-2021", 2021)
    seg_sens, sum_sens, cmp_sens, qc_sens = run_window(rows, "1990-2019", 2019)

    segment_fieldnames = [
        "analysis_window",
        "metric_column",
        "metric_label",
        "risk",
        "cause",
        "location_name",
        "selected_breakpoint_count",
        "selected_breakpoint_years",
        "segment_index",
        "year_start",
        "year_end",
        "n_years",
        "slope_log_linear",
        "slope_se",
        "p_value",
        "apc_percent",
        "apc_lower",
        "apc_upper",
        "segment_sse",
        "model_bic",
    ]
    summary_fieldnames = [
        "analysis_window",
        "metric_column",
        "metric_label",
        "risk",
        "cause",
        "location_name",
        "n_points",
        "selected_breakpoint_count",
        "selected_breakpoint_years",
        "model_bic",
        "model_sse",
        "overall_aapc_percent",
    ]

    write_csv(OUTPUT_MAIN / "breakpoint_segments_1990_2021.csv", seg_main, segment_fieldnames)
    write_csv(OUTPUT_MAIN / "breakpoint_series_summary_1990_2021.csv", sum_main, summary_fieldnames)
    write_csv(
        OUTPUT_SUPP / "breakpoint_model_comparison_1990_2021.csv",
        cmp_main,
        [
            "analysis_window",
            "metric_column",
            "metric_label",
            "risk",
            "cause",
            "location_name",
            "n_points",
            "selected_model",
            "selected_breakpoint_years",
            "bic_0_break",
            "bic_1_break",
            "bic_delta_0_minus_1",
        ],
    )
    write_csv(OUTPUT_SUPP / "breakpoint_segments_1990_2019.csv", seg_sens, segment_fieldnames)
    write_csv(OUTPUT_SUPP / "breakpoint_series_summary_1990_2019.csv", sum_sens, summary_fieldnames)
    write_csv(
        OUTPUT_SUPP / "breakpoint_model_comparison_1990_2019.csv",
        cmp_sens,
        [
            "analysis_window",
            "metric_column",
            "metric_label",
            "risk",
            "cause",
            "location_name",
            "n_points",
            "selected_model",
            "selected_breakpoint_years",
            "bic_0_break",
            "bic_1_break",
            "bic_delta_0_minus_1",
        ],
    )

    qc_payload = {
        "main_window": qc_main,
        "sensitivity_window": qc_sens,
        "method": {
            "type": "piecewise_log_linear_bic_search",
            "min_segment_length": MIN_SEGMENT_LENGTH,
            "max_breakpoints": MAX_BREAKPOINTS,
            "note": "This is a single-break piecewise log-linear model selection on annual point-estimate ASR/ASDR series. It is not the NCI Joinpoint software.",
        },
    }
    (LOG_DIR / "breakpoint_trend_summary.json").write_text(
        json.dumps(qc_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("OK: breakpoint trend analysis complete")
    print(" - outputs/main/breakpoint_segments_1990_2021.csv")
    print(" - outputs/main/breakpoint_series_summary_1990_2021.csv")
    print(" - outputs/supp/breakpoint_model_comparison_1990_2021.csv")
    print(" - outputs/supp/breakpoint_segments_1990_2019.csv")
    print(" - outputs/supp/breakpoint_series_summary_1990_2019.csv")
    print(" - outputs/supp/breakpoint_model_comparison_1990_2019.csv")
    print(" - logs/breakpoint_trend_summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
