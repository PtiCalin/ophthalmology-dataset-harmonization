# Input Data Documentation

This guide explains how to place input files so the harmonization notebooks and pipelines can run consistently.

## Where to put files

- Use `input/raw/<dataset_name>/` for untouched downloads (CSV, Parquet, ZIP, etc.).
- Use `input/processed/<dataset_name>/` for any pre-cleaned versions you want to feed into the loader.

## Naming suggestions

- Keep the original filename when possible (helps provenance).
- If renaming, prefer `source-variant-version.ext` (e.g., `retina-clinicA-v1.csv`).

## Referencing paths in notebooks

- Build paths relative to the project root: `Path('input/raw/<dataset>/file.csv')`.
- The verification/export cells now create `output/` automatically if missing.

## Reproducibility checklist

- Record the source (URL/Kaggle competition or dataset ID) and download date.
- Note any manual preprocessing performed before running the harmonizer.
- Add new sources and notes here to keep the team aligned.
