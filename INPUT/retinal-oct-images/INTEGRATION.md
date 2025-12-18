# Retinal OCT Images Dataset Integration Guide

## Integration Overview

This document describes the process for integrating the Retinal OCT Images dataset into the ophthalmology data harmonization pipeline. The dataset contains optical coherence tomography (OCT) scans classified into CNV, DME, DRUSEN, and NORMAL categories that need to be transformed into the standardized harmonized schema.

## Prerequisites

### Software Requirements
- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.20.0
- opencv-python >= 4.5.0 (for image processing)
- kagglehub >= 0.1.0 (for automated download)

### Data Access
- Kaggle account with API key configured
- Access to `paultimothymooney/kermany2018`
- Sufficient disk space for OCT image volumes

## Data Acquisition

### Automated Download
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download the dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "paultimothymooney/kermany2018",
    "",  # Load all files
)

print(f"Dataset loaded with {len(df)} records")
```

### Manual Download
1. Visit: https://www.kaggle.com/datasets/paultimothymooney/kermany2018
2. Download all files to `input/retinal-oct-images/raw/`
3. Extract archives maintaining directory structure

## Data Loading

### Loader Configuration

Create a custom loader for Retinal OCT Images data:

```python
from src.loaders.universal_loader import UniversalLoader
import pandas as pd
import os
from pathlib import Path

class RetinalOCTLoader(UniversalLoader):
    def __init__(self, data_path: str):
        super().__init__(data_path)
        self.dataset_name = "Retinal OCT Images"

    def load_raw_data(self) -> pd.DataFrame:
        """Load Retinal OCT Images dataset with proper column mapping."""
        data_records = []

        # Process each class directory
        class_dirs = ['CNV', 'DME', 'DRUSEN', 'NORMAL']

        for class_name in class_dirs:
            class_path = Path(self.data_path) / class_name
            if class_path.exists():
                for image_file in class_path.glob('*.tiff'):
                    # Parse filename: {class}_{patient_id}_{slice_number}.tiff
                    filename = image_file.stem
                    parts = filename.split('_')

                    if len(parts) >= 3:
                        diagnosis_class = parts[0]
                        patient_id = parts[1]
                        slice_number = int(parts[2])

                        record = {
                            'image_id': f"OCT_{filename}",
                            'patient_id': f"OCT_{patient_id}",
                            'class': diagnosis_class,
                            'slice_number': slice_number,
                            'volume_id': f"OCT_{patient_id}",
                            'file_path': str(image_file),
                            'file_size': image_file.stat().st_size,
                            'modality': 'OCT'
                        }
                        data_records.append(record)

        return pd.DataFrame(data_records)
```

### Column Mapping

| Retinal OCT Column | Harmonized Field | Transformation Logic |
|-------------------|------------------|---------------------|
| image_id | record_id | `lambda x: f"OCT_{x}"` |
| patient_id | patient_id | `lambda x: f"OCT_{x}"` |
| class | diagnosis_category | Category normalization |
| slice_number | clinical_findings.slice_number | Direct mapping |
| volume_id | clinical_findings.volume_id | Direct mapping |
| file_path | image_path | Direct mapping |
| modality | modality | `{'OCT': 'Optical Coherence Tomography'}` |

## Harmonization Rules

### Diagnosis Normalization

```python
DIAGNOSIS_MAPPING = {
    'CNV': 'Choroidal Neovascularization',
    'DME': 'Diabetic Macular Edema',
    'DRUSEN': 'Drusen',
    'NORMAL': 'Normal'
}
```

### OCT-Specific Processing

```python
def extract_oct_metadata(row):
    """Extract OCT-specific metadata and measurements."""
    metadata = {}

    # Volume information
    if pd.notna(row.get('volume_id')):
        metadata['volume_id'] = row['volume_id']

    # Slice information
    if pd.notna(row.get('slice_number')):
        metadata['slice_number'] = int(row['slice_number'])
        metadata['total_slices'] = 61  # Standard OCT volume

    # Image properties
    if pd.notna(row.get('file_path')):
        metadata['image_path'] = row['file_path']
        metadata['file_size'] = row.get('file_size', 0)

    # OCT acquisition parameters
    metadata.update({
        'wavelength': 840,  # nm
        'field_of_view': '6x6',  # mm
        'axial_resolution': 5,  # μm
        'transverse_resolution': 15,  # μm
        'scan_pattern': 'raster'
    })

    return metadata
