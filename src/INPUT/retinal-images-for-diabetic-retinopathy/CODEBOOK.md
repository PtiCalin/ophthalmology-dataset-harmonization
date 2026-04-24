# Retinal Images for Diabetic Retinopathy Codebook

## Overview

This codebook provides detailed specifications for the Retinal Images for Diabetic Retinopathy dataset, including field definitions, value ranges, clinical interpretations, and harmonization mappings for integration into the ophthalmology data harmonization pipeline.

## Dataset Schema

### Primary Fields

| Field Name | Data Type | Description | Required | Validation Rules |
|------------|-----------|-------------|----------|------------------|
| image_id | string | Unique identifier for each fundus image | Yes | Format: `{patient_id}_{eye}_{severity}_{grader}_{date}` |
| patient_id | string | Anonymous patient identifier | Yes | Unique per patient |
| eye | categorical | Eye laterality | Yes | OD, OS |
| severity | categorical | DR severity classification | Yes | no_dr, mild, moderate, severe, proliferative |
| grader | categorical | Grading ophthalmologist identifier | No | grader1, grader2, etc. |
| grading_date | date | Date of clinical grading | No | YYYY-MM-DD format |
| image_quality | integer | Subjective quality score | No | Range: 1-5 (5 = excellent) |

## Clinical Classifications

### Diabetic Retinopathy Severity Levels

#### No DR
- **Clinical Definition**: No apparent diabetic retinopathy
- **Fundus Features**: Normal retinal appearance
- **Risk Level**: Low risk for vision loss
- **Harmonization Mapping**: `diagnosis_category: "Normal"`

#### Mild DR
- **Clinical Definition**: Microaneurysms only
- **Fundus Features**: Small red dots (microaneurysms)
- **Risk Level**: Very low risk for vision loss
- **Harmonization Mapping**: `diagnosis_category: "Diabetic Retinopathy"`

#### Moderate DR
- **Clinical Definition**: More than microaneurysms but less than severe
- **Fundus Features**: Microaneurysms, hemorrhages, hard exudates
- **Risk Level**: Low to moderate risk
- **Harmonization Mapping**: `diagnosis_category: "Diabetic Retinopathy"`

#### Severe DR
- **Clinical Definition**: Severe non-proliferative diabetic retinopathy
- **Fundus Features**: Extensive hemorrhages, venous beading, IRMA
- **Risk Level**: High risk for progression
- **Harmonization Mapping**: `diagnosis_category: "Diabetic Retinopathy"`

#### Proliferative DR
- **Clinical Definition**: Neovascularization present
- **Fundus Features**: Neovascularization, vitreous hemorrhage, fibrous proliferation
- **Risk Level**: High risk for vision loss
- **Harmonization Mapping**: `diagnosis_category: "Diabetic Retinopathy"`

## Image Specifications

### Technical Parameters

| Parameter | Value | Unit | Description |
|-----------|-------|------|-------------|
| resolution_x | 1024-2048 | pixels | Horizontal resolution |
| resolution_y | 1024-2048 | pixels | Vertical resolution |
| color_depth | 24 | bits | RGB color depth |
| field_of_view | 45 | degrees | Angular field of view |
| compression | JPEG | - | Image compression format |

### Image Quality Metrics

| Metric | Range | Description | Clinical Relevance |
|--------|-------|-------------|-------------------|
| focus_score | 0-1 | Image sharpness assessment | Higher values indicate better focus |
| illumination_score | 0-1 | Lighting adequacy | 1.0 = optimal illumination |
| field_completeness | 0-1 | FOV coverage | 1.0 = complete retinal view |
| media_clarity | 0-1 | Media opacity assessment | 1.0 = clear media |

## Clinical Measurements

### Diabetic Retinopathy Lesions

| Lesion Type | Description | Clinical Significance |
|-------------|-------------|----------------------|
| Microaneurysms | Small red dots | Earliest DR sign |
| Hemorrhages | Flame-shaped or dot hemorrhages | Vascular damage indicator |
| Hard Exudates | Yellow lipid deposits | Macular edema risk |
| Cotton Wool Spots | Nerve fiber layer infarcts | Ischemic damage |
| Venous Beading | Sausage-shaped veins | Severe vascular change |
| IRMA | Intraretinal microvascular abnormalities | Pre-proliferative sign |

### Anatomical Landmarks

| Landmark | Description | DR Assessment Role |
|----------|-------------|-------------------|
| Optic Disc | Optic nerve head | Neovascularization site |
| Macula | Central retina | Edema assessment |
| Major Vessels | Retinal arteries/veins | Vascular changes |
| Mid-periphery | Peripheral retina | Neovascularization detection |

## Harmonization Mappings

### Modality Standardization
```python
MODALITY_MAPPING = {
    "fundus": "Fundus Photography",
    "fundus_photography": "Fundus Photography",
    "retinal_photography": "Fundus Photography"
}
```

### Anatomy Mapping
```python
ANATOMY_MAPPING = {
    "retina": "Retina",
    "optic_disc": "Optic Disc",
    "macula": "Macula",
    "posterior_pole": "Posterior Pole"
}
```

### Diagnosis Category Mapping
```python
DIAGNOSIS_MAPPING = {
    "no_dr": "Normal",
    "mild": "Diabetic Retinopathy",
    "moderate": "Diabetic Retinopathy",
    "severe": "Diabetic Retinopathy",
    "proliferative": "Diabetic Retinopathy"
}
```

### Severity Mapping
```python
SEVERITY_MAPPING = {
    "no_dr": "None",
    "mild": "Mild",
    "moderate": "Moderate",
    "severe": "Severe",
    "proliferative": "Proliferative"
}
```

### Laterality Mapping
```python
LATERALITY_MAPPING = {
    "OD": "Right",
    "OS": "Left",
    "OU": "Both"
}
```

## Data Quality Validation

### Completeness Checks
- All required fields present
- Image files exist and are readable
- Patient IDs are unique and consistent
- Severity levels are valid

### Clinical Validation
- Severity classifications align with fundus features
- Image quality meets screening standards
- Anatomical landmarks are identifiable
- No severe artifacts or media opacity

### Statistical Validation
- Class distribution assessment
- Image quality distribution analysis
- Lesion prevalence validation
- Inter-grader agreement metrics

## Processing Considerations

### Image Preprocessing
- Color normalization for consistent appearance
- Geometric distortion correction
- Illumination compensation
- Contrast enhancement for lesion visibility

### Feature Extraction
- Lesion detection and classification
- Anatomical landmark identification
- Vessel network analysis
- Texture and morphological features

### Quality Control
- Automated quality scoring
- Manual review of borderline cases
- Outlier detection and removal
- Consistency validation across batches

## Integration Notes

### Schema Compatibility
- Maps to harmonized ophthalmology schema
- Supports DR screening workflows
- Enables severity-based stratification
- Facilitates comparative studies

### Pipeline Integration
- DR-specific fundus image loader
- Batch processing for screening volumes
- Quality filtering for clinical use
- Metadata preservation for audit trails

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2023-01-01 | Initial dataset release |
| 1.1 | 2023-06-15 | Quality annotations enhanced |
| 1.2 | 2024-01-20 | Harmonization mappings updated |

## References

### Clinical Standards
- Diabetic retinopathy classification (ETDRS)
- DR screening guidelines (AAO, ADA)
- Image quality standards (NHS DESP)
- Grading protocol standards

### Technical References
- Fundus camera specifications
- Image processing algorithms
- Quality assessment methods
- Standardization protocols