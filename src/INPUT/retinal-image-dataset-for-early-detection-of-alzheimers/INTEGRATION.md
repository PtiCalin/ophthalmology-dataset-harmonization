# Retinal Image Dataset for Early Detection of Alzheimer's Integration Guide

## Integration Overview

This document describes the process for integrating the Retinal Image Dataset for Early Detection of Alzheimer's into the ophthalmology data harmonization pipeline. The dataset contains fundus images with neurological diagnoses that need to be transformed into the standardized harmonized schema.

## Prerequisites

### Software Requirements
- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.20.0
- opencv-python >= 4.5.0 (for image processing)
- pillow >= 8.0.0 (for image handling)
- kagglehub >= 0.1.0 (for automated download)

### Data Access
- Kaggle account with API key configured
- Access to retinal Alzheimer's dataset on Kaggle
- Sufficient disk space for high-resolution images

## Data Acquisition

### Automated Download
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download the dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "retinal-alzheimers-dataset-id",  # Replace with actual dataset ID
    "",  # Load all files
)

print(f"Dataset loaded with {len(df)} records")
```

### Manual Download
1. Visit the Kaggle retinal Alzheimer's dataset page
2. Download all files to `input/retinal-image-dataset-for-early-detection-of-alzheimers/raw/`
3. Extract archives maintaining directory structure

## Data Loading

### Loader Configuration

Create a custom loader for Retinal Alzheimer's dataset:

```python
from src.loaders.universal_loader import UniversalLoader
import pandas as pd
import os
from pathlib import Path

class RetinalAlzheimersLoader(UniversalLoader):
    def __init__(self, data_path: str):
        super().__init__(data_path)
        self.dataset_name = "Retinal Alzheimer's Dataset"

    def load_raw_data(self) -> pd.DataFrame:
        """Load Retinal Alzheimer's dataset with proper column mapping."""
        data_records = []

        # Process each diagnosis directory
        diagnosis_dirs = ['alzheimers', 'mci', 'controls', 'other_dementias']

        for diagnosis in diagnosis_dirs:
            diagnosis_path = Path(self.data_path) / diagnosis
            if diagnosis_path.exists():
                for image_file in diagnosis_path.glob('*'):
                    if image_file.suffix.lower() in ['.tiff', '.jpg', '.jpeg', '.png']:
                        # Parse filename: {patient_id}_{eye}_{diagnosis}_{cognitive_score}.tiff
                        filename = image_file.stem
                        parts = filename.split('_')

                        if len(parts) >= 4:
                            patient_id = parts[0]
                            eye = parts[1]
                            diagnosis_type = parts[2]
                            cognitive_score = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None

                            record = {
                                'image_id': f"ALZ_{filename}",
                                'patient_id': f"ALZ_{patient_id}",
                                'eye': eye,
                                'diagnosis': diagnosis_type,
                                'cognitive_score': cognitive_score,
                                'file_path': str(image_file),
                                'file_size': image_file.stat().st_size,
                                'modality': 'Fundus Photography'
                            }
                            data_records.append(record)

        # Load clinical data if available
        clinical_file = Path(self.data_path) / 'clinical_data.csv'
        if clinical_file.exists():
            clinical_df = pd.read_csv(clinical_file)
            # Merge with image data
            image_df = pd.DataFrame(data_records)
            merged_df = pd.merge(image_df, clinical_df, on='patient_id', how='left')
            return merged_df

        return pd.DataFrame(data_records)
```

### Column Mapping

| Retinal Alzheimer's Column | Harmonized Field | Transformation Logic |
|---------------------------|------------------|---------------------|
| image_id | record_id | `lambda x: f"ALZ_{x}"` |
| patient_id | patient_id | `lambda x: f"ALZ_{x}"` |
| eye | laterality | Laterality mapping |
| diagnosis | diagnosis_category | Diagnosis normalization |
| cognitive_score | clinical_findings.cognitive_score | Direct mapping |
| age | demographics.age | Direct mapping |
| gender | demographics.gender | Gender mapping |
| file_path | image_path | Direct mapping |

## Harmonization Rules

### Diagnosis Normalization

```python
DIAGNOSIS_MAPPING = {
    'alzheimers': "Alzheimer's Disease",
    'mci': 'Mild Cognitive Impairment',
    'controls': 'Normal',
    'other_dementias': 'Other Dementia'
}
```

### Laterality Standardization

```python
LATERALITY_MAPPING = {
    'OD': 'Right',
    'OS': 'Left',
    'OU': 'Both'
}
```

### Gender Mapping

```python
GENDER_MAPPING = {
    'M': 'Male',
    'F': 'Female',
    'Male': 'Male',
    'Female': 'Female'
}
```

### Clinical Feature Extraction

```python
def extract_alzheimers_features(row):
    """Extract Alzheimer's-specific clinical features."""
    features = {}

    # Image properties
    if pd.notna(row.get('file_path')):
        features['image_path'] = row['file_path']
        features['file_size'] = row.get('file_size', 0)

    # Acquisition parameters
    features.update({
        'field_of_view': 45,  # degrees, typical for vascular imaging
        'modality': 'Fundus Photography',
        'color_space': 'RGB',
        'vascular_analysis': True  # Flag for vascular-focused imaging
    })

    # Cognitive assessment
    if pd.notna(row.get('cognitive_score')):
        features['cognitive_score'] = int(row['cognitive_score'])
        features['cognitive_assessment_type'] = 'MMSE'  # Assuming MMSE scale

    # Research context
    features['research_context'] = 'Alzheimer\'s Disease Biomarker Research'

    return features
