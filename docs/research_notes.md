# PaymentRisk360: Research Notes

A portfolio project designed to demonstrate **second-line enterprise risk oversight capability** across **credit risk, liquidity risk, and fraud analytics** in a Canadian payments context.

---

## Table of Contents

- [Project Objective](#project-objective)
- [Why this Project Exists](#why-this-project-exists)
- [Project Scope](#project-scope)
- [Regulatory Context](#regulatory-context)
- [Liquidity Risk Basics](#liquidity-risk-basics)
- [Project Positioning Notes](#project-positioning-notes)
- [Top Concepts to Remember](#top-concepts-to-remember)

[Back to Top](#paymentrisk360-research-notes)

---

## Project Objective

This project simulates the type of analytical and governance work an Enterprise Risk Management (ERM) second-line function would perform for a payments network. It is being built to demonstrate practical understanding of:

- Credit risk assessment for payment participants and merchants
- Liquidity risk monitoring for payment settlement activity
- Fraud risk analytics, KRI monitoring, and model oversight
- Executive and board-level risk reporting
- Second-line challenge aligned to Canadian payments oversight expectations

[Back to Top](#paymentrisk360-research-notes)

---

## Why This Project Exists

My background is strongest in IT risk, GRC, product/vendor risk, and analytics. This project is intended to close the most relevant gap for payments-focused ERM roles: **financial risk and fraud analytics in a payments environment**.

Rather than treating this as an academic exercise, the project is structured as a **second-line oversight portfolio**:

- Build risk models and KRI dashboards
- Document assumptions and limitations
- Apply challenge and oversight language throughout
- Tie outputs to regulatory expectations relevant to Canadian payments

[Back to Top](#paymentrisk360-research-notes)

---

## Project Scope

The project contains three integrated workstreams:

### 1. Credit Risk
A synthetic merchant/counterparty risk model that estimates payment participant risk using exposure, transaction behavior, concentration, and adverse performance indicators.

### 2. Liquidity Risk
A synthetic intraday settlement simulation that tests liquidity sufficiency under baseline and stressed conditions, using LCR-inspired logic and escalation thresholds.

### 3. Fraud Risk
A synthetic transaction monitoring framework combining rule-based fraud flags, KRI reporting, and later-stage ML-based anomaly detection with second-line model challenge.

[Back to Top](#paymentrisk360-research-notes)

---

## Regulatory Context

The Bank of Canada oversees designated clearing and settlement systems under the *Payment Clearing and Settlement Act* (PCSA) and oversees systems that may pose systemic or payments system risk.[1](https://www.bankofcanada.ca/regulatory-oversight/financial-market-infrastructures/oversight-designated-clearing-settlement-systems/)

The Bank has also expanded oversight responsibilities to include **prominent payment systems**, where disruption could materially affect economic activity or public confidence in payments.[2](https://www.bankofcanada.ca/2023/10/bank-canada-designates-additional-prominent-payment-systems/) [3](https://www.bankofcanada.ca/regulatory-oversight/financial-market-infrastructures/oversight-designated-clearing-settlement-systems/)

Under the *Retail Payment Activities Act* (RPAA), payment service providers must register with the Bank of Canada and must manage operational risks, respond to incidents, and protect end-user funds. As of September 8, 2025, they must also maintain risk management and funds safeguarding frameworks and submit annual reports.[4](https://www.bankofcanada.ca/regulatory-oversight/retail-payments/)

Liquidity supervision in Canada also relies on concepts embedded in OSFI's *Liquidity Adequacy Requirements* guideline, including the Liquidity Coverage Ratio (LCR), where high-quality liquid assets should at least equal total net cash outflows over a 30-day stress period. [5](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf) 

Interac team's focus is credit risk and liquidity risk, the broader payments risk environment still emphasizes:

- Control maturity
- Incident readiness
- Operational resilience
- Governance discipline
- Clear reporting and escalation

This aligns strongly with second-line oversight responsibilities.

### Things to remember

- "Under the RPAA framework, operational risk management and incident response are supervisory expectations, not optional good practice." [6](https://www.bankofcanada.ca/regulatory-oversight/retail-payments/)
- "The payments environment in Canada is becoming more structured and supervision-driven, particularly around operational risk, safeguarding, and reporting discipline." [7](https://www.bankofcanada.ca/publications/annual-reports-quarterly-financial-reports/annual-report-2024/retail-payments-supervision/) [8](https://www.bankofcanada.ca/regulatory-oversight/retail-payments/)
- "A second-line function in payments should help ensure first-line activity remains within risk appetite while also meeting supervisory expectations." [9](https://www.bankofcanada.ca/regulatory-oversight/retail-payments/)

[Back to Top](#paymentrisk360-research-notes)

---

## Liquidity Risk Basics

### What matters

OSFI's *Liquidity Adequacy Requirements* (LAR) guideline helps assess whether institutions can meet obligations in cash or in assets that can quickly be converted into cash. [10](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/liquidity-coverage-ratio-lcr-reporting) [11](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)

One of the core measures is the **Liquidity Coverage Ratio (LCR)**. In the 30-day stress scenario used in the standard, the value of the ratio should be no lower than 100 percent on an ongoing basis, meaning the stock of unencumbered high-quality liquid assets should at least equal total net cash outflows. [12](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)

The guideline also caps inflows that can offset outflows, to avoid over-reliance on anticipated incoming cash. [13](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)

### What this means for this project

This project is not trying to replicate a full bank treasury function. Instead, it will adapt the logic conceptually to a payments setting by asking:

- Are settlement obligations likely to be met under stress?
- Is there enough liquidity buffer for intraday or short-horizon payment pressure?
- At what point would pre-defined thresholds be breached?

### Things to remember

- "I am using LCR-style thinking as a way to structure liquidity sufficiency under stress, not to claim a full prudential treasury model." [14](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)
- "In a payments context, liquidity risk can be framed operationally as the ability to continue meeting obligations under stressed transaction and settlement conditions." [15](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/liquidity-coverage-ratio-lcr-reporting)[16](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)
- "The key practical question is whether a disruption in flows, a volume spike, or a counterparty problem creates a breach of liquidity tolerance." [17](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)

[Back to Top](#paymentrisk360-research-notes)

---

## Project Positioning Notes

### How to frame the entire project

This project should be described as:

- A **synthetic, interview-ready second-line risk portfolio**
- Built to demonstrate practical understanding of **credit risk, liquidity risk, and fraud analytics**
- Written using **oversight, challenge, KRI, and risk appetite language**
- Anchored in Canadian payments oversight context rather than generic analytics

### Note

- This project intentionally used synthetic data so that it could demonstrate the risk methodology, second-line challenge, and governance framing without relying on proprietary financial data. The purpose of the project is not to recreate a live payment system, but to show how one would structure independent risk oversight in one.

[Back to Top](#paymentrisk360-research-notes)

---

## Top Concepts to Remember

### Must-know terms

- Payment Clearing and Settlement Act (PCSA)
- Prominent payment system
- Systemic risk vs. payments system risk
- Retail Payment Activities Act (RPAA)
- Operational risk management
- Incident response
- End-user funds safeguarding
- Liquidity Coverage Ratio (LCR)
- High-quality liquid assets (HQLA)
- Risk appetite
- Key risk indicators (KRIs)
- Second-line challenge
- Three Lines of Defense

### Short talking points

- "The Bank of Canada designates and oversees payment systems that may pose systemic or payments system risk." [18](https://www.bankofcanada.ca/regulatory-oversight/financial-market-infrastructures/oversight-designated-clearing-settlement-systems/)
- "Prominent payment systems are important because disruption can affect confidence in payments and economic activity even if they are not systemically important in the narrowest sense." [19](https://www.bankofcanada.ca/regulatory-oversight/financial-market-infrastructures/oversight-designated-clearing-settlement-systems/guideline-related-oversight-activities/) [20](https://www.bankofcanada.ca/2023/10/bank-canada-designates-additional-prominent-payment-systems/)
- "Under the RPAA, PSPs are expected to manage operational risks, respond to incidents, and protect end-user funds." [21](https://www.bankofcanada.ca/regulatory-oversight/retail-payments/)
- "Liquidity sufficiency under stress is a useful way to frame payment-system liquidity monitoring." [22](https://www.osfi-bsif.gc.ca/sites/default/files/documents/2026-lar-nl-chpt-2-en.pdf)
- "The second-line role is to provide independent challenge, risk appetite alignment, and governance-quality reporting." [23](https://www.bankofcanada.ca/regulatory-oversight/financial-market-infrastructures/oversight-designated-clearing-settlement-systems/) [24](https://www.bankofcanada.ca/regulatory-oversight/retail-payments/)

[Back to Top](#paymentrisk360-research-notes)

---