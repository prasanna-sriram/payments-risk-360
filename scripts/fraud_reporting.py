"""
PaymentRisk360 - Fraud Risk Module
Script 03: Fraud Reporting and Visualization

Purpose
-------
This script converts the rules-based fraud outputs into a small set of
portfolio-style reporting assets:

- charts of rule hit rates and high-risk cards
- a markdown report summarizing fraud KRIs and second-line interpretation

Inputs
------
- data/processed/fraud_transactions_with_rules.csv
- outputs/fraud_card_kri_summary.csv
- outputs/fraud_portfolio_kri_overview.csv

Outputs
-------
- outputs/fraud_rule_hit_rates.png
- outputs/fraud_top_risk_cards.png
- outputs/fraud_risk_report.md
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

TX_INPUT = Path("data/processed/fraud_transactions_with_rules.csv")
CARD_KRI_INPUT = Path("outputs/fraud_card_kri_summary.csv")
PORTFOLIO_KRI_INPUT = Path("outputs/fraud_portfolio_kri_overview.csv")

CHART_RULE_HITS_OUTPUT = Path("outputs/fraud_rule_hit_rates.png")
CHART_TOP_CARDS_OUTPUT = Path("outputs/fraud_top_risk_cards.png")
REPORT_OUTPUT = Path("outputs/fraud_risk_report.md")


def plot_rule_hit_rates(df_tx: pd.DataFrame, output_path: Path) -> None:
    """
    Plot rule hit rates (velocity vs high-amount) at portfolio level.
    """
    total_tx = len(df_tx)

    counts = {
        "velocity_hits": df_tx["rule_velocity"].sum(),
        "high_amount_hits": df_tx["rule_high_amount"].sum(),
    }

    rates = {k: v / total_tx for k, v in counts.items()}

    labels = ["Velocity Rule", "High Amount Rule"]
    values = [rates["velocity_hits"], rates["high_amount_hits"]]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=["#4C78A8", "#E45756"])
    plt.ylabel("Hit Rate (share of transactions)")
    plt.title("Fraud Rule Hit Rates (Portfolio Level)")
    plt.ylim(0, max(values) * 1.3 if max(values) > 0 else 1)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_top_risk_cards(df_card: pd.DataFrame, output_path: Path, top_n: int = 15) -> None:
    """
    Plot top N cards by number of rule hits, colored by status.
    """
    df_top = df_card.sort_values(["any_rule_hits", "fraud_tx"], ascending=[False, False]).head(top_n)

    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        df_top["card_id"],
        df_top["any_rule_hits"],
        color=["#E45756" if s.startswith("High") else "#F2A541" if s.startswith("Medium") else "#4C78A8"
               for s in df_top["status"]],
    )
    plt.xticks(rotation=45)
    plt.ylabel("Rule Hits (per card)")
    plt.title(f"Top {top_n} Cards by Rule Hits")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()


def build_markdown_report(
    df_tx: pd.DataFrame,
    df_card: pd.DataFrame,
    df_portfolio: pd.DataFrame,
) -> str:
    """
    Build a second-line style markdown report using portfolio and card KRIs.
    """
    # Extract key metrics
    metrics = {row["metric"]: row["value"] for _, row in df_portfolio.iterrows()}

    total_tx = int(metrics.get("total_transactions", 0))
    total_fraud = int(metrics.get("total_fraud_transactions", 0))
    fraud_rate = metrics.get("fraud_rate", None)
    total_rule_hits = int(metrics.get("total_rule_hits", 0))
    rule_hit_rate = metrics.get("rule_hit_rate", None)
    fraud_captured = int(metrics.get("fraud_captured_by_rules", 0))
    fraud_capture_rate = metrics.get("fraud_capture_rate", None)
    fraud_not_flagged = int(metrics.get("fraud_not_flagged_by_rules", 0))
    rule_hits_not_fraud = int(metrics.get("rule_hits_not_fraud", 0))

    # Top cards table (for the report)
    top_cards = (
        df_card.sort_values(["any_rule_hits", "fraud_tx"], ascending=[False, False])
        .head(10)[["card_id", "tx_count", "fraud_tx", "any_rule_hits", "status"]]
    )

    top_cards_md = top_cards.to_markdown(index=False)

    report = f"""# Fraud Risk Report

## Executive Summary

This analysis uses simple, interpretable fraud rules applied at the card level
to identify unusual transaction patterns and support second-line fraud risk
monitoring.

