# Retinal Disease Detection Dataset Integration Guide

## Integration Overview

This document describes the process for integrating the Retinal Disease Detection dataset into the ophthalmology data harmonization pipeline. The dataset contains retinal fundus images with multi-class disease annotations that need to be transformed into the standardized harmonized schema.

## Prerequisites

### Software Requirements
- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.20.0
- kagglehub >= 0.1.0 (for automated download)

### Data Access
- Kaggle account with API key configured
- Access to `mohamedabdalkader/retinal-disease-detection`
- Sufficient disk space for dataset storage

## Data Acquisition

### Automated Download
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download the dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "mohamedabdalkader/retinal-disease-detection",
    "",  # Load all files
)

print(f"Dataset loaded with {len(df)} records")
```

### Manual Download
1. Visit: https://www.kaggle.com/datasets/mohamedabdalkader/retinal-disease-detection
2. Download all files to `input/retinal-disease-detection-dataset/raw/`
3. Extract archives maintaining directory structure

## Data Loading

### Loader Configuration

Create a custom loader for Retinal Disease Detection data:

```python
from src.loaders.universal_loader import UniversalLoader
import pandas as pd

class RetinalDiseaseDetectionLoader(UniversalLoader):
    def __init__(self, data_path: str):
        super().__init__(data_path)
        self.dataset_name = "Retinal Disease Detection"

    def load_raw_data(self) -> pd.DataFrame:
        """Load Retinal Disease Detection dataset with proper column mapping."""
        # Load clinical annotations
        clinical_df = pd.read_csv(f"{self.data_path}/clinical_annotations.csv")

        # Load image metadata
        image_df = pd.read_csv(f"{self.data_path}/image_metadata.csv")

        # Merge datasets
        merged_df = pd.merge(clinical_df, image_df, on='image_id', how='left')

        return merged_df
```

### Column Mapping

| Retinal Disease Detection Column | Harmonized Field | Transformation Logic |
|-----------------------------------|------------------|---------------------|
| image_id | record_id | `lambda x: f"RDD_{x}"` |
| patient_id | patient_id | Direct mapping |
| eye | laterality | `{'OD': 'Right', 'OS': 'Left'}` |
| diagnosis | diagnosis_category | Category normalization |
| secondary_diagnosis | secondary_diagnosis | Direct mapping |
| severity | severity | Direct mapping |
| cdr | clinical_findings.cup_disc_ratio | Direct mapping |
| image_quality | image_quality | Direct mapping |

## Harmonization Rules

### Diagnosis Normalization

```python
DIAGNOSIS_MAPPING = {
    'diabetic_retinopathy': 'Diabetic Retinopathy',
    'glaucoma': 'Glaucoma',
    'amd': 'Age-Related Macular Degeneration',
    'hypertensive_retinopathy': 'Hypertensive Retinopathy',
    'rvo': 'Retinal Vein Occlusion',
    'normal': 'Normal',
    'other': 'Other Retinal Pathology'
}
```

### Multi-class Classification Handling

```python
def handle_multi_class_diagnosis(row):
    """Handle primary and secondary diagnoses."""
    primary = normalize_diagnosis(row.get('diagnosis', ''))

    findings = []
    if primary:
        findings.append(primary)

    secondary = row.get('secondary_diagnosis')
    if secondary:
        secondary_normalized = normalize_diagnosis(secondary)
        if secondary_normalized and secondary_normalized != primary:
            findings.append(secondary_normalized)

    return findings
```

### Clinical Findings Extraction

```python
def extract_clinical_findings(row):
    """Extract clinical measurements into structured format."""
    findings = {}

    # Cup-to-disc ratio
    if pd.notna(row.get('cdr')):
        findings['cup_disc_ratio'] = float(row['cdr'])

    # Retinal thickness
    if pd.notna(row.get('retinal_thickness')):
        findings['retinal_thickness'] = float(row['retinal_thickness'])

    # Vessel density
    if pd.notna(row.get('vessel_density')):
        findings['vessel_density'] = float(row['vessel_density'])

    # Lesion count
    if pd.notna(row.get('lesion_count')):
        findings['lesion_count'] = int(row['lesion_count'])

    return findings
