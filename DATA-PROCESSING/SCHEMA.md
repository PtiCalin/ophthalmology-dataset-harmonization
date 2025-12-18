# Schema Reference

Complete documentation of the 122-field canonical ophthalmology schema.

---

## Overview

The `HarmonizedRecord` is a comprehensive dataclass designed to capture all ophthalmology imaging data across modalities, diseases, and patient demographics.

**Total Fields:** 122

- Top-level columns: 30
- Nested objects: 4 dataclasses with 92+ additional fields

### Design Rationale

The schema was developed through iterative analysis of 12+ ophthalmology datasets, prioritizing:

- **Clinical Completeness:** Capture of all relevant diagnostic, demographic, and technical information
- **Interoperability:** Compatibility with healthcare standards (DICOM, FHIR) and research requirements
- **Extensibility:** Modular structure allowing addition of new fields without breaking existing implementations
- **Type Safety:** Use of Python dataclasses for runtime validation and IDE support
- **Nested Organization:** Logical grouping of related fields to reduce top-level complexity while maintaining accessibility

### Validation Framework

All fields include type hints and runtime validation:

- **Required Fields:** Must be non-null for valid records
- **Optional Fields:** May be None, with appropriate handling in processing
- **Range Validation:** Numeric fields validated against clinical reference ranges
- **Enum Constraints:** Categorical fields restricted to predefined values
- **Cross-Field Consistency:** Logical relationships validated (e.g., severity must match diagnosis category)

---

## Top-Level Columns (30)

### Identifiers (Required)

```txt
image_id: str                    # Unique per-image ID
dataset_source: str              # Source dataset name
patient_id: Optional[str]        # De-identified patient ID
visit_number: Optional[int]      # Sequential visit (1, 2, 3...)
```

**Rationale:** Unique identification enables tracking across datasets and longitudinal studies. Dataset source maintains provenance for quality assessment and bias analysis.

### Imaging Characteristics

```txt
modality: str                    # Type: Fundus, OCT, OCTA, Slit-Lamp, FA, FAF, Infrared, 
                                # Ultrasound, Anterior Segment, Specular, Visual Field
laterality: Optional[str]        # OD (right), OS (left), OU (both)
view_type: Optional[str]         # macula, optic_disc, full_field, peripheral, etc.
image_path: Optional[str]        # File path or URL
```

**Rationale:** Modality classification enables appropriate analysis pipelines. Laterality and view type support bilateral comparison and anatomical localization. Path field facilitates data access while maintaining flexibility for different storage systems.

### Diagnosis & Severity

```txt
diagnosis_raw: Optional[str]           # Original label
diagnosis_category: Optional[str]      # Standardized (28 categories)
diagnosis_confidence: Optional[float]  # 0.0-1.0
severity: Optional[str]                # None, Mild, Moderate, Severe, Proliferative
multiple_diagnoses: List[str]          # Secondary diagnoses
disease_specific_fields: Dict[str, Any] # Condition-specific metrics
```

**Rationale:** Preservation of raw diagnosis allows auditability of standardization. Confidence scoring enables quality filtering. Multiple diagnoses support complex cases. Disease-specific fields provide extensibility for specialized metrics.

### Nested Objects (4)

```txt
clinical_findings: ClinicalFindings              # 25 fields
patient_clinical: PatientClinicalData            # 35+ fields
device_and_acquisition: DeviceAndAcquisition     # 12 fields
image_metadata: ImageMetadata                    # 20 fields
```

**Rationale:** Nested structure organizes related fields logically, reducing top-level complexity while maintaining data relationships. Each nested object focuses on a specific domain (clinical, patient, technical), enabling modular validation and processing.

### Study Context

```txt
exam_date: Optional[str]         # ISO format
exam_time: Optional[str]         # ISO format
facility_name: Optional[str]     # Where exam was performed
follow_up_recommended: Optional[bool]
```

**Rationale:** Temporal and facility information enables longitudinal analysis and quality assessment. Follow-up recommendations support clinical workflow integration.

### Quality & Validation

```txt
quality_flags: List[str]         # Issues: ["low_illumination", "motion_artifact", ...]
is_valid: bool                   # Passed all validation checks
validation_notes: Optional[str]  # Specific validation errors
annotation_quality: Optional[str] # Expert, Clinician, Consensus, Crowdsourced, Automated
data_source_reliability: Optional[str] # Clinical Trial, Hospital, Kaggle, etc.
internal_consistency_check: Optional[bool]
```

**Rationale:** Comprehensive quality tracking enables filtering for research applications. Multiple quality dimensions (technical, annotation, source) support appropriate use case selection.

### Extensibility

```txt
extra_json: Dict[str, Any]  # Non-standard fields
created_at: str             # ISO timestamp of creation
```

**Rationale:** Extensibility field accommodates emerging requirements without schema changes. Timestamp enables versioning and audit trails.

---

## ClinicalFindings (25 Fields)

Structured representation of clinical signs visible in images.

### Retinal Findings

