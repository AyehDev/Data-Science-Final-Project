# Step-by-Step Project Guide

This guide turns the [eight-week project plan](/workflow%20scope/plan.md) into a practical sequence of tasks for the **Statistical Anomaly Detection System for Fraudulent Banking Transactions** project.

The goal is a reproducible comparison on one historical dataset—not a production banking system. Keep the scope to the methods listed here and complete the core comparison before considering any extensions.

## Project checklist

- [ ] Use only the European credit-card fraud dataset described below.
- [ ] Compare Z-score, IQR, Isolation Forest, a class-weighted Random Forest, a small autoencoder, and one equal-weight hybrid.
- [ ] Fix a random seed and create one stratified 70%/15%/15% train/validation/test split.
- [ ] Fit transformations and models without using test data.
- [ ] Select thresholds and settings using validation data only.
- [ ] Evaluate on the test set once, after freezing the methods and thresholds.
- [ ] Report rare-event metrics, false alerts, model assumptions, and limitations.

## Step 1 — Agree on scope and responsibilities

1. Read the [project plan](./plan/plan.md) and the project proposal.
2. Confirm the research question and divide the work: setup/data, statistical baselines, machine-learning models, evaluation, and report/presentation.
3. Keep the comparison to:
   - Statistical baselines: Z-score and IQR.
   - Unsupervised detectors: Isolation Forest and a small autoencoder.
   - Supervised benchmark: class-weighted Random Forest.
   - Hybrid: an equal-weight combination of normalized statistical and unsupervised anomaly scores.
4. Do not add a second dataset, synthetic-data generation, GANs, diffusion or graph models, production deployment, or extra hybrid variants.

**Checkpoint:** The team agrees on the scope, responsibilities, random seed, and a single experiment protocol.

## Step 2 — Set up the Python project

