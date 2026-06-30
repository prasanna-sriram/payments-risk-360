# Power BI Design Notes

---

## Table of Contents

- [Objective](#objective)
- [Dashboard Goals](#dashboard-goals)
- [Dashboard Pages](#dashboard-pages)
    - [Executive Overview](#executive-overview)
    - [Credit Risk](#credit-risk)
    - [Liquidity Risk](#liquidity-risk)
    - [Fraud Risk](#fraud-risk)
    - [AI Fraud Detection](#ai-fraud-detection)
- [Power BI Build Notes](#power-bi-build-notes)

[Back to Top](#power-bi-design-notes)

---

## Objective

Build an integrated **Enterprise Risk Management (ERM)** dashboard in Power BI that brings together the project's four workstreams:

- Credit Risk
- Intraday Liquidity Risk
- Fraud Risk (rules + KRIs)
- AI-Driven Fraud Detection

The dashboard should present a **second-line executive view** of the risk profile, showing where risk is concentrated, where thresholds are breached, and where escalation may be needed. It should support both high-level oversight and drill-down into each risk module.

[Back to Top](#power-bi-design-notes)

---

## Dashboard Goals

- Combine outputs from multiple Python workstreams into one executive reporting layer.
- Show **portfolio-level risk posture** across credit, liquidity, and fraud.
- Highlight **key KRIs**, threshold breaches, and scenario outcomes.
- Demonstrate how **rules-based** and **AI-driven** fraud monitoring fit into a governance-friendly ERM framework.
- Support discussions with Product, Risk, and Executive stakeholders.

[Back to Top](#power-bi-design-notes)

---

## Dashboard Pages

### Executive Overview
**Goal:** Provide a one-page cross-risk snapshot for leadership.

**Suggested visuals:**
- KPI cards for top portfolio metrics
- Credit risk tier distribution
- Intraday liquidity scenario status summary
- Fraud rule / AI monitoring summary
- High-risk items table (top merchants/cards/scenarios)

**Primary data sources:**
- `outputs/merchant_pd_metrics.csv`
- `outputs/merchant_industry_summary.csv`
- `outputs/top_20_merchants_by_exposure.csv`
- `outputs/intraday_liquidity_kri_summary.csv`
- `outputs/fraud_portfolio_kri_overview.csv`
- `outputs/fraud_card_kri_with_scores.csv`
- `outputs/fraud_score_buckets_summary.csv`

### Credit Risk
**Goal:** Show merchant/participant credit exposure, risk tiers, concentration, and PD-style model outputs.

**Suggested visuals:**
- KPI cards (portfolio default rate, average PD, % exposure in high/severe tiers)
- Risk tier distribution chart
- Industry concentration chart
- Top merchants by exposure chart/table
- Merchant detail table

**Primary data sources:**
- `data/processed/merchant_pd_scored.csv`
- `outputs/merchant_pd_metrics.csv`
- `outputs/merchant_industry_summary.csv`
- `outputs/top_20_merchants_by_exposure.csv`

### Liquidity Risk
**Goal:** Show intraday scenario monitoring, buffer usage, warnings, and breaches.

**Suggested visuals:**
- KPI cards (scenario statuses, min buffer, time-to-first-breach)
- Intraday liquidity line chart by scenario
- Buffer availability line chart by scenario
- Scenario comparison table

**Primary data sources:**
- `data/processed/intraday_liquidity_positions.csv`
- `outputs/intraday_liquidity_kri_summary.csv`

### Fraud Risk
**Goal:** Show rules-based fraud monitoring and card-level risk concentrations.

**Suggested visuals:**
- KPI cards (fraud rate, rule hit rate, fraud capture rate)
- Rule hit rate chart
- Top high-risk cards chart/table
- Fraud transactions / cards breakdown by status

**Primary data sources:**
- `data/processed/fraud_transactions_with_rules.csv`
- `outputs/fraud_portfolio_kri_overview.csv`
- `outputs/fraud_card_kri_summary.csv`

### AI Fraud Detection
**Goal:** Show fraud model performance, score distributions, and how scores integrate with KRIs.

**Suggested visuals:**
- KPI cards (ROC-AUC, average precision, recall)
- Fraud rate by score bucket chart
- Top features chart
- Combined rules + model high-risk cards table

**Primary data sources:**
- `data/processed/fraud_transactions_with_scores.csv`
- `outputs/fraud_ml_metrics.csv`
- `outputs/fraud_ml_feature_importance.csv`
- `outputs/fraud_card_kri_with_scores.csv`
- `outputs/fraud_score_buckets_summary.csv`

[Back to Top](#power-bi-design-notes)

---

## Power BI Build Notes

- Import CSV outputs directly from the project folders.
- Create a simple star-like model where practical, but for this portfolio dashboard, a light relational model is acceptable.
- Use consistent risk colors across pages:
  - Green = normal / within tolerance
  - Amber = early warning / elevated
  - Red = breach / high risk
- Use slicers sparingly on executive pages; reserve detailed filters for module pages.
- Keep the executive page simple and visual, with detailed analysis on the supporting pages.

[Back to Top](#power-bi-design-notes)

---