```

## Quality Assurance

### Data Validation

```python
def validate_alzheimers_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate Retinal Alzheimer's data before harmonization."""

    # Check required fields
    required_fields = ['image_id', 'patient_id', 'eye', 'diagnosis']
    missing_data = df[required_fields].isnull().sum()

    if missing_data.any():
        logger.warning(f"Missing data in required fields: {missing_data}")

    # Validate diagnosis categories
    valid_diagnoses = ['alzheimers', 'mci', 'controls', 'other_dementias']
    invalid_diagnosis = df[~df['diagnosis'].isin(valid_diagnoses)]
    if len(invalid_diagnosis) > 0:
        logger.warning(f"Invalid diagnosis values: {len(invalid_diagnosis)} records")

    # Validate cognitive scores
    invalid_scores = df[(df['cognitive_score'] < 0) | (df['cognitive_score'] > 30)]
    if len(invalid_scores) > 0:
        logger.warning(f"Invalid cognitive scores: {len(invalid_scores)} records")

    # Check file existence
    missing_files = df[~df['file_path'].apply(lambda x: os.path.exists(x) if pd.notna(x) else False)]
    if len(missing_files) > 0:
        logger.warning(f"Missing image files: {len(missing_files)} records")

    return df
```

### Statistical Validation

```python
def generate_alzheimers_quality_report(df: pd.DataFrame) -> dict:
    """Generate quality metrics for Retinal Alzheimer's dataset."""

    report = {
        'total_records': len(df),
        'unique_patients': df['patient_id'].nunique(),
        'diagnosis_distribution': df['diagnosis'].value_counts().to_dict(),
        'laterality_distribution': df['eye'].value_counts().to_dict(),
        'age_stats': {
            'min': df['age'].min(),
            'max': df['age'].max(),
            'mean': df['age'].mean(),
            'std': df['age'].std()
        } if 'age' in df.columns else None,
        'cognitive_score_stats': {
            'min': df['cognitive_score'].min(),
            'max': df['cognitive_score'].max(),
            'mean': df['cognitive_score'].mean(),
            'std': df['cognitive_score'].std()
        } if 'cognitive_score' in df.columns else None,
        'missing_files': df['file_path'].isna().sum()
    }

    return report
```

## Pipeline Integration

### Configuration Setup

Add Retinal Alzheimer's dataset to the harmonization pipeline configuration:

```python
# config/pipeline_config.yaml
datasets:
  - name: RetinalAlzheimers
    loader: RetinalAlzheimersLoader
    path: "input/retinal-image-dataset-for-early-detection-of-alzheimers/"
    validation_rules:
      - validate_required_fields
      - validate_diagnosis_categories
      - validate_cognitive_scores
      - validate_file_existence
    harmonization_rules:
      - normalize_diagnosis
      - standardize_laterality
      - map_gender
      - extract_alzheimers_features
```

### Batch Processing

```python
from src.pipeline.harmonize_all import HarmonizationPipeline

# Initialize pipeline
pipeline = HarmonizationPipeline(config_path="config/pipeline_config.yaml")

# Process Retinal Alzheimer's dataset
results = pipeline.process_dataset("RetinalAlzheimers")

print(f"Processed {results['records_processed']} records")
print(f"Harmonization quality: {results['quality_score']:.2f}")
```

## Testing and Validation

### Unit Tests

```python
def test_alzheimers_loading():
    """Test Retinal Alzheimer's data loading functionality."""
    loader = RetinalAlzheimersLoader("input/retinal-image-dataset-for-early-detection-of-alzheimers/")
    df = loader.load_raw_data()

    assert len(df) > 0, "No data loaded"
    assert 'image_id' in df.columns, "Missing image_id column"
    assert 'diagnosis' in df.columns, "Missing diagnosis column"

def test_alzheimers_harmonization():
    """Test Retinal Alzheimer's harmonization pipeline."""
    pipeline = HarmonizationPipeline()
    result = pipeline.harmonize_record({
        'image_id': 'ALZ_AD001_OD_alzheimers_18',
        'eye': 'OD',
        'diagnosis': 'alzheimers',
        'cognitive_score': 18
    })

    assert result['laterality'] == 'Right'
    assert result['diagnosis_category'] == "Alzheimer's Disease"
    assert result['clinical_findings']['cognitive_score'] == 18
```

## Performance Optimization

### Memory Management
- Process images in batches of 500 records
- Load images on-demand rather than preloading
- Use streaming for large datasets
- Implement garbage collection checkpoints

### Parallel Processing
- Utilize multiple cores for image preprocessing
- Parallel validation checks
- Distributed harmonization for large datasets

## Troubleshooting

### Common Issues

1. **High-Resolution Images**
   - Ensure sufficient memory for processing
   - Use image downsampling if needed
   - Implement progressive loading

2. **Clinical Data Integration**
   - Verify patient ID matching
   - Check for data type consistency
   - Validate cognitive score ranges

3. **File Path Issues**
   - Ensure consistent path separators
   - Check file permissions
   - Validate directory structure

### Error Handling

```python
try:
    loader = RetinalAlzheimersLoader(data_path)
    df = loader.load_raw_data()
    validated_df = validate_alzheimers_data(df)
    harmonized_data = pipeline.harmonize_batch(validated_df)
except Exception as e:
    logger.error(f"Retinal Alzheimer's integration failed: {e}")
    raise
```

## Maintenance

### Version Updates
- Monitor dataset for updates
- Update integration code for schema changes
- Revalidate harmonization rules annually

### Documentation Updates
- Update this guide when integration changes
- Document any custom rules or exceptions
- Maintain changelog for integration modifications