```

## Quality Assurance

### Data Validation

```python
def validate_retinal_disease_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate Retinal Disease Detection data before harmonization."""

    # Check required fields
    required_fields = ['image_id', 'patient_id', 'eye', 'diagnosis']
    missing_data = df[required_fields].isnull().sum()

    if missing_data.any():
        logger.warning(f"Missing data in required fields: {missing_data}")

    # Validate cup-disc ratio range
    invalid_cdr = df[(df['cdr'] < 0) | (df['cdr'] > 1)]
    if len(invalid_cdr) > 0:
        logger.warning(f"Invalid CDR values: {len(invalid_cdr)} records")

    # Validate diagnosis categories
    valid_diagnoses = ['Diabetic Retinopathy', 'Glaucoma', 'AMD',
                      'Hypertensive Retinopathy', 'RVO', 'Normal', 'Other']
    invalid_diagnosis = df[~df['diagnosis'].isin(valid_diagnoses)]
    if len(invalid_diagnosis) > 0:
        logger.warning(f"Invalid diagnosis values: {len(invalid_diagnosis)} records")

    return df
```

### Statistical Validation

```python
def generate_quality_report(df: pd.DataFrame) -> dict:
    """Generate quality metrics for Retinal Disease Detection dataset."""

    report = {
        'total_records': len(df),
        'unique_patients': df['patient_id'].nunique(),
        'diagnosis_distribution': df['diagnosis'].value_counts().to_dict(),
        'laterality_distribution': df['eye'].value_counts().to_dict(),
        'severity_distribution': df['severity'].value_counts().to_dict(),
        'quality_distribution': df['image_quality'].value_counts().to_dict(),
        'cdr_stats': {
            'min': df['cdr'].min(),
            'max': df['cdr'].max(),
            'mean': df['cdr'].mean(),
            'std': df['cdr'].std()
        }
    }

    return report
```

## Pipeline Integration

### Configuration Setup

Add Retinal Disease Detection to the harmonization pipeline configuration:

```python
# config/pipeline_config.yaml
datasets:
  - name: RetinalDiseaseDetection
    loader: RetinalDiseaseDetectionLoader
    path: "input/retinal-disease-detection-dataset/"
    validation_rules:
      - validate_required_fields
      - validate_cdr_range
      - validate_diagnosis_categories
    harmonization_rules:
      - normalize_diagnosis
      - handle_multi_class_diagnosis
      - standardize_laterality
      - extract_clinical_findings
```

### Batch Processing

```python
from src.pipeline.harmonize_all import HarmonizationPipeline

# Initialize pipeline
pipeline = HarmonizationPipeline(config_path="config/pipeline_config.yaml")

# Process Retinal Disease Detection dataset
results = pipeline.process_dataset("RetinalDiseaseDetection")

print(f"Processed {results['records_processed']} records")
print(f"Harmonization quality: {results['quality_score']:.2f}")
```

## Testing and Validation

### Unit Tests

```python
def test_retinal_disease_loading():
    """Test Retinal Disease Detection data loading functionality."""
    loader = RetinalDiseaseDetectionLoader("input/retinal-disease-detection-dataset/")
    df = loader.load_raw_data()

    assert len(df) > 0, "No data loaded"
    assert 'image_id' in df.columns, "Missing image_id column"
    assert 'diagnosis' in df.columns, "Missing diagnosis column"

def test_retinal_disease_harmonization():
    """Test Retinal Disease Detection harmonization pipeline."""
    pipeline = HarmonizationPipeline()
    result = pipeline.harmonize_record({
        'image_id': 'RDD_001',
        'eye': 'OD',
        'diagnosis': 'diabetic_retinopathy',
        'cdr': 0.6
    })

    assert result['laterality'] == 'Right'
    assert result['diagnosis_category'] == 'Diabetic Retinopathy'
    assert result['clinical_findings']['cup_disc_ratio'] == 0.6
```

## Performance Optimization

### Memory Management
- Process images in batches of 1000 records
- Use streaming for large datasets
- Implement garbage collection checkpoints

### Parallel Processing
- Utilize multiple cores for image preprocessing
- Parallel validation checks
- Distributed harmonization for large datasets

## Troubleshooting

### Common Issues

1. **Kaggle API Authentication**
   - Ensure `~/.kaggle/kaggle.json` exists
   - Check API key permissions

2. **Memory Errors**
   - Reduce batch size in configuration
   - Use streaming data loading

3. **Data Quality Issues**
   - Run validation report first
   - Check for encoding issues in CSV files

### Error Handling

```python
try:
    loader = RetinalDiseaseDetectionLoader(data_path)
    df = loader.load_raw_data()
    validated_df = validate_retinal_disease_data(df)
    harmonized_data = pipeline.harmonize_batch(validated_df)
except Exception as e:
    logger.error(f"Retinal Disease Detection integration failed: {e}")
    raise
```

## Maintenance

### Version Updates
- Monitor Kaggle dataset for updates
- Update integration code for schema changes
- Revalidate harmonization rules annually

### Documentation Updates
- Update this guide when integration changes
- Document any custom rules or exceptions
- Maintain changelog for integration modifications