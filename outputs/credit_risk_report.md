# Credit Risk Report

## Executive Summary

This analysis evaluates synthetic merchant-level credit risk in a payments context using a PD-style logistic regression model, exposure analysis, and concentration review. The objective is to simulate how a second-line risk function might identify elevated merchant risk, challenge exposure build-up, and translate portfolio signals into management-ready reporting.

The portfolio-level view shows a weighted average predicted PD of **69.32%** and a top-5 merchant exposure concentration of **4.43%**. High and Severe risk tiers together account for **74.57%** of total net exposure, indicating that portfolio quality cannot be assessed using average loss indicators alone.

The highest industry exposure is concentrated in **travel**, which represents **22.76%** of synthetic portfolio exposure. This makes concentration monitoring as important as standalone PD estimates.

## Business Problem

In a payments environment, credit risk is not limited to classic lending. It can also arise through merchant settlement exposure, chargeback-driven obligations, reserve insufficiency, and concentration to higher-risk sectors. A second-line function should therefore evaluate not only who is risky, but also where portfolio exposure is building faster than control or reserve capacity.

## Methodology

The analysis uses a synthetic merchant dataset with merchant characteristics such as transaction volume, average ticket size, chargeback rate, fraud alert rate, reserve coverage, prior distress, and net exposure. A logistic regression model was selected because it is interpretable, easy to challenge, and suitable for portfolio segmentation in a second-line oversight setting.

After model scoring, merchants were grouped into four risk tiers: Low, Medium, High, and Severe. Portfolio analysis then focused on exposure concentration, segment-level average PD, and the share of exposure tied to higher-risk merchants.

## Results and Business Recommendations

### Key findings

- Weighted average predicted PD: **69.32%**
- Top-5 merchant exposure share: **4.43%**
- High + Severe risk exposure share: **74.57%**
- Highest exposure industry: **travel**

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