Run these commands in Windows PowerShell from the project folder:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install jupyter pandas numpy matplotlib seaborn scikit-learn torch
```

1. Confirm that `py --version` reports a supported Python 3 installation.
2. If PowerShell prevents environment activation, follow your institution's or Python installation's guidance for enabling the activation script; do not bypass security policies.
3. Record the successfully installed package versions in `requirements.txt`.
4. Use the existing project folders where they fit: `data` for local data, `notebooks` for experiments, and `src` for shared code. Save generated tables and figures in a clearly named results folder, and drafts/final reporting in a report folder if needed.
5. Add setup instructions, dataset instructions, notebook run order, and the random seed to the README.
6. Never put Kaggle credentials or tokens in the project, notebook, or README. Keep credentials outside the project.
7. Start Jupyter from the activated environment, select its Python kernel, and run a small import check.

**Checkpoint:** Jupyter uses the project environment, required packages import successfully, and package versions and setup steps are recorded.

## Step 3 — Download and verify the dataset

1. Review the access terms on the [Kaggle dataset page](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).
2. Download `creditcard.csv` and place it in `data`.
3. Keep the CSV out of version control. Document its source and schema instead; do not commit the data or credentials.
4. Load the CSV with pandas and confirm it has the expected columns: `Time`, `V1`–`V28`, `Amount`, and `Class`.
5. Check the dimensions and fraud count against the expected scale: 284,807 transactions and 492 fraud cases (about 0.172%). Treat these as verification expectations; record any discrepancy rather than silently assuming the data matches.
6. Record the source, expected schema, and any download/date notes in the project documentation.

**Checkpoint:** The local file loads and its columns, dimensions, and target counts are documented.

## Step 4 — Audit and explore the data

1. Check column types, missing values, duplicate rows, ranges, and class counts.
2. Summarize the class imbalance and inspect `Amount` and selected feature distributions.
3. Create plots that help explain the data, including the class imbalance and selected feature/fraud comparisons.
4. Write down what the anonymized variables and the dataset's historical, two-day observation period mean for interpretation.
5. Create one reproducible stratified split, using a fixed random seed and approximately 70% train, 15% validation, and 15% test.
6. Store the split indices or the exact reproducible split code. Keep the test data set aside; do not use it to inspect model performance or make decisions.

**Checkpoint:** The data-quality summary, exploratory plots, and reproducible split are saved.

## Step 5 — Establish the evaluation protocol

Before modeling, define how every method will be compared:

1. Fit scalers, statistical reference values, and models on training data only. Reuse fitted transformations for validation and test data.
2. Do not give fraud labels to Z-score, IQR, Isolation Forest, or autoencoder training. Labels may be used to evaluate their predictions.
3. Train the autoencoder only on legitimate transactions from the training split.
4. Train the Random Forest with training labels and class weighting. Identify it clearly as a supervised benchmark, not an unsupervised detector.
5. Use validation data to select operating thresholds and model settings. Record the chosen threshold and the reason for choosing it.
6. Do not use accuracy as the main measure. Report precision, recall, F1, PR-AUC, false-positive rate, false-positive count, and confusion matrices. Accuracy may be included as a supplement.
7. Record training and scoring time where practical.

**Checkpoint:** The split, seed, metrics, and threshold-selection procedure are fixed before the final test evaluation.

## Step 6 — Build the statistical baselines

1. Calculate per-feature Z-score and IQR statistics using training data only.
2. Define a clear, documented way to combine feature-level flags or scores into one transaction-level anomaly score for each method.
3. Apply the training-fitted reference values to the validation data.
4. Compare validation precision-recall behavior and select operating thresholds on validation data.
5. Record validation metrics, assumptions, and any limitations of these simple feature-wise rules.

**Checkpoint:** Both baselines produce transaction-level scores and validation results using training-only reference statistics.

## Step 7 — Train and assess Isolation Forest

1. Fit scikit-learn's Isolation Forest on training features without fraud labels.
2. Generate anomaly scores for validation transactions.
3. Choose an operating threshold using validation labels and the agreed evaluation procedure.
4. Compare its validation results with the statistical baselines at comparable operating points.
5. Record the random seed and model settings needed to reproduce the experiment.

**Checkpoint:** Isolation Forest results are reproducible and added to the validation comparison.

## Step 8 — Train and assess the supervised Random Forest

1. Train a modest scikit-learn Random Forest using training features and labels, with class weighting.
2. Tune only with training and validation data.
3. Use validation results to choose the operating threshold or settings.
4. Record the validation metrics and explain that this model had access to fraud labels during training, unlike the unsupervised detectors.

**Checkpoint:** The supervised benchmark has validation results and a clear statement of its different training assumption.

## Step 9 — Train and assess the autoencoder

1. Fit feature-scaling transformations on training data only.
2. Implement a small, fully connected PyTorch encoder/decoder.
3. Train it using only legitimate transactions from the training split.
4. Use reconstruction error as its anomaly score.
5. Apply the fitted scaler and model to validation data; select a threshold using validation results.
6. Record the architecture, training settings, random seed, and validation performance. Keep the architecture and tuning modest.

**Checkpoint:** The autoencoder experiment can be reproduced and its validation threshold is documented.

## Step 10 — Build the hybrid and freeze the comparison

1. Normalize the statistical, Isolation Forest, and autoencoder anomaly scores without using test data.
2. Combine the normalized statistical and unsupervised scores with the proposal-aligned equal-weight hybrid.
3. Do not add learned weights or another hybrid variant.
4. Compare the hybrid with all other methods on validation data.
5. Freeze the methods, settings, score normalization, thresholds, and final evaluation code. Record these choices before opening the test results.

**Checkpoint:** A complete validation comparison exists, and all test-time decisions are fixed.

## Step 11 — Run the final test evaluation

1. Run each frozen method on the untouched test split once.
2. Apply only transformations fitted on training data and thresholds chosen with validation data.
3. Produce a final comparison table, precision-recall curves, confusion matrices, and false-alert counts.
4. Report precision, recall, F1, PR-AUC, false-positive rate and count; include accuracy only as a supplement.
5. Include training/scoring time where practical.
6. Do not adjust thresholds or model settings based on test results. If a method is changed, treat that as a new experiment and preserve the original test evaluation rather than tuning against it.

**Checkpoint:** Final results come from the frozen evaluation protocol and the test set was not used for model selection.

## Step 12 — Write, reproduce, and present

1. Explain the goal, dataset, preprocessing, split, and each method clearly.
2. Compare detection quality, false-alert burden, interpretability, and computational cost.
3. Discuss class imbalance, uncertainty from the small number of fraud cases, anonymized features, and the short historical observation period.
4. Avoid claiming that results demonstrate effectiveness on current real-world bank transactions.
5. Include limitations and future work, and be transparent about failed experiments or deviations from the plan.
6. Restart the notebook kernel and run the notebooks in the documented order from the setup instructions.
7. Check that the report, figures, tables, code, and setup documentation agree and can be reproduced without committing the dataset or credentials.

**Checkpoint:** The final report/presentation and reproducible project materials are ready.

## Final deliverables

- Reproducible Python/Jupyter project with concise setup and dataset instructions.
- Data-quality summary, exploratory analysis, and saved figures.
- Implementations of Z-score, IQR, Isolation Forest, class-weighted Random Forest, and the PyTorch autoencoder.
- One equal-weight statistical-plus-unsupervised hybrid score.
- Validation-based threshold selection and one final evaluation on the untouched test set.
- Comparison tables and plots, with rare-event metrics and false-alert counts.
- A report/presentation discussing results, assumptions, interpretability, computational cost, uncertainty, limitations, and future work.
