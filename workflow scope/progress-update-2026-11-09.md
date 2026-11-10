# Progress Update — November 9, 2026

## Progress since the last update

Based on the repository history available for today, two implementation commits were made:

- Added Z-score and IQR statistical baselines, training-reference statistics, validation threshold selection, and a reusable evaluation script. Saved validation settings and statistical-baseline test results are present in `results/`.
- Implemented the Isolation Forest notebook and added its evaluation logic to the shared evaluation code.
- Updated the final test-evaluation notebook and data-audit notebook to support the current workflow.

The statistical-baseline implementation and its saved test results are in place. Isolation Forest has an implementation and evaluation logic, but the project-wide comparison is not complete.

## Work in progress and remaining work

- Implement and evaluate the Random Forest benchmark and autoencoder.
- Build the hybrid and validation-comparison notebook after the model scores are available.
- Complete the cross-model comparison, freeze settings using validation data, and then evaluate the remaining finalized methods on the untouched test split. Existing statistical-baseline test results should not be used to retune that method.
- Review notebook execution order, reproducibility, and final report materials.

## Challenges and response

- The Random Forest, autoencoder, and hybrid notebooks are currently empty placeholders. Implement these in the planned order, reusing the existing fixed split and evaluation conventions.
- The history records both commits from today under Chukwuyem Ayeh; it does not verify how work was divided among three members. The member sections below are a suggested reporting allocation by implementation area, not confirmed individual authorship. Confirm ownership with the team before presenting them as individual contributions.
- Final test evaluation must remain separate from model/threshold selection. Complete model decisions with validation data first, then preserve the test split for final reporting.

## Plan for the next two weeks

**November 10–16**

1. Implement the class-weighted Random Forest and autoencoder experiments.
2. Select thresholds/settings using validation data only and save reproducible metrics.
3. Check that the Isolation Forest evaluation can be run in the documented notebook workflow.

**November 17–23**

1. Implement the equal-weight hybrid and validation comparison.
2. Freeze model settings and thresholds, then run the remaining final test evaluations once.
3. Assemble comparison tables/figures and document limitations, results, and each member's verified contribution.

## Member contribution sections

The following split separates today's implementation work for reporting. Individual ownership is unverified in the available commit history.

### Member 1

**Implementation area: statistical baselines.** Added the Z-score and IQR baseline workflow, training-set reference statistics, validation-based threshold selection, and saved statistical-baseline evaluation outputs.

### Member 2

**Implementation area: Isolation Forest.** Added the unsupervised Isolation Forest notebook workflow and evaluation logic, extending the project beyond the statistical methods.

### Member 3

**Implementation area: evaluation workflow.** Updated the shared evaluation logic and final test-evaluation notebook to support the methods and saved results available so far. The broader cross-model final evaluation remains to be completed after the remaining models and hybrid are ready.
