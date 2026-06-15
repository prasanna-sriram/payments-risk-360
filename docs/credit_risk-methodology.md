# Credit Risk Methodology
## PaymentRisk360 – Merchant / Participant Credit Risk Module

---

## Table of Contents

- [Purpose of this Module](#purpose-of-this-module)
- [Business Framing of Credit Risk in Payments](#business-framing-of-credit-risk-in-payments)
- [Data Design Overview](#data-design-overview)
- [Modelling Approach](#modelling-approach)
- [Features Used in the Model](#features-used-in-the-model)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Risk Tiering](#risk-tiering)
- [Concentration Risk and Portfolio View](#concentration-risk-and-portfolio-view)
- [Intended Governance Story](#intended-governance-story)
- [Limitations](#limitations)


[Back to Top](#credit-risk-methodology)

---

## Purpose of this Module

This document explains how the **credit risk** component of the PaymentRisk360 project is designed and implemented. The goal is to show how a second-line risk function in a payments environment might:

- Identify merchants/participants with elevated **probability of distress or default**.
- Understand where **exposure is concentrated** in the portfolio.
- Translate those signals into **risk tiers**, early warnings, and governance-ready insights.

The methodology is deliberately **transparent and explainable**, since second-line oversight needs to be able to challenge assumptions and communicate clearly with product, finance, and executive stakeholders. Probability of default (PD) is treated in the usual sense: the likelihood a borrower or counterparty will fail to meet obligations over a given horizon (typically one year in standard credit practice).

[Back to Top](#credit-risk-methodology)

---

## Business Framing of Credit Risk in Payments

In this project, “credit risk” is not treated as traditional loan underwriting. Instead, it is framed around **merchant and participant exposure** in a payments network:

- **Settlement exposure** between authorization and settlement.
- **Chargeback-driven exposure**, where disputes can create contingent liabilities for the network or acquirer.
- **Reserve adequacy**, i.e., whether reserve levels are directionally consistent with risk.
- **Concentration risk**, where too much exposure is tied to a small number of merchants or high-risk segments.

Typical merchant risk assessments in payments consider business type, chargeback history, transaction volume, and financial strength, since some business models structurally introduce more exposure and chargeback risk than others.

This module is designed to simulate that environment using synthetic data.

[Back to Top](#credit-risk-methodology)

---

## Data Design Overview

The synthetic dataset is merchant-level and includes four main groups of variables:

1. **Business profile**
   - `merchant_id`
   - `industry_segment`
   - `settlement_frequency`

2. **Behaviour and risk signals**
   - `monthly_txn_count`
   - `average_ticket_size`
   - `monthly_transaction_volume`
   - `chargeback_rate`
   - `fraud_alert_rate`
   - `days_since_last_chargeback`

3. **Exposure and mitigants**
   - `concentration_ratio`
   - `reserve_coverage_ratio`
   - `gross_exposure`
   - `net_exposure`

4. **Outcome and latent signal**
   - `prior_default_flag`
   - `synthetic_pd_signal`
   - `risk_label` (binary distress/default flag)

The data is generated to reflect realistic relationships between these factors, not to match any specific institution’s actual distribution. For example, higher chargeback rates and higher transaction volumes tend to increase exposure, while stronger reserve coverage helps mitigate it.

A separate `data_dictionary.md` explains each field in more detail.

[Back to Top](#credit-risk-methodology)

---

## Modelling Approach

### Target: Synthetic Distress / Default Flag

The target variable `risk_label` is a synthetic binary outcome that indicates whether a merchant ends up in a “distress/default” state. The label is created from an internal score (`synthetic_pd_signal`) that combines:

- chargeback behaviour,
- fraud alert rate,
- exposure size,
- concentration,
- reserve coverage,
- recency of chargebacks,
- industry base risk,
- and prior distress.

This mirrors how PD in practice is a function of borrower characteristics and history, capturing the likelihood that a borrower or counterparty will not meet its obligations over a given horizon.

### Model Type: Logistic Regression

The module uses **logistic regression** for the PD-style model because:

- It is a standard statistical technique for estimating probability of default from borrower or counterparty characteristics.
- Coefficients can be examined and explained to stakeholders.
- It aligns with a second-line oversight context where model transparency and challengeability are important.

The model estimates a **predicted probability of default (`predicted_pd`)** for each merchant.

[Back to Top](#credit-risk-methodology)

---

## Features Used in the Model

The feature set is intentionally compact and interpretable.

### Numeric Features

- `monthly_txn_count` – volume of transactions, indicating scale and operational exposure.
- `average_ticket_size` – typical transaction value; higher values can increase loss per incident.
- `monthly_transaction_volume` – total processed volume; higher volumes increase exposure.
- `chargeback_rate` – historical chargeback proportion, a critical signal of merchant risk.
- `fraud_alert_rate` – synthetic fraud-related alerts; captures fraud-linked deterioration.
- `days_since_last_chargeback` – recency of chargeback activity (more recent may be riskier).
- `concentration_ratio` – how concentrated exposure is for this merchant vs. broader portfolio.
- `reserve_coverage_ratio` – how much exposure is offset by reserves/mitigants.
- `prior_default_flag` – prior distress history, a common credit risk factor.
- `gross_exposure` – synthetic gross exposure estimate.
- `net_exposure` – exposure after reserves; more decision-useful for oversight.

### Categorical Features

- `industry_segment` – differentiates structurally higher-risk sectors.
- `settlement_frequency` – reflects exposure duration (e.g., weekly settlement carries more exposure than daily).

[Back to Top](#credit-risk-methodology)

---

## Model Training and Evaluation

### Preprocessing

- **Numeric features** are standardized using `StandardScaler`.
- **Categorical features** are one-hot encoded via `OneHotEncoder`.
- The transformations are combined with `ColumnTransformer` and wrapped in a `Pipeline`.

### Train/Test Split

- 75% training / 25% test split.
- Stratified by `risk_label` to maintain class balance.

### Metrics

The model is evaluated using:

- **ROC-AUC** – overall ranking ability for default vs. non-default.
- **Accuracy at a 0.25 PD threshold** – directional classification performance.
- **Precision and recall at 0.25 PD threshold** – tradeoff between catching risk and false alarms.
- **Confusion matrix** – counts of true/false positives/negatives.

Thresholds are **illustrative**; in a real environment they would be aligned with risk appetite and loss tolerances.

[Back to Top](#credit-risk-methodology)

---

## Risk Tiering

### PD to Tier Mapping

The model’s `predicted_pd` is mapped into four risk tiers:

- **Low** – PD < 10%
- **Medium** – 10% ≤ PD < 25%
- **High** – 25% ≤ PD < 50%
- **Severe** – PD ≥ 50%

These bands are chosen for interpretability and prioritization, not as regulatory thresholds. In practice, tier boundaries would be:

- aligned with expected loss and capital considerations,
- informed by historical experience,
- and approved through governance.

Probability of default is only one component of expected loss; in standard formulations, expected credit loss combines **PD × LGD × EAD** (loss given default and exposure at default).

### Oversight Use

The risk tiers are intended to support:

- **Prioritization of reviews** (High/Severe merchants).
- **Monitoring of risk migration** over time.
- **Discussion of risk appetite** and onboarding/reserve policies.

[Back to Top](#credit-risk-methodology)

---

## Concentration Risk and Portfolio View

The module performs a simple concentration analysis:

1. **Top-merchant concentration**
   - Share of total net exposure in the top 5 merchants.
2. **High-risk exposure share**
   - Share of net exposure tied to High and Severe risk tiers.
3. **Industry-level view**
   - Net exposure by industry.
   - Average predicted PD by industry.
   - Counts of High/Severe merchants per industry.

Concentration risk matters because portfolios with exposure heavily weighted toward a small number of borrowers or sectors are more vulnerable to shocks. A second-line risk function often cares as much about **where exposure sits** as about individual risk scores.

The chart “Credit Risk Portfolio View: Exposure and Average PD by Industry” is used to visually support that oversight conversation.

[Back to Top](#credit-risk-methodology)

---

## Intended Governance Story

This credit module is meant to support a narrative like:

- “We have a view of **who** is risky (PD, risk tiers).”
- “We have a view of **where** exposure is concentrated (top merchants, industries).”
- “We can identify **how much** of the portfolio is in High/Severe risk tiers.”
- “We can propose **concentration thresholds** and **enhanced review** for high-risk pockets.”
- “We understand the **limitations** of the model and data.”

That is the kind of integrated view a second-line function would take to a Product Council or risk committee for discussion.

[Back to Top](#credit-risk-methodology)

---

## Limitations

This module has several intentional limitations:

- The dataset is **fully synthetic** and designed for portfolio demonstration, not production use.
- PD thresholds and tier boundaries are illustrative; they are not calibrated to real loss history.
- No explicit loss severity (LGD) or EAD curve is modelled; net exposure is treated as a simplified exposure proxy.
- Macroeconomic and forward-looking factors are out of scope for this version.

Despite these limitations, the module demonstrates:

- practical understanding of PD-style credit modelling,
- awareness of concentration risk,
- and the ability to translate analytical outputs into second-line risk and governance language.

[Back to Top](#credit-risk-methodology)

---