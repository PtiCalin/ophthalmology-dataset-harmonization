# Input Data Staging

Use this folder to stage raw source datasets before running the harmonization pipeline.

## Recommended layout

- `input/raw/<dataset_name>/...` : exact files as downloaded (CSV/Parquet/ZIP).
- `input/processed/<dataset_name>/...` : optional pre-cleaned outputs you want to feed into the loader.

## Notes

- Keep original filenames when possible so provenance is clear.
- Large files are typically ignored by Git; verify `.gitignore` rules before committing.
- The notebook and pipeline expect paths relative to the project root (e.g., `input/raw/my_dataset/data.csv`).
- If you add new sources, document them in `docs/inputs.md` so others can reproduce the setup.
