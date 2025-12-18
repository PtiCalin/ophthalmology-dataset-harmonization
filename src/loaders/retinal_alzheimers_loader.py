from src.loaders.universal_loader import UniversalLoader
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class RetinalAlzheimersLoader(UniversalLoader):
    """
    Custom loader for Retinal Image Dataset for Early Detection of Alzheimer's.

    This loader handles fundus images with neurological diagnoses and cognitive
    assessments, integrating ophthalmology and neurology data.
    """

    def __init__(self, dataset_name: str, data_path: str, column_mapping: Dict[str, str] = None):
        super().__init__(dataset_name, column_mapping)
        self.data_path = Path(data_path)
        self.clinical_data = None

    def load_raw_data(self) -> pd.DataFrame:
        """
        Load Retinal Alzheimer's dataset with clinical correlations.

        Returns:
            pd.DataFrame: DataFrame with integrated ophthalmology and neurology data
        """
        data_records = []

        # Process each diagnosis directory
        diagnosis_dirs = ['alzheimers', 'mci', 'controls', 'other_dementias']

        for diagnosis in diagnosis_dirs:
            diagnosis_path = Path(self.data_path) / diagnosis
            if diagnosis_path.exists():
                for image_file in diagnosis_path.glob('*'):
                    if image_file.suffix.lower() in ['.tiff', '.jpg', '.jpeg', '.png']:
                        record = self._parse_alzheimers_filename(image_file, diagnosis)
                        if record:
                            data_records.append(record)

        df = pd.DataFrame(data_records)

        # Load and merge clinical data if available
        df = self._merge_clinical_data(df)

        return df

    def _parse_alzheimers_filename(self, image_file: Path, diagnosis: str) -> Optional[Dict]:
        """
        Parse Alzheimer's dataset filename with clinical information.

        Args:
            image_file: Path to image file
            diagnosis: Diagnosis directory name

        Returns:
            Dict containing parsed record data or None if parsing fails
        """
        filename = image_file.stem
        # Parse filename: {patient_id}_{eye}_{diagnosis}_{cognitive_score}.tiff
        parts = filename.split('_')

        if len(parts) < 4:
            logger.warning(f"Invalid filename format: {filename}")
            return None

        try:
            patient_id = parts[0]
            eye = parts[1]
            diagnosis_type = parts[2]
            cognitive_score = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None

            record = {
                'image_id': f"ALZ_{filename}",
                'patient_id': f"ALZ_{patient_id}",
                'eye': eye,
                'diagnosis': diagnosis_type,
                'cognitive_score': cognitive_score,
                'file_path': str(image_file),
                'file_size': image_file.stat().st_size,
                'modality': 'Fundus Photography',
                'research_context': 'Alzheimer\'s Disease Biomarker Research'
            }

            return record

        except (ValueError, IndexError) as e:
            logger.warning(f"Error parsing filename {filename}: {e}")
            return None

    def _merge_clinical_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge clinical data (demographics, detailed assessments) with image data.

        Args:
            df: DataFrame with image records

        Returns:
            pd.DataFrame: DataFrame with merged clinical data
        """
        clinical_file = Path(self.data_path) / 'clinical_data.csv'

        if clinical_file.exists():
            try:
                clinical_df = pd.read_csv(clinical_file)

                # Standardize patient ID format for merging
                clinical_df['patient_id'] = clinical_df['patient_id'].apply(
                    lambda x: f"ALZ_{x}" if not str(x).startswith('ALZ_') else x
                )

                # Merge on patient_id
                merged_df = pd.merge(df, clinical_df, on='patient_id', how='left')

                logger.info(f"Merged clinical data for {len(merged_df)} records")
                return merged_df

            except Exception as e:
                logger.warning(f"Error loading clinical data: {e}")
                return df
        else:
            logger.info("No clinical data file found, proceeding with image data only")
            return df

    def validate_alzheimers_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate Alzheimer's dataset with clinical and image quality checks.

        Args:
            df: DataFrame to validate

        Returns:
            pd.DataFrame: Validated DataFrame
        """
        logger.info("Validating Alzheimer's dataset...")

        # Basic field validation
        required_fields = ['image_id', 'patient_id', 'eye', 'diagnosis']
        missing_data = df[required_fields].isnull().sum()

        if missing_data.any():
            logger.warning(f"Missing data in required fields: {missing_data}")

        # Validate diagnosis categories
        valid_diagnoses = ['alzheimers', 'mci', 'controls', 'other_dementias']
        invalid_diagnosis = df[~df['diagnosis'].isin(valid_diagnoses)]
        if len(invalid_diagnosis) > 0:
            logger.warning(f"Invalid diagnosis values: {len(invalid_diagnosis)} records")

        # Validate cognitive scores
        if 'cognitive_score' in df.columns:
            invalid_scores = df[
                (df['cognitive_score'].notna()) &
                ((df['cognitive_score'] < 0) | (df['cognitive_score'] > 30))
            ]
            if len(invalid_scores) > 0:
                logger.warning(f"Invalid cognitive scores: {len(invalid_scores)} records")

        # Clinical consistency checks
        consistency_issues = self._check_clinical_consistency(df)
        if consistency_issues:
            logger.warning(f"Clinical consistency issues: {consistency_issues}")

        # File existence checks
        missing_files = df[~df['file_path'].apply(lambda x: Path(x).exists())]
        if len(missing_files) > 0:
            logger.warning(f"Missing image files: {len(missing_files)} records")

        return df

    def _check_clinical_consistency(self, df: pd.DataFrame) -> List[str]:
        """
        Check consistency between diagnosis and clinical measures.

        Args:
            df: DataFrame with clinical data

        Returns:
            List of consistency issue descriptions
        """
        issues = []

        if 'cognitive_score' in df.columns and 'diagnosis' in df.columns:
            # Check for normal controls with low cognitive scores
            normal_low_score = df[
                (df['diagnosis'] == 'controls') &
                (df['cognitive_score'].notna()) &
                (df['cognitive_score'] < 24)
            ]
            if len(normal_low_score) > 0:
                issues.append(f"{len(normal_low_score)} normal controls have low cognitive scores")

            # Check for Alzheimer's cases with high cognitive scores
            alzheimers_high_score = df[
                (df['diagnosis'] == 'alzheimers') &
                (df['cognitive_score'].notna()) &
                (df['cognitive_score'] > 20)
            ]
            if len(alzheimers_high_score) > 0:
                issues.append(f"{len(alzheimers_high_score)} Alzheimer's cases have high cognitive scores")

        return issues

    def harmonize_alzheimers_record(self, record: Dict) -> Dict:
        """
        Harmonize a single Alzheimer's record to the standard schema.

        Args:
            record: Raw Alzheimer's record

        Returns:
            Dict: Harmonized record
        """
        # Diagnosis mapping
        diagnosis_mapping = {
            'alzheimers': "Alzheimer's Disease",
            'mci': 'Mild Cognitive Impairment',
            'controls': 'Normal',
            'other_dementias': 'Other Dementia'
        }

        # Laterality mapping
        laterality_mapping = {
            'OD': 'Right',
            'OS': 'Left',
            'OU': 'Both'
        }

        harmonized = {
            'record_id': record['image_id'],
            'patient_id': record['patient_id'],
            'modality': 'Fundus Photography',
            'laterality': laterality_mapping.get(record.get('eye'), 'Unknown'),
            'diagnosis_category': diagnosis_mapping.get(record['diagnosis'], 'Other'),
            'anatomy': 'Retina',
            'image_path': record['file_path'],
            'clinical_findings': {}
        }

        # Add cognitive assessment if available
        if pd.notna(record.get('cognitive_score')):
            harmonized['clinical_findings']['cognitive_score'] = record['cognitive_score']
            harmonized['clinical_findings']['cognitive_assessment_type'] = 'MMSE'

        # Add demographic information if available
        if pd.notna(record.get('age')):
            harmonized['demographics'] = harmonized.get('demographics', {})
            harmonized['demographics']['age'] = int(record['age'])

        if pd.notna(record.get('gender')):
            harmonized['demographics'] = harmonized.get('demographics', {})
            gender_mapping = {'M': 'Male', 'F': 'Female', 'Male': 'Male', 'Female': 'Female'}
            harmonized['demographics']['gender'] = gender_mapping.get(record['gender'], record['gender'])

        return harmonized

    def generate_clinical_report(self, df: pd.DataFrame) -> Dict:
        """
        Generate clinical summary report for the Alzheimer's dataset.

        Args:
            df: DataFrame with clinical data

        Returns:
            Dict containing clinical statistics
        """
        report = {
            'total_records': len(df),
            'unique_patients': df['patient_id'].nunique(),
            'diagnosis_distribution': df['diagnosis'].value_counts().to_dict(),
            'laterality_distribution': df['eye'].value_counts().to_dict(),
        }

        # Cognitive score statistics
        if 'cognitive_score' in df.columns:
            cognitive_data = df['cognitive_score'].dropna()
            if len(cognitive_data) > 0:
                report['cognitive_score_stats'] = {
                    'mean': cognitive_data.mean(),
                    'std': cognitive_data.std(),
                    'min': cognitive_data.min(),
                    'max': cognitive_data.max(),
                    'median': cognitive_data.median()
                }

        # Demographic statistics
        if 'age' in df.columns:
            age_data = df['age'].dropna()
            if len(age_data) > 0:
                report['age_stats'] = {
                    'mean': age_data.mean(),
                    'std': age_data.std(),
                    'min': age_data.min(),
                    'max': age_data.max()
                }

        if 'gender' in df.columns:
            report['gender_distribution'] = df['gender'].value_counts().to_dict()

        return report