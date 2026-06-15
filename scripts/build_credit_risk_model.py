"""
PaymentRisk360 - Credit Risk Module
Script 02: Build PD-Style Credit Risk Model

Purpose
-------
This script transforms the synthetic merchant dataset into a model-ready feature
set, trains an interpretable logistic regression model, estimates default
probabilities, and assigns portfolio-style risk tiers.

Why this exists
---------------
The purpose is to demonstrate financial risk thinking in a second-line ERM
context. The script emphasizes interpretability and governance-readiness over
algorithmic complexity. That makes it well suited to a portfolio intended for a
risk leadership role where independent challenge, explainability, and practical
risk segmentation are more important than black-box performance.

What the script does
--------------------
1. Reads the synthetic credit dataset
2. One-hot encodes industry and settlement fields
3. Trains a logistic regression PD-style model
4. Scores all merchants with predicted default probability
5. Buckets merchants into Low / Medium / High / Severe risk tiers
6. Exports model-ready data, coefficients, metrics, and a top exposure file

Outputs
-------
- data/processed/credit_risk_features.csv
- outputs/credit_model_metrics.csv
- outputs/credit_model_coefficients.csv
- outputs/top_exposure_merchants.csv
"""

from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_INPUT = Path("data/raw/credit_risk_synthetic.csv")
PROCESSED_OUTPUT = Path("data/processed/credit_risk_features.csv")
METRICS_OUTPUT = Path("outputs/credit_model_metrics.csv")
COEFF_OUTPUT = Path("outputs/credit_model_coefficients.csv")
TOP_EXPOSURE_OUTPUT = Path("outputs/top_exposure_merchants.csv")

NUMERIC_FEATURES = [
    "monthly_txn_count",
    "average_ticket_size",
    "monthly_transaction_volume",
    "chargeback_rate",
    "fraud_alert_rate",
    "days_since_last_chargeback",
    "concentration_ratio",
    "reserve_coverage_ratio",
    "prior_default_flag",
    "gross_exposure",
    "net_exposure",
]

CATEGORICAL_FEATURES = ["industry_segment", "settlement_frequency"]
TARGET = "risk_label"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def assign_risk_tier(pd_score: float) -> str:
    """
    Convert a predicted default probability into a simple risk tier.

    Thresholds are illustrative and can be tuned to desired risk appetite.
    """
    if pd_score >= 0.50:
        return "Severe"
    if pd_score >= 0.25:
        return "High"
    if pd_score >= 0.10:
        return "Medium"
    return "Low"


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main() -> None:
    # Ensure output folders exist
    for path in [PROCESSED_OUTPUT.parent, METRICS_OUTPUT.parent]:
        path.mkdir(parents=True, exist_ok=True)

    # 1. Read raw data
    df = pd.read_csv(RAW_INPUT)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    # 2. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # 3. Preprocessing: scale numeric features, one-hot encode categoricals
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )

    # 4. Logistic regression model
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
            )),
        ]
    )

    # 5. Fit model
    model.fit(X_train, y_train)

    # 6. Evaluate on test set
    test_pd = model.predict_proba(X_test)[:, 1]
    test_pred = (test_pd >= 0.25).astype(int)  # illustrative classification threshold

    metrics_rows = [
        {
            "metric": "roc_auc",
            "value": roc_auc_score(y_test, test_pd),
        },
        {
            "metric": "accuracy_at_0_25",
            "value": accuracy_score(y_test, test_pred),
        },
        {
            "metric": "precision_at_0_25",
            "value": precision_score(y_test, test_pred, zero_division=0),
        },
        {
            "metric": "recall_at_0_25",
            "value": recall_score(y_test, test_pred, zero_division=0),
        },
    ]

    tn, fp, fn, tp = confusion_matrix(y_test, test_pred).ravel()
    metrics_rows.extend(
        [
            {"metric": "true_negative", "value": tn},
            {"metric": "false_positive", "value": fp},
            {"metric": "false_negative", "value": fn},
            {"metric": "true_positive", "value": tp},
        ]
    )

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(METRICS_OUTPUT, index=False)

    # 7. Score full dataset
    full_pd = model.predict_proba(X)[:, 1]
    df["predicted_pd"] = full_pd.round(4)
    df["risk_tier"] = df["predicted_pd"].apply(assign_risk_tier)

    df.to_csv(PROCESSED_OUTPUT, index=False)

    # 8. Extract model coefficients for transparency
    preprocessor_fitted = model.named_steps["preprocessor"]
    classifier = model.named_steps["classifier"]

    feature_names = preprocessor_fitted.get_feature_names_out()
    coeffs = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": classifier.coef_[0],
        }
    ).sort_values("coefficient", ascending=False)
    coeffs.to_csv(COEFF_OUTPUT, index=False)

    # 9. Top exposure merchants
    top_exposure = df.sort_values(
        ["net_exposure", "predicted_pd"], ascending=[False, False]
    ).head(25)
    top_exposure.to_csv(TOP_EXPOSURE_OUTPUT, index=False)

    # 10. Console summary
    print(
        {
            "processed_rows": len(df),
            "mean_predicted_pd": round(df["predicted_pd"].mean(), 4),
            "risk_tier_counts": df["risk_tier"].value_counts().to_dict(),
        }
    )


if __name__ == "__main__":
    main()