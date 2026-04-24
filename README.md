# Ophthalmology Dataset Harmonization

A local-first Python workspace for transforming heterogeneous ophthalmology datasets into a consistent, analysis-ready structure.

## Purpose

This repository exists to solve a recurring research problem: ophthalmology datasets are highly inconsistent across naming, labels, severity scales, modalities, and metadata quality.

The project standardizes those differences into one canonical schema and one consistent rule system so data can be reliably compared, validated, and reused across studies.

## What This Workspace Enables

- Cross-dataset harmonization of retinal and ophthalmic imaging data.
- Standardized diagnosis normalization and severity mapping.
- Reproducible data processing with transparent, rule-based logic.
- Better downstream readiness for analytics, machine learning, and registry-style studies.

## Core Process

1. Discover or ingest input datasets under src/INPUT/.
2. Load data through the loader layer in src/loaders/.
3. Standardize structure using the canonical schema in src/schema.py.
4. Apply harmonization and inference rules from src/rules.py.
5. Validate outputs and quality flags in pipeline/testing workflows.
6. Export harmonized artifacts to src/OUTPUT/ for analysis.

## Outcomes

Current documentation and codebase design target the following outcomes:

- One shared schema vocabulary across source datasets.
- Consistent diagnosis category mapping and severity interpretation.
- Cleaner provenance and input tracking.
- Reduced ambiguity when extending pipelines or onboarding new datasets.

## Capacities

The workspace is designed to support:

- Multi-modality ophthalmology data harmonization.
- Clinical finding extraction and normalization.
- Confidence-aware inference for noisy labels.
- Dataset onboarding at scale using automated discovery utilities.
- Rule and schema extension without rewriting the full pipeline.

See detailed references:

- docs/DATA-PROCESSING/SCHEMA.md
- docs/DATA-PROCESSING/RULES.md
- docs/DATA-PROCESSING/CODEBOOK.md

## Discoveries Enabled

This project structure helps surface discoveries such as:

- Which diagnosis labels collapse into equivalent clinical categories.
- Where datasets disagree semantically despite similar field names.
- Which imaging modalities and metadata patterns create frequent validation failures.
- How much harmonization confidence varies by source and data quality.

## Repository Structure

```txt
ophthalmology-dataset-harmonization/
├── README.md
├── docs/
│   ├── INDEX.md
│   ├── METHODOLOGY.md
│   ├── PROJECT_FILES.md
│   ├── inputs.md
│   ├── AUTOMATED_DISCOVERY_README.md
│   └── DATA-PROCESSING/
│       ├── SCHEMA.md
│       ├── RULES.md
│       └── CODEBOOK.md
├── src/
│   ├── schema.py
│   ├── rules.py
│   ├── loaders/
│   ├── pipeline/
│   ├── INPUT/
│   └── OUTPUT/
└── test/
```

## Documentation Entry Points

- docs/INDEX.md: start here for role-based reading paths.
- docs/METHODOLOGY.md: conceptual and methodological framework.
- docs/PROJECT_FILES.md: authoritative map of maintained documentation.
- docs/inputs.md: how to structure and register incoming datasets.
- docs/AUTOMATED_DISCOVERY_README.md: automated dataset discovery workflow.

## Quick Validation Commands

```bash
python -m pytest test/test_robust_schema.py -v
python -m pytest test/test_expanded_rules.py -v
```

## Status

Documentation and structure have been refactored to remove merge conflicts and align the narrative with the actual repository purpose: ophthalmology dataset harmonization.
