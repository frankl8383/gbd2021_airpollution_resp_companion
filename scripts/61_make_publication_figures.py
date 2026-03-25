#!/usr/bin/env python3
"""Generate publication-style main figures from current analysis outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_READY = PROJECT_ROOT / "data_processed" / "analysis_ready"
MAIN_DIR = PROJECT_ROOT / "outputs" / "main"

LOCATION_ORDER = ["China", "Japan", "Republic of Korea", "East Asia", "Global", "High SDI"]
LOCATION_COLORS = {
    "China": "#B33C2E",
    "Japan": "#2D6A4F",
    "Republic of Korea": "#355C7D",
    "East Asia": "#C06C84",
    "Global": "#4F5D75",
    "High SDI": "#7A9E7E",
}
RISK_CAUSE_ORDER = [("pm25", "copd"), ("pm25", "lri"), ("ozone", "copd")]
RISK_CAUSE_TITLE = {
    ("pm25", "copd"): "PM2.5-attributable COPD",
    ("pm25", "lri"): "PM2.5-attributable LRI",
    ("ozone", "copd"): "Ozone-attributable COPD",
}
PANEL_TITLE_SIZE = 10.5
AXIS_LABEL_SIZE = 9.5
TICK_LABEL_SIZE = 8.8
LEGEND_FONT_SIZE = 9


def add_box(ax, x, y, w, h, text, fontsize=10):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.2,
        facecolor="white",
        edgecolor="#222222",
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)


def add_arrow(ax, x1, y1, x2, y2):
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=12, linewidth=1.2, color="#222222")
    ax.add_patch(arrow)


def make_figure1() -> None:
    fig = plt.figure(figsize=(12.8, 7.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    w, h = 0.26, 0.14
    x1, x2, x3 = 0.05, 0.37, 0.69
    y1, y2, y3, y4 = 0.77, 0.54, 0.31, 0.04

    add_box(ax, x1, y1, w, h, "Data source:\nGBD 2021 Results Tool\nRisk-attributable burden estimates", fontsize=10)
    add_box(ax, x2, y1, w, h, "Locations:\nChina; Japan; Republic of Korea;\nEast Asia; Global; High SDI", fontsize=10)
    add_box(ax, x3, y1, w, h, "Risk-cause pairs:\nPM2.5 -> COPD\nPM2.5 -> LRI\nOzone -> COPD", fontsize=10)

    add_box(ax, x1, y2, w, h, "Input layers:\nBaseline ASR/ASDR tables\nAttributable + total age-sex burden\nPopulation by age and sex", fontsize=10)
    add_box(ax, x2, y2, w, h, "Temporal module:\nData-driven breakpoint analysis\n1990-2021 main window\n1990-2019 sensitivity", fontsize=10)
    add_box(ax, x3, y2, w, h, "Count interpretation:\nFour-factor accounting decomposition\nPopulation growth\nAging\nUnderlying rate + PAF", fontsize=10)

    add_box(ax, x1, y3, w, h, "Vulnerability module:\nUnder-5 focus for PM2.5-LRI\nAge-70-plus focus for COPD\nBoth/Female/Male", fontsize=10)
    add_box(ax, x2, y3, w, h, "Main text outputs:\nTrend figure\nDecomposition figure\nVulnerability figure", fontsize=10)
    add_box(ax, x3, y3, w, h, "Main tables:\nBreakpoint summary\nDecomposition summary", fontsize=10)

    add_box(
        ax,
        0.12,
        y4,
        0.76,
        0.11,
        "Scientific question:\nCan age-standardized decline offset demographic aging,\n"
        "or does residual burden remain high because total disease-rate and PAF changes do not fully compensate?",
        fontsize=9.2,
    )

    add_arrow(ax, x1 + w, y1 + h / 2, x2, y1 + h / 2)
    add_arrow(ax, x2 + w, y1 + h / 2, x3, y1 + h / 2)
    add_arrow(ax, x1 + w / 2, y1, x1 + w / 2, y2 + h)
    add_arrow(ax, x2 + w / 2, y1, x2 + w / 2, y2 + h)
    add_arrow(ax, x3 + w / 2, y1, x3 + w / 2, y2 + h)
    add_arrow(ax, x1 + w, y2 + h / 2, x2, y2 + h / 2)
    add_arrow(ax, x2 + w, y2 + h / 2, x3, y2 + h / 2)
    add_arrow(ax, x1 + w / 2, y2, x1 + w / 2, y3 + h)
    add_arrow(ax, x2 + w / 2, y2, x2 + w / 2, y3 + h)
    add_arrow(ax, x3 + w / 2, y2, x3 + w / 2, y3 + h)
    add_arrow(ax, 0.5, y3, 0.5, y4 + 0.11)

    for ext in ("png", "pdf"):
        fig.savefig(MAIN_DIR / f"figure1_study_workflow.{ext}", dpi=300 if ext == "png" else None, bbox_inches="tight")
    plt.close(fig)


def make_figure2() -> None:
    summary = pd.read_csv(ANALYSIS_READY / "national_summary_panel.csv")
    bp = pd.read_csv(MAIN_DIR / "breakpoint_series_summary_1990_2021.csv")

    fig, axes = plt.subplots(2, 3, figsize=(18, 9), sharex=True)
    panel_labels = ["A", "B", "C", "D", "E", "F"]

    for col, pair in enumerate(RISK_CAUSE_ORDER):
        risk, cause = pair
        title = RISK_CAUSE_TITLE[pair]
        for row_idx, metric_col in enumerate(["deaths_asr", "dalys_asdr"]):
            ax = axes[row_idx, col]
            for location in LOCATION_ORDER:
                sub = summary[(summary["risk"] == risk) & (summary["cause"] == cause) & (summary["location_name"] == location)].copy()
                if sub.empty:
                    continue
                sub = sub.sort_values("year")
                alpha = 1.0 if location in ("China", "East Asia", "Global") else 0.45
                width = 2.4 if location in ("China", "East Asia", "Global") else 1.3
                ax.plot(sub["year"], sub[metric_col], label=location, color=LOCATION_COLORS[location], linewidth=width, alpha=alpha)
            ax.set_title(f"{panel_labels[row_idx * 3 + col]}. {title}", fontsize=PANEL_TITLE_SIZE, loc="left", fontweight="bold")
            ax.grid(alpha=0.2, linewidth=0.6)
            if row_idx == 0:
                ax.set_ylabel("Deaths ASR per 100,000", fontsize=AXIS_LABEL_SIZE)
            else:
                ax.set_ylabel("DALYs ASDR per 100,000", fontsize=AXIS_LABEL_SIZE)
                ax.set_xlabel("Year", fontsize=AXIS_LABEL_SIZE)
            ax.tick_params(axis="both", labelsize=TICK_LABEL_SIZE)

            bp_sub = bp[(bp["risk"] == risk) & (bp["cause"] == cause) & (bp["metric_column"] == metric_col)]
            for r in bp_sub.itertuples():
                bp_year = int(r.selected_breakpoint_years)
                ax.axvline(bp_year, color=LOCATION_COLORS[r.location_name], linestyle="--", linewidth=1.0, alpha=0.35 if r.location_name not in ("China","East Asia","Global") else 0.7)
            key_locs = bp_sub[bp_sub["location_name"].isin(["China", "East Asia", "Global"])]
            bp_text = ", ".join(f"{r.location_name}:{int(r.selected_breakpoint_years)}" for r in key_locs.itertuples())
            ax.text(0.01, 0.02, bp_text, transform=ax.transAxes, fontsize=7.2, color="#444444", ha="left", va="bottom")

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(0.5, 1.01), fontsize=LEGEND_FONT_SIZE)
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    for ext in ("png", "pdf"):
        fig.savefig(MAIN_DIR / f"figure2_trends_breakpoints.{ext}", dpi=300 if ext == "png" else None, bbox_inches="tight")
    plt.close(fig)


def make_figure3() -> None:
    df = pd.read_csv(MAIN_DIR / "four_factor_decomposition_main_both.csv")
    df = df[
        (df["sex_name"] == "Both")
        & (df["period_label"] == "main_overall_1990_2021")
        & (df["paf_variant"] == "raw")
        & (df["time_path_variant"] == "endpoint_direct")
    ].copy()
    df = df[df["location_name"].isin(["China", "East Asia", "Global"])].copy()

    fig, axes = plt.subplots(2, 3, figsize=(18, 9.6))
    colors = {
        "Population growth": "#2A9D8F",
        "Aging": "#E9C46A",
        "Underlying rate": "#D1495B",
        "PAF change": "#3D5A80",
    }

    for idx, (risk, cause) in enumerate(RISK_CAUSE_ORDER):
        for row_idx, measure in enumerate(["deaths", "dalys"]):
            ax = axes[row_idx, idx]
            sub = df[(df["risk"] == risk) & (df["cause"] == cause) & (df["measure"] == measure)].copy()
            sub["location_name"] = pd.Categorical(sub["location_name"], ["China", "East Asia", "Global"])
            sub = sub.sort_values("location_name")
            y = range(len(sub))
            width = 0.18
            ax.barh([v - width for v in y], sub["population_growth_contribution"], height=width, color=colors["Population growth"], label="Population growth")
            ax.barh([v - width / 3 for v in y], sub["aging_contribution"], height=width, color=colors["Aging"], label="Aging")
            ax.barh([v + width / 3 for v in y], sub["underlying_rate_change_contribution"], height=width, color=colors["Underlying rate"], label="Underlying disease rate")
            ax.barh([v + width for v in y], sub["paf_change_contribution"], height=width, color=colors["PAF change"], label="PAF change")
            ax.axvline(0, color="#444444", linewidth=0.8)
            ax.set_yticks(list(y))
            ax.set_yticklabels(sub["location_name"])
            title = RISK_CAUSE_TITLE[(risk, cause)]
            metric_label = "Deaths" if measure == "deaths" else "DALYs"
            ax.set_title(f"{chr(65 + row_idx * 3 + idx)}. {title} ({metric_label})", fontsize=11, loc="left", fontweight="bold")
            ax.grid(axis="x", alpha=0.2, linewidth=0.6)
            if row_idx == 1:
                ax.set_xlabel("Contribution to count change")

    handles, labels = axes[0, 0].get_legend_handles_labels()
    dedup = dict(zip(labels, handles))
    fig.legend(dedup.values(), dedup.keys(), loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.01))
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    for ext in ("png", "pdf"):
        fig.savefig(MAIN_DIR / f"figure3_decomposition.{ext}", dpi=300 if ext == "png" else None, bbox_inches="tight")
    plt.close(fig)


def dumbbell_panel(ax, df: pd.DataFrame, title: str, panel_label: str) -> None:
    desired_order = ["China", "East Asia", "Global", "Japan", "Republic of Korea", "High SDI"]
    df = df.set_index("location_name").loc[desired_order].reset_index()
    y = range(len(df))
    for i, row in enumerate(df.itertuples()):
        ax.plot([row.value_1990, row.value_2021], [i, i], color="#999999", linewidth=2)
        ax.scatter(row.value_1990, i, color="#4F5D75", s=40, label="1990" if i == 0 else "")
        ax.scatter(row.value_2021, i, color="#B33C2E", s=40, label="2021" if i == 0 else "")
        if row.location_name in ("China", "East Asia", "Global"):
            ax.text(row.value_2021, i + 0.14, f"{row.value_2021:.1f}", fontsize=7, color="#B33C2E")
    ax.set_yticks(list(y))
    ax.set_yticklabels(df["location_name"])
    ax.set_title(f"{panel_label}. {title}", fontsize=PANEL_TITLE_SIZE, loc="left", fontweight="bold")
    ax.grid(axis="x", alpha=0.2, linewidth=0.6)
    ax.tick_params(axis="both", labelsize=TICK_LABEL_SIZE)


def make_figure4() -> None:
    v = pd.read_csv(MAIN_DIR / "vulnerability_main_snapshot.csv")
    v = v[v["sex_name"] == "Both"].copy()

    def prep(risk: str, cause: str, measure: str, col: str) -> pd.DataFrame:
        sub = v[(v["risk"] == risk) & (v["cause"] == cause) & (v["measure"] == measure) & (v["year"].isin([1990, 2021]))].copy()
        pivot = sub.pivot(index="location_name", columns="year", values=col).reset_index()
        pivot.columns = ["location_name", "value_1990", "value_2021"]
        return pivot

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    dumbbell_panel(
        axes[0, 0],
        prep("pm25", "lri", "deaths", "under5_share_percent"),
        "PM2.5-attributable LRI deaths: under-5 share (%)",
        "A",
    )
    dumbbell_panel(
        axes[0, 1],
        prep("pm25", "lri", "dalys", "under5_share_percent"),
        "PM2.5-attributable LRI DALYs: under-5 share (%)",
        "B",
    )
    dumbbell_panel(
        axes[1, 0],
        prep("pm25", "copd", "dalys", "age70plus_share_percent"),
        "PM2.5-attributable COPD DALYs: age-70-plus share (%)",
        "C",
    )
    dumbbell_panel(
        axes[1, 1],
        prep("ozone", "copd", "dalys", "age70plus_share_percent"),
        "Ozone-attributable COPD DALYs: age-70-plus share (%)",
        "D",
    )

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.01), fontsize=LEGEND_FONT_SIZE)
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    for ext in ("png", "pdf"):
        fig.savefig(MAIN_DIR / f"figure4_vulnerability.{ext}", dpi=300 if ext == "png" else None, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.titleweight"] = "bold"
    make_figure1()
    make_figure2()
    make_figure3()
    make_figure4()
    print("OK: publication figures generated")
    print(" - outputs/main/figure1_study_workflow.png/.pdf")
    print(" - outputs/main/figure2_trends_breakpoints.png/.pdf")
    print(" - outputs/main/figure3_decomposition.png/.pdf")
    print(" - outputs/main/figure4_vulnerability.png/.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
