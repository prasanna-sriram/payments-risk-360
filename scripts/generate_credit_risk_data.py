"""
PaymentRisk360 - Credit Risk Module
Script 01: Generate Synthetic Credit Risk Data

Purpose
-------
This script generates a synthetic merchant / participant-level dataset for the
credit risk workstream of the PaymentRisk360 portfolio project.

Why this exists
---------------
The target ERM role requires evidence of financial risk capability, particularly
credit risk and second-line oversight thinking. Real payment network datasets are
not available for public portfolio use, so this script creates a controlled,
reproducible synthetic dataset that supports:

- PD-style (Probability of Default) modelling
- exposure and concentration analysis
- risk tier segmentation
- second-line challenge and governance reporting

What the script does
--------------------
1. Creates a synthetic merchant population with industry-specific risk behaviour
2. Generates merchant attributes such as transaction volume, chargebacks,
   exposure, reserve coverage, and prior distress indicators
3. Injects realistic risk relationships so the downstream model learns
   meaningful patterns
4. Creates a binary default label for supervised modelling
5. Writes a raw dataset to data/raw/credit_risk_synthetic.csv

Notes for reviewers / hiring managers
-------------------------------------
This is not intended to replicate a production-grade bank underwriting model.
It is a portfolio-grade analytical artifact showing how a second-line risk
function might structure an interpretable credit risk view in a payments context.
"""

from pathlib import Path
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RANDOM_SEED = 42
N_MERCHANTS = 2500  # adjust here if you want more/fewer rows
RAW_OUTPUT = Path("data/raw/credit_risk_synthetic.csv")

# Industry-level risk patterns (synthetic but directionally realistic)
INDUSTRY_RISK = {
    "grocery": {
        "base_risk": 0.03,
        "chargeback_mean": 0.002,
        "ticket_mean": 40,
    },
    "fuel": {
        "base_risk": 0.035,
        "chargeback_mean": 0.003,
        "ticket_mean": 55,
    },
    "retail": {
        "base_risk": 0.05,
        "chargeback_mean": 0.006,
        "ticket_mean": 85,
    },
    "travel": {
        "base_risk": 0.11,
        "chargeback_mean": 0.018,
        "ticket_mean": 320,
    },
    "gaming": {
        "base_risk": 0.14,
        "chargeback_mean": 0.022,
        "ticket_mean": 110,
    },
    "digital_services": {
        "base_risk": 0.09,
        "chargeback_mean": 0.014,
        "ticket_mean": 95,
    },
    "marketplace": {
        "base_risk": 0.08,
        "chargeback_mean": 0.011,
        "ticket_mean": 70,
    },
    "restaurants": {
        "base_risk": 0.045,
        "chargeback_mean": 0.004,
        "ticket_mean": 45,
    },
    "healthcare": {
        "base_risk": 0.04,
        "chargeback_mean": 0.003,
        "ticket_mean": 140,
    },
    "electronics": {
        "base_risk": 0.085,
        "chargeback_mean": 0.013,
        "ticket_mean": 260,
    },
}

