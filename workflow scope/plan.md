# Eight-Week Project Plan

## Project and scope

**Project:** Statistical Anomaly Detection System for Fraudulent Banking Transactions: A Comparative Study of Statistical Methods, Machine Learning, and Deep Learning.

This plan follows the **Updated project proposal** and is sized for a second-year university project. The goal is a careful, reproducible comparison—not a production banking system or a new deep-learning architecture. Use one dataset, one fixed experiment protocol, and small, understandable models.

The core comparison is:

- Statistical baselines: Z-score and IQR.
- Unsupervised anomaly detectors: Isolation Forest and a small autoencoder.
- Supervised benchmark: class-weighted Random Forest, clearly identified as using fraud labels.
- Hybrid: a simple, equal-weight combination of normalized statistical and unsupervised anomaly scores.

GANs, diffusion models, graph models, synthetic data generation, a second dataset, and production deployment are out of scope. Do not add optional experiments; complete the core comparison and report first.

## Dataset

Use only the proposal's **European credit-card fraud dataset** from Kaggle:

- Source: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- File: `creditcard.csv`
- Expected scale: 284,807 transactions, 492 fraud cases (approximately 0.172%).
- Features: `Time`, anonymized `V1`–`V28`, `Amount`; target `Class`.

Download from the Kaggle dataset page after reviewing its access terms. If using the Kaggle API, keep its credentials outside the project and never commit them. Keep the downloaded CSV out of version control; document its source and expected schema instead. Treat the dataset as a historical benchmark, not evidence of performance on current bank transactions.

## Tools and setup

### Recommended tools

- Python 3 and a project-local virtual environment.
- Jupyter Notebook for documented experiments.
- Pandas and NumPy for data inspection and transformations.
- Matplotlib and Seaborn for plots.
- scikit-learn for preprocessing, statistical utilities, Isolation Forest, Random Forest, and evaluation.
- PyTorch for the small feedforward autoencoder.
- Git for source and notebook version history, if available to the group.

Use CPU-compatible packages as the baseline; a GPU is not required. Keep the analysis in a small number of clearly named notebooks or Python modules rather than building an application.

### Initial setup procedure (Windows PowerShell)

1. Install a supported Python 3 release and confirm `py --version` works.
2. Create and activate a project-local environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```

3. Install `jupyter`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, and `torch` using their standard installation instructions. Verify imports and record the successful package versions in a dependency file (for example, `requirements.txt`).
4. Create a simple project layout, for example:

   ```text
   data/           # downloaded data; exclude the CSV from version control
   notebooks/      # EDA and model experiments
   src/            # shared preprocessing, scoring, and evaluation helpers
   results/        # tables and figures
   report/         # report draft and final report
   ```

5. Add a README with setup, dataset download instructions, notebook run order, and the random seed. Do not place Kaggle tokens or other credentials in the README or notebooks.
6. Open Jupyter from the activated environment, select its Python kernel, and run a small import/data-loading check before beginning the experiments.

### Experimental safeguards

- Fix and record random seeds and one stratified train/validation/test split (a practical starting point is 70%/15%/15%).
- Fit scalers, statistical reference values, and models using training data only. Reuse those fitted transformations on validation and test data.
- Keep the test split untouched until the final comparison. Use validation data—not test results—to choose thresholds and model settings.
- Do not pass fraud labels to Z-score, IQR, Isolation Forest, or autoencoder training. Use labels to assess their predictions.
- Train the autoencoder only on legitimate transactions from the training split. Train the Random Forest on training labels and describe it as a supervised benchmark.
- Do not use accuracy as the principal measure. Report precision, recall, F1, PR-AUC, false-positive rate and count, and confusion matrices; report accuracy only as a supplement. Include training/scoring time where practical.

## Weekly plan

| Week | Focus and activities | End-of-week deliverable |
|---|---|---|
| **1 — Setup and reproducibility** | Confirm team responsibilities and research questions against the proposal. Set up Python, the virtual environment, Jupyter, and the agreed packages. Download the single Kaggle dataset securely; establish the project layout, dependency record, README, and fixed random seed. | A working notebook kernel, documented setup, and verified dataset file/schema. |
| **2 — Data audit and EDA** | Check dimensions, column types, missing values, duplicates, ranges, and fraud prevalence. Plot class imbalance, `Amount` and selected feature distributions, and selected feature/fraud comparisons. Create and record a stratified train/validation/test split. Explain dataset limitations. | Data dictionary/quality summary, EDA figures, and saved split indices or reproducible split code. |
| **3 — Statistical baselines** | Implement per-feature Z-score and IQR scores and an understandable rule for combining feature flags into transaction-level scores. Fit reference statistics on training data only. Compare validation precision-recall behavior and select operating thresholds using validation data. | Working Z-score and IQR baselines, validation metrics, and a brief explanation of their assumptions. |
| **4 — Isolation Forest** | Fit a scikit-learn Isolation Forest without labels. Inspect anomaly scores and use validation data to select an operating threshold. Compare with the statistical baselines at comparable operating points. | Reproducible Isolation Forest results and updated validation comparison. |
| **5 — Supervised Random Forest** | Train a modest scikit-learn Random Forest with class weighting. Tune only on training/validation data; do not use the test set. State explicitly that this benchmark has access to labels and is not directly equivalent to unsupervised detection. | Supervised benchmark, validation results, and clear documentation of its training assumption. |
| **6 — PyTorch autoencoder** | Scale features with training-fitted transformations. Implement a small fully connected encoder/decoder with a reconstruction-error score. Train using legitimate training transactions only; use validation results to set a threshold. Keep the architecture and tuning modest. | Trained/reproducible autoencoder experiment, validation results, and a short description of architecture and threshold choice. |
| **7 — Hybrid and comparison preparation** | Normalize statistical, Isolation Forest, and autoencoder anomaly scores without test-set information. Implement the proposal-aligned equal-weight hybrid; avoid extra learned weights or a second hybrid variant. Compare validation precision-recall behavior and prepare the final evaluation code and result tables. | Hybrid score and frozen model/threshold choices, plus a complete validation comparison. |
| **8 — Final evaluation and reporting** | Run the frozen methods once on the untouched test set. Produce the final comparison table, precision-recall curves, confusion matrices, and false-alert counts. Discuss performance, interpretability, computational cost, uncertainty from the small fraud count, and dataset limitations. Check that notebooks run from documented setup steps. | Final report/presentation, reproducible notebooks/code, figures and tables, and a limitations/future-work section. |

## Final expected outputs

1. A reproducible Python/Jupyter project and concise setup instructions.
2. Exploratory analysis of the one Kaggle dataset.
3. Implementations of Z-score, IQR, Isolation Forest, class-weighted Random Forest, and the PyTorch autoencoder.
4. A simple statistical-plus-unsupervised hybrid score.
5. Validation-based threshold selection and a final evaluation on an untouched test set using rare-event metrics.
6. A report comparing the methods and honestly discussing false alerts, interpretability, computational cost, class imbalance, and limits on generalization.

## Considerations for a second-year project

- Prefer clear baselines and defensible evaluation over complex tuning or a large number of models.
- Explain the distinction between anomaly detection trained without labels and the supervised Random Forest benchmark.
- A small number of fraud cases makes metric estimates uncertain; present the counts behind the metrics and avoid overstating small differences.
- The anonymized features and two-day 2013 observation period constrain interpretation. Do not claim operational banking effectiveness.
- If a setup or model proves too difficult, preserve the valid experiment protocol and simplify the implementation rather than adding a more advanced method.