```txt
hemorrhages_present: Optional[bool]
hemorrhage_locations: List[str]  # ["macula", "periphery", ...]
microaneurysms_present: Optional[bool]
hard_exudates_present: Optional[bool]
cotton_wool_spots_present: Optional[bool]
macular_edema_present: Optional[bool]
macular_edema_severity: Optional[str]  # mild, moderate, severe
```

### Optic Disc

```txt
cup_to_disc_ratio: Optional[float]  # 0.0-1.0
optic_disc_pallor: Optional[bool]
optic_disc_cupping: Optional[bool]
disc_size_mm: Optional[float]
```

### Vascular

```txt
vessel_tortuosity: Optional[bool]
vessel_narrowing: Optional[bool]
vein_occlusion: Optional[bool]
artery_occlusion: Optional[bool]
neovascularization: Optional[bool]
shunt_vessels: Optional[bool]
```

### Macular Metrics (from OCT)

```txt
macular_thickness_microns: Optional[float]
central_subfield_thickness: Optional[float]
macular_volume: Optional[float]
macular_pit: Optional[bool]
```

### Other

```txt
vitreous_hemorrhage: Optional[bool]
retinal_detachment: Optional[bool]
laser_scars_present: Optional[bool]
findings_notes: Optional[str]
```

---

## PatientClinicalData (35+ Fields)

Complete patient health profile.

### Demographics (4)

```txt
age: Optional[int]              # Years (0-150)
sex: Optional[str]              # M, F, O (other), U (unknown)
ethnicity: Optional[str]        # Caucasian, African, Asian, Hispanic, etc.
race: Optional[str]
```

### Systemic Conditions (8)

```txt
diabetes: Optional[bool]
diabetes_type: Optional[str]    # Type 1, Type 2, Gestational
diabetes_duration_years: Optional[float]
hba1c: Optional[float]          # Hemoglobin A1c percentage
hypertension: Optional[bool]
systolic_bp: Optional[float]    # mmHg
diastolic_bp: Optional[float]   # mmHg
hyperlipidemia: Optional[bool]
cholesterol_level: Optional[float]
```

### Physical Metrics (3)

```txt
bmi: Optional[float]            # 10-60 valid range
height_cm: Optional[float]
weight_kg: Optional[float]
```

### Renal Function (2)

```txt
eGFR: Optional[float]           # Estimated GFR
creatinine: Optional[float]     # mg/dL
```

### Ocular Measurements (8)

```txt
intraocular_pressure_od: Optional[float]  # mmHg (5-80 range)
intraocular_pressure_os: Optional[float]
visual_acuity_od: Optional[str]           # 20/20, 6/6, decimal, etc.
visual_acuity_os: Optional[str]
axial_length_od: Optional[float]          # mm
axial_length_os: Optional[float]
keratometry_od: Optional[float]           # Diopters
keratometry_os: Optional[float]
```

### Medications & Lifestyle (5)

```txt
medications: List[str]          # Current medications
insulin_dependent: Optional[bool]
smoking_status: Optional[str]   # Current, Former, Never
alcohol_use: Optional[str]      # None, Moderate, Heavy
exercise_hours_per_week: Optional[float]
```

---

## DeviceAndAcquisition (12+ Fields)

Device specifications and acquisition parameters.

### Device Info (3)

```txt
device_type: Optional[str]      # Fundus camera, OCT, etc.
manufacturer: Optional[str]     # Canon, Zeiss, Topcon, etc.
model: Optional[str]            # Specific model number
```

### Acquisition (4)

```txt
pupil_dilated: Optional[bool]
dilation_agent: Optional[str]   # Tropicamide, Phenylephrine, etc.
imaging_eye: Optional[str]      # OD, OS, or OU
scan_type: Optional[str]        # 2D, 3D, Volume, Line, etc.
```

### Software (2)

```txt
software_name: Optional[str]
software_version: Optional[str]
```

### Environment (3)

```txt
ambient_light_conditions: Optional[str]
room_temperature: Optional[float]  # Celsius
humidity: Optional[float]          # Percent
```

---

## ImageMetadata (20+ Fields)

Technical image specifications.

### Spatial

```txt
resolution_x: Optional[int]     # Pixels
resolution_y: Optional[int]
```

### Color/Signal

```txt
color_space: Optional[str]      # RGB, Grayscale, Multi-channel
bits_per_pixel: Optional[int]   # Bit depth (8, 12, 16, etc.)
channels: Optional[int]
```

### Optical

```txt
field_of_view: Optional[str]    # e.g., "45°", "60°"
wavelength: Optional[str]       # For specific modalities
```

### Quality (4 separate scores)

```txt
quality_score: Optional[float]      # Overall (0.0-1.0)
sharpness_score: Optional[float]
illumination_score: Optional[float]
contrast_score: Optional[float]
```

### Artifacts

```txt
has_artifacts: Optional[bool]
artifact_types: List[str]       # Motion, opacity, glare, etc.
image_usable: Optional[bool]
```

### Device

```txt
device_model: Optional[str]
device_manufacturer: Optional[str]
software_version: Optional[str]
```

### Acquisition Timing

```txt
acquisition_date: Optional[str]     # ISO format
acquisition_time: Optional[str]
```

### Compression