```

### Quality Assessment

```python
def assess_oct_quality(row):
    """Assess OCT image quality based on file and metadata."""
    quality_score = 1.0  # Default high quality

    # Check file size (proxy for image quality)
    file_size = row.get('file_size', 0)
    if file_size < 10000:  # Very small files may be corrupted
        quality_score = 0.3
    elif file_size < 50000:  # Small files may have compression artifacts
        quality_score = 0.7

    # Check for motion artifacts in filename or metadata
    # (This would require image analysis in production)

    return quality_score
```

## Quality Assurance

### Data Validation

```python
def validate_oct_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate Retinal OCT Images data before harmonization."""

    # Check required fields
    required_fields = ['image_id', 'patient_id', 'class']
    missing_data = df[required_fields].isnull().sum()

    if missing_data.any():
        logger.warning(f"Missing data in required fields: {missing_data}")

    # Validate diagnosis categories
    valid_classes = ['CNV', 'DME', 'DRUSEN', 'NORMAL']
    invalid_class = df[~df['class'].isin(valid_classes)]
    if len(invalid_class) > 0:
        logger.warning(f"Invalid class values: {len(invalid_class)} records")

    # Check file existence
    missing_files = df[~df['file_path'].apply(lambda x: os.path.exists(x) if pd.notna(x) else False)]
    if len(missing_files) > 0:
        logger.warning(f"Missing image files: {len(missing_files)} records")

    return df
```

### Statistical Validation

```python
def generate_oct_quality_report(df: pd.DataFrame) -> dict:
    """Generate quality metrics for Retinal OCT Images dataset."""

    report = {
        'total_records': len(df),
        'unique_patients': df['patient_id'].nunique(),
        'unique_volumes': df['volume_id'].nunique(),
        'class_distribution': df['class'].value_counts().to_dict(),
        'slices_per_volume': df.groupby('volume_id')['slice_number'].count().describe().to_dict(),
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

Add Retinal OCT Images to the harmonization pipeline configuration:

```python
# config/pipeline_config.yaml
datasets:
  - name: RetinalOCT
    loader: RetinalOCTLoader
    path: "input/retinal-oct-images/"
    validation_rules:
      - validate_required_fields
      - validate_class_categories
      - validate_file_existence
    harmonization_rules:
      - normalize_diagnosis
      - extract_oct_metadata
      - assess_oct_quality
      - standardize_modality
```

### Batch Processing

```python
from src.pipeline.harmonize_all import HarmonizationPipeline

# Initialize pipeline
pipeline = HarmonizationPipeline(config_path="config/pipeline_config.yaml")

# Process Retinal OCT Images dataset
results = pipeline.process_dataset("RetinalOCT")

print(f"Processed {results['records_processed']} records")
print(f"Harmonization quality: {results['quality_score']:.2f}")
```

## Testing and Validation

### Unit Tests

```python
def test_oct_loading():
    """Test Retinal OCT Images data loading functionality."""
    loader = RetinalOCTLoader("input/retinal-oct-images/")
    df = loader.load_raw_data()

    assert len(df) > 0, "No data loaded"
    assert 'image_id' in df.columns, "Missing image_id column"
    assert 'class' in df.columns, "Missing class column"

def test_oct_harmonization():
    """Test Retinal OCT Images harmonization pipeline."""
    pipeline = HarmonizationPipeline()
    result = pipeline.harmonize_record({
        'image_id': 'OCT_CNV_001_031',
        'class': 'CNV',
        'slice_number': 31,
        'volume_id': 'OCT_001'
    })

    assert result['diagnosis_category'] == 'Choroidal Neovascularization'
    assert result['modality'] == 'Optical Coherence Tomography'
    assert result['clinical_findings']['slice_number'] == 31
```

## Performance Optimization

### Memory Management
- Process images in batches of 500 records
- Load images on-demand rather than preloading
- Use streaming for large volumes
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
   - Process one class at a time

### Error Handling

```python
try:
    loader = RetinalOCTLoader(data_path)
    df = loader.load_raw_data()
    validated_df = validate_oct_data(df)
    harmonized_data = pipeline.harmonize_batch(validated_df)
except Exception as e:
    logger.error(f"Retinal OCT Images integration failed: {e}")
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