# Regulatory Alignment

This document explains how the synthetic **PaymentRisk360** framework maps to key Canadian and international regulatory expectations, focusing on:
- OSFI’s Liquidity Adequacy Requirements (LAR) and Basel III credit risk concepts,
- the Bank of Canada’s risk-management standards for prominent payment systems (PPS),
- the Retail Payment Activities Act (RPAA) and its regulations for fraud and operational risk management,
- and the **Three Lines of Defence** model as described in OSFI’s operational risk guidance.

The goal is not to replicate legal or regulatory text, but to show that the project is structured in a way that is conceptually aligned with how Canadian regulators think about credit, liquidity, and operational/fraud risk.

---

## Table of Contents

- [Credit Risk and OFSI/Basel III Concpets](#credit-risk-and-osfi--basel-iii-concepts)
    - [Basel Style Credit Risk Concepts](#basel-style-credit-risk-concepts)
    - [Concentration Risk](#concentration-risk)
    - [OFSI Expectations](#osfi-expectations)
- [Liquidity Risk and OFSI LAR / Bank of Canada PPS Standards](#liquidity-risk-and-osfi-lar--bank-of-canada-pps-standards)
    - [OFSI Liqiodity Adequacy Requirements (LAR)](#osfi-liquidity-adequacy-requirements-lar)
    - [Bank of Canada PPS Risk-Management Standards](#bank-of-canada-pps-risk-management-standards)
    - [Alignment Summary](#alignment-summary)
- [Fraud KRI's and RPAA Expectations](#fraud-kris-and-rpaa-expectations)
    - [RPAA and Retail Payment Risk Management](#rpaa-and-retail-payment-risk-management)
    - [Alignment of Fraud Workstream with RPAA Concepts](#alignment-of-fraud-workstream-with-rpaa-concepts)
- [Three Lines of Defence](#three-lines-of-defence)
    - [Regulatory View](#regulatory-view)
    - [How this project embeds the Three Lines](#how-this-project-embeds-the-three-lines)
- [Summary](#summary)

[Back to Top](#regulatory-alignment)

---

## Credit Risk and OSFI / Basel III Concepts

### Basel-Style Credit Risk Concepts

The credit workstream uses a PD-style model to estimate the likelihood that a merchant or participant falls into a synthetic distress or default state. This mirrors the Basel framework, where **Probability of Default (PD)** is a key component of expected loss and risk-weighted asset calculations. PD represents the likelihood that a borrower fails to meet obligations over a defined time horizon.

In this project:

- Logistic regression is used to estimate a PD-style probability of distress at merchant level.
- Net exposure fields approximate **Exposure at Default (EAD)** in a simplified way.
- Reserve coverage notions loosely echo the idea that loss given default (LGD) can be mitigated by collateral or reserves.

While the project does not explicitly calculate LGD or EAD, the combination of PD-style estimates and net exposure is consistent with the expected loss framing:
  
```math
Expected Loss =  PD * LGD * EAD
```

at a conceptual level.

### Concentration Risk

Basel and various central banks highlight that credit risk at the portfolio level is heavily influenced by **concentration risk**—for example, excessive exposure to a small number of borrowers, sectors, or correlated segments.

The credit module reflects this by:

- Producing **industry-level exposure and PD summaries**,
- Listing top merchants by net exposure and risk score,
- Calculating portfolio exposure shares for major industries and large merchants,
- Highlighting High and Severe risk tiers and their share of total net exposure.

These outputs demonstrate how a second-line function might identify concentration risk and relate it to risk appetite and governance discussions.

### OSFI Expectations

OSFI’s guidance on credit and liquidity risk emphasises that institutions should:

- Understand individual counterparty risk and **portfolio concentration**,
- Consider both quantitative models and **qualitative assessments**,
- Have clear documentation of methodologies, assumptions, and limitations.

This project does not implement a full Internal Ratings-Based (IRB) capital model, but it is structured in a way that:

- Uses PD-style scoring and concentration metrics consistent with OSFI/Basel language,
- Includes documentation (methodology, reports) that a second-line team could use to challenge first-line views,
- Can support risk appetite and concentration limit discussions at an ERM or Product Council level.

[Back to Top](#regulatory-alignment)

---

## Liquidity Risk and OSFI LAR / Bank of Canada PPS Standards

### OSFI Liquidity Adequacy Requirements (LAR)

OSFI’s **Liquidity Adequacy Requirements (LAR) Guideline** sets out expectations for how institutions manage and monitor liquidity risk, including the Liquidity Coverage Ratio (LCR) and related tools. The LAR guideline focuses on the ability of institutions to meet their obligations in cash or high-quality liquid assets under periods of stress.

Key ideas include:

- Holding sufficient unencumbered **High-Quality Liquid Assets (HQLA)**,
- Meeting net cash outflows over a 30‑day stress period (LCR),
- Having robust liquidity risk management processes and metrics.

The intraday liquidity module in this project does not calculate a formal LCR, but it uses similar principles on a **shorter intraday horizon**:

- Identifying a starting **liquidity buffer**,
- Simulating stress scenarios that increase outflows and reduce/delay inflows,
- Measuring how quickly buffers are consumed,
- Tracking breaches of intraday buffer thresholds.

### Bank of Canada PPS Risk-Management Standards

The Bank of Canada’s risk-management standards for prominent payment systems (PPS) require that systems maintain sufficient liquid resources to effect same-day and, where appropriate, **intraday settlement** of obligations. They expect robust tools to measure, monitor, and manage liquidity risk throughout the settlement cycle and to withstand stress scenarios.

The intraday liquidity workstream aligns with these principles by:

- Modelling **intraday payment flows** (inflows and outflows over the business day) across multiple scenarios (base, stress volume, severe stress),
- Tracking **intraday positions** and **buffer availability** at each time step,
- Calculating key intraday KRIs:
  - minimum intraday position,
  - minimum buffer available,
  - number of warning and breach intervals,
  - time-to-first-warning and time-to-first-breach,
- Assigning **Green / Amber / Red** statuses per scenario to support governance and escalation.

This is conceptually consistent with the PPS requirement to ensure that core payment obligations can be met on time (including intraday), and that liquidity risk is understood under both normal operations and stress.

### Alignment Summary

Although simplified and synthetic, the liquidity module:

- Applies **LCR-like thinking** in terms of buffer sufficiency and stress testing, on an intraday time scale,
- Follows PPS-style emphasis on intraday liquidity monitoring and settlement resilience,
- Produces metrics and statuses that a second-line liquidity or ERM team could use to monitor risk appetite and trigger escalation.

[Back to Top](#regulatory-alignment)

---

## Fraud KRIs and RPAA Expectations

### RPAA and Retail Payment Risk Management

The **Retail Payment Activities Act (RPAA)** and its regulations establish a framework for retail payment service providers (PSPs) in Canada. Among other things, PSPs must:

- Develop and maintain a **risk management and incident response framework**,
- Identify and assess risks related to their retail payment activities, including fraud, cybersecurity, and business continuity,
- Implement mitigation measures and controls,
- Monitor the effectiveness of those controls and review the framework at least annually,
- Maintain documentation that describes the framework and its application.

Fraud is explicitly listed as a key risk that must be considered in this framework.

### Alignment of Fraud Workstream with RPAA Concepts

The fraud workstream is structured in a way that mirrors these expectations:

- It identifies **fraud risk** as a key operational risk for a retail debit/card product.
- It implements **rules-based controls** such as:
  - card-level velocity checks (e.g., more than N transactions in a short time window),
  - high-amount filters (transactions above a defined threshold).
- It defines **fraud KRIs** including:
  - overall fraud rate,
  - rule hit rate,
  - fraud capture rate by rules,
  - number of rule hits that are false positives.
- It introduces an **AI-driven logistic regression model** that:
  - assigns a fraud risk score to each transaction based on transaction features and rule flags,
  - is evaluated with ROC-AUC, precision/recall, and average precision metrics,
  - remains explainable via feature importance, in line with expectations around model transparency.
- It integrates model scores into the fraud KRI layer (e.g., maximum score per card, combined statuses), providing a clear view of which cards and transactions are highest risk.

These elements together illustrate how a PSP could document its fraud monitoring approach and use KRIs to evidence that fraud risk is being identified, monitored, and escalated in line with RPAA expectations.

[Back to Top](#regulatory-alignment)

---

## Three Lines of Defence

### Regulatory View

OSFI’s guidance on operational risk and related governance explicitly references the **Three Lines of Defence** model (or an appropriately robust structure) to organise risk management activities:

- **First line:** business units that own and manage risk (e.g., product, operations).
- **Second line:** independent risk management and compliance functions.
- **Third line:** internal audit providing independent assurance.

### How This Project Embeds the Three Lines

This project is intentionally written from a **second-line** perspective, but the artifacts are designed to sit across all three lines:

**First Line (simulated):**

- Owns the debit payment product, merchant relationships, and day-to-day operations.
- Would be accountable for:
  - implementing credit and counterparty limits in production systems,
  - managing intraday liquidity buffers and payment queues,
  - running real-time fraud rules and responding to alerts.

**Second Line (project lens):**

- Designs and maintains the **risk analytics modules**:
  - credit risk PD model and concentration analysis,
  - intraday liquidity scenarios and KRIs,
  - fraud rules and AI-driven fraud scoring.
- Defines **KRIs**, thresholds, and statuses (Green/Amber/Red).
- Produces governance-oriented documentation:
  - methodology notes,
  - risk reports,
  - regulatory alignment and RCSA templates.
- Uses the integrated ERM dashboard to:
  - monitor cross-risk positions,
  - challenge first-line assumptions,
  - assess alignment with risk appetite and regulatory expectations.

**Third Line (conceptual):**

- Would review whether:
  - the analytics and KRIs are appropriate and aligned with the institution’s risk framework,
  - the documentation (e.g., regulatory-alignment.md, RCSA) is complete and accurate,
  - first and second line are executing their roles effectively.

This structure shows that the analytics are not “standalone models” but are embedded in a **governance mindset** that reflects OSFI and Bank of Canada expectations about risk management frameworks and organisational roles.

[Back to Top](#regulatory-alignment)

---

## Summary

While all underlying data and scenarios in this project are synthetic, the design choices are intentional:

- The **credit** module uses PD-style scoring and concentration analysis aligned with Basel and OSFI credit risk concepts.
- The **liquidity** module focuses on intraday settlement flows and buffer sufficiency in a way that resonates with LAR principles and PPS liquidity standards.
- The **fraud** and **AI-driven fraud** modules implement rules, KRIs, and an explainable model consistent with RPAA expectations and best practices for fraud risk management and AI explainability.
- The project explicitly frames its outputs through the **Three Lines of Defence**, reinforcing its relevance to a second-line ERM or payments risk leadership role.

These alignments are intended to demonstrate not only technical skills but also regulatory awareness and governance thinking.

[Back to Top](#regulatory-alignment)

---