"""
Simple Automated Dataset Discovery

A simplified version that works with the existing datasets list.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple configuration
KAGGLE_USER = "ptiCalin"
INPUT_DIR = Path("./INPUT")

def read_existing_datasets() -> List[Dict]:
    """Read datasets from the existing Kagle datasets.txt file."""
    datasets_file = Path("kaggle") / "Kagle datasets.txt"

    datasets = []
    if datasets_file.exists():
        with open(datasets_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse dataset URLs
        import re
        urls = re.findall(r'https://www\.kaggle\.com/datasets/([^/\s]+/[^/\s]+)', content)

        for url in urls:
            owner, dataset_slug = url.split('/')
            datasets.append({
                'owner': owner,
                'dataset_slug': dataset_slug,
                'title': dataset_slug.replace('-', ' ').title(),
                'description': f"Ophthalmology dataset from {owner}",
                'url': f"https://www.kaggle.com/datasets/{url}"
            })

    return datasets

def get_existing_dataset_slugs() -> set:
    """Get slugs of existing datasets."""
    if not INPUT_DIR.exists():
        return set()

    existing = set()
    for item in INPUT_DIR.iterdir():
        if item.is_dir() and item.name not in ['__pycache__']:
            existing.add(item.name)

    return existing

def create_basic_documentation(dataset_dir: Path, dataset: Dict):
    """Create basic documentation files."""

    # DESCRIPTION.md
    desc_content = f"""# {dataset['title']} Description

## Dataset Overview

{dataset.get('description', 'This dataset contains ophthalmology-related data.')}

## Source Information

- **Kaggle URL**: {dataset['url']}
- **Owner**: {dataset['owner']}
- **Dataset Slug**: {dataset['dataset_slug']}

## Data Access

```python
import kagglehub

# Download the dataset
path = kagglehub.dataset_download("{dataset['owner']}/{dataset['dataset_slug']}")
print("Dataset downloaded to:", path)
```

## Integration Notes

*This dataset was automatically discovered. Manual review and completion of clinical documentation is recommended.*
"""

    with open(dataset_dir / "DESCRIPTION.md", 'w', encoding='utf-8') as f:
        f.write(desc_content)

    # CODEBOOK.md
    codebook_content = f"""# {dataset['title']} Codebook

## Overview

This codebook provides specifications for the {dataset['title']} dataset.

## Dataset Schema

### Primary Fields

| Field Name | Data Type | Description | Required |
|------------|-----------|-------------|----------|
| image_id | string | Unique identifier | Yes |
| dataset_source | string | Source identifier | Yes |

## Notes

This codebook was automatically generated. Please review and complete with dataset-specific information.
"""

    with open(dataset_dir / "CODEBOOK.md", 'w', encoding='utf-8') as f:
        f.write(codebook_content)

    # INTEGRATION.md
    integration_content = f"""# {dataset['title']} Integration Guide

## Data Acquisition

```python
import kagglehub

dataset_path = kagglehub.dataset_download("{dataset['owner']}/{dataset['dataset_slug']}")
print("Dataset downloaded to:", dataset_path)
```

## Notes

This integration guide was automatically generated. Please review and complete with dataset-specific integration logic.
"""

    with open(dataset_dir / "INTEGRATION.md", 'w', encoding='utf-8') as f:
        f.write(integration_content)

def update_input_md(new_datasets: List[Dict]):
    """Update INPUT.md with new datasets."""
    input_md = INPUT_DIR / "INPUT.md"

    if not input_md.exists():
        logger.warning("INPUT.md not found")
        return

    with open(input_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find insertion point
    marker = "### Documentation Pending Datasets"
    if marker not in content:
        logger.warning("Could not find insertion point in INPUT.md")
        return

    # Create new entries
    new_entries = []
    for dataset in new_datasets:
        entry = f"""- **{dataset['title']}** (`{dataset['dataset_slug']}/`)
  - {dataset.get('description', 'Ophthalmology dataset').split('.')[0]}
  - Status: Documentation auto-generated, manual review pending"""
        new_entries.append(entry)

    # Insert entries
    insert_point = content.find(marker) + len(marker)
    insert_content = "\n\n" + "\n\n".join(new_entries) + "\n\n"

    updated_content = content[:insert_point] + insert_content + content[insert_point:]

    with open(input_md, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    logger.info(f"Updated INPUT.md with {len(new_entries)} entries")

def discover_and_document(dry_run: bool = False) -> List[Dict]:
    """Main discovery function."""
    logger.info("Starting automated dataset discovery")

    # Read all available datasets
    all_datasets = read_existing_datasets()
    logger.info(f"Found {len(all_datasets)} datasets in source")

    # Get existing datasets
    existing_slugs = get_existing_dataset_slugs()
    logger.info(f"Found {len(existing_slugs)} existing datasets")

    # Filter for new datasets
    new_datasets = [
        dataset for dataset in all_datasets
        if dataset['dataset_slug'] not in existing_slugs
    ]

    if not new_datasets:
        logger.info("No new datasets found")
        return []

    if dry_run:
        logger.info(f"Dry run: Would process {len(new_datasets)} datasets:")
        for dataset in new_datasets:
            print(f"  - {dataset['title']} ({dataset['dataset_slug']})")
        return new_datasets

    # Process new datasets
    processed = []
    for dataset in new_datasets:
        try:
            dataset_slug = dataset['dataset_slug']
            dataset_dir = INPUT_DIR / dataset_slug

            # Create directory
            dataset_dir.mkdir(parents=True, exist_ok=True)
            (dataset_dir / "raw").mkdir(exist_ok=True)

            # Create documentation
            create_basic_documentation(dataset_dir, dataset)

            processed.append(dataset)
            logger.info(f"Processed: {dataset_slug}")

        except Exception as e:
            logger.error(f"Failed to process {dataset['dataset_slug']}: {e}")

    # Update registry
    if processed:
        update_input_md(processed)

    logger.info(f"Discovery complete. Processed {len(processed)} datasets")
    return processed

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple dataset discovery")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")

    args = parser.parse_args()
    discover_and_document(dry_run=args.dry_run)