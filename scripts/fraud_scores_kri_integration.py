"""
PaymentRisk360 - Fraud Risk Module
Script 06: Integrate AI Fraud Scores into KRI View

Purpose
-------
This script integrates the AI-driven fraud risk scores into the existing
fraud KRI framework. It:

- Aggregates transaction-level fraud_risk_score to card-level KRIs.
- Combines rules-based and model-based signals into a simple status.
- Summarizes fraud rate by score buckets at portfolio level.

Inputs
------
- data/processed/fraud_transactions_with_scores.csv
- outputs/fraud_card_kri_summary.csv

Outputs
-------
- outputs/fraud_card_kri_with_scores.csv
- outputs/fraud_score_buckets_summary.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

TX_SCORED_INPUT = Path("data/processed/fraud_transactions_with_scores.csv")
CARD_KRI_INPUT = Path("outputs/fraud_card_kri_summary.csv")

CARD_KRI_WITH_SCORES_OUTPUT = Path("outputs/fraud_card_kri_with_scores.csv")
SCORE_BUCKETS_OUTPUT = Path("outputs/fraud_score_buckets_summary.csv")


def main() -> None:
    CARD_KRI_WITH_SCORES_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df_tx = pd.read_csv(TX_SCORED_INPUT, parse_dates=["timestamp"])
    df_card_kri = pd.read_csv(CARD_KRI_INPUT)

    # Basic checks
    if "fraud_risk_score" not in df_tx.columns:
        raise ValueError("fraud_risk_score column missing from transactions file.")

    # 1. Card-level aggregation of scores
    card_scores = df_tx.groupby("card_id").agg(
        avg_fraud_score=("fraud_risk_score", "mean"),
        max_fraud_score=("fraud_risk_score", "max"),
        tx_count=("transaction_id", "count"),
        fraud_tx=("is_fraud", "sum"),
        any_rule_hits=("any_rule_hit", "sum"),
    ).reset_index()

    # Merge with existing card KRIs
    df_card = df_card_kri.merge(card_scores, on="card_id", how="left", suffixes=("", "_score"))

    # 2. Combined status (rules + model)
    def combined_status(row):
        high_score = row["max_fraud_score"] is not None and row["max_fraud_score"] >= 0.8
        med_score = row["max_fraud_score"] is not None and 0.5 <= row["max_fraud_score"] < 0.8

        if row["fraud_tx"] > 0 and (row["any_rule_hits"] > 0 or high_score):
            return "High Risk (Fraud, Rules & Model)"

        if high_score and row["any_rule_hits"] > 0:
            return "High Risk (Rules & Model)"

        if high_score and row["any_rule_hits"] == 0:
            return "Medium Risk (Model Only)"

        if med_score and row["any_rule_hits"] > 0:
            return "Medium Risk (Rules & Model)"

        if row["any_rule_hits"] > 0 or med_score:
            return "Medium Risk"

        return "Low Risk"

    df_card["combined_status"] = df_card.apply(combined_status, axis=1)

    df_card.to_csv(CARD_KRI_WITH_SCORES_OUTPUT, index=False)

    # 3. Score bucket summary at transaction level
    # Create decile buckets of fraud_risk_score
    df_tx["score_bucket"] = pd.qcut(df_tx["fraud_risk_score"], q=10, labels=False, duplicates="drop")

    bucket_summary = (
        df_tx.groupby("score_bucket")
        .agg(
            tx_count=("transaction_id", "count"),
            fraud_tx=("is_fraud", "sum"),
            avg_score=("fraud_risk_score", "mean"),
        )
        .reset_index()
        .sort_values("score_bucket")
    )

    bucket_summary["fraud_rate"] = bucket_summary["fraud_tx"] / bucket_summary["tx_count"]
    bucket_summary.to_csv(SCORE_BUCKETS_OUTPUT, index=False)

    # Console summary
    print(
        {
            "card_kri_with_scores": str(CARD_KRI_WITH_SCORES_OUTPUT),
            "score_buckets_summary": str(SCORE_BUCKETS_OUTPUT),
        }
    )


if __name__ == "__main__":
    main()