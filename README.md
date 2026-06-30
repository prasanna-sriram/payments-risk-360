# Enterprise Risk, Fraud Analytics, Credit Risk, Liquidity Risk, and AI-Driven Fraud Detection Framework for Canadian Payments

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Business Problem](#business-problem)
- [Project Workstreams](#project-workstreams)
- [Methodology](#methodology)
- [Integrated Dashboard](#integrated-dashboard)
- [Skills](#skills)
- [Regulatory Alignment](#regulatory-alignment)
- [Repository Structure](#repository-structure)
- [Results and Business Recommendations](#results-and-business-recommendations)
- [Project Artifacts](#project-artifacts)
- [Next Steps](#next-steps)
- [License](#license)
- [Author Info](#author-info)

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Executive Summary

This project simulates a second-line **Enterprise Risk Management (ERM)** framework for a Canadian payments environment operating in a highly regulated context. The core problem is that payment systems must remain resilient under fraud events, participant stress, and liquidity disruption while staying within risk appetite and aligning with regulatory and oversight expectations for payments risk management.

To address this, I built a synthetic end-to-end risk analytics portfolio covering **credit risk**, **intraday liquidity risk**, **fraud risk**, and **AI-driven fraud detection**, supported by governance-oriented reporting, KRI logic, and second-line style challenge documentation. The project combines Python-based analytics with an integrated **Power BI dashboard** built from Python-generated outputs to demonstrate how a second-line risk function can turn operational and financial signals into executive-ready oversight.

At a high level, the project is designed to:

- Assess participant / merchant risk using PD-style credit risk logic and concentration analysis.
- Simulate intraday liquidity sufficiency under baseline and stressed settlement scenarios.
- Detect transaction anomalies using fraud rules and an AI-driven fraud risk score.
- Support second-line oversight through KRIs, escalation triggers, RCSA-style documentation, and regulatory alignment notes.

Although the data is fully synthetic, the project is structured to demonstrate realistic risk thinking, governance framing, and practical decision support for payments stakeholders. With real data and more time, the framework could be extended into richer stress testing, model validation, and production-grade executive reporting.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Business Problem

Payments organizations operate in an environment where trust, continuity, and resilience are core to the business model. A disruption in payment flows, a fraud spike, a participant failure, or a liquidity shortfall can create direct customer impact and broader confidence concerns across the network.

This creates a business need for more than just dashboards or point-in-time controls. Stakeholders need a risk framework that helps answer questions such as:

- Which participants or merchants show early signs of elevated credit or exposure risk?
- Would the network remain within liquidity tolerance if payment activity spikes or a counterparty fails?
- Are fraud indicators emerging early enough to support timely escalation and mitigation?
- How can second-line risk provide independent challenge instead of only reporting what first-line teams already know?

This project is intended to solve that problem by building a synthetic but realistic framework that shows how second-line risk can monitor financial and fraud risks, align them to risk appetite, and present them in a way that supports product, risk, and executive decision-making.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

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

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Methodology

This project uses a synthetic data strategy to simulate a Canadian payments environment without relying on proprietary transaction or participant data. The work is organized into four connected risk modules:

- **Credit Risk Analysis:** build participant / merchant-level risk scoring using exposure, concentration, transaction behaviour, and adverse performance indicators
- **Liquidity Risk Monitoring:** simulate intraday settlement flows and test liquidity sufficiency under baseline and stressed conditions using buffer thresholds and time-to-breach logic.
- **Fraud Risk Analytics:** build fraud KRIs, rule-based anomaly detection, using card-level velocity and amount rules.
- **AI-Driven Fraud Detection:** train an explainable logistic regression model on transaction and rule features to generate a fraud risk score and integrate it into the fraud KRI framework.

The project also includes governance-oriented deliverables such as executive summaries, risk threshold logic, regulatory alignment notes, and second-line challenge memos. I chose this structure because the target role is not purely analytical; it requires the ability to combine analytics, oversight, risk appetite thinking, and executive communication.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Integrated Dashboard

To tie the workstreams together, I built an integrated **ERM dashboard in Power BI** using the CSV outputs from the Python workstreams.

The dashboard is organized into module-level and executive-level views:

- **Executive Overview:** Cross-risk snapshot of credit, liquidity, fraud, and AI fraud posture.
- **Credit Risk Page:** PD-style risk tiers, industry concentration, and top merchant exposures.
- **Liquidity Risk Page:** Intraday liquidity position, buffer availability, and scenario-level KRIs.
- **Fraud Risk Page:** Rules-based fraud monitoring, rule hit rates, and top high-risk cards.
- **AI Fraud Detection Page:** Model performance, score buckets, feature importance, and top-risk transactions.

This approach reflects how second-line risk teams often combine analytical outputs with executive-ready visuals to support governance forums, Product Councils, and management decision-making.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Skills

### Python
- pandas for data transformation and feature engineering
- numpy for simulation logic and scenario generation
- scikit-learn for classification and model evaluation
- matplotlib / seaborn / plotly for KRI and scenario visualizations
- feature-importance based explainability for model interpretation and second-line challenge

### Risk Analytics
- PD-style credit risk scoring and participant / merchant segmentation
- Concentration analysis and portfolio exposure monitoring
- Intraday liquidity stress testing and buffer threshold analysis
- Fraud KRI design, rule-based anomaly detection, and AI-driven fraud scoring
- Scenario analysis and sensitivity testing

### Enterprise Risk Management
- Risk appetite alignment
- Key Risk Indicator (KRI) design
- Second-line challenge and oversight framing
- RCSA-style documentation and control thinking (Refer to RCSA Template documented in [`docs/rcsa_template,md`](docs/rcsa_template.md))
- Escalation and governance reporting logic
- Three Lines of Defence mapping

### Dashboarding and Reporting
- Power BI executive dashboard design and build
- Cross-risk portfolio reporting
- Business translation of technical outputs
- Executive summary and governance memo writing

### Business and Communication
- Business problem framing
- Stakeholder communication across technical and non-technical audiences
- Recommendation writing tied to operational and strategic decisions
- Governance-ready presentation of risk insights

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Regulatory Alignment

This project is intentionally framed in language that maps to key Canadian and international risk concepts:

- **OSFI LAR / Basel III concepts:** buffer sufficiency, stress testing, PD-style thinking, and concentration awareness.
- **Bank of Canada PPS standards:** intraday liquidity monitoring, same-day / intraday settlement resilience, and participant default preparedness.
- **RPAA concepts:** operational risk and fraud risk management, documented frameworks, and monitoring expectations for payment service providers.
- **Three Lines of Defence:** first-line ownership, second-line independent challenge, and third-line assurance.

Detailed mapping is documented in [`docs/regulatory-alignment.md`](docs/regulatory_alignment.md).

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

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
|   └── powerbi-design-notes.md
├── docs/
│   ├── regulatory-alignment.md
│   └── rcsa-template.md
└── README.md
```

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Results and Business Recommendations

This project demonstrates how second-line risk can move from reactive reporting to more proactive oversight in a payments environment. Even with synthetic data, the framework shows how credit, liquidity, fraud, and AI-driven risk indicators can be brought into a common decision model with clear thresholds, escalation logic, and management actions.

The business value of this approach includes:

- Earlier identification of elevated participant or merchant credit risk.
- Better visibility into intraday liquidity pressure under stressed settlement scenarios.
- Faster escalation of potential fraud patterns through rules, KRIs, and AI-driven fraud risk scoring.
- More structured and credible second-line challenge for product, risk, and governance stakeholders.
- Better translation of analytical outputs into executive and committee reporting.

Based on this framework, the key business recommendations are:

- Build a common KRI layer across fraud, liquidity, and participant / merchant risk rather than managing each domain in isolation.
- Use scenario testing regularly to assess resilience under volume spikes, counterparty stress, and adverse fraud conditions.
- Strengthen second-line challenge by requiring documented assumptions, thresholds, and model limitations for each monitoring process.
- Combine rules-based controls and explainable AI scoring for fraud rather than treating them as mutually exclusive approaches.
- Translate technical risk outputs into governance-ready reporting that supports Product Council, ERM committee, and executive review.

For a more detailed project reflection, **see [`docs/project_reflection.md](docs/project_reflection.md)**

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Project Artifacts

### Notebooks
- `notebooks/credit_risk.ipynb`
- `notebooks/intraday_liquidity.ipynb`
- `notebooks/fraud_rules_and_kri.ipynb`
- `notebooks/fraud_ai_model.ipynb`

### Key Outputs
- Credit risk charts and markdown report
- Intraday liquidity charts and markdown report
- Fraud rules charts and markdown report
- AI fraud model metrics, feature importance, and score bucket summaries

### Documentation
- `docs/regulatory-alignment.md`
- `docs/rcsa-template.md`
- `dashboard/powerbi-design-notes.md`

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

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
- The AI fraud model is designed for explainability and portfolio demonstration, not production deployment.

[Back to Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

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

[Back to the Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)

---

## Author Info

- Github - [Github Profile](https://github.com/prasanna-sriram)
- LinkedIn - [Prasanna Sriram](https://www.linkedin.com/in/prasanna-sriram/)
- Tableau - [Tableau Public Profile](https://public.tableau.com/app/profile/prasanna.sriram.ps)

[Back to the Top](#enterprise-risk-fraud-analytics-credit-risk-liquidity-risk-and-ai-driven-fraud-detection-framework-for-canadian-payments)