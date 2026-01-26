# Retina Dataset Codebook

## Overview

This codebook provides detailed specifications for the Retina Dataset, including field definitions, value ranges, clinical interpretations, and harmonization mappings for integration into the ophthalmology data harmonization pipeline.

## Dataset Schema

### Primary Fields

| Field Name | Data Type | Description | Required | Validation Rules |
|------------|-----------|-------------|----------|------------------|
| image_id | string | Unique identifier for each fundus image | Yes | Format: `{patient_id}_{eye}_{condition}_{severity}` |
| patient_id | string | Anonymous patient identifier | Yes | Unique per patient |
| eye | categorical | Eye laterality | Yes | OD, OS |
| condition | categorical | Primary diagnosis category | Yes | normal, diabetic_retinopathy, glaucoma, amd, other |
| severity | categorical | Disease severity level | No | mild, moderate, severe, proliferative |
| image_quality | integer | Subjective quality score | No | Range: 1-5 (5 = excellent) |

## Clinical Classifications

### Diagnosis Categories

#### Normal

- **Clinical Definition**: Healthy retina without pathological changes
- **Associated Conditions**: None
- **Fundus Features**: Normal optic disc, macula, and vessels
- **Harmonization Mapping**: `diagnosis_category: "Normal"`

#### Diabetic Retinopathy (DR)

- **Clinical Definition**: Microvascular complications of diabetes affecting the retina
- **Associated Conditions**: Diabetes mellitus
- **Fundus Features**: Microaneurysms, hemorrhages, exudates, neovascularization
- **Harmonization Mapping**: `diagnosis_category: "Diabetic Retinopathy"`

#### Glaucoma

- **Clinical Definition**: Progressive optic neuropathy with characteristic disc changes
- **Associated Conditions**: Elevated intraocular pressure, family history
- **Fundus Features**: Optic disc cupping, retinal nerve fiber layer defects
- **Harmonization Mapping**: `diagnosis_category: "Glaucoma"`

#### Age-Related Macular Degeneration (AMD)

- **Clinical Definition**: Degenerative changes in the macula
- **Associated Conditions**: Age, genetics, smoking
- **Fundus Features**: Drusen, pigment changes, geographic atrophy, neovascularization
- **Harmonization Mapping**: `diagnosis_category: "Age-Related Macular Degeneration"`

#### Other Pathologies

- **Clinical Definition**: Various other retinal conditions
- **Associated Conditions**: Multiple etiologies
- **Fundus Features**: Variable depending on specific pathology
- **Harmonization Mapping**: `diagnosis_category: "Other Retinal Pathology"`

## Image Specifications

### Technical Parameters

| Parameter | Value/Range | Unit | Description |
|-----------|-------------|------|-------------|
| resolution_x | 1024-3072 | pixels | Horizontal resolution |
| resolution_y | 1024-2048 | pixels | Vertical resolution |
| color_depth | 24 | bits | RGB color depth |
| field_of_view | 30-60 | degrees | Angular field of view |
| compression | JPEG/PNG | - | Image compression format |

### Image Quality Metrics

| Metric | Range | Description | Clinical Relevance |
|--------|-------|-------------|-------------------|
| focus_score | 0-1 | Image sharpness assessment | Higher values indicate better focus |
| illumination_uniformity | 0-1 | Lighting consistency | 1.0 = perfectly uniform |
| field_completeness | 0-1 | FOV coverage | 1.0 = complete retinal view |
| artifact_score | 0-5 | Artifact severity | 0 = no artifacts, 5 = severe |

## Clinical Measurements

### Anatomical Landmarks

| Landmark | Description | Clinical Significance |
|----------|-------------|----------------------|
| Optic Disc | Entrance of optic nerve | Glaucoma assessment, CDR measurement |
| Macula | Central retina | AMD, DR evaluation |
| Fovea | Center of macula | Visual acuity assessment |
| Major Vessels | Retinal arteries/veins | Vascular pathology detection |

### Pathological Features

#### Diabetic Retinopathy Lesions

- **Microaneurysms**: Small red dots, earliest DR sign
- **Hemorrhages**: Flame-shaped or dot hemorrhages
- **Hard Exudates**: Yellow lipid deposits
- **Cotton Wool Spots**: Nerve fiber layer infarcts

#### Glaucoma Features

- **Cup-to-Disc Ratio**: Vertical C/D ratio > 0.6 suspicious
- **Neuroretinal Rim**: Thinning of rim tissue
- **Retinal Nerve Fiber Layer**: Wedge defects
- **Disc Hemorrhages**: Splinter hemorrhages

#### AMD Features

- **Drusen**: Yellow deposits under RPE
- **Pigment Changes**: Hyper/hypopigmentation
- **Geographic Atrophy**: Well-defined areas of RPE loss
- **Neovascularization**: Choroidal new vessels

## Harmonization Mappings

### Modality Standardization

```python
MODALITY_MAPPING = {
    "fundus": "Fundus Photography",
    "fundus_photography": "Fundus Photography",
    "retinal_imaging": "Fundus Photography"
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
    "normal": "Normal",
    "diabetic_retinopathy": "Diabetic Retinopathy",
    "glaucoma": "Glaucoma",
    "amd": "Age-Related Macular Degeneration",
    "other": "Other Retinal Pathology"
}
```

### Laterality Mapping

```python
LATERALITY_MAPPING = {
    "OD": "Right",
    "OS": "Left",
    "OU": "Both",
    "right": "Right",
    "left": "Left"
}
```

### Severity Mapping

```python
SEVERITY_MAPPING = {
    "mild": "Mild",
    "moderate": "Moderate",
    "severe": "Severe",
    "proliferative": "Proliferative"
}
```

## Data Quality Validation

### Completeness Checks

- All required fields present
- Image files exist and are readable
- Patient IDs are unique and consistent
- Diagnosis categories are valid

### Clinical Validation

- Diagnosis categories align with fundus features
- Image quality meets minimum standards
- Anatomical landmarks are identifiable
- No severe artifacts or corruption

### Statistical Validation

- Class distribution balance assessment
- Image quality distribution analysis
- Clinical feature prevalence validation
- Inter-class feature separation metrics

## Processing Considerations

### Image Preprocessing

- Color normalization across devices
- Geometric distortion correction
- Illumination compensation
- Noise reduction and enhancement

### Feature Extraction

- Anatomical landmark detection
- Lesion segmentation and classification
- Vessel network analysis
- Texture and morphological features

### Quality Control

- Automated quality scoring
- Manual review of ambiguous cases
- Outlier detection and removal
- Consistency validation across batches

## Integration Notes

### Schema Compatibility

- Maps to harmonized ophthalmology schema
- Supports multi-modal integration
- Enables longitudinal analysis
- Facilitates comparative studies

### Pipeline Integration

- Standard fundus image loader
- Batch processing for large datasets
- Quality filtering options
- Metadata preservation

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2023-01-01 | Initial dataset compilation |
| 1.1 | 2023-06-15 | Quality annotations added |
| 1.2 | 2024-01-20 | Harmonization mappings updated |

## References

### Clinical Standards

- Diabetic retinopathy classification (ETDRS)
- Glaucoma staging (Hodapp-Parrish-Anderson)
- AMD classification (AREDS)
- Fundus imaging protocols

### Technical References

- Fundus camera specifications
- Image processing algorithms
- Quality assessment methods
- Standardization protocols