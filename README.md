# Fraud Transaction Anomaly Detection

This academic project compares statistical, unsupervised, and supervised methods for detecting credit-card fraud. It uses one historical dataset as a benchmark, not as evidence of performance in a production banking system.

See the [project plan](workflow%20scope/plan.md) and [step-by-step guide](workflow%20scope/step-by-step-guide.md) for the agreed scope and experiment protocol.

## Setup

From the project root in Windows PowerShell:

1. Install Python and create a virtual environment. Python 3.12 is a practical choice; the current dependency versions are not pinned.

   ```powershell
   py -3.12 --version
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m ipykernel install --user --name data-science-final-project --display-name "Python (Data Science Final Project)"
   ```

   If activation is blocked by PowerShell policy, follow your institution's guidance. Alternatively, run the commands using `.\.venv\Scripts\python.exe` instead of activating the environment.

2. In VS Code, install the Python and Jupyter extensions, open the project folder, and select **Python (Data Science Final Project)** as the notebook kernel. If using another environment, such as Conda, install the requirements and `ipykernel` in that environment and select its kernel instead.
3. Check the selected kernel by running this in a notebook cell:

   ```python
   import sys
   import joblib, numpy, pandas, sklearn, torch
   print(sys.executable)
   ```

   The executable should belong to the environment you selected. A GPU is not required.
4. Download the [European credit-card fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) after reviewing its access terms and place `creditcard.csv` in `data/`. The expected columns are `Time`, `V1`-`V28`, `Amount`, and `Class`; the expected dataset contains 284,807 rows and 492 fraud cases. Record any discrepancies.

The CSV is excluded by `.gitignore`. Do not commit the dataset or Kaggle credentials.

## Experiment protocol

- Use the saved stratified 70% training, 15% validation, and 15% test split and random seed `42`.
- Fit reference statistics, scalers, and models using training data. Select model settings and thresholds using validation data.
- The statistical methods do not use fraud labels for fitting. Isolation Forest and the autoencoder train on legitimate training transactions; Random Forest is a supervised benchmark trained with labels.
- Keep model choices frozen before final test evaluation. **Earlier Z-score and IQR test results already exist**, so the test split has previously been evaluated and should not be described as untouched. Document this exposure and do not tune against those results.
- Report precision, recall, F1, average precision (a precision-recall summary), false-positive rate and count, and confusion matrices. Accuracy is supplementary for this imbalanced dataset.

## Notebook workflow and completed work

Run notebooks from top to bottom in fresh kernels, in the order below. Notebooks 02-06 load the saved split rather than relying on a shared notebook session. Running a notebook again can overwrite its saved artifacts in `results/`; preserve the existing experiment records before rerunning if they are needed for comparison.

1. [Data audit and exploratory checks](notebooks/01_data_aduit_and_exploratary_check.ipynb) - loads the dataset, inspects data quality and class imbalance, produces exploratory plots, and saves `results/split_indices.npz`.
2. [Statistical baselines](notebooks/02_statistical_baselines.ipynb) - computes Z-score and IQR scores, selects validation thresholds, and saves training statistics and validation results in `results/statistical_baselines.json`.
3. [Isolation Forest](notebooks/03_isolation_forest.ipynb) - trains an anomaly detector and saves its model and validation-selected threshold.
4. [Random Forest](notebooks/04_random_forest.ipynb) - trains and compares class-weighted supervised models and saves the selected model and validation metrics. Training may take time.
5. [Autoencoder](notebooks/05_autoencoder.ipynb) - trains a small PyTorch autoencoder and saves its weights, scaler, and validation metrics.
6. [Hybrid and validation comparison](notebooks/06_hybrid_and_validation_comparison.ipynb) - combines four percentile-ranked anomaly scores with equal weights, selects a validation threshold, and saves `results/validation_comparison.json` and `results/hybrid_rank_reference.npz`. The saved comparison contains validation results for all six methods.
7. [Final test evaluation](notebooks/07_final_test_evaluation.ipynb) - currently evaluates only Z-score, IQR, and Isolation Forest using their saved thresholds. It writes `results/anomaly_baselines_test_results.json` and `.csv`; the existing `statistical_baselines_test_results` files are earlier results.

Notebook 07 uses a relative `%run` path, so its kernel working directory must be `notebooks/`. Alternatively, from the project root, run `python src\evaluate_statistical_baselines.py` after the final choices are frozen. Do not run either as a setup check: they evaluate the test split and write results.

## Remaining work

- Fix Notebook 01's schema check: its expected column list contains a nested list and currently reports a mismatch even when the columns match.
- Complete final evaluation for Random Forest, autoencoder, and hybrid. Apply the saved validation thresholds and fit-time artifacts. For the hybrid, map test scores against the saved validation rank references using a documented tie-handling convention consistent with validation; do not rank the test set against itself.
- Freeze the evaluation procedure and preserve existing results before running the final comparison. Document the previous test exposure and any experiment changes.
- Produce a final comparison table, precision-recall curves, confusion matrices, false-alert counts, and training/scoring times where practical.
- Write the report and presentation: discuss model assumptions, the supervised/unsupervised distinction, interpretability, computational cost, class imbalance, uncertainty from the small fraud count, and the historical dataset's limitations.
- Verify the documented setup and notebook workflow in a fresh environment, record package versions, and check that code, figures, tables, and report agree.
