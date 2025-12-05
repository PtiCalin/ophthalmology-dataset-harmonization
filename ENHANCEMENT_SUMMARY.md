# Schema and Harmonization Model Enhancements

## Overview
Comprehensive enhancements to the ophthalmology dataset harmonization pipeline with advanced schema fields, robust error handling, and improved data quality management.

---

## 1. Enhanced Schema (`src/schema.py`)

### New Enums for Type Safety
- **Modality**: Fundus, OCT, Slit-Lamp, Fluorescein Angiography, Infrared, Ultrasound, Anterior Segment, Unknown
- **Laterality**: OD (right), OS (left), OU (both)
- **DiagnosisCategory**: Comprehensive list of 12 standardized conditions
- **Severity**: None, Mild, Moderate, Severe, Proliferative
- **Sex**: M, F, O (other), U (unknown)

### ImageMetadata Class
New dataclass for technical image specifications:
- `resolution_x`, `resolution_y`: Image dimensions in pixels
- `color_space`: RGB, Grayscale, Multi-channel
- `bits_per_pixel`: Bit depth
- `field_of_view`: Angular field (e.g., "45°", "60°")
- `quality_score`: 0.0-1.0 custom quality metric

### Enhanced HarmonizedRecord
**Expanded from 10 to 20+ fields:**

**Core Identifiers:**
- `image_id`: Unique image identifier
- `dataset_source`: Source dataset name

**Imaging Characteristics:**
- `modality`: Type of imaging (with enum)
- `laterality`: Eye side (OD/OS/OU)
- `view_type`: Anatomical view (macula, optic_disc, full_field)
- `image_path`: Image file path/name

**Clinical Information:**
- `diagnosis_raw`: Original diagnosis label
- `diagnosis_category`: Standardized diagnosis
- `diagnosis_confidence`: 0.0-1.0 confidence score
- `severity`: Severity grading (enum)
- `clinical_notes`: Unstructured clinical text

**Patient Demographics:**
- `patient_id`: De-identified patient identifier
- `patient_age`: Age in years (validated 0-150)
- `patient_sex`: Biological sex (enum)
- `patient_ethnicity`: Optional ethnicity/race

**Image Metadata:**
- `image_metadata`: ImageMetadata object with technical specs

**Data Quality:**
- `quality_flags`: List of detected quality issues
- `is_valid`: Boolean validation status
- `validation_notes`: Validation error messages

**Extensibility:**
- `extra_json`: Dict for non-standard fields
- `created_at`: ISO timestamp of creation

### New Methods
- `add_quality_flag()`: Add quality issues
- `validate()`: Built-in validation with reasonable ranges
- `to_dict()`: Proper serialization with JSON handling

---

## 2. Comprehensive Harmonization Rules (`src/rules.py`)

### Expanded Diagnosis Mapping
**50+ diagnosis keywords** mapped to standardized categories with severity:
- Returns tuple `(diagnosis_category, severity_grade)`
- Examples:
  - "nonproliferative" → ("Diabetic Retinopathy", "Mild")
  - "wet amd" → ("Age-Related Macular Degeneration", "Severe")
  - "immature" → ("Cataract", "Mild")

### Severity Grading System
Specialized grading scales by condition:
- **DR**: None, Mild (NPDR), Moderate, Severe, Proliferative
- **AMD**: Early, Intermediate, Advanced
- **Cataract**: Mild, Moderate, Mature, Hypermature

### Enhanced Modality Inference
**100+ pattern keywords** for reliable detection:
- Fundus: fundus, color fundus, cfp, optos, messidor, refuge
- OCT: oct, optical coherence, swept source, ss-oct
- Slit-Lamp: slit, anterior segment, iris, cornea
- And more: Fluorescein, Infrared, Ultrasound

### Improved Laterality Detection
**Word boundary matching** for eye side detection:
- Handles: OD/OS/OU codes, English terms (left/right)
- Filename patterns: `_r.`, `-r-`, `_od`, etc.
- Multi-language support: droit (French for right), gauche (left)

### New Functions
1. **`infer_severity_from_diagnosis()`**: Extract severity from raw text
2. **`detect_column_role()`**: Priority-ordered field detection
3. **`harmonize_column_value()`**: Field-specific harmonization with validation

### Enhanced Validation
- Age range validation (0-150 years)
- Sex field normalization (M/F/O/U)
- Ethnicity preservation
- Resolution parsing

---

## 3. Robust Universal Loader (`src/loaders/universal_loader.py`)

### New Exception Classes
- `LoaderException`: Base exception for loader errors
- `ColumnDetectionException`: Critical column detection failures

### Confidence Scoring
- `detection_confidence`: Dict tracking confidence for each detected field
- Length-based scoring: longer field names = higher confidence
- Helps users understand auto-detection reliability

### Comprehensive Error Handling
- **Error tracking**: `load_errors` list with row index, error message, data
- **Warnings**: `warnings` list for validation issues
- **Graceful degradation**: Continues processing despite errors

