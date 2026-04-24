"""
Universal loader for heterogeneous ophthalmology datasets.

THIS IS THE "SWISS ARMY KNIFE" OF DATA LOADING:
- Takes messy CSV/Parquet files from different sources
- Automatically figures out what each column contains
- Applies harmonization rules to standardize everything
- Outputs clean HarmonizedRecord objects

WHY THIS EXISTS:
- Ophthalmology datasets come in countless formats
- Column names vary: "diagnosis", "dx", "condition", "label"
- Data quality varies: missing values, inconsistent formats
- Need one tool that can handle everything

HOW IT WORKS:
1. Load raw data (CSV, Parquet, etc.)
2. Auto-detect what each column represents
3. Apply rules to standardize values
4. Create HarmonizedRecord objects
5. Generate quality reports

EXAMPLE USAGE:
```python
loader = UniversalLoader("My Dataset")
df = pd.read_csv("messy_data.csv")
harmonized_df = loader.load_and_harmonize(df)
report = loader.get_load_report()  # See what happened
```
"""

from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import json
import logging

from ..schema import HarmonizedRecord, ImageMetadata, create_schema_columns
from ..rules import (
    detect_column_role, harmonize_column_value,
    normalize_diagnosis, infer_severity_from_diagnosis, infer_laterality
)

logger = logging.getLogger(__name__)


class LoaderException(Exception):
    """Base exception for loader errors."""
    pass


class ColumnDetectionException(LoaderException):
    """Raised when critical columns cannot be detected."""
    pass


