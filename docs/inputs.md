# Input Data Guide

This guide defines how to onboard datasets into the harmonization workspace safely and reproducibly.

## Input Location Convention

Use src/INPUT as the controlled input area.

Recommended structure:

```txt
src/INPUT/
  <dataset-slug>/
    raw/
    DESCRIPTION.md
    CODEBOOK.md
    INTEGRATION.md
```

## Onboarding Workflow

1. Create a dataset folder using a stable slug.
2. Place untouched source files in raw/.
3. Add DESCRIPTION.md with source, clinical context, and license.
4. Add CODEBOOK.md with known fields and value semantics.
5. Add INTEGRATION.md with loader assumptions and mapping notes.
6. Register dataset metadata in src/INPUT/INPUT.md or registry files when applicable.

## Provenance Requirements

For every onboarded dataset, record:

- Source URL or Kaggle reference.
- Download date.
- Version/snapshot information.
- License and usage constraints.
- Any manual pre-processing performed before harmonization.

## Naming Guidance

- Keep original filenames whenever possible.
- If renamed, use deterministic names that preserve source context.
- Avoid ambiguous ad hoc suffixes.

## Validation Expectations Before Processing

- Files are readable and uncorrupted.
- Expected columns are documented.
- Labels and coding scales are identified.
- Missing-value patterns are noted.

## Common Failure Modes

- Mixing raw and transformed files in the same folder.
- Missing provenance metadata.
- Undocumented manual cleaning steps.
- Inconsistent dataset slugs across docs and paths.

## Relationship To Automation

If using automated discovery, use docs/AUTOMATED_DISCOVERY_README.md.
Manual review is still required before data is treated as production-ready input.
