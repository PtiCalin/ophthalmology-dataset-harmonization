# Retinal OCT Images Dataset Codebook

## Overview

This codebook provides detailed specifications for the Retinal OCT Images dataset, including field definitions, value ranges, clinical interpretations, and harmonization mappings for integration into the ophthalmology data harmonization pipeline.

## Dataset Schema

### Primary Fields

| Field Name | Data Type | Description | Required | Validation Rules |
|------------|-----------|-------------|----------|------------------|
| image_id | string | Unique identifier for each OCT image | Yes | Format: `{class}_{patient_id}_{slice_number}` |
| patient_id | string | Anonymous patient identifier | Yes | Unique per patient |
| class | categorical | Diagnostic category | Yes | CNV, DME, DRUSEN, NORMAL |
| slice_number | integer | B-scan slice number within volume | Yes | Range: 1-61 |
| volume_id | string | OCT volume identifier | No | Groups slices from same scan |

## Clinical Classifications

### Diagnosis Categories

#### CNV (Choroidal Neovascularization)

- **Clinical Definition**: Abnormal growth of new blood vessels from the choroid into the subretinal space
- **Associated Conditions**: Age-related macular degeneration (AMD), pathological myopia
- **OCT Features**: Subretinal fluid, pigment epithelial detachment, hyperreflective foci
- **Harmonization Mapping**: `diagnosis_category: "Choroidal Neovascularization"`

#### DME (Diabetic Macular Edema)

- **Clinical Definition**: Accumulation of fluid in the macula due to diabetic retinopathy
- **Associated Conditions**: Diabetes mellitus, diabetic retinopathy
- **OCT Features**: Intraretinal cysts, subretinal fluid, thickened retina
- **Harmonization Mapping**: `diagnosis_category: "Diabetic Macular Edema"`

#### DRUSEN

- **Clinical Definition**: Extracellular deposits between retinal pigment epithelium and Bruch's membrane
- **Associated Conditions**: Early age-related macular degeneration
- **OCT Features**: Dome-shaped elevations, hyperreflective deposits
- **Harmonization Mapping**: `diagnosis_category: "Drusen"`

#### NORMAL

- **Clinical Definition**: Healthy retinal structure without pathological changes
- **Associated Conditions**: None
- **OCT Features**: Normal retinal layer architecture, no fluid accumulation
- **Harmonization Mapping**: `diagnosis_category: "Normal"`

## Image Specifications

### Technical Parameters

| Parameter | Value | Unit | Description |
|-----------|-------|------|-------------|
| resolution_x | 512 | pixels | Horizontal resolution |
| resolution_y | 496 | pixels | Vertical resolution |
| bit_depth | 8 | bits | Grayscale depth |
| wavelength | 840 | nm | OCT light source wavelength |
| field_of_view | 6x6 | mm | Scan area dimensions |
| axial_resolution | 5 | μm | Depth resolution |
| transverse_resolution | 15 | μm | Lateral resolution |

### Image Quality Metrics

| Metric | Range | Description | Clinical Relevance |
|--------|-------|-------------|-------------------|
| signal_strength | 0-100 | OCT signal quality | Higher values indicate better image quality |
| motion_artifacts | 0-5 | Motion artifact severity | 0 = none, 5 = severe |
| segmentation_quality | 0-1 | Automated layer segmentation accuracy | 1.0 = perfect segmentation |

## Clinical Measurements

### Retinal Layer Thickness

| Layer | Normal Range (μm) | Measurement Method |
|-------|-------------------|-------------------|
| Total Retina | 200-350 | ILM to RPE |
| Inner Retina | 80-120 | ILM to INL |
| Outer Retina | 120-230 | INL to RPE |
| Choroid | 150-300 | RPE to choroid-sclera junction |

### Pathological Features

#### Fluid Detection

- **Intraretinal Fluid**: Cystic spaces within retinal layers
- **Subretinal Fluid**: Fluid accumulation between retina and RPE
- **Pigment Epithelial Detachment**: Separation of RPE from Bruch's membrane

#### Structural Abnormalities

- **Hyperreflective Foci**: Bright spots indicating inflammation or degeneration
- **Atrophic Changes**: Thinning of retinal layers
- **Neovascular Complexes**: Abnormal vessel growth patterns

## Harmonization Mappings

### Modality Standardization

```python
MODALITY_MAPPING = {
    "OCT": "Optical Coherence Tomography",
    "oct": "Optical Coherence Tomography",
    "optical_coherence_tomography": "Optical Coherence Tomography"
}
```

### Anatomy Mapping

```python
ANATOMY_MAPPING = {
    "retina": "Retina",
    "macula": "Macula",
    "choroid": "Choroid",
    "retinal_pigment_epithelium": "Retinal Pigment Epithelium"
}
```

### Diagnosis Category Mapping

```python
DIAGNOSIS_MAPPING = {
    "CNV": "Choroidal Neovascularization",
    "DME": "Diabetic Macular Edema",
    "DRUSEN": "Drusen",
    "NORMAL": "Normal"
}
```

### Laterality Inference

```python
# OCT volumes typically include both eyes
LATERALITY_INFERENCE = {
    "OD": "Right",
    "OS": "Left",
    "OU": "Both",
    "unknown": "Unknown"
}
```

## Data Quality Validation

### Completeness Checks

- All required fields present
- Image files exist and are readable
- Patient IDs are unique and consistent
- Class labels match expected categories

### Clinical Validation

- Diagnosis categories align with OCT features
- Image quality meets minimum standards
- Anatomical landmarks are identifiable
- No severe artifacts or corruption

### Statistical Validation

- Class distribution balance assessment
- Image quality distribution analysis
- Clinical measurement range validation
- Inter-class feature separation metrics

## Processing Considerations

### Image Preprocessing

- Normalization to standard intensity range
- Motion artifact correction
- Registration across slices
- Noise reduction filtering

### Feature Extraction

- Retinal layer segmentation
- Thickness measurements
- Fluid quantification
- Morphological analysis

### Quality Control

- Automated quality scoring
- Manual review of ambiguous cases
- Outlier detection and removal
- Consistency validation across volumes

## Integration Notes

### Schema Compatibility

- Maps to harmonized ophthalmology schema
- Supports multi-modal integration
- Enables longitudinal analysis
- Facilitates comparative studies

### Pipeline Integration

- Custom loader for OCT volumes
- Batch processing for large datasets
- Quality filtering options
- Metadata preservation

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2018-01-01 | Initial dataset release |
| 1.1 | 2020-06-15 | Quality annotations added |
| 1.2 | 2023-03-20 | Harmonization mappings updated |

## References

### Clinical Standards

- OCT imaging protocols (ISOOCT guidelines)
- Retinal layer nomenclature (ISOOCT)
- Disease classification systems (AAO, Euretina)

### Technical References

- OCT device specifications
- Image processing algorithms
- Quality assessment methods