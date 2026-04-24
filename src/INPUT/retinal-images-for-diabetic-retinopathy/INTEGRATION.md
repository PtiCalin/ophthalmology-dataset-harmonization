# Retinal Images for Diabetic Retinopathy Integration Guide

## Integration Overview

This document describes the process for integrating the Retinal Images for Diabetic Retinopathy dataset into the ophthalmology data harmonization pipeline. The dataset contains fundus photographs with DR severity classifications that need to be transformed into the standardized harmonized schema.

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
- Access to retinal DR images dataset on Kaggle
- Sufficient disk space for fundus images

## Data Acquisition

### Automated Download

```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download the dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "retinal-dr-images-dataset-id",  # Replace with actual dataset ID
    "",  # Load all files
)

print(f"Dataset loaded with {len(df)} records")
```

### Manual Download

1. Visit the Kaggle retinal DR images dataset page
2. Download all files to `input/retinal-images-for-diabetic-retinopathy/raw/`
3. Extract archives maintaining directory structure

## Data Loading

### Loader Configuration

Create a custom loader for Retinal DR Images dataset:

```python
from src.loaders.universal_loader import UniversalLoader
import pandas as pd
import os
from pathlib import Path

class RetinalDRLoader(UniversalLoader):
    def __init__(self, data_path: str):
        super().__init__(data_path)
        self.dataset_name = "Retinal DR Images"

    def load_raw_data(self) -> pd.DataFrame:
        """Load Retinal DR Images dataset with proper column mapping."""
        data_records = []

        # Process each severity directory
        severity_dirs = ['no_dr', 'mild', 'moderate', 'severe', 'proliferative']

        for severity in severity_dirs:
            severity_path = Path(self.data_path) / severity
            if severity_path.exists():
                for image_file in severity_path.glob('*'):
                    if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        # Parse filename: {patient_id}_{eye}_{severity}_{grader}_{date}.jpg
                        filename = image_file.stem
                        parts = filename.split('_')

                        if len(parts) >= 5:
                            patient_id = parts[0]
                            eye = parts[1]
                            severity_level = parts[2]
                            grader = parts[3]
                            date_str = parts[4]

                            record = {
                                'image_id': f"DR_{filename}",
                                'patient_id': f"DR_{patient_id}",
                                'eye': eye,
                                'severity': severity_level,
                                'grader': grader,
                                'grading_date': date_str,
                                'file_path': str(image_file),
                                'file_size': image_file.stat().st_size,
                                'modality': 'Fundus Photography'
                            }
                            data_records.append(record)

        # Load annotations if available
        annotations_file = Path(self.data_path) / 'annotations.csv'
        if annotations_file.exists():
            annotations_df = pd.read_csv(annotations_file)
            # Merge with image data
            image_df = pd.DataFrame(data_records)
            merged_df = pd.merge(image_df, annotations_df, on='image_id', how='left')
            return merged_df

        return pd.DataFrame(data_records)
```

### Column Mapping

| Retinal DR Column | Harmonized Field | Transformation Logic |
|-------------------|------------------|---------------------|
| image_id | record_id | `lambda x: f"DR_{x}"` |
| patient_id | patient_id | `lambda x: f"DR_{x}"` |
| eye | laterality | Laterality mapping |
| severity | diagnosis_category | Diagnosis normalization |
| severity | severity | Severity mapping |
| grader | clinical_findings.grader | Direct mapping |
| grading_date | clinical_findings.grading_date | Date parsing |
| file_path | image_path | Direct mapping |

## Harmonization Rules

### Diagnosis Normalization

```python
DIAGNOSIS_MAPPING = {
    'no_dr': 'Normal',
    'mild': 'Diabetic Retinopathy',
    'moderate': 'Diabetic Retinopathy',
    'severe': 'Diabetic Retinopathy',
    'proliferative': 'Diabetic Retinopathy'
}
```

### Severity Classification

