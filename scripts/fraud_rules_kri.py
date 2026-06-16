"""
PaymentRisk360 - Fraud Risk Module
Script 02: Rules-Based Fraud Flags and KRI Summary

Purpose
-------
This script applies simple, interpretable fraud rules to the synthetic
card transaction dataset and produces KRIs suitable for second-line
fraud risk monitoring.

Rules included
--------------
1. Card-level velocity rule:
   - Flag cards that exceed a given transaction count threshold within a
     short time window (e.g., more than N transactions within W minutes).

2. High-amount rule:
   - Flag transactions above a configurable "unusually high" amount
     threshold for a card portfolio.

Outputs
-------
- data/processed/fraud_transactions_with_rules.csv
- outputs/fraud_card_kri_summary.csv
- outputs/fraud_portfolio_kri_overview.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

RAW_INPUT = Path("data/raw/fraud_transactions.csv")
PROCESSED_OUTPUT = Path("data/processed/fraud_transactions_with_rules.csv")
CARD_KRI_OUTPUT = Path("outputs/fraud_card_kri_summary.csv")
PORTFOLIO_KRI_OUTPUT = Path("outputs/fraud_portfolio_kri_overview.csv")

# ---------------------------------------------------------------------------
# Rule configuration (tunable thresholds)
# ---------------------------------------------------------------------------

# Velocity rule: if a card has more than this many transactions
# within the time window_minutes, transactions within that hot window are flagged.
VELOCITY_TX_THRESHOLD = 8
VELOCITY_WINDOW_MINUTES = 15

# High amount rule: any transaction above this amount is flagged.
HIGH_AMOUNT_THRESHOLD = 5_000.0

# Optional: country / channel filter could be added later (e.g., CNP only).


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def apply_velocity_rule(df: pd.DataFrame) -> pd.Series:
    """
    Apply a simple card-level velocity rule.

    For each card:
      - Sort transactions by timestamp.
      - Create a rolling count of transactions over a defined time window.
      - Flag transactions that occur when the rolling count exceeds threshold.

    Returns:
      pd.Series of booleans (same length as df) indicating velocity rule hits.
    """
    df = df.sort_values(["card_id", "timestamp"]).copy()
    hits = pd.Series(False, index=df.index)

    # Convert timestamps to pandas datetime if not already
    if not np.issubdtype(df["timestamp"].dtype, np.datetime64):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    window = pd.Timedelta(minutes=VELOCITY_WINDOW_MINUTES)

    for card_id, group in df.groupby("card_id"):
        times = group["timestamp"].values
        idx = group.index

        # Two-pointer approach for sliding window
        start = 0
        count_in_window = np.zeros(len(group), dtype=int)

        for end in range(len(group)):
            # Move start until window constraint is satisfied
            while times[end] - times[start] > window:
                start += 1
            count_in_window[end] = end - start + 1

        # Flag where count exceeds threshold
        card_hits = count_in_window > VELOCITY_TX_THRESHOLD
        hits.loc[idx] = card_hits | hits.loc[idx]

    return hits


def apply_high_amount_rule(df: pd.DataFrame) -> pd.Series:
    """
    Flag transactions with unusually high amounts.

    For now this is a simple global threshold rule, but in practice
    it could be segment-specific or card-history-specific. [web:153][web:160]
    """
    return df["amount"] >= HIGH_AMOUNT_THRESHOLD


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main() -> None:
    PROCESSED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    CARD_KRI_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_INPUT, parse_dates=["timestamp"])

    # Ensure required columns
    expected_cols = {
        "transaction_id",
        "card_id",
        "timestamp",
        "amount",
        "merchant_segment",
        "channel",
        "country",
        "is_fraud",
    }
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # 1. Apply rules
    df["rule_velocity"] = apply_velocity_rule(df)
    df["rule_high_amount"] = apply_high_amount_rule(df)

    # Composite rule flag
    df["any_rule_hit"] = df[["rule_velocity", "rule_high_amount"]].any(axis=1)

    # 2. Save transaction-level output
    df.to_csv(PROCESSED_OUTPUT, index=False)

    # 3. Card-level KRIs
    card_group = df.groupby("card_id")

    card_kri = card_group.agg(
        tx_count=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        fraud_tx=("is_fraud", "sum"),
        velocity_hits=("rule_velocity", "sum"),
        high_amount_hits=("rule_high_amount", "sum"),
        any_rule_hits=("any_rule_hit", "sum"),
    ).reset_index()

    card_kri["fraud_rate_card"] = card_kri["fraud_tx"] / card_kri["tx_count"]
    card_kri["rule_hit_rate"] = card_kri["any_rule_hits"] / card_kri["tx_count"]

    # Simple card-level status
    def card_status(row):
        if row["fraud_tx"] > 0 and row["any_rule_hits"] > 0:
            return "High Risk (Fraud & Rules)"
        if row["any_rule_hits"] > 0:
            return "Medium Risk (Rules Only)"
        return "Low Risk"

    card_kri["status"] = card_kri.apply(card_status, axis=1)

    card_kri.to_csv(CARD_KRI_OUTPUT, index=False)

    # 4. Portfolio-level KRI overview
    total_tx = len(df)
    total_fraud = int(df["is_fraud"].sum())
    total_rule_hits = int(df["any_rule_hit"].sum())

    # How many fraud tx are caught by rules?
    fraud_and_rule = int(df[(df["is_fraud"]) & (df["any_rule_hit"])].shape[0])
    fraud_not_flagged = total_fraud - fraud_and_rule

    # How many rule hits are likely false positives?
    rule_hits_not_fraud = int(df[(~df["is_fraud"]) & (df["any_rule_hit"])].shape[0])

    portfolio_rows = [
        {"metric": "total_transactions", "value": total_tx},
        {"metric": "total_fraud_transactions", "value": total_fraud},
        {"metric": "fraud_rate", "value": round(total_fraud / total_tx, 4)},
        {"metric": "total_rule_hits", "value": total_rule_hits},
        {"metric": "rule_hit_rate", "value": round(total_rule_hits / total_tx, 4)},
        {"metric": "fraud_captured_by_rules", "value": fraud_and_rule},
        {
            "metric": "fraud_capture_rate",
            "value": round(fraud_and_rule / total_fraud, 4) if total_fraud > 0 else None,
        },
        {"metric": "fraud_not_flagged_by_rules", "value": fraud_not_flagged},
        {"metric": "rule_hits_not_fraud", "value": rule_hits_not_fraud},
    ]

    portfolio_kri = pd.DataFrame(portfolio_rows)
    portfolio_kri.to_csv(PORTFOLIO_KRI_OUTPUT, index=False)

    # Console summary
    print(portfolio_kri.to_dict(orient="records")[:6])


if __name__ == "__main__":
    main()