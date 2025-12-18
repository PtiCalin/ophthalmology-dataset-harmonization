"""
Comprehensive test suite for expanded harmonization ruleset.
Tests all 15+ new functions and enhanced patterns across 269+ diagnosis keywords.
"""

import pytest
from src.rules import (
    normalize_diagnosis,
    find_clinical_findings,
    infer_modality,
    infer_laterality,
    infer_severity_from_diagnosis,
    assess_image_quality,
    detect_artifacts,
    standardize_age,
    standardize_sex,
    standardize_ethnicity,
    detect_column_role,
    harmonize_column_value,
    DIAGNOSIS_MAPPING,
    CLINICAL_FINDINGS_KEYWORDS,
    MODALITY_PATTERNS,
    LATERALITY_PATTERNS,
)


class TestDiagnosisNormalization:
    """Test expanded diagnosis mapping with 269+ keywords"""
    
    def test_diabetic_retinopathy_variants(self):
        # Basic DR
        assert normalize_diagnosis('diabetic retinopathy') == ('Diabetic Retinopathy', None)
        assert normalize_diagnosis('dr') == ('Diabetic Retinopathy', None)
        
        # DR Severity (ICDR)
        assert normalize_diagnosis('mild npdr')[0] == 'Diabetic Retinopathy'
        assert normalize_diagnosis('mild npdr')[1] == 'Mild'
        assert normalize_diagnosis('moderate npdr')[1] == 'Moderate'
        assert normalize_diagnosis('severe npdr')[1] == 'Severe'
        assert normalize_diagnosis('proliferative dr')[1] == 'Proliferative'
    
    def test_amd_variants(self):
        # Basic AMD
        assert normalize_diagnosis('age-related macular degeneration')[0] == 'Age-Related Macular Degeneration'
        
        # AMD subtypes (wet/dry)
        assert normalize_diagnosis('wet amd')[0] == 'Age-Related Macular Degeneration'
        assert normalize_diagnosis('dry amd')[0] == 'Age-Related Macular Degeneration'
        assert normalize_diagnosis('geographic atrophy')[0] == 'Age-Related Macular Degeneration'
    
    def test_cataract_variants(self):
        # Cataract types
        cat_result = normalize_diagnosis('nuclear cataract')
        assert cat_result[0] == 'Cataract'
        assert cat_result[1] == 'Moderate'
        
        # Hypermature (highest severity)
        assert normalize_diagnosis('hypermature cataract')[1] == 'Severe'
        assert normalize_diagnosis('immature cataract')[1] == 'Mild'
    
    def test_glaucoma_variants(self):
        assert normalize_diagnosis('glaucoma')[0] == 'Glaucoma'
        assert normalize_diagnosis('open angle glaucoma')[0] == 'Glaucoma'
        assert normalize_diagnosis('angle closure')[0] == 'Glaucoma'
    
    def test_corneal_disease_variants(self):
        assert normalize_diagnosis('corneal scar')[0] == 'Corneal Disease'
        assert normalize_diagnosis('keratoconus')[0] == 'Corneal Disease'
        assert normalize_diagnosis('pterygium')[0] == 'Corneal Disease'
    
    def test_vascular_occlusions(self):
        assert normalize_diagnosis('central retinal artery occlusion')[0] == 'Vascular Occlusion'
        assert normalize_diagnosis('crao')[0] == 'Vascular Occlusion'
        assert normalize_diagnosis('branch retinal vein occlusion')[0] == 'Vascular Occlusion'
    
    def test_retinal_detachment(self):
        assert normalize_diagnosis('retinal detachment')[0] == 'Retinal Detachment'
        assert normalize_diagnosis('rhegmatogenous')[0] == 'Retinal Detachment'
        assert normalize_diagnosis('macula-off')[0] == 'Retinal Detachment'
    
    def test_normal_variants(self):
        assert normalize_diagnosis('normal')[0] == 'Normal'
        assert normalize_diagnosis('no pathology')[0] == 'Normal'
        assert normalize_diagnosis('healthy')[0] == 'Normal'