SETTLEMENT_MAP = {
    "daily": 1,
    "twice_weekly": 2,
    "weekly": 3,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def sigmoid(x: np.ndarray) -> np.ndarray:
    """Standard sigmoid used to convert a risk score into PD-like probability."""
    return 1 / (1 + np.exp(-x))


def generate_credit_dataset(
    n_merchants: int = N_MERCHANTS,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Generate a synthetic merchant-level credit risk dataset.

    Parameters
    ----------
    n_merchants : int
        Number of synthetic merchants to generate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Synthetic merchant dataset with behavioural, exposure, and risk fields.
    """
    rng = np.random.default_rng(seed)

    # Industry mix: skewed toward retail / grocery / restaurants, smaller high-risk niches
    industries = list(INDUSTRY_RISK.keys())
    industry_probs = np.array(
        [0.14, 0.09, 0.18, 0.07, 0.06, 0.11, 0.09, 0.12, 0.07, 0.07]
    )

    merchant_ids = [f"M{str(i).zfill(5)}" for i in range(1, n_merchants + 1)]
    industry_segment = rng.choice(industries, size=n_merchants, p=industry_probs)
    settlement_frequency = rng.choice(
        ["daily", "twice_weekly", "weekly"],
        size=n_merchants,
        p=[0.58, 0.24, 0.18],
    )

    rows = []

    for merchant_id, industry, settlement in zip(
        merchant_ids, industry_segment, settlement_frequency
    ):
        risk_profile = INDUSTRY_RISK[industry]

        # Transaction behaviour
        monthly_txn_count = max(
            80, int(rng.lognormal(mean=7.2, sigma=0.75))
        )  # heavier tail for big merchants
        avg_ticket_size = max(
            8, rng.normal(risk_profile["ticket_mean"], risk_profile["ticket_mean"] * 0.25)
        )
        monthly_transaction_volume = monthly_txn_count * avg_ticket_size

        # Chargeback and fraud behaviour
        chargeback_rate = max(
            0.0002,
            rng.normal(
                risk_profile["chargeback_mean"],
                risk_profile["chargeback_mean"] * 0.45,
            ),
        )
        fraud_alert_rate = max(
            0.0001,
            chargeback_rate * rng.uniform(0.7, 1.8),
        )

        # Concentration and reserves
        concentration_ratio = np.clip(rng.beta(2.2, 8.0), 0.02, 0.85)
        reserve_coverage_ratio = np.clip(
            rng.normal(0.85 - risk_profile["base_risk"], 0.15),
            0.10,
            1.40,
        )
        prior_default_flag = int(rng.random() < (risk_profile["base_risk"] * 0.6))
        days_since_last_chargeback = int(np.clip(rng.exponential(scale=75), 0, 365))
        settlement_days = SETTLEMENT_MAP[settlement]

        # Exposure: simple structural approximation
        gross_exposure = monthly_transaction_volume * rng.uniform(0.06, 0.18)
        settlement_exposure = gross_exposure * (1 + settlement_days / 10)
        net_exposure = settlement_exposure * (1 - min(reserve_coverage_ratio * 0.35, 0.45))

        # Distress score: combine risk drivers into a PD-like signal
        distress_score = (
            -3.8
            + 4.5 * chargeback_rate * 100
            + 3.2 * fraud_alert_rate * 100
            + 0.000004 * net_exposure
            + 1.8 * concentration_ratio
            - 1.6 * reserve_coverage_ratio
            + 1.1 * prior_default_flag
            + 0.002 * max(0, 40 - min(days_since_last_chargeback, 40))
            + risk_profile["base_risk"] * 4
        )

        default_probability = float(sigmoid(np.array([distress_score]))[0])
        risk_label = int(rng.random() < default_probability)

        rows.append(
            {
                "merchant_id": merchant_id,
                "industry_segment": industry,
                "settlement_frequency": settlement,
                "monthly_txn_count": monthly_txn_count,
                "average_ticket_size": round(avg_ticket_size, 2),
                "monthly_transaction_volume": round(monthly_transaction_volume, 2),
                "chargeback_rate": round(chargeback_rate, 5),
                "fraud_alert_rate": round(fraud_alert_rate, 5),
                "days_since_last_chargeback": days_since_last_chargeback,
                "concentration_ratio": round(concentration_ratio, 4),
                "reserve_coverage_ratio": round(reserve_coverage_ratio, 4),
                "prior_default_flag": prior_default_flag,
                "gross_exposure": round(gross_exposure, 2),
                "net_exposure": round(net_exposure, 2),
                "synthetic_pd_signal": round(default_probability, 4),
                "risk_label": risk_label,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    # Ensure output folder exists
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df = generate_credit_dataset()
    df.to_csv(RAW_OUTPUT, index=False)

    # Simple console summary for quick validation
    summary = {
        "rows": len(df),
        "default_rate": round(df["risk_label"].mean(), 4),
        "avg_net_exposure": round(df["net_exposure"].mean(), 2),
        "top_industries": df["industry_segment"].value_counts().head(5).to_dict(),
    }
    print(summary)


if __name__ == "__main__":
    main()