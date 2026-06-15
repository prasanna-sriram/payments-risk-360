# Intraday Liquidity Risk Report

## Executive Summary

This analysis simulates intraday liquidity positions for a payments participant
under three scenarios:

- **Base case** - normal day with typical inflows and outflows
- **Stress volume** - higher payment outflows and modest inflow delay
- **Severe stress** - large outflow spike and material inflow disruption

All scenarios start from the same synthetic intraday buffer and balance.
The objective is to illustrate how quickly the intraday buffer is consumed and
when warning or breach conditions would be triggered.

From a second-line perspective, the key conclusions are:

- The **base case** remains within buffer limits but generates a meaningful number of warning intervals, which is consistent with a buffer being actively used rather than purely static.
- The **stress volume** scenario shows multiple breaches and a later time-to-first-breach, indicating that sustained volume pressure can exhaust the buffer in the second half of the day.
- The **severe stress** scenario exhausts the buffer earlier and more frequently, with both warning and breach conditions becoming prominent.

## Scenario-Level KRIs

### Base Case

- Status: **Amber**
- Minimum intraday position: 34,079,586.10
- Minimum buffer available: 4,079,586.10
- Warning intervals: 9
- Breach intervals: 0
- Time to first warning: 135.0 minutes
- Time to first breach: nan minutes

Interpretation:

The base case uses the buffer but does not fully exhaust it (min buffer remains positive). Warning intervals indicate periods where buffer usage enters a lower comfort zone, which should be tracked, but this profile is generally consistent with a well-calibrated intraday buffer for normal conditions.

### Stress Volume Scenario

- Status: **Red**
- Minimum intraday position: 28,182,308.48
- Minimum buffer available: 0.00
- Warning intervals: 12
- Breach intervals: 5
- Time to first warning: 120.0 minutes
- Time to first breach: 180.0 minutes

Interpretation:

The stress volume scenario shows that elevated outflows and modest inflow delays can push the buffer into breach territory, especially later in the day. This highlights the need for intraday monitoring and, potentially, payment pacing or prioritisation if similar patterns emerge in real operations.

### Severe Stress Scenario

- Status: **Red**
- Minimum intraday position: 3,872,893.75
- Minimum buffer available: 0.00
- Warning intervals: 26
- Breach intervals: 17
- Time to first warning: 90.0 minutes
- Time to first breach: 120.0 minutes

Interpretation:

The severe stress scenario produces early and repeated breaches of the buffer, signalling conditions under which intraday funding, payment throttling, or contingency funding actions would be required. This scenario is useful for illustrating how quickly risk can escalate if inflows are disrupted and outflows are elevated.

## Second-Line Considerations and Recommendations

From a second-line ERM perspective, this synthetic intraday view suggests:

- **KRIs:** Time-to-first-breach, number of breach intervals, and minimum buffer available are suitable intraday liquidity KRIs for monitoring and escalation.
- **Governance:** Clear escalation paths should be defined for Red scenarios, including thresholds for when to engage treasury, payment operations, or senior management.
- **Payment Sequencing:** In stress conditions, payment pacing or prioritisation could be used to slow non-critical outflows and protect critical settlement obligations.
- **Scenario Testing:** Regularly running intraday stress scenarios helps validate whether buffers and intraday limits remain appropriate as payment patterns evolve.

## Limitations

- The dataset is synthetic and uses stylised inflow/outflow patterns.
- Buffer levels and thresholds are illustrative and would need calibration to real balances, credit lines, and operational constraints.
- The simulation focuses on a single participant-level view and does not model broader system-level contagion or network effects.
