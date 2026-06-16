"""
PaymentRisk360 - Fraud Risk Module
Script 01: Generate Synthetic Card Transaction Data

Purpose
-------
This script generates a synthetic card-level transaction dataset for the
fraud module. It is designed to support rules-based fraud monitoring,
with a focus on:

- card-level velocity checks (number/amount of transactions in a short window)
- amount anomaly rules (very large or unusual amounts)
- simple fraud KRIs and second-line reporting

Why this exists
---------------
Fraud monitoring in payments often starts with rules that detect unusual
behaviour patterns such as too many transactions in a short period, or
suspiciously large or out-of-pattern transaction amounts for a card.

This synthetic dataset is built to contain:

- mostly legitimate traffic with realistic distributions,
- a small fraction of fraud-like patterns that would trigger such rules.

Outputs
-------
- data/raw/fraud_transactions.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RANDOM_SEED = 42
N_TRANSACTIONS = 50_000

RAW_OUTPUT = Path("data/raw/fraud_transactions.csv")

# Transaction date range (e.g., one synthetic day with intraday times)
BASE_DATE = "2026-01-10"

MERCHANT_SEGMENTS = [
    "grocery",
    "fuel",
    "electronics",
    "fashion",
    "digital_content",
    "gaming",
    "travel",
    "marketplace",
]

CHANNELS = ["card_present", "card_not_present"]
COUNTRIES = ["CA", "US", "GB", "FR", "DE", "IN", "BR"]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_base_transactions(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Generate base transaction population with mostly legitimate behaviour.
    """
    # Card population: fewer cards than transactions to allow multiple tx per card
    n_cards = int(n / 20)  # ~2500 cards for 50k tx
    card_ids = [f"C{str(i).zfill(6)}" for i in range(1, n_cards + 1)]
    card_sample = rng.choice(card_ids, size=n, replace=True)

    # Transaction timestamps across a single day
    start = pd.Timestamp(f"{BASE_DATE} 00:00:00")
    end = pd.Timestamp(f"{BASE_DATE} 23:59:00")
    timestamps = start + pd.to_timedelta(
        rng.integers(0, int((end - start).total_seconds()), size=n), unit="s"
    )

    merchant_segment = rng.choice(MERCHANT_SEGMENTS, size=n, replace=True)
    channel = rng.choice(CHANNELS, size=n, p=[0.45, 0.55], replace=True)
    country = rng.choice(COUNTRIES, size=n, replace=True)

    # Base amounts: mix per segment
    base_amounts = []
    for seg in merchant_segment:
        if seg in ("grocery", "fuel"):
            amt = rng.lognormal(mean=3.5, sigma=0.4)  # around 30-50
        elif seg in ("electronics", "travel"):
            amt = rng.lognormal(mean=5.0, sigma=0.7)  # higher-value items
        elif seg in ("digital_content", "gaming"):
            amt = rng.lognormal(mean=3.2, sigma=0.6)  # smaller, frequent
        else:
            amt = rng.lognormal(mean=4.1, sigma=0.5)
        base_amounts.append(amt)

    amount = np.round(base_amounts, 2)

    df = pd.DataFrame(
        {
            "transaction_id": [f"T{str(i).zfill(7)}" for i in range(1, n + 1)],
            "card_id": card_sample,
            "timestamp": timestamps,
            "merchant_segment": merchant_segment,
            "channel": channel,
            "country": country,
            "amount": amount,
        }
    )

    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


