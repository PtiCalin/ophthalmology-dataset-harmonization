# Documentation Index

This index is the main map for understanding and extending the ophthalmology dataset harmonization workspace.

## Read By Goal

### Understand the project quickly

1. README.md
2. docs/METHODOLOGY.md
3. docs/PROJECT_FILES.md

### Add or register a new dataset

1. docs/inputs.md
2. docs/AUTOMATED_DISCOVERY_README.md
3. docs/DATA-PROCESSING/SCHEMA.md
4. docs/DATA-PROCESSING/RULES.md

### Extend harmonization logic

1. docs/DATA-PROCESSING/RULES.md
2. docs/DATA-PROCESSING/CODEBOOK.md
3. docs/DATA-PROCESSING/SCHEMA.md
4. test/test_expanded_rules.py

### Validate quality and consistency

1. docs/METHODOLOGY.md
2. docs/DATA-PROCESSING/CODEBOOK.md
3. test/test_robust_schema.py
4. test/test_notebook.py

## Read By Role

### Researcher

- README.md
- docs/METHODOLOGY.md
- docs/DATA-PROCESSING/RULES.md
- docs/DATA-PROCESSING/SCHEMA.md

### Data Engineer

- docs/inputs.md
- docs/DATA-PROCESSING/SCHEMA.md
- docs/DATA-PROCESSING/CODEBOOK.md
- docs/PROJECT_FILES.md

### Maintainer

- docs/PROJECT_FILES.md
- docs/AUTOMATED_DISCOVERY_README.md
- .claude/CLAUDE.md

## Documentation Inventory

- README.md: project purpose, scope, outcomes, capacities, discoveries.
- docs/METHODOLOGY.md: conceptual framework and process lifecycle.
- docs/PROJECT_FILES.md: source-of-truth file map and doc responsibilities.
- docs/inputs.md: manual input onboarding and provenance process.
- docs/AUTOMATED_DISCOVERY_README.md: automation for discovering new datasets.
- docs/DATA-PROCESSING/SCHEMA.md: canonical schema definitions.
- docs/DATA-PROCESSING/RULES.md: harmonization rules and inference logic.
- docs/DATA-PROCESSING/CODEBOOK.md: enumerations, coding reference, validation semantics.

## Core Topics To Files

| Topic | Primary File |
|------|--------------|
| Project purpose and outcomes | README.md |
| Methodological choices | docs/METHODOLOGY.md |
| Schema design | docs/DATA-PROCESSING/SCHEMA.md |
| Rule engine behavior | docs/DATA-PROCESSING/RULES.md |
| Value dictionaries and scales | docs/DATA-PROCESSING/CODEBOOK.md |
| Dataset onboarding | docs/inputs.md |
| Automated discovery pipeline | docs/AUTOMATED_DISCOVERY_README.md |
| Documentation governance | docs/PROJECT_FILES.md |
| AI assistant operating context | .claude/CLAUDE.md |

## Maintenance Rule

When changing project behavior, update at least:

1. The relevant deep technical file in docs/DATA-PROCESSING/.
2. README.md if user-visible scope or outcomes changed.
3. docs/PROJECT_FILES.md if documentation ownership or structure changed.
