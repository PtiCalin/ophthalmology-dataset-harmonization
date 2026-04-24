# Retinal Disease Detection Dataset Codebook

## Dataset Schema

### Core Fields

| Field Name | Data Type | Description | Validation Rules |
|------------|-----------|-------------|------------------|
| image_id | string | Unique identifier for each fundus image | Required, unique |
| patient_id | string | De-identified patient identifier | Required |
| eye | string | Laterality (OD/OS) | Required, enum: ['OD', 'OS'] |
| diagnosis | string | Primary clinical diagnosis | Required |
| secondary_diagnosis | string | Additional diagnoses (if any) | Optional |
| severity | string | Disease severity level | Optional, enum: ['Mild', 'Moderate', 'Severe'] |
| image_path | string | File path to image | Required |
| image_quality | string | Image quality assessment | Optional, enum: ['Excellent', 'Good', 'Moderate', 'Poor'] |

### Clinical Annotations

| Field Name | Data Type | Description | Units |
|------------|-----------|-------------|-------|
| cdr | float | Cup-to-disc ratio | Ratio (0.0-1.0) |
| retinal_thickness | float | Average retinal thickness | μm |
| vessel_density | float | Retinal vessel density | % |
| lesion_count | integer | Number of pathological lesions | Count |

### Image Metadata

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| modality | string | Imaging modality | Fixed: 'Fundus Photography' |
| resolution | string | Image resolution | Format: 'WIDTHxHEIGHT' |
| compression | string | Image compression format | e.g., 'JPEG', 'PNG' |
| acquisition_date | date | Date of image acquisition | ISO format |
| device_model | string | Camera/model used | e.g., 'Topcon TRC-50DX' |

## Enumerated Values

### Diagnosis Categories
- `Diabetic Retinopathy` - Diabetes-related retinal changes
- `Glaucoma` - Optic nerve damage
- `Age-Related Macular Degeneration` - AMD
- `Hypertensive Retinopathy` - Hypertension-related changes
- `Retinal Vein Occlusion` - Vascular occlusion
- `Normal` - Healthy retina
- `Other` - Other retinal pathologies

### Severity Levels
- `Mild` - Early stage disease
- `Moderate` - Intermediate progression
- `Severe` - Advanced disease stage

### Image Quality
- `Excellent` - Optimal for analysis
- `Good` - Suitable for analysis
- `Moderate` - Acceptable with limitations
- `Poor` - Not suitable for analysis

### Laterality
- `OD` - Right eye (oculus dexter)
- `OS` - Left eye (oculus sinister)

## Data Quality Standards

### Completeness
- All required fields must be present
- Missing optional fields should be marked as `null` or empty

### Accuracy
- Clinical annotations verified by ophthalmologists
- Image quality assessed by trained graders
- Diagnosis confirmed through comprehensive clinical evaluation

### Consistency
- Standardized terminology across all records
- Consistent units and measurement protocols
- Uniform data formatting

## Mapping to Harmonized Schema

This dataset maps to the harmonized ophthalmology schema as follows:

| Retinal Disease Detection Field | Harmonized Field | Transformation |
|----------------------------------|------------------|----------------|
| image_id | record_id | `lambda x: f"RDD_{x}"` |
| patient_id | patient_id | Direct mapping |
| eye | laterality | OD → Right, OS → Left |
| diagnosis | diagnosis_category | Category mapping |
| severity | severity | Direct mapping |
| cdr | clinical_findings.cup_disc_ratio | Direct mapping |
| image_quality | image_quality | Direct mapping |

## Validation Rules

### Field Validation
- `cdr`: Must be between 0.0 and 1.0
- `retinal_thickness`: Must be positive value
- `vessel_density`: Must be between 0 and 100
- `lesion_count`: Must be non-negative integer

### Cross-field Validation
- If diagnosis = 'Normal', severity must be null
- Image quality cannot be 'Poor' for training set images
- Laterality must be consistent within patient records

## Data Dictionary Notes

- All measurements follow standardized protocols
- Images are de-identified and anonymized
- Clinical annotations performed by board-certified ophthalmologists
- Dataset split into training/validation/test sets for model development