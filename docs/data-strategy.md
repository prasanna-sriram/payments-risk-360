# Data Strategy: PaymentRisk360 Synthetic Data Approach

---

## Table of Contents

- [Objective](#objective)
- [Why Synthetic Data is the Right Choice](#why-synthetic-data-is-the-right-choice)
- [Workstream-Level Data Design](#workstream-level-data-design)
- [Modelling Principles](#modelling-principles)
- [Documentation Expectations](#documentation-expectations)
- [File and Folder Usage](#file-and-folder-usage)
- [Risk Governance Framing](#risk-governance-framing)
- [Future Enhancement Option](#future-enhancement-option)

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Objective

This project will use **100% synthetic data** across all workstreams. The goal is to demonstrate risk methodology, analytics capability, and second-line oversight thinking without using proprietary, customer, or operational payment data.

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Why Synthetic Data Is the Right Choice

### 1. Speed and control

Synthetic data allows the full project to move quickly without being blocked by external downloads, access issues, or data quality constraints.

### 2. Better alignment to the portfolio goal

The project is meant to show:

- How risks would be framed
- What metrics and KRIs would be monitored
- How second-line challenge would be documented
- How executive-level risk reporting would be structured

The core value is in the **risk logic and oversight framing**, not in claiming access to real production data.

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Workstream-Level Data Design

### Credit Risk Data

Synthetic merchant / participant-level data will be generated with fields such as:
- `merchant_id`
- `industry_segment`
- `monthly_transaction_volume`
- `average_ticket_size`
- `chargeback_rate`
- `days_since_last_chargeback`
- `settlement_frequency`
- `net_exposure`
- `concentration_ratio`
- `prior_default_flag`
- `risk_label` (for supervised modelling where needed)

**Purpose:** support PD-style scoring, segmentation, and concentration analysis.

### Liquidity Risk Data

Synthetic settlement-flow data will be generated with fields such as:
- `timestamp`
- `participant_id`
- `payment_inflow`
- `payment_outflow`
- `net_flow`
- `available_liquidity_buffer`
- `stress_scenario`
- `counterparty_delay_flag`
- `counterparty_default_flag`

**Purpose:** support intraday liquidity stress testing, threshold monitoring, and time-to-breach analysis.

### Fraud Risk Data

Synthetic transaction-level data will be generated with fields such as:
- `transaction_id`
- `merchant_id`
- `customer_id`
- `device_id`
- `transaction_amount`
- `transaction_timestamp`
- `geo_region`
- `merchant_category`
- `is_high_risk_hour`
- `velocity_count_10m`
- `distance_from_home_region`
- `chargeback_outcome`
- `fraud_label`

**Purpose:** support rule-based fraud detection, KRI monitoring, and later ML-based anomaly detection.

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Modelling Principles

All synthetic datasets should follow these principles:

- Be realistic enough to support business interpretation
- Include both normal and stressed scenarios
- Allow explicit documentation of assumptions
- Include edge cases that support second-line challenge
- Be reproducible through scripts with fixed random seeds

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Documentation Expectations

Every script and output should document:

- Key assumptions used in data generation
- What the synthetic fields represent
- What limitations exist versus a live payment environment
- Where thresholds are illustrative rather than regulatory requirements

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## File and Folder Usage

### Raw synthetic outputs
- `data/raw/` for generated base datasets

### Processed outputs
- `data/processed/` for cleaned, feature-engineered, or scenario-enriched datasets

### Metadata
- `data/data_dictionary.md` for field definitions and assumptions

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Risk Governance Framing

Synthetic data is acceptable for this project because the purpose is to simulate how a second-line ERM function would:

- Set KRIs
- Monitor threshold breaches
- Challenge first-line assumptions
- Prepare governance reporting
- Escalate material risks

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---

## Future Enhancement Option

If needed later, a public fraud dataset can be used as a benchmarking layer. However, version 1 of the project will remain fully synthetic to keep development fast, controlled, and easy to explain.

[Back to Top](#data-strategy-paymentrisk360-synthetic-data-approach)

---