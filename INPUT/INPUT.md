# Input Dataset Documentation

## Dataset Inclusion Process

To include a new dataset in the harmonization pipeline:

### Step 1: Create Dataset Folder Structure
```
input/
└── [dataset-name]/
    ├── DESCRIPTION.md     # Dataset overview and clinical context
    ├── CODEBOOK.md        # Field definitions and data dictionary
    ├── INTEGRATION.md     # Loading and harmonization instructions
    └── raw/              # Raw dataset files (optional)
```

### Step 2: Document the Dataset
1. **DESCRIPTION.md**: Provide clinical context, data source, and intended use
2. **CODEBOOK.md**: Document all fields, data types, validation rules, and enumerations
3. **INTEGRATION.md**: Detail loading procedures, column mappings, and harmonization rules

### Step 3: Implement Loader (if needed)
- Extend `UniversalLoader` class for custom loading logic
- Add dataset-specific validation and transformation rules
- Update pipeline configuration

### Step 4: Register Dataset
Add the dataset to the datasources list below and update any relevant configuration files.

## Datasources

### Active Datasets
- **REFUGE2 Dataset** (`refuge2-dataset/`)
  - Glaucoma detection dataset with fundus images
  - 1,000+ annotated retinal images
  - Includes cup-disc ratio measurements
  - Status: Integration complete, ready for harmonization

### Planned Datasets
- **Ocular Disease Dataset** - Multi-pathology retinal image collection
- **Retinal Disease Detection** - Comprehensive disease classification dataset
- **Additional Kaggle datasets** - As identified in research phase

### Dataset Template
Use the `refuge2-dataset/` folder as a template for new dataset integrations. 

