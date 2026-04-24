# Retinal Image Dataset for Early Detection of Alzheimer's Codebook

## Overview

This codebook provides detailed specifications for the Retinal Image Dataset for Early Detection of Alzheimer's, including field definitions, value ranges, clinical interpretations, and harmonization mappings for integration into the ophthalmology data harmonization pipeline.

## Dataset Schema

### Primary Fields

| Field Name | Data Type | Description | Required | Validation Rules |
|------------|-----------|-------------|----------|------------------|
| image_id | string | Unique identifier for each fundus image | Yes | Format: `{patient_id}_{eye}_{diagnosis}_{cognitive_score}` |
| patient_id | string | Anonymous patient identifier | Yes | Unique per patient |
| eye | categorical | Eye laterality | Yes | OD, OS |
| diagnosis | categorical | Neurological diagnosis | Yes | alzheimers, mci, controls, other_dementias |
| cognitive_score | integer | Cognitive assessment score | No | Range: 0-30 (MMSE scale) |
| age | integer | Patient age at imaging | No | Range: 50-100 |
| gender | categorical | Patient gender | No | M, F |

## Clinical Classifications

### Neurological Diagnoses

#### Alzheimer's Disease
- **Clinical Definition**: Confirmed Alzheimer's disease diagnosis
- **Cognitive Features**: Progressive memory loss, cognitive decline
- **Retinal Features**: Potential vascular changes, reduced vessel density
- **Harmonization Mapping**: `diagnosis_category: "Alzheimer's Disease"`

#### Mild Cognitive Impairment (MCI)
- **Clinical Definition**: Early cognitive changes not meeting dementia criteria
- **Cognitive Features**: Subjective memory complaints, mild deficits
- **Retinal Features**: Early vascular changes, subtle vessel alterations
- **Harmonization Mapping**: `diagnosis_category: "Mild Cognitive Impairment"`

#### Healthy Controls
- **Clinical Definition**: Age-matched healthy individuals without cognitive impairment
- **Cognitive Features**: Normal cognitive function
- **Retinal Features**: Normal vascular architecture
- **Harmonization Mapping**: `diagnosis_category: "Normal"`

#### Other Dementias
- **Clinical Definition**: Non-Alzheimer's neurodegenerative conditions
- **Cognitive Features**: Various dementia syndromes
- **Retinal Features**: Disease-specific vascular patterns
- **Harmonization Mapping**: `diagnosis_category: "Other Dementia"`

## Image Specifications

### Technical Parameters

| Parameter | Value/Range | Unit | Description |
|-----------|-------------|------|-------------|
| resolution_x | 2048-4096 | pixels | Horizontal resolution |
| resolution_y | 2048-4096 | pixels | Vertical resolution |
| color_depth | 24 | bits | RGB color depth |
| field_of_view | 30-50 | degrees | Angular field of view |
| compression | TIFF/JPEG | - | Image compression format |

### Image Quality Metrics

| Metric | Range | Description | Clinical Relevance |
|--------|-------|-------------|-------------------|
| vessel_contrast | 0-1 | Vessel visibility quality | Higher values for better vascular analysis |
| media_clarity | 0-1 | Media opacity assessment | 1.0 = clear media for vessel analysis |
| motion_artifacts | 0-5 | Movement artifact severity | 0 = no artifacts |
| focus_quality | 0-1 | Image sharpness | 1.0 = perfectly focused |

## Clinical Measurements

### Cognitive Assessments

| Assessment | Scale | Normal Range | Clinical Significance |
|------------|-------|--------------|----------------------|
| MMSE | 0-30 | 24-30 | General cognitive function |
| MoCA | 0-30 | 26-30 | Executive function assessment |
| CDR | 0-3 | 0 | Dementia severity staging |

### Vascular Biomarkers

| Biomarker | Measurement | Clinical Relevance |
|-----------|-------------|-------------------|
| Vessel Density | % area | Retinal perfusion assessment |
| Vessel Tortuosity | Index | Vascular health indicator |
| Branching Pattern | Complexity | Microvascular architecture |
| Capillary Dropout | Regions | Ischemic damage assessment |

### Anatomical Features

| Feature | Description | AD Relevance |
|---------|-------------|-------------|
| Optic Disc | Nerve head morphology | Potential glaucomatous changes |
| Macula | Central retina | Age-related changes |
| Vascular Arcades | Major vessels | Atherosclerotic changes |
| Periphery | Peripheral retina | Microvascular disease |

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
    "vascular_network": "Retinal Vasculature",
    "optic_disc": "Optic Disc",
    "macula": "Macula"
}
```

### Diagnosis Category Mapping
```python
DIAGNOSIS_MAPPING = {
    "alzheimers": "Alzheimer's Disease",
    "mci": "Mild Cognitive Impairment",
    "controls": "Normal",
    "other_dementias": "Other Dementia"
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
- Diagnosis categories are valid

### Clinical Validation
- Diagnosis categories align with cognitive assessments
- Image quality meets vascular analysis standards
- Anatomical landmarks are identifiable
- No severe artifacts affecting vessel analysis

### Statistical Validation
- Age and gender distribution balance
- Cognitive score distribution analysis
- Diagnosis prevalence validation
- Inter-observer agreement metrics

## Processing Considerations

### Image Preprocessing
- Vessel enhancement algorithms
- Color normalization for consistent analysis
- Geometric distortion correction
- Contrast optimization for vascular features

### Feature Extraction
- Vessel segmentation and analysis
- Morphological measurements
- Texture analysis of vascular patterns
- Anatomical landmark detection

### Quality Control
- Automated quality scoring for vascular analysis
- Manual review of ambiguous cases
- Outlier detection and removal
- Consistency validation across batches

## Integration Notes

### Schema Compatibility
- Maps to harmonized ophthalmology schema
- Supports neurological diagnosis integration
- Enables vascular biomarker research
- Facilitates multi-disciplinary studies

### Pipeline Integration
- Alzheimer's-specific fundus image loader
- Vascular analysis pipeline integration
- Cognitive assessment correlation
- Metadata preservation for research

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2023-01-01 | Initial dataset release |
| 1.1 | 2023-06-15 | Cognitive assessment data added |
| 1.2 | 2024-01-20 | Harmonization mappings updated |

## References

### Clinical Standards
- Alzheimer's disease diagnosis (NIA-AA criteria)
- Cognitive assessment standards (MMSE, MoCA)
- Retinal vascular imaging protocols
- Neurodegenerative disease classification

### Technical References
- Fundus camera specifications for vascular imaging
- Vessel analysis algorithms
- Image processing for retinal biomarkers
- Quality assessment methods