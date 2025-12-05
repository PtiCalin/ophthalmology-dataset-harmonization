# Ophthalmology Dataset Harmonization

## Project Files

### Documentation
- README.md - Project overview and getting started guide
- CONTRIBUTING.md - Guidelines for contributing to the project

### Source Code
- src/
  - __init__.py - Package initialization
  - schema.py - Canonical schema definitions
  - rules.py - Harmonization rules and inference logic
  - loaders/
    - __init__.py - Loaders module initialization
    - universal_loader.py - Universal dataset loader
  - pipeline/
    - __init__.py - Pipeline module initialization
    - harmonize_all.py - Main harmonization orchestration

### Notebooks
- notebooks/
  - dataset_harmonization.ipynb - Complete working example

### Configuration
- pyproject.toml - Project metadata and dependencies (PEP 518)
- requirements.txt - Python dependencies
- requirements-dev.txt - Development dependencies
- .gitignore - Git ignore patterns

### Output
- output/ - Directory for exported harmonized datasets
  - harmonized.parquet - Main output (Parquet format)
  - harmonized.csv - Alternative export (CSV format)

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the notebook:**
   ```bash
   jupyter notebook notebooks/dataset_harmonization.ipynb
   ```

3. **Output:** Check `output/harmonized.parquet` for the merged dataset

## Development Setup

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## Project Structure Overview

```
ophthalmology-dataset-harmonization/
├── README.md                          # Main documentation
├── pyproject.toml                     # Project configuration
├── requirements.txt                   # Core dependencies
├── requirements-dev.txt               # Development dependencies
├── .gitignore                         # Git ignore file
├── notebooks/
│   └── dataset_harmonization.ipynb   # Main executable notebook
├── src/
│   ├── __init__.py
│   ├── schema.py                     # Canonical schema
│   ├── rules.py                      # Harmonization rules
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── universal_loader.py       # Universal loader
│   └── pipeline/
│       ├── __init__.py
│       └── harmonize_all.py          # Pipeline orchestration
└── output/
    └── (harmonized datasets exported here)
```

## License

MIT License - See README.md for details
