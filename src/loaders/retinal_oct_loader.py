from src.loaders.universal_loader import UniversalLoader
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class RetinalOCTLoader(UniversalLoader):
    """
    Custom loader for Retinal OCT Images dataset.

    This loader handles OCT volume data with multiple B-scan slices per volume,
    extracting both volume-level and slice-level metadata for harmonization.
    """

    def __init__(self, dataset_name: str, data_path: str, column_mapping: Dict[str, str] = None):
        super().__init__(dataset_name, column_mapping)
        self.data_path = Path(data_path)
        self.volume_info = {}  # Cache for volume metadata

    def load_raw_data(self) -> pd.DataFrame:
        """
        Load Retinal OCT Images dataset with volume and slice information.

        Returns:
            pd.DataFrame: DataFrame with one row per OCT slice, including volume metadata
        """
        data_records = []

        # Process each class directory
        class_dirs = ['CNV', 'DME', 'DRUSEN', 'NORMAL']

        for class_name in class_dirs:
            class_path = Path(self.data_path) / class_name
            if class_path.exists():
                # Group files by volume (patient)
                volume_groups = self._group_files_by_volume(class_path)

                for volume_id, files in volume_groups.items():
                    volume_metadata = self._extract_volume_metadata(volume_id, files, class_name)

                    # Create records for each slice in the volume
                    for file_info in files:
                        record = self._create_slice_record(file_info, volume_metadata)
                        data_records.append(record)

        return pd.DataFrame(data_records)

    def _group_files_by_volume(self, class_path: Path) -> Dict[str, List[Dict]]:
        """
        Group OCT files by volume (patient) based on filename patterns.

        Args:
            class_path: Path to class directory

        Returns:
            Dict mapping volume IDs to lists of file information
        """
        volume_groups = {}

        for tiff_file in class_path.glob('*.tiff'):
            filename = tiff_file.stem
            # Parse filename: {class}_{patient_id}_{slice_number}.tiff
            parts = filename.split('_')

            if len(parts) >= 3:
                volume_id = f"{parts[0]}_{parts[1]}"  # e.g., "CNV_001"
                slice_number = int(parts[2])

                file_info = {
                    'filepath': tiff_file,
                    'filename': filename,
                    'slice_number': slice_number,
                    'file_size': tiff_file.stat().st_size
                }

                if volume_id not in volume_groups:
                    volume_groups[volume_id] = []
                volume_groups[volume_id].append(file_info)

        # Sort slices within each volume
        for volume_id in volume_groups:
            volume_groups[volume_id].sort(key=lambda x: x['slice_number'])

        return volume_groups

    def _extract_volume_metadata(self, volume_id: str, files: List[Dict], class_name: str) -> Dict:
        """
        Extract metadata for an OCT volume.

        Args:
            volume_id: Volume identifier
            files: List of file information for this volume
            class_name: Diagnosis class

        Returns:
            Dict containing volume metadata
        """
        # Calculate volume statistics
        slice_count = len(files)
        total_size = sum(f['file_size'] for f in files)
        slice_numbers = [f['slice_number'] for f in files]

        # Estimate volume dimensions (typical OCT parameters)
        estimated_slices = max(slice_numbers) if slice_numbers else 61
        volume_depth = estimated_slices * 4.5  # μm per slice (approximate)

        metadata = {
            'volume_id': f"OCT_{volume_id}",
            'diagnosis_class': class_name,
            'total_slices': slice_count,
            'estimated_volume_slices': estimated_slices,
            'volume_depth_um': volume_depth,
            'total_file_size': total_size,
            'slice_range': f"{min(slice_numbers)}-{max(slice_numbers)}" if slice_numbers else "unknown",
            'modality': 'Optical Coherence Tomography',
            'wavelength': 840,  # nm, typical for OCT
            'field_of_view': '6x6',  # mm
            'axial_resolution': 5,  # μm
            'transverse_resolution': 15,  # μm
            'scan_pattern': 'raster'
        }

        return metadata

    def _create_slice_record(self, file_info: Dict, volume_metadata: Dict) -> Dict:
        """
        Create a data record for a single OCT slice.

        Args:
            file_info: Information about the slice file
            volume_metadata: Metadata for the parent volume

        Returns:
            Dict containing slice record data
        """
        filename = file_info['filename']
        parts = filename.split('_')

        record = {
            # Primary identifiers
            'image_id': f"OCT_{filename}",
            'patient_id': f"OCT_{parts[1]}",  # Extract patient ID
            'volume_id': volume_metadata['volume_id'],
            'slice_number': file_info['slice_number'],

            # Diagnosis and classification
            'diagnosis_class': volume_metadata['diagnosis_class'],

            # File information
            'file_path': str(file_info['filepath']),
            'file_size': file_info['file_size'],

            # OCT-specific metadata
            'modality': volume_metadata['modality'],
            'wavelength': volume_metadata['wavelength'],
            'field_of_view': volume_metadata['field_of_view'],
            'axial_resolution': volume_metadata['axial_resolution'],
            'transverse_resolution': volume_metadata['transverse_resolution'],
            'scan_pattern': volume_metadata['scan_pattern'],

            # Volume context
            'total_slices_in_volume': volume_metadata['total_slices'],
            'estimated_volume_slices': volume_metadata['estimated_volume_slices'],
            'volume_depth_um': volume_metadata['volume_depth_um'],
            'slice_range': volume_metadata['slice_range'],

            # Processing flags
            'is_first_slice': file_info['slice_number'] == 1,
            'is_last_slice': file_info['slice_number'] == volume_metadata['estimated_volume_slices'],
            'relative_position': file_info['slice_number'] / volume_metadata['estimated_volume_slices']
        }

        return record

    def validate_oct_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate OCT dataset with volume-level and slice-level checks.

        Args:
            df: DataFrame to validate

        Returns:
            pd.DataFrame: Validated DataFrame
        """
        logger.info("Validating OCT dataset...")

        # Basic field validation
        required_fields = ['image_id', 'patient_id', 'volume_id', 'diagnosis_class']
        missing_data = df[required_fields].isnull().sum()

        if missing_data.any():
            logger.warning(f"Missing data in required fields: {missing_data}")

        # Validate diagnosis classes
        valid_classes = ['CNV', 'DME', 'DRUSEN', 'NORMAL']
        invalid_class = df[~df['diagnosis_class'].isin(valid_classes)]
        if len(invalid_class) > 0:
            logger.warning(f"Invalid diagnosis classes: {len(invalid_class)} records")

        # Volume consistency checks
        volume_consistency = self._check_volume_consistency(df)
        if not volume_consistency['valid']:
            logger.warning(f"Volume consistency issues: {volume_consistency['issues']}")

        # File existence checks
        missing_files = df[~df['file_path'].apply(lambda x: Path(x).exists())]
        if len(missing_files) > 0:
            logger.warning(f"Missing OCT files: {len(missing_files)} records")

        return df

    def _check_volume_consistency(self, df: pd.DataFrame) -> Dict:
        """
        Check consistency of OCT volumes.

        Args:
            df: DataFrame with OCT data

        Returns:
            Dict with validation results
        """
        issues = []

        # Check slice numbering within volumes
        for volume_id, volume_data in df.groupby('volume_id'):
            slice_numbers = sorted(volume_data['slice_number'].unique())
            expected_range = list(range(1, len(slice_numbers) + 1))

            if slice_numbers != expected_range:
                issues.append(f"Volume {volume_id}: irregular slice numbering {slice_numbers}")

            # Check for duplicate slices
            if len(slice_numbers) != len(volume_data):
                issues.append(f"Volume {volume_id}: duplicate slices detected")

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def get_volume_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate statistics for OCT volumes.

        Args:
            df: DataFrame with OCT data

        Returns:
            pd.DataFrame: Volume-level statistics
        """
        volume_stats = []

        for volume_id, volume_data in df.groupby('volume_id'):
            stats = {
                'volume_id': volume_id,
                'total_slices': len(volume_data),
                'diagnosis_class': volume_data['diagnosis_class'].iloc[0],
                'total_file_size_mb': volume_data['file_size'].sum() / (1024 * 1024),
                'slice_number_range': f"{volume_data['slice_number'].min()}-{volume_data['slice_number'].max()}",
                'estimated_volume_depth_um': volume_data['volume_depth_um'].iloc[0],
                'wavelength': volume_data['wavelength'].iloc[0],
                'field_of_view': volume_data['field_of_view'].iloc[0]
            }
            volume_stats.append(stats)

        return pd.DataFrame(volume_stats)

    def harmonize_oct_record(self, record: Dict) -> Dict:
        """
        Harmonize a single OCT record to the standard schema.

        Args:
            record: Raw OCT record

        Returns:
            Dict: Harmonized record
        """
        # Diagnosis mapping
        diagnosis_mapping = {
            'CNV': 'Choroidal Neovascularization',
            'DME': 'Diabetic Macular Edema',
            'DRUSEN': 'Drusen',
            'NORMAL': 'Normal'
        }

        harmonized = {
            'record_id': record['image_id'],
            'patient_id': record['patient_id'],
            'modality': 'Optical Coherence Tomography',
            'laterality': 'Unknown',  # OCT volumes typically don't specify eye
            'diagnosis_category': diagnosis_mapping.get(record['diagnosis_class'], 'Other'),
            'anatomy': 'Retina',
            'image_path': record['file_path'],
            'clinical_findings': {
                'volume_id': record['volume_id'],
                'slice_number': record['slice_number'],
                'total_slices': record['total_slices_in_volume'],
                'relative_position': record['relative_position'],
                'wavelength': record['wavelength'],
                'field_of_view': record['field_of_view'],
                'axial_resolution': record['axial_resolution'],
                'transverse_resolution': record['transverse_resolution']
            }
        }

        return harmonized