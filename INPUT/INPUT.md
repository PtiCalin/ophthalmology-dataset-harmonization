# Input Dataset Documentation

## Dataset Inclusion Process

To include a new dataset in the harmonization pipeline:

### Step 1: Create Dataset Folder Structure

```txt
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

### Documentation Complete Datasets

- **Retinal Disease Detection Dataset** (`retinal-disease-detection-dataset/`)
  - Multi-class retinal disease classification with clinical annotations
  - Fundus images with diagnosis categories (DR, Glaucoma, AMD, etc.)
  - Includes clinical measurements and severity assessments
  - Status: Documentation complete, loader development pending

- **Retinal OCT Images** (`retinal-oct-images/`)
  - Optical coherence tomography scans for CNV, DME, and DRUSEN classification
  - 3D volume data with B-scan slices
  - Research dataset for automated OCT analysis
  - Status: Documentation complete, custom loader developed and validated

- **Retina Dataset** (`retina-dataset/`)
  - General retinal fundus images with multiple pathology classifications
  - Comprehensive collection for retinal disease research
  - Includes normal and pathological cases
  - Status: Documentation complete, loader development pending

- **Retinal Fundus Images** (`retinal-fundus-images/`)
  - Diabetic retinopathy severity classification dataset
  - Fundus photographs graded by DR severity levels
  - Designed for automated screening systems
  - Status: Documentation complete, loader development pending

- **Retinal Image Dataset for Early Detection of Alzheimer's** (`retinal-image-dataset-for-early-detection-of-alzheimers/`)
  - Fundus images for Alzheimer's disease biomarker research
  - Links retinal vascular changes to cognitive assessments
  - Multi-disciplinary neurology-ophthalmology dataset
  - Status: Documentation complete, custom loader developed and validated

### Documentation Pending Datasets

- **Retinal Images for Diabetic Retinopathy** (`retinal-images-for-diabetic-retinopathy/`)
  - Focused DR detection and grading dataset
  - Status: Documentation pending

- **Retinal Vessel Segmentation** (`retinal-vessel-segmentation/`)
  - Vessel network analysis and segmentation
  - Status: Documentation pending

- **Retinal Lesions** (`retinal-lesions/`)
  - Lesion detection and classification dataset
  - Status: Documentation pending

- **Retinal Disease Classification** (`retinal-disease-classification/`)
  - Multi-class disease classification
  - Status: Documentation pending

- **Retinal OCT Dataset** (`retinal-oct-dataset/`)
  - Additional OCT imaging dataset
  - Status: Documentation pending

- **Retinal Fundus Images for Glaucoma** (`retinal-fundus-images-for-glaucoma/`)
  - Glaucoma-specific fundus image collection
  - Status: Documentation pending

- **Retinal Images for Optic Disc** (`retinal-images-for-optic-disc/`)
  - Optic disc analysis and segmentation
  - Status: Documentation pending

- **Retinal Blood Vessel Segmentation** (`retinal-blood-vessel-segmentation/`)
  - Blood vessel analysis dataset
  - Status: Documentation pending

- **Retinal Image Analysis for Diabetes Detection** (`retinal-image-analysis-for-diabetes-detection/`)
  - Diabetes screening through retinal imaging
  - Status: Documentation pending

- **Retinal Fundus Images for AMD** (`retinal-fundus-images-for-amd/`)
  - Age-related macular degeneration dataset
  - Status: Documentation pending

- **Retinal Images for Hypertensive Retinopathy** (`retinal-images-for-hypertensive-retinopathy/`)
  - Hypertensive vascular changes in retina
  - Status: Documentation pending

- **Retinal Fundus Images for Diabetic Retinopathy** (`retinal-fundus-images-for-diabetic-retinopathy/`)
  - Additional DR fundus image dataset
  - Status: Documentation pending

- **Retinal OCT Images for AMD** (`retinal-oct-images-for-amd/`)
  - OCT imaging for AMD diagnosis
  - Status: Documentation pending

- **Retinal Fundus Images for Vessel Segmentation** (`retinal-fundus-images-for-vessel-segmentation/`)
  - Vessel segmentation training dataset
  - Status: Documentation pending

- **Retinal Images for Macular Degeneration** (`retinal-images-for-macular-degeneration/`)
  - Macular degeneration imaging dataset
  - Status: Documentation pending

- **Retinal Fundus Images for Cataract Detection** (`retinal-fundus-images-for-cataract-detection/`)
  - Cataract assessment through fundus imaging
  - Status: Documentation pending

- **Retinal Images for Retinopathy of Prematurity** (`retinal-images-for-retinopathy-of-prematurity/`)
  - Pediatric retinal disease dataset
  - Status: Documentation pending

### Dataset Template

Use the `refuge2-dataset/` folder as a template for new dataset integrations. 

