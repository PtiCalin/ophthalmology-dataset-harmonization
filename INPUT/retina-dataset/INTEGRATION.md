# Retina Dataset Integration Guide

## Integration Overview

This document describes the process for integrating the Retina Dataset into the ophthalmology data harmonization pipeline. The dataset contains retinal fundus images with multiple pathology classifications that need to be transformed into the standardized harmonized schema.

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
- Access to retina dataset on Kaggle
- Sufficient disk space for fundus images

## Data Acquisition

### Automated Download
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download the dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "retina-dataset-identifier",  # Replace with actual dataset ID
    "",  # Load all files
)

print(f"Dataset loaded with {len(df)} records")
```

### Manual Download
1. Visit the Kaggle retina dataset page
2. Download all files to `input/retina-dataset/raw/`
3. Extract archives maintaining directory structure

## Data Loading

### Loader Configuration

Create a custom loader for Retina Dataset:

```python
from src.loaders.universal_loader import UniversalLoader
import pandas as pd
import os
from pathlib import Path

class RetinaDatasetLoader(UniversalLoader):
    def __init__(self, data_path: str):
        super().__init__(data_path)
        self.dataset_name = "Retina Dataset"

    def load_raw_data(self) -> pd.DataFrame:
        """Load Retina Dataset with proper column mapping."""
        data_records = []

        # Process each condition directory
        condition_dirs = ['normal', 'diabetic_retinopathy', 'glaucoma', 'amd', 'other']

        for condition in condition_dirs:
            condition_path = Path(self.data_path) / condition
            if condition_path.exists():
                for image_file in condition_path.glob('*'):
                    if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        # Parse filename: {patient_id}_{eye}_{condition}_{severity}.jpg
                        filename = image_file.stem
                        parts = filename.split('_')

                        if len(parts) >= 4:
                            patient_id = parts[0]
                            eye = parts[1]
                            condition_name = parts[2]
                            severity = parts[3] if len(parts) > 3 else None

                            record = {
                                'image_id': f"RETINA_{filename}",
                                'patient_id': f"RETINA_{patient_id}",
                                'eye': eye,
                                'condition': condition_name,
                                'severity': severity,
                                'file_path': str(image_file),
                                'file_size': image_file.stat().st_size,
                                'modality': 'Fundus Photography'
                            }
                            data_records.append(record)

        # Load metadata if available
        metadata_file = Path(self.data_path) / 'metadata.csv'
        if metadata_file.exists():
            metadata_df = pd.read_csv(metadata_file)
            # Merge with image data
            image_df = pd.DataFrame(data_records)
            merged_df = pd.merge(image_df, metadata_df, on='image_id', how='left')
            return merged_df

        return pd.DataFrame(data_records)
```

### Column Mapping

| Retina Dataset Column | Harmonized Field | Transformation Logic |
|----------------------|------------------|---------------------|
| image_id | record_id | `lambda x: f"RETINA_{x}"` |
| patient_id | patient_id | `lambda x: f"RETINA_{x}"` |
| eye | laterality | Laterality mapping |
| condition | diagnosis_category | Diagnosis normalization |
| severity | severity | Severity mapping |
| file_path | image_path | Direct mapping |
| modality | modality | `{'Fundus Photography': 'Fundus Photography'}` |

## Harmonization Rules

### Diagnosis Normalization

```python
DIAGNOSIS_MAPPING = {
    'normal': 'Normal',
    'diabetic_retinopathy': 'Diabetic Retinopathy',
    'glaucoma': 'Glaucoma',
    'amd': 'Age-Related Macular Degeneration',
    'other': 'Other Retinal Pathology'
}
```

### Laterality Standardization

```python
LATERALITY_MAPPING = {
    'OD': 'Right',
    'OS': 'Left',
    'OU': 'Both',
    'right': 'Right',
    'left': 'Left'
}
```

### Severity Classification

```python
SEVERITY_MAPPING = {
    'mild': 'Mild',
    'moderate': 'Moderate',
    'severe': 'Severe',
    'proliferative': 'Proliferative'
}
```

### Clinical Feature Extraction

```python
def extract_fundus_features(row):
    """Extract fundus-specific clinical features."""
    features = {}

    # Image properties
    if pd.notna(row.get('file_path')):
        features['image_path'] = row['file_path']
        features['file_size'] = row.get('file_size', 0)

    # Acquisition parameters
    features.update({
        'field_of_view': 45,  # degrees, typical value
        'modality': 'Fundus Photography',
        'color_space': 'RGB'
    })

    # Quality assessment (would require image analysis)
    features['image_quality'] = row.get('image_quality', 3)  # Default medium quality

    return features