Two types of rules are implemented:

- **Velocity rule**: flags cards that exceed a transaction count threshold within a short time window (e.g., more than {VELOCITY_TX_THRESHOLD} transactions within {VELOCITY_WINDOW_MINUTES} minutes). This reflects standard guidance to use velocity checks as a first layer to catch rapid abuse patterns.
- **High-amount rule**: flags transactions with unusually large amounts (over {HIGH_AMOUNT_THRESHOLD:,.0f}), consistent with common guidance to set upper amount filters for high-risk payments.

At portfolio level:

- Total transactions: **{total_tx:,}**
- Total fraud transactions (synthetic label): **{total_fraud:,}**
- Overall fraud rate: **{fraud_rate:.4f}**
- Total rule hits (any rule): **{total_rule_hits:,}**
- Rule hit rate: **{rule_hit_rate:.4f}**
- Fraud captured by rules: **{fraud_captured:,}** (capture rate: **{fraud_capture_rate:.4f}**)
- Fraud not flagged by rules: **{fraud_not_flagged:,}**
- Rule hits that are not fraud (potential false positives): **{rule_hits_not_fraud:,}**

These figures illustrate a typical trade-off: rules capture a large share of fraud while also generating some false positives, which must be managed through review processes and tuning.

## Card-Level View

### Top Cards by Rule Hits

The table below shows the top 10 cards by number of rule hits, along with their synthetic fraud counts and status:

{top_cards_md}

Interpretation:

- **High Risk (Fraud & Rules)** cards are those where both fraudulent transactions and rule hits are present. These cards would typically require immediate investigation and potential blocking.
- **Medium Risk (Rules Only)** cards are those with rule hits but no confirmed fraud yet; they would be candidates for monitoring, additional verification, or dynamic controls.
- **Low Risk** cards have no rule hits and no observed fraud in this synthetic dataset.

## Rules and KRI Interpretation

From a second-line perspective, key messages from these KRIs are:

- **Effectiveness:** The share of fraud captured by the rules (capture rate) indicates whether the current rules are effective as a first-line filter.
- **Efficiency:** The number of rule hits that are not fraud highlights the operational burden of false positives and whether rules are too broad.
- **Coverage:** The overall fraud rate and rule hit rate provide context on how much of the portfolio is being scrutinized by rules.

In practice, fraud monitoring programs use these types of KRIs to balance fraud prevention with customer experience and operational capacity.

## Recommendations

- Use the current velocity and high-amount rules as a **baseline** and then iteratively tune thresholds to improve fraud capture while managing false positives.
- Introduce additional conditions (e.g., card-not-present only, foreign country filters, high-risk merchant segments) to sharpen rule precision.
- Define clear **escalation criteria** for when High Risk cards should be blocked or subject to additional verification.
- Consider adding a **risk score** on top of rules in a later phase, aggregating rule hits and behaviour patterns into a single summarizing metric.

## Limitations

- The dataset is synthetic and calibrated for demonstration; real fraud rates and patterns will differ.
- Rules are intentionally simple and global; production systems often use more granular, segment-specific thresholds and machine learning models.
- The is_fraud label represents injected fraud scenarios, not confirmed historical fraud cases.

"""

    return report


# Import rule config values from script 02 if needed
# To keep this script self-contained, we re-declare the thresholds here:
VELOCITY_TX_THRESHOLD = 8
VELOCITY_WINDOW_MINUTES = 15
HIGH_AMOUNT_THRESHOLD = 5_000.0


def main() -> None:
    CHART_RULE_HITS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df_tx = pd.read_csv(TX_INPUT, parse_dates=["timestamp"])
    df_card = pd.read_csv(CARD_KRI_INPUT)
    df_portfolio = pd.read_csv(PORTFOLIO_KRI_INPUT)

    # Charts
    plot_rule_hit_rates(df_tx, CHART_RULE_HITS_OUTPUT)
    plot_top_risk_cards(df_card, CHART_TOP_CARDS_OUTPUT)

    # Report
    report_md = build_markdown_report(df_tx, df_card, df_portfolio)
    REPORT_OUTPUT.write_text(report_md, encoding="utf-8")

    print(
        {
            "rule_hits_chart": str(CHART_RULE_HITS_OUTPUT),
            "top_cards_chart": str(CHART_TOP_CARDS_OUTPUT),
            "report": str(REPORT_OUTPUT),
        }
    )


if __name__ == "__main__":
    main()