### Enhanced Row Harmonization
- Fallback `image_id` generation if missing
- Automatic severity inference from diagnosis
- Image metadata extraction and parsing
- Quality flag generation for issues
- Nested validation with detailed messages

### Validation Features
- Image ID requirement enforcement
- Age range validation (0-150)
- Diagnosis confidence scoring (placeholder for ML)
- Quality flag accumulation
- Detailed validation notes

### New Methods
- `_try_parse_int()`: Safe integer parsing
- `get_load_report()`: Summary statistics on load operation

### Load Reporting
```python
report = loader.get_load_report()
# Returns:
{
    'dataset': 'name',
    'total_errors': 0,
    'total_warnings': 5,
    'detected_columns': {...},
    'detection_confidence': {...},
    'errors': [...],  # First 10
    'warnings': [...]  # First 10
}
```

---

## 4. Key Improvements Summary

### Data Quality
| Feature | Before | After |
|---------|--------|-------|
| Schema fields | 10 | 20+ |
| Diagnosis keywords | 25 | 50+ |
| Modality patterns | 15 | 100+ |
| Validation | None | Built-in with flags |
| Error handling | None | Comprehensive with tracking |

### Extensibility
- Enum types for type safety
- Custom quality flags system
- Flexible extra_json storage
- Nested ImageMetadata objects

### Usability
- Automatic column detection with confidence scores
- Detailed error reporting per row
- Validation with explanatory messages
- Summary reports for debugging

### Robustness
- Graceful error handling
- Missing field fallbacks
- Range validation
- Type-safe harmonization

---

## 5. Usage Examples

### Creating a Record with Full Metadata
```python
from src.schema import HarmonizedRecord, ImageMetadata, Modality, Laterality

record = HarmonizedRecord(
    image_id="img_12345",
    dataset_source="DR Detection",
    modality=Modality.FUNDUS.value,
    laterality=Laterality.OD.value,
    diagnosis_raw="Moderate NPDR",
    diagnosis_category="Diabetic Retinopathy",
    diagnosis_confidence=0.92,
    severity="Moderate",
    patient_age=52,
    patient_sex="M",
    image_metadata=ImageMetadata(
        resolution_x=512,
        resolution_y=496,
        color_space="RGB",
        quality_score=0.95
    )
)

# Validate
if record.validate():
    print("Record is valid!")
else:
    print(f"Validation issues: {record.validation_notes}")

# Add quality flags
record.add_quality_flag("low_contrast")
record.add_quality_flag("motion_artifact")
```

### Loading with Error Handling
```python
from src.loaders import UniversalLoader

loader = UniversalLoader("DR Detection")
harmonized_df = loader.load_and_harmonize(df)

# Get detailed report
report = loader.get_load_report()
print(f"Errors: {report['total_errors']}")
print(f"Warnings: {report['total_warnings']}")
print(f"Detected: {report['detected_columns']}")
```

### Diagnosis Normalization
```python
from src.rules import normalize_diagnosis, infer_severity_from_diagnosis

# Returns tuple now
category, severity = normalize_diagnosis("Moderate non-proliferative DR")
# Returns: ("Diabetic Retinopathy", "Moderate")

# Get severity from raw text
severity = infer_severity_from_diagnosis("Advanced dry AMD", "AMD")
# Returns: "Severe"
```

---

## 6. Backward Compatibility Notes

⚠️ **Breaking Changes:**
1. `normalize_diagnosis()` now returns tuple instead of string
2. `HarmonizedRecord.__init__()` requires `image_id` and `dataset_source` params
3. Schema column names changed (see `create_schema_columns()`)

✓ **Maintained:**
- Core harmonization workflow
- Auto-column detection logic
- File export formats (Parquet/CSV)

**Migration Path:**
```python
# Old
diag = normalize_diagnosis("DR")

# New
diag, severity = normalize_diagnosis("DR")
```

---

## 7. Future Enhancements

Planned improvements:
1. **ML-based confidence scoring**: Train model to predict diagnosis confidence
2. **Image quality assessment**: Extract actual image metrics
3. **Duplicate detection**: Perceptual hashing for similar images
4. **Anomaly detection**: Flag outliers in patient demographics
5. **Dataset profiling**: Per-dataset statistics and comparisons
6. **Custom validators**: Plugin system for domain-specific validation

---

## Testing Recommendations

Test cases for new features:
1. Diagnosis normalization with 50+ variants
2. Severity grading accuracy per condition
3. Error handling with malformed data
4. Quality flag accumulation
5. Validation with edge cases (age=0, age=150)
6. Column detection with similar names
7. Nested object serialization
8. Load reporting accuracy

---

## Documentation Updates

- Schema docstrings: ✓ Updated
- Rules docstrings: ✓ Enhanced
- Loader docstrings: ✓ Comprehensive
- Type hints: ✓ Complete
- Examples: ✓ Added
