# Project Reflection

This project began as a portfolio exercise, but it became much more valuable as a structured way to translate my existing **IT Risk / Security GRC / Vendor Risk** background into a second-line **financial risk and payments risk** context. My goal was not only to build models and dashboards, but to show how risk analytics, governance, and executive reporting can be brought together in a way that resembles the mandate of a modern ERM function in a regulated payments environment.

[Back to Top](#project-reflection)

---

## What I learned about credit and liquidity risk

The most important lesson from the **credit risk** workstream was that even relatively simple modelling can become much more meaningful when paired with exposure and concentration analysis. Building a PD-style merchant risk model helped me think beyond individual scores and toward portfolio-level questions such as: where is risk concentrated, how much of total exposure sits in higher-risk tiers, and what should second line challenge first line on in terms of reserves, limits, or onboarding assumptions. This reinforced that credit risk is not just about model outputs; it is also about how those outputs support governance, prioritization, and risk appetite conversations.

The **liquidity risk** workstream taught me to think in a more time-sensitive and operational way. Instead of asking only whether liquidity is sufficient in aggregate, the intraday simulation forced me to ask when liquidity pressure appears, how quickly buffers are consumed, and what a breach means operationally during the day. That was an important mindset shift. It also helped me better understand why regulators and overseers care so much about intraday liquidity monitoring, settlement obligations, and time-to-breach concepts rather than only high-level liquidity ratios.

A related lesson across both modules was the importance of **scenario thinking**. Credit and liquidity risks can both appear manageable in a base case but look very different once concentrations, stress assumptions, delayed inflows, or adverse merchant behaviour are introduced. That reinforced the value of using KRIs and scenario testing not just for reporting, but as tools for independent challenge.

[Back to Top](#project-reflection)

---

## How my IT / GRC background transfers to financial risk

This project also helped me articulate how strongly my prior experience transfers into financial risk and ERM, even though much of my background has been in **Security GRC, IT Risk, and third-party risk** rather than in a traditional bank risk function. In my previous work, I regularly performed risk assessments, challenged control design, tracked remediation, mapped controls to regulatory or framework requirements, and translated technical issues into management reporting. Those are all core second-line muscles, and this project gave me a way to demonstrate them using a payments-focused lens.

A major transferable strength is my experience turning broad frameworks into practical controls and monitoring. In prior roles, I mapped requirements from ISO 27001, SOC 2, PCI DSS, and NIST CSF into usable workflows, evidence standards, dashboards, and issue management processes. In this project, I applied the same pattern to a different domain: translating concepts from OSFI, Bank of Canada PPS expectations, RPAA, and three-lines-of-defence thinking into risk modules, KRIs, reports, an RCSA template, and a regulatory alignment document.

Another important transfer is in **stakeholder communication**. My past work involved presenting dashboards and control findings to leadership, auditors, and operational teams, often in environments where I needed to balance risk discipline with delivery practicality. This project extended that same approach into a financial risk narrative: not only building the analysis, but framing it for Product Council, ERM committee, and executive-level conversations.

Finally, my background in **issue management, remediation, and third-party risk**. Payments risk leadership is not just about identifying risks; it is about making sure risks are understood, ownership is clear, escalation happens at the right time, and remediation is tracked in a structured way. That is already a core theme in my prior work, and this project helped me show it in a payments-specific context.

[Back to Top](#project-reflection)

---

## What I would do differently with real data and more time

If I had real data and more time, the first improvement would be **data realism and calibration**. The current project uses synthetic data to demonstrate structure and methodology, but real participant, merchant, and transaction data would allow for better calibration of thresholds, more defensible risk segmentation, and richer validation of model outputs. In credit risk, I would want historical defaults, reserves, and chargeback outcomes. In fraud, I would want labelled fraud outcomes across time with more realistic class imbalance and operational review decisions.

The second improvement would be **more formal model risk management and validation**. For the AI-driven fraud model, I would want challenger models, stability testing, threshold calibration, and monitoring for drift. For the credit model, I would want more rigorous feature validation and potentially a more explicit expected-loss framework that includes LGD and EAD components.

The third improvement would be to expand the portfolio from separate modules into a more mature **operating model**. That would include:
- more formal RCSA and CIRA templates,
- issue management workflows tied to KRIs,
- clearer ownership between first line and second line,
- and a more comprehensive executive reporting pack showing trends over time rather than single-period views.

I would also deepen the **Power BI dashboard** by introducing trend views, drill-throughs, and more standardized risk appetite indicators. Right now, the dashboard is already useful as a portfolio demonstration, but with more time it could evolve into a much stronger board- and committee-ready package.

[Back to Top](#project-reflection)

---

## How this work relates to the ERM mandate

This project relates well to the ERM mandate because it is intentionally built from a **second-line perspective**. The target role calls for independent challenge, product and platform risk assessments, fraud KRI monitoring, executive engagement, and alignment to Payments risk expectations under a prominent payment system context. This portfolio does not replicate a live environment, but it does demonstrate the core mindset required for that kind of role: identify risk, quantify it where useful, translate it into KRIs, map it to governance and regulatory expectations, and package it in a way that supports challenge and decision-making.

The strongest alignment is in the combination of:
- **cross-risk thinking** across credit, liquidity, and fraud,
- **governance orientation** through RCSA and regulatory documentation,
- **fraud monitoring** through both rules and AI-driven scoring,
- and **executive reporting** through markdown reports and a Power BI dashboard.

That combination reflects the kind of broad, second-line product risk leadership the role is asking for. It also allowed me to show how my prior GRC and risk background can be extended into a more financial-risk and payments-risk setting without overstating experience I do not 
have.

[Back to Top](#project-reflection)

---

## Closing thought

The biggest value of this project for me was not just learning individual concepts like PD, intraday liquidity, or fraud scoring. It was learning how to connect them into one coherent **ERM story**: one that links analytics, controls, challenge, remediation, regulatory awareness, and executive communication. That is the part of the work that feels most relevant to the role I am targeting, and it is the part I would continue developing with real product, transaction, and governance data in a live environment.

[Back to Top](#project-reflection)

---