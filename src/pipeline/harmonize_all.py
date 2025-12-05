"""
Full harmonization orchestration pipeline.

This module coordinates loading, harmonizing, and merging multiple datasets.
"""

from typing import Dict, List, Optional, Callable
import pandas as pd
from pathlib import Path
import logging

from ..loaders import UniversalLoader
from ..schema import create_schema_columns


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HarmonizationPipeline:
    """
    Orchestrates the full harmonization pipeline for multiple datasets.
    
    This class manages:
    - Dataset registration and selection
    - Loading and harmonization of each dataset
    - Merging into a unified dataframe
    - Exporting to standardized formats
    """
    
    def __init__(self, output_dir: str = None):
        """
        Initialize the pipeline.
        
        Args:
            output_dir: Directory for output files (default: './output')
        """
        self.output_dir = Path(output_dir or './output')
        self.output_dir.mkdir(exist_ok=True)
        
        self.datasets_registry: Dict[str, Dict] = {}
        self.harmonized_dfs: Dict[str, pd.DataFrame] = {}
        self.merged_df: Optional[pd.DataFrame] = None
    
    def register_dataset(
        self,
        dataset_name: str,
        loader_fn: Callable,
        column_mapping: Dict[str, str] = None,
        enabled: bool = True
    ):
        """
        Register a dataset in the pipeline.
        
        Args:
            dataset_name: Unique identifier for the dataset
            loader_fn: Function that returns a dataframe when called
            column_mapping: Optional explicit column mapping to schema
            enabled: Whether this dataset is enabled for processing
        """
        self.datasets_registry[dataset_name] = {
            'loader_fn': loader_fn,
            'column_mapping': column_mapping or {},
            'enabled': enabled,
        }
        logger.info(f"Registered dataset: {dataset_name}")
    
    def harmonize_dataset(self, dataset_name: str) -> Optional[pd.DataFrame]:
        """
        Load and harmonize a single dataset.
        
        Args:
            dataset_name: Name of the dataset to harmonize
            
        Returns:
            Harmonized dataframe or None if not found
        """
        if dataset_name not in self.datasets_registry:
            logger.warning(f"Dataset not found: {dataset_name}")
            return None
        
        config = self.datasets_registry[dataset_name]
        
        try:
            # Load the raw dataset
            logger.info(f"Loading dataset: {dataset_name}")
            raw_df = config['loader_fn']()
            
            # Harmonize using UniversalLoader
            logger.info(f"Harmonizing dataset: {dataset_name}")
            loader = UniversalLoader(dataset_name, config['column_mapping'])
            harmonized_df = loader.load_and_harmonize(raw_df)
            
            self.harmonized_dfs[dataset_name] = harmonized_df
            logger.info(f"Successfully harmonized {dataset_name}: {len(harmonized_df)} records")
            
            return harmonized_df
        
        except Exception as e:
            logger.error(f"Error harmonizing {dataset_name}: {str(e)}")
            return None
    
    def harmonize_all(self) -> pd.DataFrame:
        """
        Load and harmonize all enabled datasets.
        
        Returns:
            Merged dataframe containing all harmonized datasets
        """
        for dataset_name, config in self.datasets_registry.items():
            if config['enabled']:
                self.harmonize_dataset(dataset_name)
        
        return self.merge_all()
    
    def merge_all(self) -> pd.DataFrame:
        """
        Merge all harmonized datasets into a single dataframe.
        
        Returns:
            Merged dataframe
        """
        if not self.harmonized_dfs:
            logger.warning("No harmonized datasets to merge")
            return pd.DataFrame(columns=create_schema_columns())
        
        logger.info(f"Merging {len(self.harmonized_dfs)} datasets")
        
        # Concatenate all harmonized dataframes
        self.merged_df = pd.concat(
            list(self.harmonized_dfs.values()),
            ignore_index=True
        )
        
        logger.info(f"Merged dataset has {len(self.merged_df)} total records")
        return self.merged_df
    
    def export_to_parquet(self, filename: str = 'harmonized.parquet') -> Path:
        """
        Export merged dataframe to Parquet format.
        
        Args:
            filename: Output filename (default: 'harmonized.parquet')
            
        Returns:
            Path to output file
        """
        if self.merged_df is None:
            logger.error("No merged dataframe to export. Run harmonize_all() first.")
            return None
        
        output_path = self.output_dir / filename
        
        try:
            self.merged_df.to_parquet(output_path, index=False)
            logger.info(f"Exported harmonized dataset to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error exporting to parquet: {str(e)}")
            return None
    
    def export_to_csv(self, filename: str = 'harmonized.csv') -> Path:
        """
        Export merged dataframe to CSV format.
        
        Args:
            filename: Output filename (default: 'harmonized.csv')
            
        Returns:
            Path to output file
        """
        if self.merged_df is None:
            logger.error("No merged dataframe to export. Run harmonize_all() first.")
            return None
        
        output_path = self.output_dir / filename
        
        try:
            self.merged_df.to_csv(output_path, index=False)
            logger.info(f"Exported harmonized dataset to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return None
    
    def get_statistics(self) -> Dict:
        """
        Get summary statistics about harmonized datasets.
        
        Returns:
            Dictionary with statistics
        """
        if self.merged_df is None:
            return {}
        
        return {
            'total_records': len(self.merged_df),
            'datasets': len(self.harmonized_dfs),
            'modalities': self.merged_df['modality'].nunique(),
            'unique_diagnoses': self.merged_df['diagnosis_normalized'].nunique(),
            'datasets_breakdown': {
                name: len(df) for name, df in self.harmonized_dfs.items()
            }
        }
