# Methodology

## Objective

Build a transparent, reproducible harmonization workflow that converts heterogeneous ophthalmology datasets into a shared schema and rule-consistent representation for research and analytical reuse.

## Why Harmonization Is Needed

Ophthalmology datasets often vary across:

- Label vocabulary and diagnosis naming.
- Severity scales and disease staging conventions.
- Imaging modality naming conventions.
- Metadata completeness and quality.
- Field semantics for similar column names.

Without harmonization, combining datasets can introduce silent semantic errors and biased analysis.

## Methodological Principles

1. Determinism over opacity: use explicit rules where possible.
2. Clinical interpretability: keep mappings auditable and reviewable.
3. Reproducibility: same input should produce the same normalized output.
4. Extensibility: new datasets should integrate without schema rewrites.
5. Safety: preserve provenance and avoid destructive input mutations.

## Process Lifecycle

### 1. Discovery and Intake

- Manual and automated discovery identify candidate datasets.
- Source metadata and provenance are captured at intake.
- Inputs are staged in src/INPUT with dataset-specific folders.

### 2. Structural Normalization

- Input data is loaded through loader components.
- Records are transformed into the canonical HarmonizedRecord shape.
- Nested objects preserve semantic grouping (clinical findings, patient data, acquisition, image metadata).

### 3. Semantic Harmonization

- Diagnosis text is normalized into standardized categories.
- Severity scales are mapped to consistent representations.
- Modality and laterality are inferred from metadata and text patterns.
- Confidence-aware transformations expose uncertain inferences.

### 4. Validation and Quality Controls

- Type and range checks enforce schema consistency.
- Cross-field checks prevent contradictory combinations.
- Quality flags and validation notes preserve auditability.
- Tests provide regression protection for schema and rules.

### 5. Output and Reuse

- Harmonized records are written to output artifacts.
- Outputs are designed for downstream analysis, model development, and documentation-driven review.

## Outcomes This Method Supports

- Cleaner cross-dataset comparison with reduced semantic drift.
- Better confidence in diagnosis and severity aggregation.
- More reliable input for machine learning experiments.
- Transparent documentation for peer review and reproducibility.

## Capacities

Current architecture supports:

- Rule-based normalization at scale across multiple datasets.
- Incremental extension of mappings and schema fields.
- Mixed quality input handling through validation and confidence flags.
- Operational automation for discovering and scaffolding new datasets.

## Discoveries Enabled

The methodology is designed to reveal:

- Vocabulary mismatches across ophthalmology datasets.
- Severity labeling inconsistencies and edge cases.
- Dataset-specific data quality failure patterns.
- Gaps where additional rule coverage is needed.

## Limits and Risks

- Rule-based systems can miss unseen phrasing patterns.
- Source dataset bias remains even after schema harmonization.
- Confidence scoring is informative but not equivalent to clinical adjudication.

## Continuous Improvement Loop

1. Run harmonization and validations.
2. Inspect warnings, low-confidence mappings, and failures.
3. Update rules/codebook/schema where justified.
4. Re-run tests.
5. Document changes in the relevant source-of-truth docs.
