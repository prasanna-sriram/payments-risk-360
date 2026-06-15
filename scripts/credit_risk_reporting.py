"""
PaymentRisk360 - Credit Risk Module
Script 03: Concentration Analysis and Reporting Outputs

Purpose
-------
This script converts the model-scored merchant dataset into governance-oriented
credit risk outputs suitable for portfolio reporting.

Why this exists
---------------
A second-line credit risk role is not only about modelling probability of
default. It is also about understanding where exposures are concentrated,
identifying segments that warrant challenge, and converting analysis into clear
management information.

What the script does
--------------------
1. Aggregates portfolio exposure and average PD by industry
2. Calculates exposure concentration in top merchants
3. Exports an industry concentration summary table
4. Produces a chart comparing exposure and average PD by industry
5. Creates a short markdown report that can be published to GitHub

Outputs
-------
- outputs/credit_industry_summary.csv
- outputs/credit_risk_exposure_chart.png
- outputs/credit_risk_report.md
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_PATH = Path("data/processed/credit_risk_features.csv")
SUMMARY_OUTPUT = Path("outputs/credit_industry_summary.csv")
CHART_OUTPUT = Path("outputs/credit_risk_exposure_chart.png")
REPORT_OUTPUT = Path("outputs/credit_risk_report.md")


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main() -> None:
    # Ensure output folder exists
    SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # 1. Load processed/scored data
    df = pd.read_csv(INPUT_PATH)

    # 2. Industry-level summary
    industry_summary = (
        df.groupby("industry_segment", as_index=False)
        .agg(
            merchant_count=("merchant_id", "count"),
            total_net_exposure=("net_exposure", "sum"),
            avg_predicted_pd=("predicted_pd", "mean"),
            avg_chargeback_rate=("chargeback_rate", "mean"),
            severe_risk_merchants=("risk_tier", lambda x: (x == "Severe").sum()),
            high_or_severe_merchants=("risk_tier", lambda x: x.isin(["High", "Severe"]).sum()),
        )
        .sort_values("total_net_exposure", ascending=False)
    )
    industry_summary["portfolio_exposure_share"] = (
        industry_summary["total_net_exposure"]
        / industry_summary["total_net_exposure"].sum()
    )

    industry_summary.to_csv(SUMMARY_OUTPUT, index=False)

    # 3. Portfolio-level concentration metrics
    top5_share = (
        df.sort_values("net_exposure", ascending=False)
        .head(5)["net_exposure"]
        .sum()
        / df["net_exposure"].sum()
    )
    high_risk_exposure = (
        df[df["risk_tier"].isin(["High", "Severe"])]["net_exposure"].sum()
        / df["net_exposure"].sum()
    )
    weighted_pd = (
        (df["predicted_pd"] * df["net_exposure"]).sum() / df["net_exposure"].sum()
    )

    # 4. Build chart dataset
    chart_df = industry_summary.copy()
    chart_df["avg_predicted_pd_pct"] = chart_df["avg_predicted_pd"] * 100
    chart_df["total_net_exposure_m"] = chart_df["total_net_exposure"] / 1_000_000

    # 5. Create exposure vs PD chart
    fig, ax1 = plt.subplots(figsize=(12, 7))

    ax1.bar(
        chart_df["industry_segment"],
        chart_df["total_net_exposure_m"],
        color="#4C78A8",
        alpha=0.85,
        label="Net Exposure ($M)",
    )
    ax1.set_ylabel("Total Net Exposure ($M)")
    ax1.set_xlabel("Industry Segment")
    ax1.tick_params(axis="x", rotation=35)

    ax2 = ax1.twinx()
    ax2.plot(
        chart_df["industry_segment"],
        chart_df["avg_predicted_pd_pct"],
        color="#E45756",
        marker="o",
        linewidth=2.5,
        label="Average Predicted PD (%)",
    )
    ax2.set_ylabel("Average Predicted PD (%)")

    plt.title("Credit Risk Portfolio View: Exposure and Average PD by Industry")
    fig.tight_layout()
    plt.savefig(CHART_OUTPUT, dpi=200, bbox_inches="tight")
    plt.close()

    # 6. Create markdown report
    top_industry = industry_summary.iloc[0]

    report = f"""# Credit Risk Report

## Executive Summary

This analysis evaluates synthetic merchant-level credit risk in a payments context using a PD-style logistic regression model, exposure analysis, and concentration review. The objective is to simulate how a second-line risk function might identify elevated merchant risk, challenge exposure build-up, and translate portfolio signals into management-ready reporting.

The portfolio-level view shows a weighted average predicted PD of **{weighted_pd:.2%}** and a top-5 merchant exposure concentration of **{top5_share:.2%}**. High and Severe risk tiers together account for **{high_risk_exposure:.2%}** of total net exposure, indicating that portfolio quality cannot be assessed using average loss indicators alone.

The highest industry exposure is concentrated in **{top_industry['industry_segment']}**, which represents **{top_industry['portfolio_exposure_share']:.2%}** of synthetic portfolio exposure. This makes concentration monitoring as important as standalone PD estimates.

## Business Problem

In a payments environment, credit risk is not limited to classic lending. It can also arise through merchant settlement exposure, chargeback-driven obligations, reserve insufficiency, and concentration to higher-risk sectors. A second-line function should therefore evaluate not only who is risky, but also where portfolio exposure is building faster than control or reserve capacity.

## Methodology

The analysis uses a synthetic merchant dataset with merchant characteristics such as transaction volume, average ticket size, chargeback rate, fraud alert rate, reserve coverage, prior distress, and net exposure. A logistic regression model was selected because it is interpretable, easy to challenge, and suitable for portfolio segmentation in a second-line oversight setting.

After model scoring, merchants were grouped into four risk tiers: Low, Medium, High, and Severe. Portfolio analysis then focused on exposure concentration, segment-level average PD, and the share of exposure tied to higher-risk merchants.

## Results and Business Recommendations

### Key findings

- Weighted average predicted PD: **{weighted_pd:.2%}**
- Top-5 merchant exposure share: **{top5_share:.2%}**
- High + Severe risk exposure share: **{high_risk_exposure:.2%}**
- Highest exposure industry: **{top_industry['industry_segment']}**

### Recommendations

- Apply enhanced review to merchants with both high predicted PD and high net exposure.
- Establish concentration thresholds at industry and top-merchant levels, not only at individual merchant level.
- Review reserve adequacy for higher-risk merchants with recent chargeback activity.
- Use the PD model as an early-warning tool, then supplement it with policy thresholds and second-line challenge rather than treating the score as a final decision engine.

## Next Steps

- Add loss severity logic so the framework can evolve from PD-only thinking to PD × Exposure-style prioritization.
- Introduce scenario stress tests for industry-specific deterioration or chargeback spikes.
- Benchmark logistic regression against a tree-based challenger model while preserving explainability.
- Integrate the output into the portfolio-wide ERM dashboard planned for later project stages.

## Limitations

This analysis uses synthetic data and illustrative thresholds. It is intended to demonstrate methodology, governance thinking, and risk segmentation rather than replicate a production credit model. Real calibration would require historical default, settlement loss, chargeback, and reserve data.
"""

    REPORT_OUTPUT.write_text(report, encoding="utf-8")

    # 7. Console summary for quick validation
    print(
        {
            "industry_rows": len(industry_summary),
            "top5_share": round(float(top5_share), 4),
            "high_risk_exposure_share": round(float(high_risk_exposure), 4),
        }
    )


if __name__ == "__main__":
    main()