def inject_velocity_fraud(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Inject fraud-like patterns using card-level velocity:

    - Choose a small set of cards.
    - For each, create a burst of many small/medium transactions in a short window.
    """
    df = df.copy()

    candidate_cards = df["card_id"].value_counts().head(200).index.tolist()
    n_cards_velocity = min(25, len(candidate_cards))
    fraud_cards = rng.choice(candidate_cards, size=n_cards_velocity, replace=False)

    fraud_rows = []

    for card in fraud_cards:
        # Choose a random starting time in the day
        base_time = pd.Timestamp(f"{BASE_DATE} 10:00:00") + pd.to_timedelta(
            rng.integers(-3, 5), unit="h"
        )

        # Generate a burst of 10-25 transactions within 10-20 minutes
        burst_size = rng.integers(10, 25)
        for _ in range(burst_size):
            delta_seconds = int(rng.integers(0, 20 * 60))  # up to 20 minutes
            ts = base_time + pd.to_timedelta(delta_seconds, unit="s")

            seg = rng.choice(MERCHANT_SEGMENTS)
            if seg in ("digital_content", "gaming"):
                amt = rng.lognormal(mean=3.7, sigma=0.4)
            else:
                amt = rng.lognormal(mean=4.0, sigma=0.5)

            fraud_rows.append(
                {
                    "transaction_id": None,  # will assign later
                    "card_id": card,
                    "timestamp": ts,
                    "merchant_segment": seg,
                    "channel": "card_not_present",
                    "country": rng.choice(COUNTRIES),
                    "amount": round(amt, 2),
                    "fraud_pattern": "velocity_burst",
                }
            )

    fraud_df = pd.DataFrame(fraud_rows)

    if not fraud_df.empty:
        # Assign new transaction_ids for injected rows
        start_index = len(df) + 1
        fraud_df["transaction_id"] = [
            f"T{str(i).zfill(7)}" for i in range(start_index, start_index + len(fraud_df))
        ]

        df["fraud_pattern"] = None
        df = pd.concat([df, fraud_df], ignore_index=True)

    return df


def inject_high_amount_fraud(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Inject fraud-like patterns using unusually high amounts:

    - Pick random cards and timestamps.
    - Create a small number of very large transactions.
    """
    df = df.copy()

    n_high_amount = 150  # number of high-value suspicious transactions
    card_sample = rng.choice(df["card_id"].unique(), size=n_high_amount, replace=True)

    high_rows = []
    for card in card_sample:
        ts_base = pd.Timestamp(f"{BASE_DATE} 02:00:00") + pd.to_timedelta(
            rng.integers(-2, 4), unit="h"
        )
        ts = ts_base + pd.to_timedelta(rng.integers(0, 60 * 60), unit="s")

        # Very large amounts, out of pattern for most segments
        amt = rng.uniform(4_000, 12_000)

        seg = rng.choice(["electronics", "travel", "marketplace"])
        high_rows.append(
            {
                "transaction_id": None,
                "card_id": card,
                "timestamp": ts,
                "merchant_segment": seg,
                "channel": "card_not_present",
                "country": rng.choice(COUNTRIES),
                "amount": round(amt, 2),
                "fraud_pattern": "high_amount",
            }
        )

    high_df = pd.DataFrame(high_rows)

    start_index = len(df) + 1
    high_df["transaction_id"] = [
        f"T{str(i).zfill(7)}" for i in range(start_index, start_index + len(high_df))
    ]

    if "fraud_pattern" not in df.columns:
        df["fraud_pattern"] = None

    df = pd.concat([df, high_df], ignore_index=True)
    return df


def finalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Final clean-up:
    - sort by timestamp
    - add a synthetic is_fraud label (True for injected patterns, small noise)
    """
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Base label: mark injected patterns as fraud
    df["is_fraud"] = False
    df.loc[df["fraud_pattern"].notna(), "is_fraud"] = True

    # Optionally, add a tiny bit of label noise (e.g., some legit marked as fraud and vice versa)
    # For now, keep it simple and deterministic.

    return df


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main() -> None:
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)

    # 1) Base transactions
    df = generate_base_transactions(N_TRANSACTIONS, rng)

    # 2) Inject velocity fraud pattern
    df = inject_velocity_fraud(df, rng)

    # 3) Inject high-amount fraud pattern
    df = inject_high_amount_fraud(df, rng)

    # 4) Finalize
    df = finalize_dataframe(df)
    df.to_csv(RAW_OUTPUT, index=False)

    # Simple summary for quick validation
    summary = {
        "rows": len(df),
        "cards": df["card_id"].nunique(),
        "fraud_tx": int(df["is_fraud"].sum()),
        "fraud_rate": round(df["is_fraud"].mean(), 4),
        "velocity_fraud_tx": int((df["fraud_pattern"] == "velocity_burst").sum()),
        "high_amount_fraud_tx": int((df["fraud_pattern"] == "high_amount").sum()),
    }
    print(summary)


if __name__ == "__main__":
    main()