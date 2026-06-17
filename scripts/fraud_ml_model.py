"""
PaymentRisk360 - Fraud Risk Module
Script 05: AI-Driven Fraud Model (Explainable Logistic Regression)

Purpose
-------
This script adds an AI-driven layer on top of the rules-based fraud module.
It trains a simple, explainable logistic regression model to estimate the
probability that a transaction is fraudulent.

The model uses:
- underlying transaction attributes (amount, channel, merchant segment, country)
- rules-based flags (velocity and high-amount rules)
- simple card-level statistics (transaction count, total amount)

Why this exists
---------------
Many payment fraud stacks combine rules and machine learning:
- Rules provide transparent, tunable controls.
- Machine learning models provide a continuous risk score and adapt to patterns
  in high-dimensional data.

This script demonstrates an AI-driven fraud detection component that remains
governance-friendly and explainable, suitable for a second-line risk context.

Outputs
-------
- data/processed/fraud_transactions_with_scores.csv
- outputs/fraud_ml_metrics.csv
- outputs/fraud_ml_feature_importance.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support, average_precision_score

# Paths
TX_INPUT = Path("data/processed/fraud_transactions_with_rules.csv")
SCORED_OUTPUT = Path("data/processed/fraud_transactions_with_scores.csv")
METRICS_OUTPUT = Path("outputs/fraud_ml_metrics.csv")
FEATURE_IMPORTANCE_OUTPUT = Path("outputs/fraud_ml_feature_importance.csv")


# ---------------------------------------------------------------------------
# Helper: simple card-level summaries used as features
# ---------------------------------------------------------------------------

def add_card_level_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple card-level features that can help the model:

    - card_tx_count: number of transactions per card
    - card_total_amount: total amount per card
    - card_avg_amount: average amount per card
    """
    card_group = df.groupby("card_id")["amount"].agg(
        card_tx_count="count",
        card_total_amount="sum",
        card_avg_amount="mean",
    )

    df = df.merge(card_group, on="card_id", how="left")
    return df


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main() -> None:
    SCORED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    METRICS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(TX_INPUT, parse_dates=["timestamp"])

    # Basic sanity checks
    required_cols = {
        "transaction_id", "card_id", "amount",
        "merchant_segment", "channel", "country",
        "rule_velocity", "rule_high_amount",
        "any_rule_hit", "is_fraud",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns for modelling: {missing}")

    # Add card-level features
    df = add_card_level_features(df)

    # Feature selection
    numeric_features = [
        "amount",
        "card_tx_count",
        "card_total_amount",
        "card_avg_amount",
    ]

    binary_rule_features = [
        "rule_velocity",
        "rule_high_amount",
        "any_rule_hit",
    ]

    categorical_features = [
        "merchant_segment",
        "channel",
        "country",
    ]

    # Define X and y
    X = df[numeric_features + binary_rule_features + categorical_features]
    y = df["is_fraud"].astype(int)

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # Preprocessing + model
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features + binary_rule_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                solver="lbfgs",
            )),
        ]
    )

    # Fit model
    model.fit(X_train, y_train)

    # Evaluate
    y_scores = model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_scores)
    avg_precision = average_precision_score(y_test, y_scores)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        (y_scores >= 0.5).astype(int),
        average="binary",
        zero_division=0,
    )

    metrics_rows = [
        {"metric": "roc_auc", "value": roc_auc},
        {"metric": "average_precision", "value": avg_precision},
        {"metric": "precision_at_0_5", "value": precision},
        {"metric": "recall_at_0_5", "value": recall},
        {"metric": "f1_at_0_5", "value": f1},
    ]
    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(METRICS_OUTPUT, index=False)

    # Feature importance (coefficients)
    preproc = model.named_steps["preprocessor"]
    clf = model.named_steps["classifier"]

    feature_names_num = numeric_features + binary_rule_features
    feature_names_cat = preproc.named_transformers_["cat"].get_feature_names_out(categorical_features)
    all_feature_names = np.concatenate([feature_names_num, feature_names_cat])

    coeffs = clf.coef_[0]
    feature_importance = pd.DataFrame(
        {
            "feature": all_feature_names,
            "coefficient": coeffs,
            "abs_coefficient": np.abs(coeffs),
        }
    ).sort_values("abs_coefficient", ascending=False)

    feature_importance.to_csv(FEATURE_IMPORTANCE_OUTPUT, index=False)

    # Score full dataset
    df["fraud_risk_score"] = model.predict_proba(X)[:, 1]

    df.to_csv(SCORED_OUTPUT, index=False)

    # Console summary
    print(
        {
            "roc_auc": round(roc_auc, 4),
            "average_precision": round(avg_precision, 4),
            "precision_at_0_5": round(precision, 4),
            "recall_at_0_5": round(recall, 4),
            "f1_at_0_5": round(f1, 4),
        }
    )


if __name__ == "__main__":
    main()