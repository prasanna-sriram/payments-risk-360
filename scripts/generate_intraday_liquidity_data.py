"""
PaymentRisk360 - Liquidity Risk Module
Script 01: Generate Synthetic Intraday Liquidity Data

Purpose
-------
This script generates synthetic intraday payment flows and liquidity buffer
usage for one or more scenarios. It is designed to illustrate how intraday
liquidity positions can evolve over the course of a business day in a payments
context.

Why this exists
---------------
Intraday liquidity risk in payment and settlement systems arises from timing
mismatches between incoming and outgoing payments during the day. Institutions
need enough readily available funds (buffers) to meet obligations as they fall due,
and must monitor how quickly those buffers are consumed under normal and
stressed conditions.

This script creates a controlled, reproducible dataset for:
- monitoring intraday balances,
- identifying potential buffer breaches,
- and supporting basic KRIs (e.g., minimum position, time-to-breach).

What the script does
--------------------
1. Defines a set of time buckets over a business day (e.g., every 15 minutes).
2. Simulates baseline inflows and outflows for a synthetic participant.
3. Creates three scenarios:
   - base_case: normal day
   - stress_volume: higher outflows (volume spike) and modest inflow delay
   - severe_stress: larger outflow shock plus delayed/weak inflows
4. Tracks intraday liquidity position and buffer usage for each scenario.
5. Flags intervals where the buffer is breached or falls into a warning zone.
6. Writes the combined dataset to data/raw/intraday_liquidity_scenarios.csv.

Notes for reviewers / hiring managers
-------------------------------------
This is not a full treasury system. It is a simplified, portfolio-style
simulation to demonstrate understanding of intraday liquidity concepts and how
a second-line risk function might structure monitoring data.
"""

from pathlib import Path
from typing import List
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RANDOM_SEED = 42

RAW_OUTPUT = Path("data/raw/intraday_liquidity_scenarios.csv")

# Intraday time buckets: 9:00 to 17:00 in 15-minute increments (32 buckets)
START_TIME = "09:00"
END_TIME = "17:00"
FREQUENCY = "15min"

# Base starting cash / buffer
BASE_STARTING_BALANCE = 64_000_000.0  # synthetic units, e.g., CAD
BASE_LIQUIDITY_BUFFER = 34_000_000.0  # portion considered as dedicated intraday buffer

# Warning / breach thresholds as % of buffer
WARNING_THRESHOLD_PCT = 0.40  # below 40% buffer triggers warning
BREACH_THRESHOLD_PCT = 0.05   # below 1% buffer treated as breach


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_time_index() -> pd.DatetimeIndex:
    """Create a business-day intraday time index."""
    rng = pd.date_range(
        "2026-01-05 " + START_TIME,
        "2026-01-05 " + END_TIME,
        freq=FREQUENCY,
        inclusive="left",
    )
    return rng