```

## Quality Assurance

### Data Validation

```python
def validate_retina_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate Retina Dataset data before harmonization."""

    # Check required fields
    required_fields = ['image_id', 'patient_id', 'eye', 'condition']
    missing_data = df[required_fields].isnull().sum()

    if missing_data.any():
        logger.warning(f"Missing data in required fields: {missing_data}")

    # Validate diagnosis categories
    valid_conditions = ['normal', 'diabetic_retinopathy', 'glaucoma', 'amd', 'other']
    invalid_condition = df[~df['condition'].isin(valid_conditions)]
    if len(invalid_condition) > 0:
        logger.warning(f"Invalid condition values: {len(invalid_condition)} records")

    # Validate laterality
    valid_eyes = ['OD', 'OS', 'OU']
    invalid_eye = df[~df['eye'].isin(valid_eyes)]
    if len(invalid_eye) > 0:
        logger.warning(f"Invalid eye values: {len(invalid_eye)} records")

    # Check file existence
    missing_files = df[~df['file_path'].apply(lambda x: os.path.exists(x) if pd.notna(x) else False)]
    if len(missing_files) > 0:
        logger.warning(f"Missing image files: {len(missing_files)} records")

    return df
```

### Statistical Validation

```python
def generate_retina_quality_report(df: pd.DataFrame) -> dict:
    """Generate quality metrics for Retina Dataset."""

    report = {
        'total_records': len(df),
        'unique_patients': df['patient_id'].nunique(),
        'condition_distribution': df['condition'].value_counts().to_dict(),
        'laterality_distribution': df['eye'].value_counts().to_dict(),
        'severity_distribution': df['severity'].value_counts().to_dict(),
        'file_size_stats': {
            'min': df['file_size'].min(),
            'max': df['file_size'].max(),
            'mean': df['file_size'].mean(),
            'std': df['file_size'].std()
        },
        'missing_files': df['file_path'].isna().sum()
    }

    return report
```

## Pipeline Integration

### Configuration Setup

Add Retina Dataset to the harmonization pipeline configuration:

```python
# config/pipeline_config.yaml
datasets:
  - name: RetinaDataset
    loader: RetinaDatasetLoader
    path: "input/retina-dataset/"
    validation_rules:
      - validate_required_fields
      - validate_condition_categories
      - validate_laterality
      - validate_file_existence
    harmonization_rules:
      - normalize_diagnosis
      - standardize_laterality
      - map_severity
      - extract_fundus_features
```

### Batch Processing

```python
from src.pipeline.harmonize_all import HarmonizationPipeline

# Initialize pipeline
pipeline = HarmonizationPipeline(config_path="config/pipeline_config.yaml")

# Process Retina Dataset
results = pipeline.process_dataset("RetinaDataset")

print(f"Processed {results['records_processed']} records")
print(f"Harmonization quality: {results['quality_score']:.2f}")
```

## Testing and Validation

### Unit Tests

```python
def test_retina_loading():
    """Test Retina Dataset data loading functionality."""
    loader = RetinaDatasetLoader("input/retina-dataset/")
    df = loader.load_raw_data()

    assert len(df) > 0, "No data loaded"
    assert 'image_id' in df.columns, "Missing image_id column"
    assert 'condition' in df.columns, "Missing condition column"

def test_retina_harmonization():
    """Test Retina Dataset harmonization pipeline."""
    pipeline = HarmonizationPipeline()
    result = pipeline.harmonize_record({
        'image_id': 'RETINA_P001_OD_normal_mild',
        'eye': 'OD',
        'condition': 'normal',
        'severity': 'mild'
    })

    assert result['laterality'] == 'Right'
    assert result['diagnosis_category'] == 'Normal'
    assert result['severity'] == 'Mild'
```

## Performance Optimization

### Memory Management
- Process images in batches of 1000 records
- Load images on-demand rather than preloading
- Use streaming for large datasets
- Implement garbage collection checkpoints

### Parallel Processing
- Utilize multiple cores for image preprocessing
- Parallel validation checks
- Distributed harmonization for large datasets

## Troubleshooting

### Common Issues

1. **Large Dataset Size**
   - Process in smaller batches
   - Use external storage for images
   - Implement lazy loading

2. **File Path Issues**
   - Ensure consistent path separators
   - Check file permissions
   - Validate directory structure

3. **Memory Errors**
   - Reduce batch size in configuration
   - Use streaming data loading
   - Process one condition at a time

### Error Handling

```python
try:
    loader = RetinaDatasetLoader(data_path)
    df = loader.load_raw_data()
    validated_df = validate_retina_data(df)
    harmonized_data = pipeline.harmonize_batch(validated_df)
except Exception as e:
    logger.error(f"Retina Dataset integration failed: {e}")
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