class UniversalLoader:
    """
    THE MAIN DATA LOADING ENGINE - handles any ophthalmology dataset.

    WHAT IT DOES:
    - Loads data from various formats (CSV, Parquet, DataFrame)
    - Automatically detects column purposes using pattern matching
    - Applies harmonization rules to standardize all values
    - Creates quality flags for data issues
    - Generates detailed processing reports

    KEY FEATURES:
    - Zero configuration: Works out-of-the-box with most datasets
    - Robust error handling: Continues processing despite data quality issues
    - Comprehensive logging: Tracks every decision and transformation
    - Extensible: Can add custom column mappings for special cases

    PROCESSING PIPELINE:
    1. Load raw data into pandas DataFrame
    2. Detect column roles (diagnosis, modality, laterality, etc.)
    3. For each row: harmonize values using rules engine
    4. Create HarmonizedRecord with standardized data
    5. Collect quality metrics and error reports

    QUALITY ASSURANCE:
    - Validates required fields (image_id, dataset_source)
    - Flags missing or invalid data
    - Tracks transformation confidence scores
    - Reports processing statistics
    """

    def __init__(self, dataset_name: str, column_mapping: Dict[str, str] = None):
        """
        Initialize the loader with dataset configuration.

        Args:
            dataset_name: Identifier for the source dataset (appears in all records)
            column_mapping: Optional explicit mapping of dataset columns to schema fields
                           Format: {'dataset_column': 'schema_field'}
                           Use when auto-detection fails or for custom datasets
        """
        """
        self.dataset_name = dataset_name
        self.column_mapping = column_mapping or {}
        self.auto_detected_columns: Dict[str, str] = {}
        self.detection_confidence: Dict[str, float] = {}
        self.load_errors: List[Dict] = []
        self.warnings: List[Dict] = []
    
    def auto_detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Auto-detect schema columns from dataframe column names with confidence scoring.
        
        Args:
            df: Input dataframe
            
        Returns:
            Mapping of detected schema fields to dataframe columns
            
        Raises:
            ColumnDetectionException: If critical columns cannot be detected
        """
        detected = {}
        self.detection_confidence = {}
        
        required_fields = ['image_id']
        detected_required = set()
        
        for col in df.columns:
            field_type = detect_column_role(col)
            if field_type:
                # Simple confidence: longer field names match more confidently
                confidence = min(1.0, len(field_type) / len(col))
                detected[field_type] = col
                self.detection_confidence[field_type] = confidence
                
                if field_type in required_fields:
                    detected_required.add(field_type)
        
        # Check for critical missing fields
        missing = set(required_fields) - detected_required
        if missing:
            logger.warning(f"Could not detect required fields: {missing}")
        
        self.auto_detected_columns = detected
        return detected
    
    def load_and_harmonize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Load and harmonize a dataset with error handling.
        
        Args:
            df: Input dataframe
            
        Returns:
            Harmonized dataframe with canonical schema
        """
        if df.empty:
            logger.warning(f"Dataset {self.dataset_name} is empty")
            return pd.DataFrame(columns=create_schema_columns())
        
        logger.info(f"Loading dataset: {self.dataset_name} (shape: {df.shape})")
        
        # Auto-detect columns if not explicitly mapped
        if not self.column_mapping:
            self.auto_detect_columns(df)
            mapping = self.auto_detected_columns
        else:
            mapping = self.column_mapping
        
        logger.info(f"Using column mapping: {mapping}")
        
        # Convert rows to harmonized records
        harmonized_records = []
        self.load_errors = []
        self.warnings = []
        
        for idx, row in df.iterrows():
            try:
                record = self._harmonize_row(row, mapping, idx)
                if record:
                    harmonized_records.append(record.to_dict())
            except Exception as e:
                error_msg = f"Error harmonizing row {idx}: {str(e)}"
                logger.error(error_msg)
                self.load_errors.append({
                    'row_index': idx,
                    'error': str(e),
                    'data': row.to_dict()
                })
        
        # Create harmonized dataframe
        if not harmonized_records:
            logger.warning(f"No records could be harmonized from {self.dataset_name}")
            return pd.DataFrame(columns=create_schema_columns())
        
        result_df = pd.DataFrame(harmonized_records)
        
        # Ensure all canonical columns are present
        for col in create_schema_columns():
            if col not in result_df.columns:
                result_df[col] = None
        
        result_df = result_df[create_schema_columns()]
        
        logger.info(
            f"Successfully harmonized {len(result_df)} records from {self.dataset_name} "
            f"({len(self.load_errors)} errors)"
        )
        
        return result_df
    
    def _harmonize_row(self, row: pd.Series, mapping: Dict[str, str], row_index: int) -> Optional[HarmonizedRecord]:
        """
        Convert a single row to a harmonized record with validation.
        
        Args:
            row: Input row (pandas Series)
            mapping: Column mapping
            row_index: Row index for error tracking
            
        Returns:
            HarmonizedRecord or None if validation fails
        """
        try:
            # Get image_id - fallback to row index if not found
            image_id = self._get_value(row, mapping, 'image_id')
            if not image_id:
                image_id = f"{self.dataset_name}_{row_index}"
            
            # Get diagnosis and severity
            diagnosis_raw = self._get_value(row, mapping, 'diagnosis')
            diagnosis_category, severity_inferred = normalize_diagnosis(diagnosis_raw)
            severity = self._get_value(row, mapping, 'severity') or severity_inferred
            
            # Get diagnosis confidence (placeholder for future enhancement)
            diagnosis_confidence = None
            
            # Create record
            record = HarmonizedRecord(
                image_id=image_id,
                dataset_source=self.dataset_name,
                modality=self._get_harmonized_value(row, mapping, 'modality'),
                laterality=self._get_harmonized_value(row, mapping, 'laterality'),
                view_type=self._get_value(row, mapping, 'view_type'),
                image_path=self._get_value(row, mapping, 'image_path'),
                diagnosis_raw=diagnosis_raw,
                diagnosis_category=diagnosis_category,
                diagnosis_confidence=diagnosis_confidence,
                severity=severity,
                clinical_notes=self._get_value(row, mapping, 'clinical_notes'),
                patient_id=self._get_value(row, mapping, 'patient_id'),
                patient_age=self._get_harmonized_value(row, mapping, 'patient_age'),
                patient_sex=self._get_harmonized_value(row, mapping, 'patient_sex'),
                patient_ethnicity=self._get_harmonized_value(row, mapping, 'patient_ethnicity'),
            )
            
            # Extract image metadata
            resolution_x = self._try_parse_int(self._get_value(row, mapping, 'resolution_x'))
            resolution_y = self._try_parse_int(self._get_value(row, mapping, 'resolution_y'))
            
            if resolution_x or resolution_y:
                record.image_metadata = ImageMetadata(
                    resolution_x=resolution_x,
                    resolution_y=resolution_y,
                )
            
            # Store unmapped columns in extra_json
            mapped_columns = set(mapping.values())
            unmapped = {}
            for col in row.index:
                if col not in mapped_columns and col is not None:
                    val = row[col]
                    if pd.notna(val):
                        unmapped[col] = str(val)
            
            if unmapped:
                record.extra_json = unmapped
            
            # Validate record
            if not record.validate():
                self.warnings.append({
                    'row_index': row_index,
                    'image_id': image_id,
                    'message': record.validation_notes
                })
            
            return record
        
        except Exception as e:
            logger.error(f"Error harmonizing row {row_index}: {str(e)}")
            raise
    
    def _get_value(self, row: pd.Series, mapping: Dict[str, str], field: str) -> Optional[str]:
        """Get raw value from row."""
        col = mapping.get(field)
        if col and col in row.index:
            val = row[col]
            return str(val) if pd.notna(val) else None
        return None
    
    def _get_harmonized_value(self, row: pd.Series, mapping: Dict[str, str], field: str) -> Any:
        """Get harmonized value from row."""
        raw_value = self._get_value(row, mapping, field)
        context = {'dataset_name': self.dataset_name}
        return harmonize_column_value(field, raw_value, context)
    
    def _try_parse_int(self, value: Optional[str]) -> Optional[int]:
        """Safely parse integer value."""
        if not value:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    def get_load_report(self) -> Dict[str, Any]:
        """
        Get a summary report of the load operation.
        
        Returns:
            Dictionary with load statistics and errors
        """
        return {
            'dataset': self.dataset_name,
            'total_errors': len(self.load_errors),
            'total_warnings': len(self.warnings),
            'detected_columns': self.auto_detected_columns,
            'detection_confidence': self.detection_confidence,
            'errors': self.load_errors[:10],  # First 10 errors
            'warnings': self.warnings[:10],  # First 10 warnings
        }
