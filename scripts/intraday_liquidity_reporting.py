"""
PaymentRisk360 - Liquidity Risk Module
Script 03: Intraday Liquidity Reporting and Visualization

Purpose
-------
This script produces portfolio-style reporting assets for the intraday
liquidity module, including:

- charts of intraday positions and buffer usage
- a scenario comparison chart
- a markdown report that summarizes key intraday liquidity KRIs

These outputs are designed to look like what a second-line risk function
might bring to a risk committee or product council discussion.

Inputs
------
- data/processed/intraday_liquidity_positions.csv
- outputs/intraday_liquidity_kri_summary.csv

Outputs
-------
- outputs/intraday_liquidity_positions_chart.png
- outputs/intraday_liquidity_scenarios_comparison.png
- outputs/intraday_liquidity_report.md
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

POSITIONS_INPUT = Path("data/processed/intraday_liquidity_positions.csv")
KRI_INPUT = Path("outputs/intraday_liquidity_kri_summary.csv")

CHART_POSITIONS_OUTPUT = Path("outputs/intraday_liquidity_positions_chart.png")
CHART_SCENARIOS_OUTPUT = Path("outputs/intraday_liquidity_scenarios_comparison.png")
REPORT_OUTPUT = Path("outputs/intraday_liquidity_report.md")


def plot_positions_by_scenario(df: pd.DataFrame, output_path: Path) -> None:
    """
    Plot intraday positions and buffer usage for each scenario on one chart.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    for scenario, group in df.groupby("scenario"):
        ax.plot(
            group["timestamp"],
            group["intraday_position"] / 1_000_000,
            label=f"{scenario} - position",
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Intraday Position ($M)")
    ax.set_title("Intraday Liquidity Position by Scenario")
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_buffer_usage(df: pd.DataFrame, output_path: Path) -> None:
    """
    Plot buffer availability (base_case vs stress scenarios) over time.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    for scenario, group in df.groupby("scenario"):
        ax.plot(
            group["timestamp"],
            group["buffer_available"] / 1_000_000,
            label=f"{scenario} - buffer",
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Buffer Available ($M)")
    ax.set_title("Intraday Liquidity Buffer Available by Scenario")
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def build_markdown_report(df_kri: pd.DataFrame) -> str:
    """
    Build a second-line style markdown report using KRI metrics.
    """
    base_row = df_kri[df_kri["scenario"] == "base_case"].iloc[0]
    stress_row = df_kri[df_kri["scenario"] == "stress_volume"].iloc[0]
    severe_row = df_kri[df_kri["scenario"] == "severe_stress"].iloc[0]

    report = f"""# Intraday Liquidity Risk Report

## Executive Summary

This analysis simulates intraday liquidity positions for a payments participant
under three scenarios:

- **Base case** - normal day with typical inflows and outflows
- **Stress volume** - higher payment outflows and modest inflow delay
- **Severe stress** - large outflow spike and material inflow disruption

All scenarios start from the same synthetic intraday buffer and balance.
The objective is to illustrate how quickly the intraday buffer is consumed and
when warning or breach conditions would be triggered.

From a second-line perspective, the key conclusions are:

- The **base case** remains within buffer limits but generates a meaningful number of warning intervals, which is consistent with a buffer being actively used rather than purely static.
- The **stress volume** scenario shows multiple breaches and a later time-to-first-breach, indicating that sustained volume pressure can exhaust the buffer in the second half of the day.
- The **severe stress** scenario exhausts the buffer earlier and more frequently, with both warning and breach conditions becoming prominent.

## Scenario-Level KRIs

### Base Case

- Status: **{base_row['status']}**
- Minimum intraday position: {base_row['min_intraday_position']:,.2f}
- Minimum buffer available: {base_row['min_buffer_available']:,.2f}
- Warning intervals: {int(base_row['warning_intervals'])}
- Breach intervals: {int(base_row['breach_intervals'])}
- Time to first warning: {base_row['time_to_first_warning_min']} minutes
- Time to first breach: {base_row['time_to_first_breach_min']} minutes

Interpretation:

The base case uses the buffer but does not fully exhaust it (min buffer remains positive). Warning intervals indicate periods where buffer usage enters a lower comfort zone, which should be tracked, but this profile is generally consistent with a well-calibrated intraday buffer for normal conditions.

### Stress Volume Scenario

- Status: **{stress_row['status']}**
- Minimum intraday position: {stress_row['min_intraday_position']:,.2f}
- Minimum buffer available: {stress_row['min_buffer_available']:,.2f}
- Warning intervals: {int(stress_row['warning_intervals'])}
- Breach intervals: {int(stress_row['breach_intervals'])}
- Time to first warning: {stress_row['time_to_first_warning_min']} minutes
- Time to first breach: {stress_row['time_to_first_breach_min']} minutes

Interpretation:

The stress volume scenario shows that elevated outflows and modest inflow delays can push the buffer into breach territory, especially later in the day. This highlights the need for intraday monitoring and, potentially, payment pacing or prioritisation if similar patterns emerge in real operations.

### Severe Stress Scenario

- Status: **{severe_row['status']}**
- Minimum intraday position: {severe_row['min_intraday_position']:,.2f}
- Minimum buffer available: {severe_row['min_buffer_available']:,.2f}
- Warning intervals: {int(severe_row['warning_intervals'])}
- Breach intervals: {int(severe_row['breach_intervals'])}
- Time to first warning: {severe_row['time_to_first_warning_min']} minutes
- Time to first breach: {severe_row['time_to_first_breach_min']} minutes

Interpretation:

The severe stress scenario produces early and repeated breaches of the buffer, signalling conditions under which intraday funding, payment throttling, or contingency funding actions would be required. This scenario is useful for illustrating how quickly risk can escalate if inflows are disrupted and outflows are elevated.

## Second-Line Considerations and Recommendations

From a second-line ERM perspective, this synthetic intraday view suggests:

- **KRIs:** Time-to-first-breach, number of breach intervals, and minimum buffer available are suitable intraday liquidity KRIs for monitoring and escalation.
- **Governance:** Clear escalation paths should be defined for Red scenarios, including thresholds for when to engage treasury, payment operations, or senior management.
- **Payment Sequencing:** In stress conditions, payment pacing or prioritisation could be used to slow non-critical outflows and protect critical settlement obligations.
- **Scenario Testing:** Regularly running intraday stress scenarios helps validate whether buffers and intraday limits remain appropriate as payment patterns evolve.

## Limitations

- The dataset is synthetic and uses stylised inflow/outflow patterns.
- Buffer levels and thresholds are illustrative and would need calibration to real balances, credit lines, and operational constraints.
- The simulation focuses on a single participant-level view and does not model broader system-level contagion or network effects.
"""
    return report


def main() -> None:
    CHART_POSITIONS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df_positions = pd.read_csv(POSITIONS_INPUT, parse_dates=["timestamp"])
    df_kri = pd.read_csv(KRI_INPUT)

    # Plot intraday positions for all scenarios
    plot_positions_by_scenario(df_positions, CHART_POSITIONS_OUTPUT)

    # Plot buffer availability for all scenarios
    plot_buffer_usage(df_positions, CHART_SCENARIOS_OUTPUT)

    # Build and write markdown report
    report_md = build_markdown_report(df_kri)
    REPORT_OUTPUT.write_text(report_md, encoding="utf-8")

    print(
        {
            "positions_chart": str(CHART_POSITIONS_OUTPUT),
            "scenarios_chart": str(CHART_SCENARIOS_OUTPUT),
            "report": str(REPORT_OUTPUT),
        }
    )


if __name__ == "__main__":
    main()