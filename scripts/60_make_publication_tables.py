#!/usr/bin/env python3
"""Build publication-ready main-text tables from analysis outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_DIR = PROJECT_ROOT / "outputs" / "main"


def fmt_num(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def fmt_percent(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def fmt_apc(apc: float, lo: float, hi: float) -> str:
    return f"{apc:.2f} ({lo:.2f} to {hi:.2f})"


def build_table2() -> pd.DataFrame:
    summary = pd.read_csv(MAIN_DIR / "breakpoint_series_summary_1990_2021.csv")
    segments = pd.read_csv(MAIN_DIR / "breakpoint_segments_1990_2021.csv")

    seg1 = (
        segments[segments["segment_index"] == 1]
        .copy()
        .rename(
            columns={
                "year_start": "segment1_year_start",
                "year_end": "segment1_year_end",
                "apc_percent": "segment1_apc",
                "apc_lower": "segment1_apc_lower",
                "apc_upper": "segment1_apc_upper",
                "p_value": "segment1_p",
            }
        )
    )
    seg2 = (
        segments[segments["segment_index"] == 2]
        .copy()
        .rename(
            columns={
                "year_start": "segment2_year_start",
                "year_end": "segment2_year_end",
                "apc_percent": "segment2_apc",
                "apc_lower": "segment2_apc_lower",
                "apc_upper": "segment2_apc_upper",
                "p_value": "segment2_p",
            }
        )
    )

    keys = ["metric_column", "risk", "cause", "location_name", "selected_breakpoint_years"]
    out = summary.merge(seg1[keys + ["segment1_year_start", "segment1_year_end", "segment1_apc", "segment1_apc_lower", "segment1_apc_upper", "segment1_p"]], on=keys, how="left")
    out = out.merge(seg2[keys + ["segment2_year_start", "segment2_year_end", "segment2_apc", "segment2_apc_lower", "segment2_apc_upper", "segment2_p"]], on=keys, how="left")

    metric_label_map = {
        "deaths_asr": "Deaths ASR",
        "dalys_asdr": "DALYs ASDR",
    }
    risk_label_map = {
        "pm25": "PM2.5",
        "ozone": "Ozone",
    }
    cause_label_map = {
        "copd": "COPD",
        "lri": "Lower respiratory infections",
    }
    location_order = ["China", "Japan", "Republic of Korea", "East Asia", "Global", "High SDI"]
    metric_order = ["deaths_asr", "dalys_asdr"]
    risk_order = ["pm25", "ozone"]
    cause_order = ["copd", "lri"]

    out["Metric"] = out["metric_column"].map(metric_label_map)
    out["Risk"] = out["risk"].map(risk_label_map).fillna(out["risk"])
    out["Cause"] = out["cause"].map(cause_label_map).fillna(out["cause"])
    out["Location"] = out["location_name"]
    out["Breakpoint year"] = out["selected_breakpoint_years"]
    out["Segment 1 APC (95% CI), %"] = out.apply(
        lambda r: fmt_apc(r["segment1_apc"], r["segment1_apc_lower"], r["segment1_apc_upper"]),
        axis=1,
    )
    out["Segment 2 APC (95% CI), %"] = out.apply(
        lambda r: fmt_apc(r["segment2_apc"], r["segment2_apc_lower"], r["segment2_apc_upper"]),
        axis=1,
    )
    out["Overall AAPC, %"] = out["overall_aapc_percent"].map(lambda v: fmt_percent(v, 2))
    out["Segment 1 years"] = out.apply(lambda r: f"{int(r['segment1_year_start'])}-{int(r['segment1_year_end'])}", axis=1)
    out["Segment 2 years"] = out.apply(lambda r: f"{int(r['segment2_year_start'])}-{int(r['segment2_year_end'])}", axis=1)

    out["__metric"] = out["metric_column"].map(lambda x: metric_order.index(x))
    out["__risk"] = out["risk"].map(lambda x: risk_order.index(x))
    out["__cause"] = out["cause"].map(lambda x: cause_order.index(x))
    out["__loc"] = out["location_name"].map(lambda x: location_order.index(x))
    out = out.sort_values(["__metric", "__risk", "__cause", "__loc"]).drop(columns=["__metric", "__risk", "__cause", "__loc"])

    out = out[
        [
            "Metric",
            "Risk",
            "Cause",
            "Location",
            "Breakpoint year",
            "Segment 1 years",
            "Segment 1 APC (95% CI), %",
            "Segment 2 years",
            "Segment 2 APC (95% CI), %",
            "Overall AAPC, %",
        ]
    ]
    out = out.rename(
        columns={
            "Breakpoint year": "Brk year",
            "Segment 1 years": "Seg 1 years",
            "Segment 1 APC (95% CI), %": "Seg 1 APC (95% CI), %",
            "Segment 2 years": "Seg 2 years",
            "Segment 2 APC (95% CI), %": "Seg 2 APC (95% CI), %",
            "Overall AAPC, %": "AAPC, %",
        }
    )
    return out


def build_table3() -> pd.DataFrame:
    df = pd.read_csv(MAIN_DIR / "four_factor_decomposition_main_both.csv")
    df = df[
        (df["sex_name"] == "Both")
        & (df["period_label"] == "main_overall_1990_2021")
        & (df["paf_variant"] == "raw")
        & (df["time_path_variant"] == "endpoint_direct")
    ].copy()

    risk_label_map = {"pm25": "PM2.5", "ozone": "Ozone"}
    cause_label_map = {"copd": "COPD", "lri": "Lower respiratory infections"}
    measure_label_map = {"deaths": "Deaths", "dalys": "DALYs"}
    location_order = ["China", "Japan", "Republic of Korea", "East Asia", "Global", "High SDI"]
    risk_order = ["pm25", "ozone"]
    cause_order = ["copd", "lri"]
    measure_order = ["deaths", "dalys"]

    df["Measure"] = df["measure"].map(measure_label_map)
    df["Risk"] = df["risk"].map(risk_label_map).fillna(df["risk"])
    df["Cause"] = df["cause"].map(cause_label_map).fillna(df["cause"])
    df["Location"] = df["location_name"]
    df["Population growth contribution"] = df["population_growth_contribution"].map(lambda v: fmt_num(v, 0))
    df["Aging contribution"] = df["aging_contribution"].map(lambda v: fmt_num(v, 0))
    df["Underlying disease rate contribution"] = df["underlying_rate_change_contribution"].map(
        lambda v: fmt_num(v, 0)
    )
    df["PAF contribution"] = df["paf_change_contribution"].map(lambda v: fmt_num(v, 0))
    df["Net change"] = df["delta_total"].map(lambda v: fmt_num(v, 0))

    df["__measure"] = df["measure"].map(lambda x: measure_order.index(x))
    df["__risk"] = df["risk"].map(lambda x: risk_order.index(x))
    df["__cause"] = df["cause"].map(lambda x: cause_order.index(x))
    df["__loc"] = df["location_name"].map(lambda x: location_order.index(x))
    df = df.sort_values(["__measure", "__risk", "__cause", "__loc"]).drop(columns=["__measure", "__risk", "__cause", "__loc"])

    df = df[
        [
            "Measure",
            "Risk",
            "Cause",
            "Location",
            "Net change",
            "Population growth contribution",
            "Aging contribution",
            "Underlying disease rate contribution",
            "PAF contribution",
        ]
    ]
    df = df.rename(
        columns={
            "Population growth contribution": "Pop growth",
            "Aging contribution": "Aging",
            "Underlying disease rate contribution": "Underlying rate",
            "PAF contribution": "PAF",
        }
    )
    return df


def main() -> int:
    table2 = build_table2()
    table3 = build_table3()

    table2_csv = MAIN_DIR / "table2_breakpoint_main.csv"
    table2_xlsx = MAIN_DIR / "table2_breakpoint_main.xlsx"
    table3_csv = MAIN_DIR / "table3_decomposition_main.csv"
    table3_xlsx = MAIN_DIR / "table3_decomposition_main.xlsx"
    supp_table3_csv = PROJECT_ROOT / "outputs" / "supp" / "table3_decomposition_full_with_percent.csv"

    table2.to_csv(table2_csv, index=False, encoding="utf-8-sig")
    table3.to_csv(table3_csv, index=False, encoding="utf-8-sig")
    table2.to_excel(table2_xlsx, index=False, sheet_name="Table2")
    table3.to_excel(table3_xlsx, index=False, sheet_name="Table3")
    pd.read_csv(PROJECT_ROOT / "outputs" / "supp" / "four_factor_decomposition_all_periods_by_sex.csv").to_csv(
        supp_table3_csv,
        index=False,
        encoding="utf-8-sig",
    )

    print("OK: publication tables generated")
    print(" -", table2_csv)
    print(" -", table2_xlsx)
    print(" -", table3_csv)
    print(" -", table3_xlsx)
    print(" -", supp_table3_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
