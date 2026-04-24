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

- **Refuge2 And Refuge2Cross Dataset** (`refuge2-and-refuge2cross-dataset/`)
  - Ophthalmology dataset from ferencjuhsz
  - Status: Documentation auto-generated, manual review pending

- **Retinal Disease Detection** (`retinal-disease-detection/`)
  - Ophthalmology dataset from mohamedabdalkader
  - Status: Documentation auto-generated, manual review pending

- **Fundus Images** (`fundus-images/`)
  - Ophthalmology dataset from arjunbhushan005
  - Status: Documentation auto-generated, manual review pending

- **Retinal Colorized Oct Images** (`retinal-colorized-oct-images/`)
  - Ophthalmology dataset from shuvokumarbasak2030
  - Status: Documentation auto-generated, manual review pending

- **Macular Degeneration Disease Dataset** (`macular-degeneration-disease-dataset/`)
  - Ophthalmology dataset from orvile
  - Status: Documentation auto-generated, manual review pending

- **Octdl Optical Coherence Tomography Dataset** (`octdl-optical-coherence-tomography-dataset/`)
  - Ophthalmology dataset from orvile
  - Status: Documentation auto-generated, manual review pending

- **Fundus Aptosddridirdeyepacsmessidor** (`fundus-aptosddridirdeyepacsmessidor/`)
  - Ophthalmology dataset from sehastrajits
  - Status: Documentation auto-generated, manual review pending

- **Denoising** (`denoising/`)
  - Ophthalmology dataset from stiflerxd
  - Status: Documentation auto-generated, manual review pending

- **Diabetic Retinopathy Detection Classification Data** (`diabetic-retinopathy-detection-classification-data/`)
  - Ophthalmology dataset from pritpal2873
  - Status: Documentation auto-generated, manual review pending

- **Octdl Retinal Oct Images Dataset** (`octdl-retinal-oct-images-dataset/`)
  - Ophthalmology dataset from shakilrana
  - Status: Documentation auto-generated, manual review pending

- **Cataract Classification Dataset In Ds** (`cataract-classification-dataset-in-ds/`)
  - Ophthalmology dataset from sheemazain
  - Status: Documentation auto-generated, manual review pending

- **Oct2017Uniquedataset** (`oct2017uniquedataset/`)
  - Ophthalmology dataset from rahulkumar99
  - Status: Documentation auto-generated, manual review pending

- **Retina Blood Vessel** (`retina-blood-vessel/`)
  - Ophthalmology dataset from abdallahwagih
  - Status: Documentation auto-generated, manual review pending

- **Cornea In Diabetes** (`cornea-in-diabetes/`)
  - Ophthalmology dataset from drbasanthkb
  - Status: Documentation auto-generated, manual review pending

- **Intraretinal Cystoid Fluid** (`intraretinal-cystoid-fluid/`)
  - Ophthalmology dataset from zeeshanahmed13
  - Status: Documentation auto-generated, manual review pending

- **Fundus Image Registration** (`fundus-image-registration/`)
  - Ophthalmology dataset from andrewmvd
  - Status: Documentation auto-generated, manual review pending

- **Messidor2 Dr Grades** (`messidor2-dr-grades/`)
  - Ophthalmology dataset from google-brain
  - Status: Documentation auto-generated, manual review pending

- **Kermany2018** (`kermany2018/`)
  - Ophthalmology dataset from paultimothymooney
  - Status: Documentation auto-generated, manual review pending

- **Retinal Disease Classification** (`retinal-disease-classification/`)
  - Ophthalmology dataset from andrewmvd
  - Status: Documentation auto-generated, manual review pending

- **Retina** (`retina/`)
  - Ophthalmology dataset from ahtcmstp
  - Status: Documentation auto-generated, manual review pending

- **Diabetic Retinopathy 224X224 Gaussian Filtered** (`diabetic-retinopathy-224x224-gaussian-filtered/`)
  - Ophthalmology dataset from sovitrath
  - Status: Documentation auto-generated, manual review pending

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
