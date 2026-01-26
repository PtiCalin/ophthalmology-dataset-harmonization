# Ophthalmology Dataset Harmonization

A research-oriented Python framework for standardizing heterogeneous ophthalmology datasets through systematic data harmonization techniques.

**Status:** v2.0 Production | **Coverage:** 122 fields | **Mappings:** 269+ diagnosis keywords | **Tests:** 18 passing

---

## Project Context and Motivation

This project emerges from professional experience at the intersection of healthcare software development and clinical research. Over several years, the author has contributed to registry studies, harmonization frameworks across disease areas, and interoperability initiatives in complex data environments. Currently serving as an administrative agent at one of Canada's largest ophthalmology tertiary care centers, the author observes the critical need for standardized, high-quality datasets to advance patient care and research outcomes.

Rooted in a background spanning healthcare coordination, community advocacy, and research support, this work represents a personal exploration into digital infrastructure and open-source tooling. The technical development began with automation and documentation practices, evolving into repository management, custom workflows, and digital tool creation under the alias PtiCalin. This persona emphasizes clarity, compassion, and structured scalability in all creations.

The project's objective aligns directly with my expertise in healthcare data harmonization, focusing on methodological approaches to dataset standardization in ophthalmology. It serves as a skill development initiative, applying research principles to practical data challenges in clinical settings.

## Methodological Approach

The harmonization framework employs a multi-stage process grounded in clinical data standards and software engineering best practices:

1. **Schema Design:** Development of a canonical data structure based on clinical interoperability requirements and existing standards (e.g., DICOM, FHIR).

2. **Rule-Based Inference:** Implementation of pattern matching and mapping algorithms for automated diagnosis normalization, modality detection, and clinical feature extraction.

3. **Validation Framework:** Establishment of quality assurance mechanisms including data type validation, range checking, logical consistency verification, and confidence scoring.

4. **Iterative Refinement:** Exploratory development model incorporating feedback from clinical data sources, testing against diverse datasets, and continuous improvement through versioned releases.

This approach reflects an academic exploration of data harmonization challenges, balancing theoretical rigor with practical implementation in healthcare contexts.

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Harmonization

```bash
jupyter notebook notebooks/dataset_harmonization.ipynb
```

### Output

```txt
output/
├── harmonized.parquet    # Main dataset (all records)
└── harmonized.csv       # CSV export for easy inspection
```

---

## Methodology

!!! Write a summary paragraph on the methodologies 

## Harmonization Process

!!! Summary description of the Harmonization work required

### 1. Schema Standardization

The framework consolidates heterogeneous datasets into a standardized 122-field structure comprising 30 top-level columns and 4 nested dataclasses. This canonical schema is designed to capture comprehensive clinical, imaging, and metadata information while maintaining compatibility with existing healthcare data standards.

### 2. Intelligent Field Mapping

Automated detection and mapping of dataset columns through pattern recognition algorithms:

- Diagnosis normalization using keyword mapping to standardized categories and severity scales
- Modality inference based on filename patterns and metadata analysis
- Laterality detection supporting multiple languages and notation systems
- Patient data extraction with validation against clinical reference ranges

### 3. Rule-Based Harmonization

Application of domain-specific rules for:

- Mapping 269+ diagnosis keywords to 28 standardized disease categories
- Implementation of 8+ severity grading systems (e.g., ICDR for diabetic retinopathy, AREDS for AMD)
- Recognition of 150+ modality patterns across 12 imaging types
- Detection of 37 clinical finding types
- Comprehensive validation with 10+ built-in checks and confidence scoring

### 4. Multi-Dataset Integration

Support for integration of multiple ophthalmology datasets, including those from public repositories, with an extensible loader architecture designed for scalability across research and clinical environments.

---

## Architecture

### Core Components

| Component | Purpose |
|-----------|---------|
| `src/schema.py` | Canonical data structure definition (122 fields) |
| `src/rules.py` | Inference algorithms for diagnosis, modality, and laterality mapping |
| `src/loaders/universal_loader.py` | Dataset loading and harmonization engine |
| `src/pipeline/harmonize_all.py` | Multi-dataset orchestration framework |
| `notebooks/dataset_harmonization.ipynb` | Executable demonstration and validation |

### Data Model

The harmonization process utilizes structured dataclasses for type-safe data representation:

```python
# Define harmonized records
from src.schema import HarmonizedRecord, ClinicalFindings, PatientClinicalData

record = HarmonizedRecord(
    image_id="img_001",
    dataset_source="Messidor",
    diagnosis_category="Diabetic Retinopathy",
    severity="Moderate",
    patient_clinical=PatientClinicalData(
        age=52,
        sex="M",
        diabetes_type="Type 2",
        hba1c=7.2
    ),
    clinical_findings=ClinicalFindings(
        hemorrhages_present=True,
        microaneurysms_present=True
    )
)
```

### Processing Pipeline

```python
# Load and harmonize dataset
from src.loaders import UniversalLoader

loader = UniversalLoader("Messidor DR Detection")
harmonized_df = loader.load_and_harmonize(df)

# Generate processing diagnostics
report = loader.get_load_report()
print(f"Processed {len(harmonized_df)} records")
print(f"Validation errors: {report['total_errors']}, Warnings: {report['total_warnings']}")
```

---

## Schema Overview

The canonical schema comprises 122 fields organized into 30 top-level columns and 4 nested dataclasses, designed to capture the full spectrum of ophthalmology data requirements.

### Top-Level Fields (30)