def simulate_base_flows(
    time_index: pd.DatetimeIndex,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """
    Generate baseline intraday inflows and outflows.

    Assumptions (illustrative):
    - Outflows are heavier in the morning as queued payments are released.
    - Inflows pick up late morning and early afternoon.
    - Noise is added around a stylized profile.
    """
    n = len(time_index)
    hours_since_start = (time_index - time_index[0]).seconds.values / 3600

    # Stylized profiles (0 to 1 scale over day)
    morning_peak = np.exp(-0.5 * ((hours_since_start - 2) / 1.1) ** 2)
    afternoon_peak = np.exp(-0.5 * ((hours_since_start - 5) / 1.5) ** 2)
    inflow_profile = 0.6 * afternoon_peak + 0.4 * morning_peak[::-1]
    outflow_profile = 0.7 * morning_peak + 0.3 * afternoon_peak

    # Normalize profiles
    inflow_profile = inflow_profile / inflow_profile.sum()
    outflow_profile = outflow_profile / outflow_profile.sum()

    # Target total daily flows (synthetic)
    total_inflows = 92_000_000.0
    total_outflows = 64_000_000.0

    inflows = total_inflows * inflow_profile * rng.uniform(0.85, 1.15, size=n)
    outflows = total_outflows * outflow_profile * rng.uniform(0.85, 1.15, size=n)

    df = pd.DataFrame(
        {
            "timestamp": time_index,
            "inflow": inflows,
            "outflow": outflows,
        }
    )
    return df


def apply_scenario_transforms(
    base_df: pd.DataFrame,
    scenario_name: str,
) -> pd.DataFrame:
    """
    Transform baseline flows into different intraday liquidity scenarios.
    """
    df = base_df.copy()
    df["scenario"] = scenario_name

    if scenario_name == "base_case":
        # Minimal changes: baseline noise is sufficient
        pass

    elif scenario_name == "stress_volume":
        # Higher outflows overall, mild delay in inflows
        # Increase outflows by ~20%, tilt them slightly later in the day
        df["outflow"] *= 1.12
        hour = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60
        late_factor = 1 + 0.10 * (hour > 12)
        df["outflow"] *= late_factor

        # Inflows are slightly weaker and tilt later
        df["inflow"] *= 0.95
        inflow_delay_factor = 1 - 0.08 * (hour < 11)
        df["inflow"] *= inflow_delay_factor

    elif scenario_name == "severe_stress":
        # Significant outflow spike + temporary inflow disruption
        hour = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60

        # Outflows: +35% overall, with a sharp peak mid-morning
        df["outflow"] *= 1.35
        spike_mask = (hour >= 10) & (hour <= 11.5)
        df.loc[spike_mask, "outflow"] *= 1.40

        # Inflows: reduced and delayed, especially early in the day
        df["inflow"] *= 0.85
        early_mask = hour < 11.5
        df.loc[early_mask, "inflow"] *= 0.70

    else:
        raise ValueError(f"Unknown scenario: {scenario_name}")

    return df


def compute_intraday_positions(
    df: pd.DataFrame,
    starting_balance: float,
    liquidity_buffer: float,
) -> pd.DataFrame:
    """
    Given inflows and outflows, compute intraday liquidity position and buffer usage.

    - intraday_position_t = starting_balance + cumulative(inflow - outflow)_t
    - buffer_remaining_t = max(intraday_position_t - core_balance_floor, 0)
      For simplicity, assume core_balance_floor = starting_balance - liquidity_buffer.
    """
    df = df.sort_values("timestamp").copy()

    core_floor = starting_balance - liquidity_buffer
    net_flow = df["inflow"] - df["outflow"]
    df["net_flow"] = net_flow
    df["cumulative_net_flow"] = net_flow.cumsum()

    df["intraday_position"] = starting_balance + df["cumulative_net_flow"]
    df["buffer_available"] = (df["intraday_position"] - core_floor).clip(lower=0.0)

    # Express buffer usage as % of original buffer
    df["buffer_usage_pct"] = 1 - df["buffer_available"] / liquidity_buffer

    # Flags for warning and breach
    df["warning_flag"] = df["buffer_available"] < (liquidity_buffer * WARNING_THRESHOLD_PCT)
    df["breach_flag"] = df["buffer_available"] < (liquidity_buffer * BREACH_THRESHOLD_PCT)

    return df


def add_time_to_breach(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute time-to-first-breach for each scenario and tag rows accordingly.

    For this synthetic dataset, we record the timestamp of the first buffer breach
    (if any) and calculate elapsed minutes from the start of day.
    """
    df = df.copy()
    df["time_since_start_min"] = (
        df["timestamp"] - df["timestamp"].min()
    ).dt.total_seconds() / 60

    # Scenario-level metrics (computed later in reporting script as well if needed)
    return df


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main() -> None:
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)

    # Step 1: Generate baseline flows
    time_index = generate_time_index()
    base_flows = simulate_base_flows(time_index, rng)

    # Step 2: Build scenarios
    scenarios: List[str] = ["base_case", "stress_volume", "severe_stress"]
    all_rows = []

    for scenario in scenarios:
        df_scn = apply_scenario_transforms(base_flows, scenario)
        df_scn = compute_intraday_positions(
            df_scn,
            starting_balance=BASE_STARTING_BALANCE,
            liquidity_buffer=BASE_LIQUIDITY_BUFFER,
        )
        df_scn = add_time_to_breach(df_scn)
        all_rows.append(df_scn)

    full_df = pd.concat(all_rows, ignore_index=True)
    full_df.to_csv(RAW_OUTPUT, index=False)

    # Simple console summary
    summary = (
        full_df.groupby("scenario")
        .agg(
            min_intraday_position=("intraday_position", "min"),
            min_buffer_available=("buffer_available", "min"),
            warning_intervals=("warning_flag", "sum"),
            breach_intervals=("breach_flag", "sum"),
        )
        .reset_index()
    )

    print(summary.to_dict(orient="records"))


if __name__ == "__main__":
    main()