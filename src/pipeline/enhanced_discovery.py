"""
Enhanced Automated Dataset Discovery and Documentation Generator

This script automatically discovers new ophthalmology datasets from Kaggle
and creates the necessary documentation structure for integration.

Features:
- Searches Kaggle for ophthalmology-related datasets
- Filters datasets by relevance keywords
- Automatically generates documentation templates
- Updates the INPUT.md registry
- Can be run periodically to discover new datasets

USAGE:
    python -m src.pipeline.enhanced_discovery
    python -c "from src.pipeline.enhanced_discovery import discover_and_document; discover_and_document()"
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Set
import logging
from datetime import datetime
import re

try:
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    print("Warning: kagglehub not available. Install with: pip install kagglehub")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .config import KAGGLE_CONFIG, DESCRIPTION_TEMPLATE, CODEBOOK_TEMPLATE, INTEGRATION_TEMPLATE, DIRECTORIES

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KaggleAPISearch:
    """Enhanced Kaggle dataset search using API and web scraping."""

    def __init__(self):
        self.base_url = "https://www.kaggle.com/api/v1"
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
        self._setup_auth()

    def _setup_auth(self):
        """Set up authentication."""
        if not REQUESTS_AVAILABLE:
            return

        api_key = os.getenv('KAGGLE_API_TOKEN')
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})

    def search_datasets(self, query: str = "", user: str = "", tags: List[str] = None,
                       max_results: int = 100) -> List[Dict]:
        """
        Search for datasets on Kaggle.

        Args:
            query: Search query string
            user: Specific user to search (optional)
            tags: List of tags to filter by
            max_results: Maximum number of results to return

        Returns:
            List of dataset metadata dictionaries
        """
        if not REQUESTS_AVAILABLE:
            logger.warning("requests not available, using fallback method")
            return self._fallback_search(query, user)

        datasets = []

        try:
            # Use Kaggle API search
            search_url = f"{self.base_url}/datasets/list"
            params = {
                'search': query,
                'user': user,
                'sortBy': 'hotness',
                'group': 'public',
                'maxSize': max_results
            }

            if tags:
                params['tags'] = ','.join(tags)

            response = self.session.get(search_url, params=params)
            response.raise_for_status()

            data = response.json()
            datasets = self._parse_api_response(data)

        except Exception as e:
            logger.warning(f"API search failed: {e}, using fallback")
            datasets = self._fallback_search(query, user)

        return datasets[:max_results]

    def _parse_api_response(self, data: List[Dict]) -> List[Dict]:
        """Parse Kaggle API response into standardized format."""
        datasets = []

        for item in data:
            dataset = {
                'owner': item.get('ownerName', item.get('owner', {}).get('name', '')),
                'dataset_slug': item.get('slug', item.get('datasetSlug', '')),
                'title': item.get('title', item.get('name', '')),
                'description': item.get('description', ''),
                'tags': [tag.get('name', '') for tag in item.get('tags', [])],
                'size': item.get('totalSize', 'Unknown'),
                'downloads': item.get('downloadCount', 0),
                'last_updated': item.get('lastUpdated', ''),
                'license': item.get('licenseName', 'Unknown'),
                'url': f"https://www.kaggle.com/datasets/{item.get('ownerName', '')}/{item.get('slug', '')}",
                'file_types': self._extract_file_types(item)
            }
            datasets.append(dataset)

        return datasets

    def _extract_file_types(self, item: Dict) -> List[str]:
        """Extract file types from dataset metadata."""
        file_types = set()

        # Check file extensions in the dataset
        files = item.get('files', [])
        for file_info in files:
            name = file_info.get('name', '')
            if '.' in name:
                ext = name.split('.')[-1].lower()
                file_types.add(ext)

        return list(file_types)

    def _fallback_search(self, query: str, user: str) -> List[Dict]:
        """Fallback search method using local data."""
        logger.info("Using fallback search method")

        # Read from existing datasets file
        datasets_file = Path(__file__).parent.parent.parent / "kaggle" / "Kagle datasets.txt"

        datasets = []
        if datasets_file.exists():
            with open(datasets_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse URLs and create basic metadata
            urls = re.findall(r'https://www\.kaggle\.com/datasets/([^/\s]+/[^/\s]+)', content)

            for url in urls:
                owner, dataset_slug = url.split('/')
                datasets.append({
                    'owner': owner,
                    'dataset_slug': dataset_slug,
                    'title': dataset_slug.replace('-', ' ').title(),
                    'description': f"Ophthalmology dataset from {owner}",
                    'tags': ['ophthalmology'],
                    'size': 'Unknown',
                    'downloads': 0,
                    'last_updated': datetime.now().isoformat(),
                    'license': 'Unknown',
                    'url': f"https://www.kaggle.com/datasets/{url}",
                    'file_types': []
                })

        return datasets


class OphthalmologyDatasetFilter:
    """Filters datasets for ophthalmology relevance."""

    def __init__(self):
        self.include_keywords = KAGGLE_CONFIG['collection_keywords']
        self.exclude_keywords = KAGGLE_CONFIG['exclude_keywords']

    def is_ophthalmology_dataset(self, dataset: Dict) -> bool:
        """Check if a dataset is ophthalmology-related."""
        text_to_check = ' '.join([
            dataset.get('title', ''),
            dataset.get('description', ''),
            ' '.join(dataset.get('tags', [])),
            dataset.get('dataset_slug', '')
        ]).lower()

        # Check for inclusion keywords
        has_include = any(keyword.lower() in text_to_check for keyword in self.include_keywords)

        # Check for exclusion keywords
        has_exclude = any(keyword.lower() in text_to_check for keyword in self.exclude_keywords)

        return has_include and not has_exclude


class EnhancedDatasetDiscoverer:
    """Enhanced dataset discovery with intelligent filtering."""

    def __init__(self, kaggle_user: str = None):
        self.kaggle_user = kaggle_user or KAGGLE_CONFIG['username']
        self.search_api = KaggleAPISearch()
        self.filter = OphthalmologyDatasetFilter()
        self.input_dir = Path(DIRECTORIES['input_base'])

    def discover_new_datasets(self) -> List[Dict]:
        """Discover new ophthalmology datasets."""
        logger.info(f"Searching for ophthalmology datasets by user: {self.kaggle_user}")

        # Search for datasets
        all_datasets = self.search_api.search_datasets(
            user=self.kaggle_user,
            max_results=200
        )

        # Filter for ophthalmology relevance
        ophthalmology_datasets = [
            dataset for dataset in all_datasets
            if self.filter.is_ophthalmology_dataset(dataset)
        ]

        logger.info(f"Found {len(ophthalmology_datasets)} ophthalmology-related datasets")

        # Filter out existing datasets
        existing_slugs = self._get_existing_dataset_slugs()
        new_datasets = [
            dataset for dataset in ophthalmology_datasets
            if dataset['dataset_slug'] not in existing_slugs
        ]

        logger.info(f"Found {len(new_datasets)} new datasets to process")
        return new_datasets

    def _get_existing_dataset_slugs(self) -> Set[str]:
        """Get slugs of existing datasets."""
        if not self.input_dir.exists():
            return set()

        existing = set()
        for item in self.input_dir.iterdir():
            if item.is_dir() and item.name not in ['__pycache__']:
                existing.add(item.name)

        return existing


class EnhancedDocumentationGenerator:
    """Enhanced documentation generator with better templates."""

    def __init__(self):
        self.input_dir = Path(DIRECTORIES['input_base'])

    def generate_dataset_documentation(self, dataset: Dict) -> Path:
        """Generate complete documentation for a dataset."""
        dataset_slug = dataset['dataset_slug']
        dataset_dir = self.input_dir / dataset_slug

        # Create directory structure
        dataset_dir.mkdir(parents=True, exist_ok=True)
        (dataset_dir / DIRECTORIES['raw_data']).mkdir(exist_ok=True)

        # Generate documentation files
        self._generate_description(dataset_dir, dataset)
        self._generate_codebook(dataset_dir, dataset)
        self._generate_integration(dataset_dir, dataset)

        logger.info(f"Generated documentation for {dataset_slug}")
        return dataset_dir

    def _generate_description(self, dataset_dir: Path, dataset: Dict):
        """Generate DESCRIPTION.md."""
        content = DESCRIPTION_TEMPLATE.format(**dataset)
        with open(dataset_dir / "DESCRIPTION.md", 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_codebook(self, dataset_dir: Path, dataset: Dict):
        """Generate CODEBOOK.md."""
        content = CODEBOOK_TEMPLATE.format(**dataset)
        with open(dataset_dir / "CODEBOOK.md", 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_integration(self, dataset_dir: Path, dataset: Dict):
        """Generate INTEGRATION.md."""
        content = INTEGRATION_TEMPLATE.format(**dataset)
        with open(dataset_dir / "INTEGRATION.md", 'w', encoding='utf-8') as f:
            f.write(content)


def discover_and_document(dry_run: bool = False) -> List[Dict]:
    """
    Main function to discover and document new datasets.

    Args:
        dry_run: If True, only show what would be done without making changes

    Returns:
        List of newly discovered datasets
    """
    logger.info("Starting automated dataset discovery and documentation")

    # Initialize components
    discoverer = EnhancedDatasetDiscoverer()
    generator = EnhancedDocumentationGenerator()
    updater = InputRegistryUpdater(Path(DIRECTORIES['input_base']))

    try:
        # Discover new datasets
        new_datasets = discoverer.discover_new_datasets()

        if not new_datasets:
            logger.info("No new datasets found")
            return []

        if dry_run:
            logger.info(f"Dry run: Would process {len(new_datasets)} datasets:")
            for dataset in new_datasets:
                print(f"  - {dataset['title']} ({dataset['dataset_slug']})")
            return new_datasets

        # Process each dataset
        processed_datasets = []
        for dataset in new_datasets:
            try:
                generator.generate_dataset_documentation(dataset)
                processed_datasets.append(dataset)
                logger.info(f"Processed: {dataset['dataset_slug']}")

                # Small delay to avoid overwhelming the system
                time.sleep(0.1)

            except Exception as e:
                logger.error(f"Failed to process {dataset['dataset_slug']}: {e}")
                continue

        # Update registry
        if processed_datasets:
            updater.update_registry(processed_datasets)
            logger.info(f"Updated registry with {len(processed_datasets)} new datasets")

        logger.info("Dataset discovery and documentation completed")
        return processed_datasets

    except Exception as e:
        logger.error(f"Dataset discovery failed: {e}")
        raise


class InputRegistryUpdater:
    """Updates INPUT.md with new datasets."""

    def __init__(self, input_dir: Path):
        self.input_dir = input_dir
        self.input_md = input_dir / "INPUT.md"

    def update_registry(self, new_datasets: List[Dict]):
        """Update INPUT.md with new datasets."""
        if not self.input_md.exists():
            logger.warning("INPUT.md not found")
            return

        with open(self.input_md, 'r', encoding='utf-8') as f:
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

        with open(self.input_md, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        logger.info(f"Updated INPUT.md with {len(new_entries)} entries")


if __name__ == "__main__":
    # Run discovery when script is executed directly
    discover_and_document()</content>
<parameter name="filePath">c:\Users\charl\OneDrive\Projets\ophthalmology-dataset-harmonization\src\pipeline\enhanced_discovery.py