# Fraud Risk Report

## Executive Summary

This analysis uses simple, interpretable fraud rules applied at the card level
to identify unusual transaction patterns and support second-line fraud risk
monitoring.

Two types of rules are implemented:

- **Velocity rule**: flags cards that exceed a transaction count threshold within a short time window (e.g., more than 8 transactions within 15 minutes). This reflects standard guidance to use velocity checks as a first layer to catch rapid abuse patterns.
- **High-amount rule**: flags transactions with unusually large amounts (over 5,000), consistent with common guidance to set upper amount filters for high-risk payments.

At portfolio level:

- Total transactions: **50,563**
- Total fraud transactions (synthetic label): **563**
- Overall fraud rate: **0.0111**
- Total rule hits (any rule): **362**
- Rule hit rate: **0.0072**
- Fraud captured by rules: **351** (capture rate: **0.6234**)
- Fraud not flagged by rules: **212**
- Rule hits that are not fraud (potential false positives): **11**

These figures illustrate a typical trade-off: rules capture a large share of fraud while also generating some false positives, which must be managed through review processes and tuning.

## Card-Level View

### Top Cards by Rule Hits

The table below shows the top 10 cards by number of rule hits, along with their synthetic fraud counts and status:

| card_id   |   tx_count |   fraud_tx |   any_rule_hits | status                    |
|:----------|-----------:|-----------:|----------------:|:--------------------------|
| C000469   |         52 |         24 |              17 | High Risk (Fraud & Rules) |
| C001763   |         51 |         24 |              17 | High Risk (Fraud & Rules) |
| C000804   |         54 |         21 |              13 | High Risk (Fraud & Rules) |
| C002071   |         49 |         21 |              13 | High Risk (Fraud & Rules) |
| C001160   |         50 |         20 |              13 | High Risk (Fraud & Rules) |
| C001188   |         46 |         19 |              13 | High Risk (Fraud & Rules) |
| C001243   |         49 |         20 |              12 | High Risk (Fraud & Rules) |
| C001730   |         49 |         19 |              11 | High Risk (Fraud & Rules) |
| C002136   |         48 |         18 |              11 | High Risk (Fraud & Rules) |
| C002420   |         49 |         18 |              11 | High Risk (Fraud & Rules) |

Interpretation:

- **High Risk (Fraud & Rules)** cards are those where both fraudulent transactions and rule hits are present. These cards would typically require immediate investigation and potential blocking.
- **Medium Risk (Rules Only)** cards are those with rule hits but no confirmed fraud yet; they would be candidates for monitoring, additional verification, or dynamic controls.
- **Low Risk** cards have no rule hits and no observed fraud in this synthetic dataset.

## Rules and KRI Interpretation

From a second-line perspective, key messages from these KRIs are:

- **Effectiveness:** The share of fraud captured by the rules (capture rate) indicates whether the current rules are effective as a first-line filter.
- **Efficiency:** The number of rule hits that are not fraud highlights the operational burden of false positives and whether rules are too broad.
- **Coverage:** The overall fraud rate and rule hit rate provide context on how much of the portfolio is being scrutinized by rules.

In practice, fraud monitoring programs use these types of KRIs to balance fraud prevention with customer experience and operational capacity.

## Recommendations

- Use the current velocity and high-amount rules as a **baseline** and then iteratively tune thresholds to improve fraud capture while managing false positives.
- Introduce additional conditions (e.g., card-not-present only, foreign country filters, high-risk merchant segments) to sharpen rule precision.
- Define clear **escalation criteria** for when High Risk cards should be blocked or subject to additional verification.
- Consider adding a **risk score** on top of rules in a later phase, aggregating rule hits and behaviour patterns into a single summarizing metric.

## Limitations

- The dataset is synthetic and calibrated for demonstration; real fraud rates and patterns will differ.
- Rules are intentionally simple and global; production systems often use more granular, segment-specific thresholds and machine learning models.
- The is_fraud label represents injected fraud scenarios, not confirmed historical fraud cases.