class TestClinicalFindings:
    """Test clinical findings detection"""
    
    def test_hemorrhage_detection(self):
        findings = find_clinical_findings('Patient has intraretinal hemorrhage')
        assert 'hemorrhages' in findings or 'microhemorrhages' in findings
    
    def test_exudate_detection(self):
        findings = find_clinical_findings('Hard exudates present along arcades')
        assert 'hard_exudates' in findings or 'exudates' in findings
    
    def test_edema_detection(self):
        findings = find_clinical_findings('Macular edema with cystoid pattern')
        assert 'macular_edema' in findings or 'cysts' in findings
    
    def test_microaneurysm_detection(self):
        findings = find_clinical_findings('Multiple microaneurysms detected')
        assert 'microaneurysms' in findings
    
    def test_neovascularization_detection(self):
        findings = find_clinical_findings('Neovascular changes with CNV')
        assert any('neovascular' in f for f in findings)
    
    def test_multiple_findings(self):
        findings = find_clinical_findings('Hemorrhage, exudates, and edema visible')
        assert len(findings) >= 2


class TestModalityInference:
    """Test modality detection across 12 modalities"""
    
    def test_fundus_detection(self):
        assert infer_modality('Messidor', None) == 'Fundus'
        assert infer_modality('EyePACS', None) == 'Fundus'
        assert infer_modality('color fundus photo', None) == 'Fundus'
    
    def test_oct_detection(self):
        assert infer_modality('OCT_scan', None) == 'OCT'
        assert infer_modality('spectral domain OCT', None) == 'OCT'
        assert infer_modality('3d OCT volume', None) == 'OCT'
    
    def test_octa_detection(self):
        assert infer_modality('OCTA', None) == 'OCTA'
        assert infer_modality('oct angiography', None) == 'OCTA'
    
    def test_fluorescein_detection(self):
        assert infer_modality('fundus_FA', None) == 'Fluorescein Angiography'
    
    def test_infrared_detection(self):
        assert infer_modality('infrared imaging', None) == 'Infrared'
    
    def test_ultrasound_detection(self):
        assert infer_modality('B-scan ultrasound', None) == 'Ultrasound'


class TestLateralityInference:
    """Test laterality detection (multi-language)"""
    
    def test_english_right(self):
        assert infer_laterality('right') == 'OD'
        assert infer_laterality('od') == 'OD'
        assert infer_laterality('oculus dexter') == 'OD'
        assert infer_laterality('image_r.jpg') == 'OD'
        assert infer_laterality('_od') == 'OD'
    
    def test_english_left(self):
        assert infer_laterality('left') == 'OS'
        assert infer_laterality('os') == 'OS'
        assert infer_laterality('oculus sinister') == 'OS'
        assert infer_laterality('image_l.jpg') == 'OS'
        assert infer_laterality('_os') == 'OS'
    
    def test_bilateral(self):
        assert infer_laterality('bilateral') == 'OU'
        assert infer_laterality('both eyes') == 'OU'
        assert infer_laterality('ou') == 'OU'
    
    def test_french_variants(self):
        assert infer_laterality('droit') == 'OD'
        assert infer_laterality('gauche') == 'OS'
    
    def test_filename_patterns(self):
        assert infer_laterality('exam_r_2024') == 'OD'
        assert infer_laterality('scan-l-final') == 'OS'


class TestSeverityInference:
    """Test severity grading from diagnosis text"""
    
    def test_proliferative_severity(self):
        sev = infer_severity_from_diagnosis('proliferative diabetic retinopathy', 'Diabetic Retinopathy')
        assert sev == 'Proliferative'
    
    def test_severe_severity(self):
        sev = infer_severity_from_diagnosis('severe AMD', 'Age-Related Macular Degeneration')
        assert sev == 'Severe'
    
    def test_moderate_severity(self):
        sev = infer_severity_from_diagnosis('moderate disease', 'Glaucoma')
        assert sev == 'Moderate'
    
    def test_mild_severity(self):
        sev = infer_severity_from_diagnosis('mild glaucoma', 'Glaucoma')
        assert sev == 'Mild'