```txt
compression: Optional[str]          # JPEG, PNG, TIFF, etc.
compression_quality: Optional[int]  # 0-100 (for lossy)
file_size_bytes: Optional[int]
```

---

## Enum Types (7)

### Modality (12 values)

- Fundus
- OCT
- OCTA (OCT Angiography)
- Slit-Lamp
- Fluorescein Angiography
- Fundus Autofluorescence
- Infrared
- Ultrasound
- Anterior Segment
- Specular Microscopy
- Visual Field
- Unknown

### Laterality (3 values)

- OD (Right eye)
- OS (Left eye)
- OU (Both eyes)

### DiagnosisCategory (28 values)

- Normal
- Diabetic Retinopathy
- Diabetic Macular Edema
- Age-Related Macular Degeneration (AMD)
- Cataract
- Glaucoma / Glaucoma Suspect
- Corneal Disease
- Retinoblastoma
- Macular Edema
- Drusen
- Myopia / Hyperopia / Astigmatism / Presbyopia
- Hypertensive Retinopathy
- Retinal Detachment
- Retinal Vein / Artery Occlusion
- Optic Disc Disease
- Vitreous Hemorrhage
- Keratoconus
- Pterygium
- Refractive Error
- Cotton Wool Spots
- Hard Exudates
- Microaneurysms
- Hemorrhages
- Neovascularization
- Anterior Segment Disease
- Other

### Severity (6 values)

- None
- Mild
- Moderate
- Severe
- Proliferative
- Very Severe

### Sex (4 values)

- M (Male)
- F (Female)
- O (Other)
- U (Unknown)

### DiabetesType (5 values)

- Type 1
- Type 2
- Gestational
- Unknown
- No Diabetes

### DRSeverityScale (5 values) - International ICDR

- No DR
- Mild NPDR
- Moderate NPDR
- Severe NPDR
- PDR (Proliferative)

### AnnotationQuality (6 values)

- Expert (Ophthalmologist with subspecialty)
- Clinician (General eye care provider)
- Consensus (Multiple graders agreed)
- Crowd-sourced (Community contributed)
- Automated (AI/algorithmic)
- Unverified (Not validated)

### DataSource (7 values)

- Clinical Trial
- Hospital Records
- Telehealth
- Research Study
- Public Dataset (Kaggle, etc.)
- Crowdsourced
- Synthetic Data

---

## Validation Rules (10+)

Built-in validations ensure data quality and clinical plausibility:

**Core Requirements:**

- **Required fields:** image_id, dataset_source must be present for all records with image files

- **Rationale:** Ensures unique identification and provenance tracking

**Clinical Range Validations:**

- **Age range:** 0-130 years (covers pediatric to geriatric populations, while preventing invalid age dat >130 years old)
- **Confidence scores:** 0.0-1.0 (standardized probability scale)
- **Cup-to-disc ratio:** 0.0-1.0 (anatomical constraint for optic nerve assessment)
- **BMI:** 10-60 kg/m² (clinically plausible range excluding extreme outliers)
- **IOP (Intraocular Pressure):** 5-80 mmHg per eye (normal to severe glaucoma range)
- **Blood Pressure:** Systolic 80-200 mmHg, Diastolic 40-120 mmHg (hypertension ranges)
- **eGFR (kidney function):** 0-150 mL/min (from end-stage renal disease to supernormal)
- **Creatinine:** 0-10 mg/dL (renal function biomarker range)

**Validation Methodology:**

- Range checks prevent data entry errors and identify outliers
- Cross-field consistency validates relationships (e.g., severity matches diagnosis)
- Type validation ensures data integrity at runtime
- Confidence scoring enables quality-based filtering for research applications

---

## Example Usage

```python
from src.schema import (
    HarmonizedRecord, ClinicalFindings, PatientClinicalData,
    DeviceAndAcquisition, ImageMetadata
)

# Create a comprehensive record
record = HarmonizedRecord(
    image_id="messidor_0001",
    dataset_source="Messidor",
    diagnosis_category="Diabetic Retinopathy",
    severity="Moderate",
    diagnosis_confidence=0.92,
    
    patient_clinical=PatientClinicalData(
        age=52,
        sex="M",
        diabetes_type="Type 2",
        diabetes_duration_years=8,
        hba1c=7.2,
        intraocular_pressure_od=14.5,
        intraocular_pressure_os=15.2,
    ),
    
    clinical_findings=ClinicalFindings(
        hemorrhages_present=True,
        microaneurysms_present=True,
        hard_exudates_present=True,
        macular_edema_present=False,
        cup_to_disc_ratio=0.45,
    ),
    
    image_metadata=ImageMetadata(
        resolution_x=2048,
        resolution_y=2048,
        color_space="RGB",
        field_of_view="45°",
        quality_score=0.88,
    ),
)

# Validate
is_valid = record.validate()
print(record.quality_flags)  # Any issues detected
print(record.to_dict())      # Export to JSON/DataFrame
```

---

## Backward Compatibility

All old schema fields are accessible via the new nested structure. Example migration:

```python
# Old way: record.patient_age
# New way: record.patient_clinical.age

# For compatibility, you can still access old fields
age = record.patient_clinical.age
```

