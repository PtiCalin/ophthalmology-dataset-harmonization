# Schema Reference

Complete documentation of the 122-field canonical ophthalmology schema.

---

## Overview

The `HarmonizedRecord` is a comprehensive dataclass designed to capture all ophthalmology imaging data across modalities, diseases, and patient demographics.

**Total Fields:** 122
- Top-level columns: 30
- Nested objects: 4 dataclasses with 92+ additional fields

---

## Top-Level Columns (30)

### Identifiers (Required)
```
image_id: str                    # Unique per-image ID
dataset_source: str              # Source dataset name
patient_id: Optional[str]        # De-identified patient ID
visit_number: Optional[int]      # Sequential visit (1, 2, 3...)
```

### Imaging Characteristics
```
modality: str                    # Type: Fundus, OCT, OCTA, Slit-Lamp, FA, FAF, Infrared, 
                                # Ultrasound, Anterior Segment, Specular, Visual Field
laterality: Optional[str]        # OD (right), OS (left), OU (both)
view_type: Optional[str]         # macula, optic_disc, full_field, peripheral, etc.
image_path: Optional[str]        # File path or URL
```

### Diagnosis & Severity
```
diagnosis_raw: Optional[str]           # Original label
diagnosis_category: Optional[str]      # Standardized (28 categories)
diagnosis_confidence: Optional[float]  # 0.0-1.0
severity: Optional[str]                # None, Mild, Moderate, Severe, Proliferative
multiple_diagnoses: List[str]          # Secondary diagnoses
disease_specific_fields: Dict[str, Any] # Condition-specific metrics
```

### Nested Objects (4)
```
clinical_findings: ClinicalFindings              # 25 fields
patient_clinical: PatientClinicalData            # 35+ fields
device_and_acquisition: DeviceAndAcquisition     # 12 fields
image_metadata: ImageMetadata                    # 20 fields
```

### Study Context
```
exam_date: Optional[str]         # ISO format
exam_time: Optional[str]         # ISO format
facility_name: Optional[str]     # Where exam was performed
follow_up_recommended: Optional[bool]
```

### Quality & Validation
```
quality_flags: List[str]         # Issues: ["low_illumination", "motion_artifact", ...]
is_valid: bool                   # Passed all validation checks
validation_notes: Optional[str]  # Specific validation errors
annotation_quality: Optional[str] # Expert, Clinician, Consensus, Crowdsourced, Automated
data_source_reliability: Optional[str] # Clinical Trial, Hospital, Kaggle, etc.
internal_consistency_check: Optional[bool]
```

### Extensibility
```
extra_json: Dict[str, Any]  # Non-standard fields
created_at: str             # ISO timestamp of creation
```

---

## ClinicalFindings (25 Fields)

Structured representation of clinical signs visible in images.

### Retinal Findings
```
hemorrhages_present: Optional[bool]
hemorrhage_locations: List[str]  # ["macula", "periphery", ...]
microaneurysms_present: Optional[bool]
hard_exudates_present: Optional[bool]
cotton_wool_spots_present: Optional[bool]
macular_edema_present: Optional[bool]
macular_edema_severity: Optional[str]  # mild, moderate, severe
```

### Optic Disc
```
cup_to_disc_ratio: Optional[float]  # 0.0-1.0
optic_disc_pallor: Optional[bool]
optic_disc_cupping: Optional[bool]
disc_size_mm: Optional[float]
```

### Vascular
```
vessel_tortuosity: Optional[bool]
vessel_narrowing: Optional[bool]
vein_occlusion: Optional[bool]
artery_occlusion: Optional[bool]
neovascularization: Optional[bool]
shunt_vessels: Optional[bool]
```

### Macular Metrics (from OCT)
```
macular_thickness_microns: Optional[float]
central_subfield_thickness: Optional[float]
macular_volume: Optional[float]
macular_pit: Optional[bool]
```

### Other
```
vitreous_hemorrhage: Optional[bool]
retinal_detachment: Optional[bool]
laser_scars_present: Optional[bool]
findings_notes: Optional[str]
```

---

## PatientClinicalData (35+ Fields)

Complete patient health profile.

### Demographics (4)
```
age: Optional[int]              # Years (0-150)
sex: Optional[str]              # M, F, O (other), U (unknown)
ethnicity: Optional[str]        # Caucasian, African, Asian, Hispanic, etc.
race: Optional[str]
```

### Systemic Conditions (8)
```
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
```
bmi: Optional[float]            # 10-60 valid range
height_cm: Optional[float]
weight_kg: Optional[float]
```

### Renal Function (2)
```
eGFR: Optional[float]           # Estimated GFR
creatinine: Optional[float]     # mg/dL
```

### Ocular Measurements (8)
```
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
```
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
```
device_type: Optional[str]      # Fundus camera, OCT, etc.
manufacturer: Optional[str]     # Canon, Zeiss, Topcon, etc.
model: Optional[str]            # Specific model number
```

### Acquisition (4)
```
pupil_dilated: Optional[bool]
dilation_agent: Optional[str]   # Tropicamide, Phenylephrine, etc.
imaging_eye: Optional[str]      # OD, OS, or OU
scan_type: Optional[str]        # 2D, 3D, Volume, Line, etc.
```

### Software (2)
```
software_name: Optional[str]
software_version: Optional[str]
```

### Environment (3)
```
ambient_light_conditions: Optional[str]
room_temperature: Optional[float]  # Celsius
humidity: Optional[float]          # Percent
```

---

## ImageMetadata (20+ Fields)

Technical image specifications.

### Spatial
```
resolution_x: Optional[int]     # Pixels
resolution_y: Optional[int]
```

### Color/Signal
```
color_space: Optional[str]      # RGB, Grayscale, Multi-channel
bits_per_pixel: Optional[int]   # Bit depth (8, 12, 16, etc.)
channels: Optional[int]
```

### Optical
```
field_of_view: Optional[str]    # e.g., "45°", "60°"
wavelength: Optional[str]       # For specific modalities
```

### Quality (4 separate scores)
```
quality_score: Optional[float]      # Overall (0.0-1.0)
sharpness_score: Optional[float]
illumination_score: Optional[float]
contrast_score: Optional[float]
```

### Artifacts
```
has_artifacts: Optional[bool]
artifact_types: List[str]       # Motion, opacity, glare, etc.
image_usable: Optional[bool]
```

### Device
```
device_model: Optional[str]
device_manufacturer: Optional[str]
software_version: Optional[str]
```

### Acquisition Timing
```
acquisition_date: Optional[str]     # ISO format
acquisition_time: Optional[str]
```

### Compression
```
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

Built-in validations that run automatically:

```
✓ Required fields: image_id, dataset_source
✓ Age range: 0-150 years
✓ Confidence scores: 0.0-1.0
✓ Cup-to-disc ratio: 0.0-1.0
✓ BMI: 10-60 kg/m²
✓ IOP OD/OS: 5-80 mmHg
✓ Systolic BP: 80-200 mmHg
✓ Diastolic BP: 40-120 mmHg
✓ eGFR: 0-150 mL/min
✓ Creatinine: 0-10 mg/dL
```

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