class TestImageQuality:
    """Test image quality assessment"""
    
    def test_excellent_quality(self):
        assert assess_image_quality('Excellent quality, perfect focus') == 'Excellent'
    
    def test_good_quality(self):
        assert assess_image_quality('Good quality fundus photo') == 'Good'
    
    def test_moderate_quality(self):
        assert assess_image_quality('Moderate quality, acceptable for analysis') == 'Moderate'
    
    def test_poor_quality(self):
        assert assess_image_quality('Poor quality with artifacts') == 'Poor'
    
    def test_ungradable(self):
        assert assess_image_quality('Cannot grade, missing', has_artifacts=True) == 'Ungradable'
    
    def test_artifact_detection(self):
        artifacts = detect_artifacts('Motion blur and media opacity present')
        assert len(artifacts) > 0


class TestDemographicStandardization:
    """Test patient demographic standardization"""
    
    def test_age_standardization(self):
        assert standardize_age(45) == 45
        assert standardize_age('67.5') == 67
        assert standardize_age(0) == 0
        assert standardize_age(150) == 150
        assert standardize_age(200) is None  # Out of range
        assert standardize_age(-5) is None  # Out of range
        assert standardize_age(None) is None
    
    def test_sex_standardization(self):
        assert standardize_sex('M') == 'M'
        assert standardize_sex('male') == 'M'
        assert standardize_sex('F') == 'F'
        assert standardize_sex('female') == 'F'
        assert standardize_sex('O') == 'O'
        assert standardize_sex('other') == 'O'
        assert standardize_sex('U') == 'U'
        assert standardize_sex('unknown') == 'U'
        assert standardize_sex(None) is None
    
    def test_ethnicity_standardization(self):
        assert standardize_ethnicity('Caucasian') == 'Caucasian'
        assert standardize_ethnicity('White') == 'Caucasian'
        assert standardize_ethnicity('Asian') == 'Asian'
        assert standardize_ethnicity('Black') == 'African'
        assert standardize_ethnicity('Hispanic') == 'Hispanic'
        assert standardize_ethnicity(None) is None


class TestColumnRoleDetection:
    """Test auto-detection of column purposes"""
    
    def test_diagnosis_detection(self):
        assert detect_column_role('diagnosis') == 'diagnosis'
        assert detect_column_role('disease_label') == 'diagnosis'
        assert detect_column_role('condition') == 'diagnosis'
    
    def test_laterality_detection(self):
        assert detect_column_role('laterality') == 'laterality'
        assert detect_column_role('eye') == 'laterality'
        assert detect_column_role('side') == 'laterality'
    
    def test_modality_detection(self):
        assert detect_column_role('modality') == 'modality'
        assert detect_column_role('imaging_type') == 'modality'
    
    def test_age_detection(self):
        assert detect_column_role('age') == 'patient_age'
        assert detect_column_role('patient_age') == 'patient_age'
    
    def test_sex_detection(self):
        assert detect_column_role('sex') == 'patient_sex'
        assert detect_column_role('gender') == 'patient_sex'


class TestHarmonizeColumnValue:
    """Test integrated column value harmonization"""
    
    def test_diagnosis_harmonization(self):
        result = harmonize_column_value('diagnosis', 'moderate npdr')
        assert result == 'Diabetic Retinopathy'
    
    def test_severity_harmonization(self):
        result = harmonize_column_value('severity', 'severe AMD')
        assert result is not None
    
    def test_modality_harmonization(self):
        result = harmonize_column_value('modality', 'OCT', {'dataset_name': 'DUKE'})
        assert result == 'OCT'
    
    def test_laterality_harmonization(self):
        result = harmonize_column_value('laterality', 'right')
        assert result == 'OD'
    
    def test_age_harmonization(self):
        result = harmonize_column_value('patient_age', '42.5')
        assert result == 42
    
    def test_sex_harmonization(self):
        result = harmonize_column_value('patient_sex', 'Female')
        assert result == 'F'


class TestComponentCounts:
    """Verify expanded component counts"""
    
    def test_diagnosis_mapping_size(self):
        assert len(DIAGNOSIS_MAPPING) > 200  # Expanded from ~50 to 269+
    
    def test_clinical_findings_size(self):
        assert len(CLINICAL_FINDINGS_KEYWORDS) > 30  # 37 finding types
    
    def test_modality_patterns_coverage(self):
        assert len(MODALITY_PATTERNS) == 12  # All 12 modalities
    
    def test_laterality_patterns_size(self):
        assert len(LATERALITY_PATTERNS) == 3  # OD, OS, OU


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
