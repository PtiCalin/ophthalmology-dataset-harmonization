"""
Configuration for automated dataset discovery and integration.
"""

# Kaggle API Configuration
KAGGLE_CONFIG = {
    "username": "ptiCalin",  # Replace with your Kaggle username
    "collection_keywords": [
        "ophthalmology", "retina", "fundus", "oct", "eye", "ocular",
        "diabetic retinopathy", "glaucoma", "macular degeneration",
        "retinal", "optical coherence tomography"
    ],
    "exclude_keywords": [
        "non-medical", "synthetic", "generated", "test", "demo"
    ]
}

# Documentation Templates
DESCRIPTION_TEMPLATE = """# {title} Description

## Dataset Overview

{description}

## Source Information

- **Kaggle URL**: https://www.kaggle.com/datasets/{owner}/{dataset_slug}
- **Owner**: {owner}
- **Dataset Slug**: {dataset_slug}
- **Last Updated**: {last_updated}
- **Size**: {size}
- **Downloads**: {downloads}

## Dataset Characteristics

### Basic Information

- **Tags**: {tags}
- **License**: {license}
- **File Types**: {file_types}

### Clinical Context

*This section should be completed with specific clinical information about the dataset's purpose and medical applications.*

## Data Access

```python
import kagglehub

# Download the dataset
path = kagglehub.dataset_download("{owner}/{dataset_slug}")
print("Dataset downloaded to:", path)
```

## Integration Notes

*This dataset was automatically discovered and added to the harmonization pipeline. Manual review and completion of clinical documentation is recommended.*
"""

CODEBOOK_TEMPLATE = """# {title} Codebook

## Overview

This codebook provides specifications for the {title} dataset. Field definitions should be reviewed and completed with specific clinical and technical details.

## Dataset Schema

### Primary Fields

| Field Name | Data Type | Description | Required | Validation Rules |
|------------|-----------|-------------|----------|------------------|
| image_id | string | Unique identifier for each image | Yes | Auto-generated |
| patient_id | string | Anonymous patient identifier | No | If available |
| dataset_source | string | Source dataset identifier | Yes | "{dataset_slug}" |

## Technical Specifications

### Image Specifications

- **Modality**: *To be determined from dataset inspection*
- **Format**: *To be determined from dataset inspection*
- **Resolution**: *To be determined from dataset inspection*

## Harmonization Mappings

*Mappings to the standardized harmonized schema should be defined here.*

## Notes

This codebook was automatically generated. Please review and complete with dataset-specific information.
"""

INTEGRATION_TEMPLATE = """# {title} Integration Guide

## Integration Overview

This document describes the process for integrating {title} into the ophthalmology data harmonization pipeline.

## Prerequisites

### Software Requirements
- Python 3.8+
- pandas >= 1.3.0
- kagglehub >= 0.1.0

### Data Access
- Kaggle account with API key configured
- Access to {owner}/{dataset_slug} on Kaggle

## Data Acquisition

```python
import kagglehub

# Download the dataset
dataset_path = kagglehub.dataset_download("{owner}/{dataset_slug}")
print("Dataset downloaded to:", dataset_path)
```

## Data Loading

```python
from src.loaders.universal_loader import UniversalLoader

# Create loader instance
loader = UniversalLoader("{dataset_slug}")

# Load and harmonize data
# harmonized_df = loader.load_and_harmonize(raw_df)
```

## Notes

This integration guide was automatically generated. Please review and complete with dataset-specific integration logic.
"""

# Directory Structure
DIRECTORIES = {
    "input_base": "./INPUT",
    "raw_data": "raw"
}</content>
<parameter name="filePath">c:\Users\charl\OneDrive\Projets\ophthalmology-dataset-harmonization\src\pipeline\config.py