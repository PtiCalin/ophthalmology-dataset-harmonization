# Automated Dataset Discovery

This document describes the automated workflow for discovering ophthalmology datasets and scaffolding the documentation required for integration.

## Purpose

Automated discovery accelerates intake by:

- Finding potentially relevant ophthalmology datasets.
- Creating standardized folder scaffolds and documentation placeholders.
- Reducing manual setup overhead for large-scale dataset curation.

## Scope and Boundaries

Automation proposes candidates and scaffolds structure. It does not replace clinical or methodological review.

Required human checkpoints:

1. Verify relevance and licensing.
2. Validate field semantics against codebook assumptions.
3. Confirm integration notes before running full harmonization.

## Main Scripts

Located in src/pipeline:

- run_discovery.py
- auto_discover_datasets.py
- enhanced_discovery.py
- simple_discovery.py
- config.py

## Typical Flow

1. Run discovery to identify candidate datasets.
2. Filter candidates using ophthalmology-focused criteria.
3. Generate per-dataset scaffold docs and raw/ directories.
4. Register newly discovered datasets for manual review.
5. Complete human review before integration into harmonization runs.

## Configuration

Tune discovery behavior in src/pipeline/config.py.

Common controls include:

- Search keywords.
- Include/exclude filters.
- Output folder naming conventions.
- Template defaults for generated docs.

## Usage Examples

From repository root:

```bash
python src/pipeline/run_discovery.py
python src/pipeline/run_discovery.py --dry-run
```

If script entry points differ in your branch, align commands with the script available under src/pipeline.

## Generated Artifacts

For each candidate dataset, discovery should create:

- DESCRIPTION.md
- CODEBOOK.md
- INTEGRATION.md
- raw/

These artifacts are drafts and must be reviewed.

## Scheduling

Automated discovery can be scheduled (Task Scheduler/Cron/CI), but production adoption should remain review-gated.

## Troubleshooting

- No datasets found: verify keywords and network access.
- API authentication issues: verify token env vars.
- Import/path errors: run from repository root and verify module paths.
- Inconsistent output folders: verify slug-generation logic in config.

## Security and Governance

- Keep API tokens in environment variables.
- Never commit secrets in scripts or docs.
- Treat generated metadata as untrusted until reviewed.