- **Identifiers:** image_id, dataset_source, patient_id, visit_number
- **Imaging Parameters:** modality (12 types), laterality (OD/OS/OU), view_type, image_path
- **Diagnostic Information:** diagnosis_raw, diagnosis_category (28 types), confidence_score, severity_level
- **Clinical Data:** clinical_findings (nested, 25 fields)
- **Patient Demographics:** patient_clinical (nested, 35 fields)
- **Acquisition Details:** device_and_acquisition (nested, 12 fields)
- **Technical Metadata:** image_metadata (nested, 20 fields)
- **Quality Assurance:** quality_flags, validation_status, validation_notes, annotation_quality
- **Temporal Metadata:** exam_date, exam_time, facility_name, extra_json, record_timestamp

### Nested Data Structures

**ClinicalFindings (25 fields):**

- Retinal pathology: hemorrhages, microaneurysms, exudates, cotton_wool_spots, macular_edema
- Optic disc assessment: cup_disc_ratio, disc_pallor, disc_cupping, disc_size
- Vascular features: vessel_tortuosity, vessel_narrowing, vessel_occlusions, neovascularization
- Macular parameters: oct_thickness, central_subfield_thickness, macular_volume

**PatientClinicalData (35 fields):**

- Demographic information: age, sex, ethnicity, race
- Systemic conditions: diabetes_type, diabetes_duration, hba1c, hypertension, hyperlipidemia
- Renal function: egfr, creatinine
- Ocular metrics: intraocular_pressure, visual_acuity, axial_length, keratometry
- Treatment history: medications, lifestyle_factors

**DeviceAndAcquisition (12 fields):**

- Equipment specifications: device_type, manufacturer, model, software_version
- Acquisition parameters: pupil_dilation, eye_side, scan_parameters
- Environmental conditions: lighting_conditions, temperature, humidity

**ImageMetadata (20 fields):**

- Image characteristics: resolution, color_space, bit_depth, field_of_view
- Quality metrics: overall_quality_score, sharpness_score, illumination_score, contrast_score
- Artifact detection: artifact_flags, compression_ratio, file_size

---

## Supported Modalities and Conditions

### Imaging Modalities (12)

- Fundus Photography (Color Fundus, Widefield)
- Optical Coherence Tomography (SD-OCT, SS-OCT, 3D OCT)
- OCT Angiography
- Slit-Lamp Biomicroscopy
- Fluorescein Angiography
- Fundus Autofluorescence
- Infrared Imaging
- Ophthalmic Ultrasound
- Anterior Segment Photography
- Specular Microscopy
- Visual Field Testing
- Anterior Segment OCT

### Disease Categories (28)

- Diabetic Retinopathy (with ICDR severity grading)
- Diabetic Macular Edema
- Age-Related Macular Degeneration (wet/dry classification)
- Cataract (morphological classification and density assessment)
- Glaucoma (with optic disc and visual field parameters)
- Corneal Pathology
- Retinal Detachment
- Retinal Vascular Occlusions
- Optic Disc Disorders
- Refractive Errors
- Additional categories including uveitis, retinal dystrophies, and inflammatory conditions

---

## Validation and Testing

The framework includes comprehensive test suites to ensure data integrity and algorithmic correctness:

```bash
# Execute validation test suites
python -m pytest test_robust_schema.py -v
python -m pytest test_expanded_rules.py -v

# Test results: 18+ test cases, 100% pass rate
```

Testing covers schema validation, rule-based inference accuracy, edge case handling, and integration with multiple dataset formats.

---

## Documentation

| Document | Content |
|----------|---------|
| **SCHEMA.md** | Comprehensive field reference (122 fields) with validation rules | `DATA-PROCESSING/` |
| **RULES.md** | Detailed inference algorithms and mapping methodologies | `DATA-PROCESSING/` |
| **CODEBOOK.md** | Data dictionary and standardized enumeration values | `DATA-PROCESSING/` |
| **UPDATES.md** | Development history and enhancement roadmap |

---

## Research Applications and Extensions

1. **Dataset Integration:** Incorporate additional ophthalmology datasets by extending the loader registry
2. **Rule Customization:** Expand diagnosis mapping and inference rules for specialized clinical domains
3. **Quality Assessment:** Implement advanced validation metrics and statistical quality controls
4. **Analysis Pipeline:** Utilize harmonized datasets for machine learning research and clinical outcome studies

---

## Performance Characteristics

- **Processing Time:** ~100ms per record for full harmonization pipeline
- **Memory Footprint:** ~2KB per harmonized record in serialized format
- **Batch Export:** 19 demonstration records → 50KB Parquet file
- **Scalability:** ~200MB memory utilization for 10,000 records in active processing

---

## System Requirements

- Python 3.8 or higher
- Core dependencies: pandas, numpy, pyarrow
- Data access: kagglehub for public dataset integration
- Interactive development: jupyter, ipykernel
- Testing framework: pytest (optional for validation)

Complete dependency specifications available in `requirements.txt`.

---

## License

MIT License - See LICENSE file

---

## External Data Integration

For integration with Kaggle-hosted ophthalmology datasets:

1. Execute `setup_kaggle_api.ps1` in PowerShell to configure API credentials for the current session
2. Install the Kaggle Python client: `pip install kaggle`
3. Utilize CLI or programmatic interfaces as required

PowerShell example:

```powershell
.\setup_kaggle_api.ps1
kaggle competitions list
```

Python integration:

```python
import os
api_token = os.getenv("KAGGLE_API_TOKEN")
```

---

**Documentation Reference:** Consult DATA-PROCESSING/SCHEMA.md for field specifications, DATA-PROCESSING/RULES.md for inference methodologies, or DATA-PROCESSING/CODEBOOK.md for standardized values.

---
