import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "creditcard.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
SPLIT_PATH = RESULTS_DIR / "split_indices.npz"
RECORD_PATH = RESULTS_DIR / "statistical_baselines.json"
ISOLATION_FOREST_PATH = RESULTS_DIR / "isolation_forest.joblib"
ISOLATION_FOREST_CONFIG_PATH = RESULTS_DIR / "isolation_forest_config.json"


def evaluate_scores(y_true, scores, threshold):
    predictions = (scores >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(
        y_true, predictions, labels=[0, 1]
    ).ravel()

    return {
        "threshold": float(threshold),
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
        "recall": float(recall_score(y_true, predictions, zero_division=0)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
        "average_precision": float(average_precision_score(y_true, scores)),
        "false_positive_rate": float(fp / (fp + tn)) if (fp + tn) else 0.0,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }


def main():
    for required_path in (
        DATA_PATH,
        SPLIT_PATH,
        RECORD_PATH,
        ISOLATION_FOREST_PATH,
        ISOLATION_FOREST_CONFIG_PATH,
    ):
        if not required_path.exists():
            raise FileNotFoundError(
                f"Required file not found: {required_path}. "
                "Run the data audit/split, statistical-baselines, and "
                "Isolation Forest notebooks first."
            )

    with RECORD_PATH.open(encoding="utf-8") as file:
        record = json.load(file)

    if record.get("random_seed") != SEED:
        raise ValueError(
            f"Expected random seed {SEED}; saved record has "
            f"{record.get('random_seed')!r}."
        )

    df = pd.read_csv(DATA_PATH)
    with np.load(SPLIT_PATH) as split_indices:
        test_indices = split_indices["test_idx"]

    if len(test_indices) == 0 or test_indices.max() >= len(df):
        raise ValueError("Saved test indices are empty or outside the dataset.")

    feature_cols = record["feature_cols"]
    missing_features = sorted(set(feature_cols) - set(df.columns))
    if missing_features or "Class" not in df.columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_features or ['Class']}."
        )

    test_df = df.loc[test_indices]
    X_test = test_df[feature_cols]
    y_test = test_df["Class"].to_numpy()

    stats = record["reference_statistics"]
    train_mean = pd.Series(stats["mean"]).reindex(feature_cols)
    train_std = pd.Series(stats["std"]).reindex(feature_cols)
    q1 = pd.Series(stats["q1"]).reindex(feature_cols)
    q3 = pd.Series(stats["q3"]).reindex(feature_cols)

    if any(values.isna().any() for values in (train_mean, train_std, q1, q3)):
        raise ValueError(
            "Saved training statistics are incomplete or do not match the features."
        )

    z_deviations = (X_test - train_mean).abs().div(train_std.replace(0, np.nan))
    z_flags = z_deviations.gt(3) | (train_std.eq(0) & X_test.ne(train_mean))
    z_test = z_flags.fillna(False).mean(axis=1).to_numpy()

    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    iqr_test = (X_test.lt(lower_fence) | X_test.gt(upper_fence)).mean(axis=1).to_numpy()

    validation_results = record["validation_results"]
    test_results = {
        "z_score": evaluate_scores(
            y_test, z_test, validation_results["z_score"]["threshold"]
        ),
        "iqr": evaluate_scores(
            y_test, iqr_test, validation_results["iqr"]["threshold"]
        ),
    }

    with ISOLATION_FOREST_CONFIG_PATH.open(encoding="utf-8") as file:
        isolation_forest_config = json.load(file)

    if isolation_forest_config.get("random_seed") != SEED:
        raise ValueError(
            f"Expected Isolation Forest random seed {SEED}; saved record has "
            f"{isolation_forest_config.get('random_seed')!r}."
        )

    isolation_feature_cols = isolation_forest_config.get("feature_cols")
    if isolation_feature_cols != feature_cols:
        raise ValueError(
            "Isolation Forest feature columns do not match the statistical "
            "baseline feature columns."
        )

    isolation_threshold = isolation_forest_config.get("threshold")
    if not isinstance(isolation_threshold, (int, float)):
        raise ValueError("Saved Isolation Forest threshold is missing or invalid.")

    isolation_forest = joblib.load(ISOLATION_FOREST_PATH)
    isolation_test_scores = -isolation_forest.decision_function(X_test)
    test_results["isolation_forest"] = evaluate_scores(
        y_test, isolation_test_scores, isolation_threshold
    )

    json_path = RESULTS_DIR / "anomaly_baselines_test_results.json"
    csv_path = RESULTS_DIR / "anomaly_baselines_test_results.csv"
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(test_results, file, indent=2)
    pd.DataFrame.from_dict(test_results, orient="index").rename_axis("method").to_csv(
        csv_path
    )

    print("Final test results using validation-selected thresholds:")
    print(json.dumps(test_results, indent=2))
    print(f"Saved results to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
