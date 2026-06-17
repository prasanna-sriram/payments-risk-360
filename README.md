# Enterprise Risk, Fraud Analytics, Credit Risk, and Liquidity Risk Framework for Canadian Payments

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Business Problem](#business-problem)
- [Project Workstreams](#project-workstreams)
- [Methodology](#methodology)
- [Skills](#skills)
- [Repository Structure](#repository-structure)
- [Results and Business Recommendations](#results-and-business-recommendations)
- [Next Steps](#next-steps)
- [License](#license)
- [Author Info](#author-info)

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Executive Summary

This project simulates a second-line Enterprise Risk Management (ERM) framework for a Canadian payments network operating in a highly regulated environment. The business problem is that payment systems must remain resilient under fraud events, participant stress, and liquidity disruption, while also staying within risk appetite and meeting oversight expectations tied to prominent payment systems and retail payments supervision.

To address this, I built a synthetic end-to-end risk analytics portfolio covering **credit risk**, **liquidity risk**, and **fraud monitoring**, supported by executive-style reporting, KRI logic, and second-line challenge documentation. The fraud module is extended with an **AI-driven logistic regression model** that assigns a transaction-level fraud risk score on top of rules-based monitoring.

The solution combines Python-based risk modelling, scenario analysis, threshold monitoring, and governance-oriented reporting to show how a second-line risk function can convert complex operational and financial signals into actionable oversight.

At a high level, the project is designed to:
- Assess participant / merchant risk using PD-style credit risk logic
- Simulate liquidity sufficiency under stressed payment settlement conditions
- Detect transaction anomalies using fraud rules and an AI-driven risk score
- Support second-line oversight through KRIs, escalation triggers, and challenge memos

With more time, this framework could be expanded into participant-level stress testing, model validation workflows, and more formal board reporting packs. Although the data is fully synthetic, the project is structured to show realistic risk thinking, strong governance framing, and practical decision support for payments stakeholders.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Business Problem

Payments organizations operate in an environment where trust, continuity, and resilience are core to the business model. A disruption in payment flows, a fraud spike, a participant failure, or a liquidity shortfall can create direct customer impact and broader confidence concerns across the network.

This creates a business need for more than just dashboards or point-in-time controls. Stakeholders need a risk framework that helps answer questions such as:

- Which participants or merchants show early signs of elevated credit or exposure risk?
- Would the network remain within liquidity tolerance if payment activity spikes or a counterparty fails?
- Are fraud indicators emerging early enough to support timely escalation and mitigation?
- How can second-line risk provide independent challenge instead of only reporting what first-line teams already know?

This project is intended to solve that problem by building a synthetic but realistic framework that shows how second-line risk can monitor financial and fraud risks, align them to risk appetite, and present them in a way that supports product, risk, and executive decision-making.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Project Workstreams

This portfolio is organized into four concrete workstreams that mirror how a second-line risk function might monitor a Canadian payments environment:

### 1. Credit Risk – Participant / Merchant PD and Concentration

- Synthetic merchant-level dataset with transaction behaviour, chargebacks, reserve coverage, and exposure.
- Logistic regression **PD-style model** that estimates probability of distress and assigns Low / Medium / High / Severe risk tiers.
- Concentration analysis by merchant and industry, including top-exposure lists and portfolio-level KRIs.
- Governance-oriented outputs: credit risk report and methodology note describing assumptions, limitations, and second-line interpretation. 

### 2. Liquidity Risk – Intraday Payment Flows and Buffers

- Intraday simulation of payment inflows and outflows for multiple scenarios (base, stress volume, severe stress).
- Monitoring of intraday liquidity positions, buffer usage, and **time-to-first-breach** against warning and breach thresholds.
- Scenario-level KRIs (min position, warning/breach intervals, status Green/Amber/Red) and an intraday liquidity report.
- Framing aligned to operational / intraday liquidity practices: ability to meet payment and settlement obligations on time under normal and stressed conditions.

### 3. Fraud Risk – Rules and KRIs

- Synthetic card transaction dataset with an injected fraud label and realistic behaviour patterns.
- **Rules-based monitoring** using card-level velocity checks and high-amount filters, consistent with common payment fraud controls.
- Transaction- and card-level fraud KRIs (rule hit rates, fraud capture, false positives; high-risk cards by rule hits).
- Fraud risk report describing rule design, trade-offs between detection and false positives, and second-line escalation logic.

### 4. AI-Driven Fraud Detection – Logistic Regression Risk Scoring

- **Logistic regression model** trained on transaction features and rules-based flags to produce a **fraud risk score** for every transaction.
- Model performance metrics (ROC-AUC, average precision, precision/recall) and feature importance for explainability and challenge.
- Score bucket view showing how fraud concentrates in high-score buckets, consistent with risk scoring practices.
- Integration of model scores into the fraud KRI layer (e.g., max fraud score per card, combined rules + model statuses), illustrating how rules and AI can be combined in a governance-friendly framework.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Methodology

This project uses a synthetic data strategy to simulate a Canadian payments environment without relying on proprietary transaction or participant data. The work is organized into four connected risk modules:

- **Credit Risk Analysis:** build participant / merchant-level risk scoring using exposure, concentration, transaction behaviour, and adverse performance indicators
- **Liquidity Risk Monitoring:** simulate intraday settlement flows and test liquidity sufficiency under baseline and stressed conditions using buffer thresholds and time-to-breach logic.
- **Fraud Risk Analytics:** build fraud KRIs, rule-based anomaly detection, using card-level velocity and amount rules.
- **AI-Driven Fraud Detection:** train an explainable logistic regression model on transaction and rule features to generate a fraud risk score and integrate it into the fraud KRI framework.

The project also includes governance-oriented deliverables such as executive summaries, risk threshold logic, regulatory alignment notes, and second-line challenge memos. I chose this structure because the target role is not purely analytical; it requires the ability to combine analytics, oversight, risk appetite thinking, and executive communication.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Skills

### Python
- pandas for data transformation and feature engineering
- numpy for simulation logic and scenario generation
- scikit-learn for classification and model evaluation
- matplotlib / seaborn / plotly for KRI and scenario visualizations
- feature-importance based explainability for model interpretation and second-line challenge

### Risk Analytics
- Credit risk scoring and participant risk segmentation
- Liquidity stress testing and buffer threshold analysis
- Fraud KRI design and anomaly detection logic
- Scenario analysis and sensitivity testing

### Enterprise Risk Management
- Risk appetite alignment
- Key Risk Indicator (KRI) design
- Second-line challenge and oversight framing
- RCSA / control-thinking mindset
- Escalation and governance reporting logic

### Business and Communication
- Executive summary writing
- Business problem framing
- Risk translation for non-technical stakeholders
- Recommendation writing tied to operational and strategic decisions

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Repository Structure

```text
payment-risk-360/
├── data/
│   ├── raw/
│   ├── processed/
│   └── data_dictionary.md
├── scripts/
├── notebooks/
├── outputs/
├── dashboard/
├── docs/
└── README.md
```

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Results and Business Recommendations

This project is designed to demonstrate how second-line risk can move from reactive reporting to proactive oversight in a payments environment. Even with synthetic data, the framework helps show how credit, liquidity, and fraud indicators can be brought into a common decision model with clear thresholds, escalation triggers, and management actions.

The expected business value of this approach includes:
- Earlier identification of elevated participant or merchant risk
- Better visibility into liquidity pressure under stressed settlement scenarios
- Faster escalation of potential fraud patterns through ules, KRIs, and AI-driven fraud risk scoring
- More structured and credible second-line challenge for product and risk stakeholders

Based on this framework, the key business recommendations are:

- Build a common KRI layer across fraud, liquidity, and participant risk rather than managing each domain in isolation
- Use scenario testing regularly to assess resilience under volume spikes, counterparty stress, and adverse fraud conditions
- Strengthen second-line challenge by requiring documented assumptions, thresholds, and model limitations for each monitoring process
- Translate technical risk outputs into governance-ready reporting that supports Product Council, ERM committee, and executive review

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Next Steps

If this project were extended further, the next logical steps would be:

- Add participant-level stress scenarios tied to specific merchant or network concentration profiles
- Introduce additional challenger models for fraud detection and compare trade-offs between false positives and fraud loss reduction
- Build a formal board / committee reporting pack with trend commentary and issue escalation summaries
- Expand the liquidity model to include more detailed inflow / outflow assumptions, participant-level views, and time-to-breach analysis
- Add a model risk management layer covering validation, monitoring drift, and periodic review expectations
- Benchmark the synthetic framework against selected public fraud or payments datasets for external comparison
- Extend the RCSA and governance layer so that analytics outputs map directly to control owners, issue management, and remediation tracking

### Limitations

- The project uses fully synthetic data, so outputs are designed to demonstrate methodology and risk thinking rather than replicate a live production environment
- Liquidity analysis uses LCR-inspired concepts for practical simulation, not a full prudential treasury implementation
- Fraud and credit thresholds are illustrative and would need calibration using real operating data, historical losses, and approved risk appetite statements

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## License

MIT License

Copyright (c) [2026] [Prasanna Sriram]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back to the Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)

---

## Author Info

- Github - [Github Profile](https://github.com/prasanna-sriram)
- LinkedIn - [Prasanna Sriram](https://www.linkedin.com/in/prasanna-sriram/)
- Tableau - [Tableau Public Profile](https://public.tableau.com/app/profile/prasanna.sriram.ps)

[Back to the Top](#enterprise-risk-fraud-analytics-credit-risk-and-liquidity-risk-framework-for-canadian-payments)