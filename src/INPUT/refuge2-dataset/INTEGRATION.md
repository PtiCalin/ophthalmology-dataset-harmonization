# REFUGE2 Dataset Integration Guide

## Integration Overview

This document describes the process for integrating the REFUGE2 dataset into the ophthalmology data harmonization pipeline. The REFUGE2 dataset contains retinal fundus images with glaucoma annotations that need to be transformed into the standardized harmonized schema.

## Prerequisites

### Software Requirements
- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.20.0
- kagglehub >= 0.1.0 (for automated download)

### Data Access
- Kaggle account with API key configured
- Access to `ferencjuhsz/refuge2-and-refuge2cross-dataset`
- Sufficient disk space for ~2GB of image data

## Data Acquisition

### Automated Download
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download the dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "ferencjuhsz/refuge2-and-refuge2cross-dataset",
    "",  # Load all files
)

print(f"Dataset loaded with {len(df)} records")
```

### Manual Download
1. Visit: https://www.kaggle.com/datasets/ferencjuhsz/refuge2-and-refuge2cross-dataset
2. Download all files to `input/refuge2-dataset/raw/`
3. Extract archives maintaining directory structure

## Data Loading

### Loader Configuration

Create a custom loader for REFUGE2 data:

```python
from src.loaders.universal_loader import UniversalLoader
import pandas as pd

class REFUGE2Loader(UniversalLoader):
    def __init__(self, data_path: str):
        super().__init__(data_path)
        self.dataset_name = "REFUGE2"

    def load_raw_data(self) -> pd.DataFrame:
        """Load REFUGE2 dataset with proper column mapping."""
        # Load clinical annotations
        clinical_df = pd.read_csv(f"{self.data_path}/clinical_annotations.csv")

        # Load image metadata
        image_df = pd.read_csv(f"{self.data_path}/image_metadata.csv")

        # Merge datasets
        merged_df = pd.merge(clinical_df, image_df, on='image_id', how='left')

        return merged_df
```

### Column Mapping

| REFUGE2 Column | Harmonized Field | Transformation Logic |
|----------------|------------------|---------------------|
| image_id | record_id | `lambda x: f"REFUGE2_{x}"` |
| patient_id | patient_id | Direct mapping |
| eye | laterality | `{'OD': 'Right', 'OS': 'Left'}` |
| diagnosis | diagnosis_category | Category normalization |
| severity | severity | Direct mapping |
| cdr | clinical_findings.cup_disc_ratio | Direct mapping |
| quality | image_quality | Direct mapping |

## Harmonization Rules

### Diagnosis Normalization

```python
DIAGNOSIS_MAPPING = {
    'glaucoma': 'Glaucoma',
    'suspect': 'Glaucoma Suspect',
    'normal': 'Normal',
    'other': 'Other Retinal Pathology'
}
```

### Severity Grading

```python
SEVERITY_MAPPING = {
    'mild': 'Mild',
    'moderate': 'Moderate',
    'severe': 'Severe'
}
```

### Clinical Findings Extraction

```python
def extract_clinical_findings(row):
    """Extract clinical measurements into structured format."""
    findings = {}

    # Cup-to-disc ratio
    if pd.notna(row.get('cdr')):
        findings['cup_disc_ratio'] = float(row['cdr'])

    # Rim area measurements
    if pd.notna(row.get('rim_area')):
        findings['rim_area'] = float(row['rim_area'])

    # Vessel density
    if pd.notna(row.get('vessel_density')):
        findings['vessel_density'] = float(row['vessel_density'])

    return findings
```

## Quality Assurance

### Data Validation

```python
def validate_refuge2_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate REFUGE2 data before harmonization."""

    # Check required fields
    required_fields = ['image_id', 'patient_id', 'eye', 'diagnosis']
    missing_data = df[required_fields].isnull().sum()

    if missing_data.any():
        logger.warning(f"Missing data in required fields: {missing_data}")

    # Validate cup-disc ratio range
    invalid_cdr = df[(df['cdr'] < 0) | (df['cdr'] > 1)]
    if len(invalid_cdr) > 0:
        logger.warning(f"Invalid CDR values: {len(invalid_cdr)} records")

    # Validate image quality
    valid_qualities = ['Excellent', 'Good', 'Moderate', 'Poor']
    invalid_quality = df[~df['quality'].isin(valid_qualities)]
    if len(invalid_quality) > 0:
        logger.warning(f"Invalid quality values: {len(invalid_quality)} records")

    return df
```

### Statistical Validation

```python
def generate_quality_report(df: pd.DataFrame) -> dict:
    """Generate quality metrics for REFUGE2 dataset."""

    report = {
        'total_records': len(df),
        'unique_patients': df['patient_id'].nunique(),
        'diagnosis_distribution': df['diagnosis'].value_counts().to_dict(),
        'laterality_distribution': df['eye'].value_counts().to_dict(),
        'quality_distribution': df['quality'].value_counts().to_dict(),
        'cdr_range': {
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

Add REFUGE2 to the harmonization pipeline configuration:

```python
# config/pipeline_config.yaml
datasets:
  - name: REFUGE2
    loader: REFUGE2Loader
    path: "input/refuge2-dataset/"
    validation_rules:
      - validate_required_fields
      - validate_cdr_range
      - validate_image_quality
    harmonization_rules:
      - normalize_diagnosis
      - standardize_laterality
      - extract_clinical_findings
```

### Batch Processing

```python
from src.pipeline.harmonize_all import HarmonizationPipeline

# Initialize pipeline
pipeline = HarmonizationPipeline(config_path="config/pipeline_config.yaml")

# Process REFUGE2 dataset
results = pipeline.process_dataset("REFUGE2")

print(f"Processed {results['records_processed']} records")
print(f"Harmonization quality: {results['quality_score']:.2f}")
```

## Testing and Validation

### Unit Tests

```python
def test_refuge2_loading():
    """Test REFUGE2 data loading functionality."""
    loader = REFUGE2Loader("input/refuge2-dataset/")
    df = loader.load_raw_data()

    assert len(df) > 0, "No data loaded"
    assert 'image_id' in df.columns, "Missing image_id column"
    assert 'diagnosis' in df.columns, "Missing diagnosis column"

def test_refuge2_harmonization():
    """Test REFUGE2 harmonization pipeline."""
    pipeline = HarmonizationPipeline()
    result = pipeline.harmonize_record({
        'image_id': 'REFUGE2_001',
        'eye': 'OD',
        'diagnosis': 'glaucoma',
        'cdr': 0.7
    })

    assert result['laterality'] == 'Right'
    assert result['diagnosis_category'] == 'Glaucoma'
    assert result['clinical_findings']['cup_disc_ratio'] == 0.7
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
    loader = REFUGE2Loader(data_path)
    df = loader.load_raw_data()
    validated_df = validate_refuge2_data(df)
    harmonized_data = pipeline.harmonize_batch(validated_df)
except Exception as e:
    logger.error(f"REFUGE2 integration failed: {e}")
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