```python
SEVERITY_MAPPING = {
    'no_dr': 'None',
    'mild': 'Mild',
    'moderate': 'Moderate',
    'severe': 'Severe',
    'proliferative': 'Proliferative'
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

### Clinical Feature Extraction

```python
def extract_dr_screening_features(row):
    """Extract DR screening-specific clinical features."""
    features = {}

    # Image properties
    if pd.notna(row.get('file_path')):
        features['image_path'] = row['file_path']
        features['file_size'] = row.get('file_size', 0)

    # Acquisition parameters
    features.update({
        'field_of_view': 45,  # degrees
        'modality': 'Fundus Photography',
        'color_space': 'RGB'
    })

    # Screening context
    features['screening_context'] = 'Diabetic Retinopathy Screening'
    features['image_quality'] = row.get('image_quality', 3)  # Default medium quality

    # Grading information
    if pd.notna(row.get('grader')):
        features['grader_id'] = row['grader']
        features['grading_date'] = row.get('grading_date')

    return features
```

## Quality Assurance

### Data Validation

```python
def validate_dr_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate Retinal DR Images data before harmonization."""

    # Check required fields
    required_fields = ['image_id', 'patient_id', 'eye', 'severity']
    missing_data = df[required_fields].isnull().sum()

    if missing_data.any():
        logger.warning(f"Missing data in required fields: {missing_data}")

    # Validate severity levels
    valid_severities = ['no_dr', 'mild', 'moderate', 'severe', 'proliferative']
    invalid_severity = df[~df['severity'].isin(valid_severities)]
    if len(invalid_severity) > 0:
        logger.warning(f"Invalid severity values: {len(invalid_severity)} records")

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
def generate_dr_quality_report(df: pd.DataFrame) -> dict:
    """Generate quality metrics for Retinal DR Images dataset."""

    report = {
        'total_records': len(df),
        'unique_patients': df['patient_id'].nunique(),
        'severity_distribution': df['severity'].value_counts().to_dict(),
        'laterality_distribution': df['eye'].value_counts().to_dict(),
        'grader_distribution': df['grader'].value_counts().to_dict() if 'grader' in df.columns else None,
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

Add Retinal DR Images to the harmonization pipeline configuration:

```python
# config/pipeline_config.yaml
datasets:
  - name: RetinalDR
    loader: RetinalDRLoader
    path: "input/retinal-images-for-diabetic-retinopathy/"
    validation_rules:
      - validate_required_fields
      - validate_severity_levels
      - validate_laterality
      - validate_file_existence
    harmonization_rules:
      - normalize_diagnosis
      - standardize_laterality
      - map_severity
      - extract_dr_screening_features
```

### Batch Processing

```python
from src.pipeline.harmonize_all import HarmonizationPipeline

# Initialize pipeline
pipeline = HarmonizationPipeline(config_path="config/pipeline_config.yaml")

# Process Retinal DR Images dataset
results = pipeline.process_dataset("RetinalDR")

print(f"Processed {results['records_processed']} records")
print(f"Harmonization quality: {results['quality_score']:.2f}")
```

## Testing and Validation

### Unit Tests

```python
def test_dr_loading():
    """Test Retinal DR Images data loading functionality."""
    loader = RetinalDRLoader("input/retinal-images-for-diabetic-retinopathy/")
    df = loader.load_raw_data()

    assert len(df) > 0, "No data loaded"
    assert 'image_id' in df.columns, "Missing image_id column"
    assert 'severity' in df.columns, "Missing severity column"

def test_dr_harmonization():
    """Test Retinal DR Images harmonization pipeline."""
    pipeline = HarmonizationPipeline()
    result = pipeline.harmonize_record({
        'image_id': 'DR_P001_OD_mild_grader1_20231201',
        'eye': 'OD',
        'severity': 'mild'
    })

    assert result['laterality'] == 'Right'
    assert result['diagnosis_category'] == 'Diabetic Retinopathy'
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
   - Process one severity level at a time

### Error Handling

```python
try:
    loader = RetinalDRLoader(data_path)
    df = loader.load_raw_data()
    validated_df = validate_dr_data(df)
    harmonized_data = pipeline.harmonize_batch(validated_df)
except Exception as e:
    logger.error(f"Retinal DR Images integration failed: {e}")
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