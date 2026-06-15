"""
PaymentRisk360 - Liquidity Risk Module
Script 02: Intraday Liquidity Metrics and KRI Summary

Purpose
-------
This script reads synthetic intraday liquidity scenarios and produces a set of
reporting-ready metrics and KRIs that a second-line risk function could use to
monitor intraday liquidity risk.

What the script does
--------------------
1. Reads data/raw/intraday_liquidity_scenarios.csv
2. Computes, by scenario:
   - minimum intraday position
   - minimum buffer available
   - time to first warning (buffer < warning threshold)
   - time to first breach (buffer < breach threshold)
   - count of warning and breach intervals
3. Writes:
   - data/processed/intraday_liquidity_positions.csv
   - outputs/intraday_liquidity_kri_summary.csv

Context
-------
Intraday liquidity risk management focuses on ensuring that payment and
settlement obligations can be met throughout the day, despite timing
mismatches in inflows and outflows. Monitoring positions, buffer usage,
and limit breaches is a key part of sound intraday liquidity practices.
"""

from pathlib import Path
import pandas as pd

RAW_INPUT = Path("data/raw/intraday_liquidity_scenarios.csv")
PROCESSED_OUTPUT = Path("data/processed/intraday_liquidity_positions.csv")
KRI_OUTPUT = Path("outputs/intraday_liquidity_kri_summary.csv")


def compute_time_to_first_flag(df: pd.DataFrame, flag_col: str) -> float:
    """
    Compute minutes from start of day to first True in `flag_col`.
    Returns:
        float minutes, or None if no flagged intervals.
    """
    flagged = df[df[flag_col]]
    if flagged.empty:
        return None
    first_time = flagged["time_since_start_min"].min()
    return float(first_time)


def main() -> None:
    PROCESSED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    KRI_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_INPUT, parse_dates=["timestamp"])

    # Ensure time_since_start_min exists (if not, compute here)
    if "time_since_start_min" not in df.columns:
        df["time_since_start_min"] = (
            df["timestamp"] - df.groupby("scenario")["timestamp"].transform("min")
        ).dt.total_seconds() / 60

    # Save a clean processed copy for downstream charts / notebooks
    df.to_csv(PROCESSED_OUTPUT, index=False)

    # Scenario-level KRI metrics
    scenario_metrics = []
    for scenario, group in df.groupby("scenario"):
        metric = {
            "scenario": scenario,
            "min_intraday_position": group["intraday_position"].min(),
            "min_buffer_available": group["buffer_available"].min(),
            "warning_intervals": int(group["warning_flag"].sum()),
            "breach_intervals": int(group["breach_flag"].sum()),
            "time_to_first_warning_min": compute_time_to_first_flag(group, "warning_flag"),
            "time_to_first_breach_min": compute_time_to_first_flag(group, "breach_flag"),
        }
        scenario_metrics.append(metric)

    kri_df = pd.DataFrame(scenario_metrics)

    # Derive simple categorical KRI statuses
    def scenario_status(row):
        # If there are breaches, check how many and how early they occur
        breach_count = row["breach_intervals"]
        warning_count = row["warning_intervals"]
        t_first_breach = row["time_to_first_breach_min"]

        # If buffer is never exhausted (min_buffer_available > 0), treat as non-breaching
        if row["min_buffer_available"] > 0:
            if warning_count and warning_count > 0:
                return "Amber"
            return "Green"

        # If we do exhaust the buffer at some point:
        if breach_count and breach_count > 0:
            # Red if breaches are frequent OR occur relatively early
            if breach_count >= 5 or (t_first_breach is not None and t_first_breach <= 180):
                return "Red"
            else:
                # Infrequent / late breaches can be Amber
                return "Amber"

        if warning_count and warning_count > 0:
            return "Amber"

        return "Green"

    kri_df["status"] = kri_df.apply(scenario_status, axis=1)

    # Round numeric columns for readability
    numeric_cols = [
        "min_intraday_position",
        "min_buffer_available",
        "time_to_first_warning_min",
        "time_to_first_breach_min",
    ]
    for col in numeric_cols:
        kri_df[col] = kri_df[col].round(2)

    kri_df.to_csv(KRI_OUTPUT, index=False)

    # Console summary for quick validation
    print(kri_df.to_dict(orient="records"))


if __name__ == "__main__":
    main()