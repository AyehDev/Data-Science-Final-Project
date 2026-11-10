# Fraud Transaction Anomaly Detection

This project compares statistical, unsupervised machine-learning, and supervised methods for detecting fraudulent credit-card transactions. It is a reproducible academic benchmark, not a production banking system.

See the [project plan](workflow%20scope/plan.md) and [step-by-step guide](workflow%20scope/step-by-step-guide.md) for the full scope and workflow.
See the [November 9 progress update](workflow%20scope/progress-update-2026-11-09.md) for implementation status and next steps.

## Setup

Use Windows PowerShell from the project root. Install Python 3 first, then create and activate a project-local virtual environment:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install jupyter pandas numpy matplotlib seaborn scikit-learn torch
```

In VS Code or Jupyter, select the Python interpreter/kernel from `.venv`. Verify that the packages import successfully before running the notebooks. Use CPU-compatible packages; a GPU is not required.

## Dataset

Use only the [European credit-card fraud dataset on Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).

1. Review the dataset's access terms and download `creditcard.csv`.
2. Place the file at `data/creditcard.csv`.
3. Confirm that it contains `Time`, `V1`–`V28`, `Amount`, and `Class`. The expected dataset has 284,807 rows and 492 fraud cases; record any discrepancy.
4. Do not commit the CSV or Kaggle credentials. Keep credentials outside the project. The `.gitignore` excludes `creditcard.csv`.
5. Document the source and schema, not a copy of the dataset. Treat it as a historical benchmark, not evidence of performance on current bank transactions.

## Reproducibility

Use **random seed `42`** throughout the project. Apply it consistently to the stratified train/validation/test split, scikit-learn estimators, and PyTorch initialization/training wherever randomness is involved. Record any library-specific seed settings alongside the experiment.

Create one stratified split of approximately 70% training, 15% validation, and 15% test data. Fit preprocessing and models on training data only; use validation data to choose model settings and thresholds. Keep the test split untouched until all choices are frozen, then evaluate on it once.

## Notebook run order

Run the existing notebooks in this order so each stage uses the decisions and outputs of the previous stage:

1. `01_data_aduit_and_exploratary_check.ipynb` — Load and verify the dataset, audit data quality, explore class imbalance and feature distributions, and create/save the fixed stratified split.
2. `02_statistical_baselines.ipynb` — Implement the Z-score and IQR baselines, fit reference statistics on training data, select thresholds using validation data, and save the thresholds, statistics, and validation metrics to `results/statistical_baselines.json`.
3. `03_isolation_forest.ipynb` — Train the unsupervised Isolation Forest and evaluate/choose its threshold on validation data.
4. `04_random_forest.ipynb` — Train the class-weighted Random Forest using training labels; report it as a supervised benchmark.
5. `05_autoencoder.ipynb` — Train a small autoencoder on legitimate training transactions and select its threshold using validation data.
6. `06_hybrid_and_validation_comparison.ipynb` — Normalize the statistical and unsupervised anomaly scores, form the equal-weight hybrid, and freeze model settings and thresholds based on validation results.
7. `07_final_test_evaluation.ipynb` — After all decisions are frozen, run the statistical-baseline test evaluation once on the untouched test split. It reuses the saved validation thresholds and training statistics and writes JSON/CSV results to `results/`.

Run each notebook from top to bottom in a fresh kernel. Do not use test results to revise preprocessing, models, score normalization, or thresholds.

## Evaluation expectations

Do not use fraud labels to train Z-score, IQR, Isolation Forest, or the autoencoder. The Random Forest is the supervised comparison and does use labels. Report precision, recall, F1, PR-AUC, false-positive rate and count, and confusion matrices. Accuracy may be included as a supplement. Record training and scoring time where practical, and discuss class imbalance, interpretability, uncertainty, and dataset limitations.