🏥 Ophthalmology Multi-Dataset Harmonization

A unified, scalable pipeline for integrating retinal and ophthalmic imaging datasets

This project builds a Python-based harmonization engine that consolidates dozens of heterogeneous ophthalmology datasets from Kaggle into a single clean, analysis-ready dataset.

It is built for:

- ML practitioners preparing training datasets
- Researchers comparing disease markers across modalities
- Students learning how to build real-world data pipelines
- Anyone needing standardized ophthalmic image metadata

Everything runs inside a Jupyter notebook and favors clarity, reproducibility, and teaching value.

## 🎯 Objectives

- Load multiple ophthalmology datasets with inconsistent formats.
- Standardize them into a canonical schema.
- Apply documented harmonization rules.
- Export a clean, merged dataset ready for modeling.
- Provide an educational, well-commented codebase.

All code is written in Python using simple, dependable dependencies.

## 📦 Features

### ✔ Unified Canonical Schema

Every dataset is mapped into a shared structure including:

- image identifiers
- modality (Fundus, OCT, Slit-Lamp, etc.)
- laterality inference (left/right)
- diagnosis (raw + normalized category)
- metadata when available (age, sex, resolution)
- fallback extra_json for anything non-standard

### ✔ Modular Loader Architecture

Each dataset is handled through a universal loader that:

- auto-detects important columns
- infers metadata when possible
- converts rows into the canonical schema

Adding a new dataset requires only one new line in the registry.

### ✔ Harmonization Rules

The pipeline currently implements:

- label keyword mapping
- automatic laterality inference
- modality inference based on dataset name
- metadata extraction fallback
- safe JSON storage of non-mapped fields

Rules are documented and easy to extend.

### ✔ Clean Export

- Produces a unified `harmonized.parquet` file.
- Suitable for ML pipelines, DuckDB, Spark, or pandas.

## 📁 Project Structure

```
notebooks/
    dataset_harmonization.ipynb   # Main executable notebook

src/
    schema.py                     # Canonical schema definitions
    rules.py                      # Harmonization rules (diagnosis, modality, etc.)
    loaders/
        universal_loader.py       # Universal loading engine
    pipeline/
        harmonize_all.py          # Full harmonization orchestration

output/
    harmonized.parquet            # Final merged dataset
```

The folder layout is intentionally simple and beginner-friendly.

## 🧠 Datasets Included

The pipeline integrates ophthalmic datasets across multiple modalities, including:

- Cataract Classification Dataset in DS
- Cornea in Diabetes
- Diabetic Retinopathy Detection
- Eye Image Dataset
- Fundus Images
- Macular Degeneration
- Messidor2 DR Grades
- OCTDL (multiple variants)
- Refuge2
- Retinal Disease Detection
- Retinoblastoma Cells
- and others…

Each dataset is listed in a central registry and can be toggled on/off.

## 📘 How It Works

1. **Load each dataset with the universal loader**
   - The loader auto-detects common column patterns and normalizes metadata.

2. **Apply harmonization rules**
   - Diagnoses, modality, and laterality are standardized.

3. **Merge into a single dataframe**
   - All datasets share the same canonical schema.

4. **Export**
   - Data is written to `harmonized.parquet`.

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install kagglehub pandas numpy pyarrow fastparquet
```

### 2. Run the notebook

Open `dataset_harmonization.ipynb` and execute all cells.

### 3. Output

The harmonized dataset will be saved under:

```
output/harmonized.parquet
```

## ❗ Why Harmonization Matters

Ophthalmology datasets vary widely in:

- annotation style
- file naming conventions
- diagnosis formats
- available metadata
- imaging modality

A raw merge is impossible. A harmonized dataset unlocks reproducibility, better model generalization, and cross-dataset research.

This project gives you a dependable baseline to build from.

## 🔭 Roadmap

Planned improvements:

- expand diagnosis taxonomy
- integrate pixel metadata extraction
- image hashing to detect duplicates
- dataset-balanced train/validation/test splitting
- detailed dataset profiling and QC reports
- refined device/quality metadata inference

## 🤝 Contributions

Contributions are welcome. You can open issues for:

- dataset loading problems
- mapping inconsistencies
- new harmonization rules
- performance improvements

## 📜 License

MIT License. Use freely for research and education.

## 🙌 Acknowledgments

This project builds on the incredible work of dataset authors across the ophthalmology community. Their contributions make large-scale research possible.
