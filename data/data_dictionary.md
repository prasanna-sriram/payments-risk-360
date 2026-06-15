# Data Dictionary

---

## Credit Risk Dataset (Synthetic Merchants)

This document describes the fields in the **synthetic credit risk dataset** used for the merchant/participant credit module in the PaymentRisk360 project.

The dataset is merchant-level and is designed to support:

- PD-style (probability of default) modelling, where PD is the likelihood a counterparty fails to meet obligations over a given horizon, typically one year.
- Exposure and concentration analysis across merchants and industries, since concentration risk arises when credit exposure becomes too heavily weighted to specific names or sectors.
- Governance and second-line review of merchant risk drivers such as chargebacks, reserves, and transaction volume.

All values are synthetic and generated for demonstration purposes.

[Back to Top](#data-dictionary)

---

## Field List

### Identification & Business Profile

**`merchant_id`**  
- Type: string  
- Example: `"M00042"`  
- Description: Unique synthetic identifier assigned to each merchant/participant.  
- Usage: Join key, reporting dimension, traceability in top-exposure lists.

**`industry_segment`**  
- Type: categorical  
- Example values: `grocery`, `retail`, `travel`, `gaming`, `digital_services`, `restaurants`, `electronics`  
- Description: Synthetic industry grouping indicating the merchant’s primary business sector.  
- Rationale: Some industries are structurally higher risk (e.g., higher chargebacks, longer fulfilment times) and therefore contribute differently to merchant risk.

**`settlement_frequency`**  
- Type: categorical  
- Example values: `daily`, `twice_weekly`, `weekly`  
- Description: Settlement cycle used for paying out funds to the merchant.  
- Rationale: Longer settlement frequencies imply funds are held longer, increasing effective exposure duration.

[Back to Top](#data-dictionary)

---

### Volume & Transaction Behaviour

**`monthly_txn_count`**  
- Type: integer  
- Example: `12_500`  
- Description: Approximate number of transactions processed by the merchant in a typical month.  
- Rationale: Higher counts increase operational and aggregate exposure.

**`average_ticket_size`**  
- Type: float (currency)  
- Example: `45.75`  
- Description: Average value of individual transactions for the merchant.  
- Rationale: Higher ticket sizes increase potential loss per transaction, especially for disputes or fraud events.

**`monthly_transaction_volume`**  
- Type: float (currency)  
- Example: `572_300.50`  
- Description: Estimated total transaction amount processed by the merchant in a month (`monthly_txn_count × average_ticket_size`).  
- Rationale: Captures the scale of merchant activity and potential settlement exposure.

[Back to Top](#data-dictionary)

---

### Risk Indicators (Behavioural Signals)

**`chargeback_rate`**  
- Type: float (ratio)  
- Example: `0.0125` (1.25%)  
- Description: Fraction of transactions that result in chargebacks.  
- Rationale: Central driver of merchant risk; high or rising chargeback rates are a classic high-risk indicator in payments.

**`fraud_alert_rate`**  
- Type: float (ratio)  
- Example: `0.0060` (0.60%)  
- Description: Synthetic rate of transactions that trigger fraud screening alerts.  
- Rationale: Captures fraud-linked deterioration and operational risk patterns.

**`days_since_last_chargeback`**  
- Type: integer (days)  
- Example: `14`  
- Description: Number of days since the last chargeback occurred.  
- Rationale: More recent activity can indicate current or emerging risk, useful in early-warning monitoring.

[Back to Top](#data-dictionary)

---

### Exposure & Mitigation

**`concentration_ratio`**  
- Type: float (ratio, 0–1)  
- Example: `0.22`  
- Description: Synthetic measure of how concentrated this merchant’s exposure is relative to the broader portfolio, or how concentrated their customer/volume sources are.  
- Rationale: Supports concentration analysis at merchant level; portfolios overloaded in a few high-concentration merchants are more vulnerable to correlated losses.

**`reserve_coverage_ratio`**  
- Type: float (ratio)  
- Example: `0.85`  
- Description: Approximate share of exposure that is effectively covered by reserves or similar mitigants (e.g., rolling reserves).  
- Rationale: Lower reserve coverage implies weaker protection against chargebacks and losses.

**`gross_exposure`**  
- Type: float (currency)  
- Example: `75_000.00`  
- Description: Synthetic estimate of exposure before reserve mitigation, driven by transaction volume and settlement timing.  
- Usage: Useful for understanding raw exposure swing if mitigants were not present.

**`net_exposure`**  
- Type: float (currency)  
- Example: `48_500.00`  
- Description: Synthetic estimate of exposure after accounting for reserve coverage (`gross_exposure` minus reserves).  
- Usage: Primary exposure measure for risk tiering and concentration analysis, more aligned with expected loss thinking where exposure at default is a key component.

[Back to Top](#data-dictionary)

---

### History & Outcome

**`prior_default_flag`**  
- Type: binary (0/1)  
- Example: `1`  
- Description: Indicates whether the merchant has a synthetic history of prior distress/default events.  
- Rationale: Prior adverse history is a standard predictor used in PD modelling and underwriting.

**`synthetic_pd_signal`**  
- Type: float (0–1)  
- Example: `0.18`  
- Description: Latent probability-like score used during data generation to represent underlying distress risk before labelling.  
- Usage: An internal artefact for understanding how the synthetic label was constructed; not used as a feature in the PD model to avoid target leakage.

**`risk_label`**  
- Type: binary (0/1)  
- Example: `1`  
- Description: Synthetic distress/default indicator, used as the target variable in the PD-style model.  
- Interpretation: `1` means the merchant is treated as having entered a default/distress state in the synthetic scenario; `0` otherwise.  
- Rationale: Represents the outcome used to train the PD model, consistent with PD definitions as the likelihood of a borrower failing to meet obligations within a defined horizon.

[Back to Top](#data-dictionary)

---

## Relationships and Design Notes

- **Expected loss thinking:** While the project does not explicitly define loss given default (LGD) or exposure at default (EAD), the `risk_label` (PD-like dimension) and `net_exposure` are designed to support an expected loss-style view (PD × exposure) in later iterations. 
- **Concentration risk:** The combination of `net_exposure`, `industry_segment`, and `concentration_ratio` is intended to support simple concentration metrics (e.g., top-5 exposure share, exposure share by industry), reflecting standard concentration risk concepts.
- **Merchant risk context:** The chargeback-related variables and reserve coverage are chosen to reflect how payment processors assess merchant risk (e.g., chargeback history, business model, reserve levels), as discussed in merchant risk management resources.

[Back to Top](#data-dictionary)

---

## Usage in the Project

- **01_generate_credit_risk_data.py**  
  Creates this dataset and writes it to `data/raw/credit_risk_synthetic.csv`.

- **02_build_credit_risk_model.py / 01_credit_risk_model.ipynb**  
  Use these fields to build the PD-style model and assign risk tiers.

- **03_credit_risk_reporting.py**  
  Uses `net_exposure`, `predicted_pd`, `risk_tier`, and `industry_segment` to produce concentration tables, charts, and a governance-oriented credit risk report.

As the project evolves (e.g., into liquidity and fraud modules), this dictionary can be extended with additional fields and cross-links (e.g., loss severity, liquidity buffers, or fraud flags).

[Back to Top](#data-dictionary)

---