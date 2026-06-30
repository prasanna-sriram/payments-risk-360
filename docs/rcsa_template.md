# RCSA Template – Debit Payment Product (Simulated)

This document is a **Risk and Control Self-Assessment (RCSA) template** for a hypothetical **retail debit payment product**. It is designed to illustrate how the analytics in the PaymentRisk360 project could be connected to risks, controls, KRIs, and second-line challenge in a way that aligns with Canadian regulatory expectations and the Three Lines of Defence model.

---

## Table of Contents

- [Scope and Product Overview](#scope-and-product-overview)
- [Risk, Control and KRI Summary Table](#risk-control-and-kri-summary-table)
- [Detailed RCSA Entries](#detailed-rcsa-entries)
    - [Credit Risk / Merchant Participant Risk](#credit-risk--merchant--participant-risk)
    - [Liqiudity Risk - Intraday Settlement and Funding](#liquidity-risk--intraday-settlement-and-funding)
    - [Fraud Risk - Transaction Level Fraud](#fraud-risk--transaction-level-fraud)
    - [Operational Risk - Systems Processes and Models](#operational-risk--systems-processes-and-models)
- [Overall Residual Risk and Action Plan](#overall-residual-risk-and-action-plan)
- [Template Notes](#template-notes)


[Back to Top](#rcsa-template--debit-payment-product-simulated)

---

## Scope and Product Overview

**Product:** Retail debit payment product (card and account-based payments)  
**Scope:** End-to-end processing of debit transactions, including authorisation, clearing, settlement, fraud monitoring, and chargeback handling.  
**Primary Risk Types Covered:** Credit risk, liquidity risk, fraud risk, operational risk.

**In-Scope Processes (Illustrative):**

- Customer and merchant onboarding
- Transaction initiation and authorisation
- Payment routing, clearing, and settlement
- Intraday funding and liquidity management
- Fraud detection and case management
- Chargeback and dispute handling
- Risk reporting and KRI monitoring

[Back to Top](#rcsa-template--debit-payment-product-simulated)

---

## Risk, Control, and KRI Summary Table

The table below provides a compact, cross-risk view. Detailed descriptions follow in later sections.

| Risk Category   | Risk Description                                   | Inherent Risk | Key Controls (High-Level)                                     | Control Effectiveness | Key KRIs (from Project)                                  |
|-----------------|----------------------------------------------------|---------------|----------------------------------------------------------------|-----------------------|----------------------------------------------------------|
| Credit Risk     | Merchant / participant default and settlement loss | High          | Underwriting, merchant reviews, reserves / limits              | Medium                | PD-style tiers, top exposures, industry concentration    |
| Liquidity Risk  | Intraday funding shortfall and settlement delays   | High          | Intraday buffers, limits, scenario monitoring                  | Medium                | Scenario statuses, min buffer, time-to-breach            |
| Fraud Risk      | Unauthorised / fraudulent debit transactions       | High          | Rules, AI fraud model, case management                         | Medium                | Fraud rate, rule hit rate, fraud capture, high-risk cards|
| Operational Risk| Process, system, or model failures                 | Medium–High   | Change management, validations, access/logging                 | Medium                | Incidents, unapproved changes, validation findings       |

[Back to Top](#rcsa-template--debit-payment-product-simulated)

---

## Detailed RCSA Entries

### Credit Risk – Merchant / Participant Risk

**Risk Description**  
Merchant or participant default leading to **settlement loss**, unrecovered chargebacks, or operational disruption (e.g., a large merchant suddenly failing while holding significant unsettled balances).

**Inherent Risk Rating:** High  
**Risk Drivers (Illustrative):**

- High transaction volumes and large ticket sizes,
- Elevated chargeback rates and recent adverse performance,
- Concentration to a small number of high-risk industries.

**Key Controls:**

- **Merchant onboarding and underwriting:** Industry risk assessment, basic financial review, and risk-based pricing / reserve policies.
- **Ongoing exposure monitoring:** Periodic review of merchant performance (chargebacks, fraud, volume trends).
- **Reserves and limits:** Use of rolling reserves or collateral and transaction / settlement limits for higher-risk merchants.

**Control Design Rating:** Medium  
**Control Effectiveness Rating:** Medium (assumes framework exists but can be strengthened)

**Associated KRIs from PaymentRisk360:**

- Proportion of portfolio net exposure in **High and Severe** PD-style risk tiers.
- Top-N merchants by net exposure and predicted PD.
- Industry-level exposure shares and concentration measures.

**Second-Line Challenge Notes:**

- Second line can use PD-style scores and concentration metrics to **challenge whether reserve levels and limits** for high-risk industries (e.g., travel, gaming, digital content) are consistent with risk appetite.
- KRI thresholds (e.g., maximum industry exposure share; acceptable share of exposure in High/Severe tiers) should be defined and documented.
- Methodology and limitations should be periodically reviewed and discussed with first line.

---

### Liquidity Risk – Intraday Settlement and Funding

**Risk Description**  
Insufficient intraday liquidity to meet **payment and settlement obligations** on time, leading to queues, payment delays, or settlement failures in a prominent or systemically important payment system.

**Inherent Risk Rating:** High  
**Risk Drivers (Illustrative):**

- Large outgoing payment batches early in the day,
- Delayed inflows from counterparties,
- Stress scenarios (volume spikes, counterparty failure, operational incidents).

**Key Controls:**

- **Intraday liquidity buffers:** Pre-defined buffers or limits for payment activities and net debit positions.
- **Monitoring tools:** Intraday dashboards that track positions, buffer usage, and time-to-breach.
- **Contingency funding:** Access to intraday credit lines or central bank facilities where applicable.

**Control Design Rating:** Medium  
**Control Effectiveness Rating:** Medium (depends on calibration and actual tools)

**Associated KRIs from PaymentRisk360:**

- Scenario-level statuses (Green / Amber / Red) for base, stress volume, and severe stress intraday scenarios.
- Minimum intraday position and **minimum buffer available** per scenario.
- **Time-to-first-warning** and **time-to-first-breach** in minutes, plus counts of breach intervals.

**Second-Line Challenge Notes:**

- Second line should challenge whether **buffer levels and limits** are calibrated using realistic stress scenarios, including intraday considerations consistent with PPS standards.
- KRIs should be linked to clear **escalation thresholds** (e.g., when intraday breaches or early warning signals trigger engagement of treasury or senior management).
- Documentation should describe key assumptions (e.g., inflow/outflow patterns, stress multipliers) and be reviewed regularly.

---

### Fraud Risk – Transaction-Level Fraud

**Risk Description**  
Unauthorised or fraudulent debit transactions resulting in financial loss, chargebacks, customer harm, and reputational damage.

**Inherent Risk Rating:** High  
**Risk Drivers (Illustrative):**

- Card-not-present transactions and cross-border activity,
- Compromised credentials, bots, and automated attacks,
- Weak or outdated rules/controls and delayed detection.

**Key Controls:**

- **Rules-based filters:** Velocity checks (transactions per card over short intervals) and high-amount filters tied to portfolio norms.
- **AI-driven fraud model:** Logistic regression model producing a fraud risk score per transaction, trained on transaction attributes and rule flags.
- **Case management:** Manual review queues and workflow for high-risk cards and transactions.

**Control Design Rating:** Medium–High  
**Control Effectiveness Rating:** Medium (recognises both strength and residual risk)

**Associated KRIs from PaymentRisk360:**

- Overall **fraud rate** (synthetic) and **rule hit rate**.
- **Fraud capture rate** by rules and by the AI model.
- Number of **High Risk** cards (based on rules and model scores).
- Fraud rate by **fraud risk score bucket** (top deciles).

**Second-Line Challenge Notes:**

- Second line should review and challenge:
  - rules and thresholds (velocity and amount),
  - model performance metrics (ROC-AUC, precision/recall, average precision),
  - false positive levels and operational capacity,
  - alignment with RPAA expectations for risk management and incident response.
- Documentation of rule logic, model design, feature importance, and limitations should be owned by first line but **independently reviewed** by second line and periodically audited by third line.

---

### Operational Risk – Systems, Processes, and Models

**Risk Description**  
Failures in processes, systems, models, or data that cause incorrect risk assessments, missed alerts, unauthorised changes, or processing errors.

**Inherent Risk Rating:** Medium–High  
**Risk Drivers (Illustrative):**

- Changes to rules or models without proper testing or approval,
- Data quality issues (e.g., missing fields, incorrect mappings),
- System outages affecting authorisation, settlement, or monitoring.

**Key Controls:**

- **Change management:** Formal processes for changing rules, thresholds, and model code, including approval and testing.
- **Model governance:** Periodic validation, monitoring, and review of fraud and credit models.
- **Access and logging:** Role-based access to risk systems and logging of changes and overrides.

**Control Design Rating:** Medium  
**Control Effectiveness Rating:** Medium (depends on implementation and oversight)

**Associated KRIs (Illustrative):**

- Number of **unplanned outages** affecting fraud and risk monitoring.
- Number of changes to rules/models executed **outside the change process**.
- Number and severity of issues identified in independent model validation or internal audit.

**Second-Line Challenge Notes:**

- Second line should ensure that analytical outputs from this project (models, KRIs, dashboards) are themselves **subject to appropriate governance**:
  - documented assumptions,
  - validation and periodic review,
  - clear ownership and escalation.
- This aligns with OSFI’s expectations around operational risk and the **three lines of defence**.

[Back to Top](#rcsa-template--debit-payment-product-simulated)

---

## Overall Residual Risk and Action Plan

**Overall Residual Risk (Illustrative Assessment):**

- **Credit Risk:** Residual risk remains **Medium–High** due to concentration in certain industries and reliance on simplified reserve logic.
- **Liquidity Risk:** Residual risk remains **Medium**, recognising sensitivity to stress scenarios and the importance of real-world calibration.
- **Fraud Risk:** Residual risk remains **Medium–High**, reflecting the evolving nature of fraud and synthetic calibration.
- **Operational Risk:** Residual risk is **Medium**, contingent on effective change management, validation, and audit.

**Illustrative Action Plan:**

- Enhance calibration of credit and fraud models and thresholds using real data, once available.
- Formalise intraday liquidity stress scenarios and link intraday KRIs to risk appetite and governance thresholds.
- Implement model risk management activities:
  - independent validation,
  - performance monitoring,
  - periodic review and documentation.
- Extend RCSA coverage to other products and services and link RCSA outputs to issue management and remediation tracking.

[Back to Top](#rcsa-template--debit-payment-product-simulated)

---

## Template Notes

This RCSA is **simulated** and uses synthetic data, illustrative ratings, and hypothetical controls. In a live environment:

- Ratings, KRIs, and control descriptions would be informed by actual incidents, loss data, and internal standards.
- First line, second line, and third line would each have defined responsibilities consistent with OSFI’s **Three Lines of Defence** expectations.
- The RCSA would be formally approved, tracked, and updated as part of the institution’s overall risk management and governance process.

The purpose of this template is to show how the analytical workstreams in PaymentRisk360 can be embedded within a broader risk and control framework, rather than existing only as stand-alone models or dashboards.

[Back to Top](#rcsa-template--debit-payment-product-simulated)

---