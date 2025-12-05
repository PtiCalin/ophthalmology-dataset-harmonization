"""
Comprehensive schema definitions for harmonized ophthalmology datasets.

This module defines the unified, extensible data structure for consolidating diverse
ophthalmology datasets including fundus imaging, OCT scans, and clinical metadata across
multiple modalities, disease categories, and patient populations.

Designed to capture:
- Image metadata (technical specs, quality metrics, device info)
- Clinical findings (diagnoses, severity, measurements, imaging signs)
- Patient demographics (age, sex, ethnicity, comorbidities, medications)
- Study context (exam date/time, facility, device, visit number)
- Quality/provenance (data source, annotation confidence, validation status)
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
from datetime import datetime


class Modality(str, Enum):
    """Imaging modality types for fundus and anterior segment imaging."""
    FUNDUS = "Fundus"  # Color fundus photography (CFP), widefield
    OCT = "OCT"  # Optical Coherence Tomography (SD-OCT, SS-OCT)
    OCT_A = "OCTA"  # OCT Angiography
    SLIT_LAMP = "Slit-Lamp"  # Slit-lamp biomicroscopy
    FLUORESCEIN_ANGIOGRAPHY = "Fluorescein Angiography"  # FA
    FUNDUS_AUTOFLUORESCENCE = "Fundus Autofluorescence"  # FAF
    INFRARED = "Infrared"  # Infrared reflectance
    ULTRASOUND = "Ultrasound"  # A/B-scan ultrasound
    ANTERIOR_SEGMENT = "Anterior Segment"  # Anterior segment imaging
    SPECULAR_MICROSCOPY = "Specular Microscopy"  # Endothelial cell imaging
    VISUAL_FIELD = "Visual Field"  # Perimetry
    OCT_ANGIO = "OCT Angio"  # Vascular imaging
    UNKNOWN = "Unknown"


class Laterality(str, Enum):
    """Eye laterality codes."""
    OD = "OD"  # Right eye (Oculus Dexter)
    OS = "OS"  # Left eye (Oculus Sinister)
    OU = "OU"  # Both eyes (Oculus Uterque)


class DiagnosisCategory(str, Enum):
    """Standardized diagnosis categories covering major retinal and anterior segment diseases."""
    NORMAL = "Normal"
    DIABETIC_RETINOPATHY = "Diabetic Retinopathy"
    DIABETIC_MACULAR_EDEMA = "Diabetic Macular Edema"
    AMD = "Age-Related Macular Degeneration"
    CATARACT = "Cataract"
    GLAUCOMA = "Glaucoma"
    GLAUCOMA_SUSPECT = "Glaucoma Suspect"
    CORNEAL_DISEASE = "Corneal Disease"
    RETINOBLASTOMA = "Retinoblastoma"
    MACULAR_EDEMA = "Macular Edema"
    DRUSEN = "Drusen"
    MYOPIA = "Myopia"
    HYPERTENSIVE_RETINOPATHY = "Hypertensive Retinopathy"
    RETINAL_DETACHMENT = "Retinal Detachment"
    VEIN_OCCLUSION = "Retinal Vein/Artery Occlusion"
    OPTIC_DISC_DISEASE = "Optic Disc Disease"
    VITREOUS_HEMORRHAGE = "Vitreous Hemorrhage"
    PRESBYOPIA = "Presbyopia"
    ASTIGMATISM = "Astigmatism"
    HYPEROPIA = "Hyperopia"
    KERATOCONUS = "Keratoconus"
    PTERYGIUM = "Pterygium"
    CATARACTS_POSTERIOR_SUBCAPSULAR = "Posterior Subcapsular Cataract"
    COTTON_WOOL_SPOTS = "Cotton Wool Spots"
    HARD_EXUDATES = "Hard Exudates"
    MICROANEURYSMS = "Microaneurysms"
    HEMORRHAGES = "Retinal Hemorrhages"
    NEOVASCULARIZATION = "Neovascularization"
    OTHER = "Other"


class Severity(str, Enum):
    """Severity grading scales for different conditions."""
    NONE = "None"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    PROLIFERATIVE = "Proliferative"
    VERY_SEVERE = "Very Severe"


class Sex(str, Enum):
    """Patient biological sex."""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    UNKNOWN = "U"


class DiabetesType(str, Enum):
    """Diabetes classification."""
    TYPE_1 = "Type 1"
    TYPE_2 = "Type 2"
    GESTATIONAL = "Gestational"
    UNKNOWN = "Unknown"
    NONE = "No Diabetes"


class DRSeverityScale(str, Enum):
    """International DR severity scale (ICDR)."""
    NO_DR = "No DR"
    MILD_NPDR = "Mild NPDR"
    MODERATE_NPDR = "Moderate NPDR"
    SEVERE_NPDR = "Severe NPDR"
    PDR = "PDR"


class DMESeverityScale(str, Enum):
    """DME severity scale."""
    NO_APPARENT_RETINAL_THICKENING = "No apparent retinal thickening"
    SOME_RETINAL_THICKENING = "Some retinal thickening"
    RETINAL_THICKENING_INVOLVING_MACULA = "Retinal thickening involving macula"


class AnnotationQuality(str, Enum):
    """Quality/confidence of expert annotation."""
    EXPERT = "Expert"
    CLINICIAN = "Clinician"
    CONSENSUS = "Consensus"
    CROWD_SOURCED = "Crowd-sourced"
    AUTOMATED = "Automated"
    UNVERIFIED = "Unverified"


class DataSource(str, Enum):
    """Data source/collection method."""
    CLINICAL_TRIAL = "Clinical Trial"
    HOSPITAL_RECORDS = "Hospital Records"
    TELEHEALTH = "Telehealth"
    RESEARCH_STUDY = "Research Study"
    PUBLIC_DATASET = "Public Dataset"
    CROWDSOURCED = "Crowdsourced"
    SYNTHETIC = "Synthetic Data"


@dataclass
class ImageMetadata:
    """Image-level technical metadata including acquisition parameters and quality metrics."""
    # Spatial properties
    resolution_x: Optional[int] = None  # Horizontal resolution in pixels
    resolution_y: Optional[int] = None  # Vertical resolution in pixels
    
    # Color/signal properties
    color_space: Optional[str] = None  # "RGB", "Grayscale", "Multi-channel", "Infrared"
    bits_per_pixel: Optional[int] = None  # Bit depth (8, 16, 32)
    channels: Optional[int] = None  # Number of color channels (1 or 3)
    
    # Optical properties
    field_of_view: Optional[str] = None  # Angular field (e.g., "45°", "60°", "200°")
    wavelength: Optional[str] = None  # For modality-specific wavelengths
    
    # Quality metrics
    quality_score: Optional[float] = None  # Overall quality (0.0-1.0)
    sharpness_score: Optional[float] = None  # Focus/sharpness metric
    illumination_score: Optional[float] = None  # Lighting quality
    contrast_score: Optional[float] = None  # Image contrast
    
    # Artifacts and issues
    has_artifacts: Optional[bool] = None
    artifact_types: List[str] = field(default_factory=list)  # e.g., ["motion", "blur", "glare"]
    image_usable: Optional[bool] = None  # Grader assessment of usability
    
    # Device/acquisition info
    device_model: Optional[str] = None  # Camera/scanner model
    device_manufacturer: Optional[str] = None
    software_version: Optional[str] = None
    acquisition_date: Optional[str] = None  # ISO format YYYY-MM-DD
    acquisition_time: Optional[str] = None  # ISO format HH:MM:SS
    
    # Compression info
    compression: Optional[str] = None  # e.g., "JPEG", "PNG", "TIFF", "RAW"
    compression_quality: Optional[int] = None  # For lossy formats
    file_size_bytes: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ClinicalFindings:
    """Structured clinical findings from image analysis."""
    # Retinal findings
    hemorrhages_present: Optional[bool] = None
    hemorrhage_locations: List[str] = field(default_factory=list)  # "macula", "periphery", etc.
    microaneurysms_present: Optional[bool] = None
    hard_exudates_present: Optional[bool] = None
    cotton_wool_spots_present: Optional[bool] = None
    macular_edema_present: Optional[bool] = None
    macular_edema_severity: Optional[str] = None  # "mild", "moderate", "severe"
    
    # Optic disc findings
    cup_to_disc_ratio: Optional[float] = None  # 0.0-1.0
    optic_disc_pallor: Optional[bool] = None
    optic_disc_cupping: Optional[bool] = None
    disc_size_mm: Optional[float] = None
    
    # Vascular findings
    vessel_tortuosity: Optional[bool] = None
    vessel_narrowing: Optional[bool] = None
    vein_occlusion: Optional[bool] = None
    artery_occlusion: Optional[bool] = None
    neovascularization: Optional[bool] = None
    shunt_vessels: Optional[bool] = None
    
    # Macula-specific
    macular_thickness_microns: Optional[float] = None  # From OCT
    central_subfield_thickness: Optional[float] = None
    macular_volume: Optional[float] = None
    macular_pit: Optional[bool] = None
    
    # General features
    vitreous_hemorrhage: Optional[bool] = None
    retinal_detachment: Optional[bool] = None
    laser_scars_present: Optional[bool] = None
    
    # Additional notes
    findings_notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class DeviceAndAcquisition:
    """Device specifications and acquisition parameters."""
    device_type: Optional[str] = None  # "Fundus Camera", "OCT", "Slit-Lamp", etc.
    manufacturer: Optional[str] = None  # "Topcon", "Zeiss", "Heidelberg", etc.
    model: Optional[str] = None  # Specific model
    
    # Acquisition parameters
    pupil_dilated: Optional[bool] = None
    dilation_agent: Optional[str] = None
    imaging_eye: Optional[str] = None  # "OD", "OS", or "OU"
    scan_type: Optional[str] = None  # For OCT: "3D", "Volume", "Line", etc.
    
    # Software/version info
    software_name: Optional[str] = None
    software_version: Optional[str] = None
    
    # Environmental conditions
    ambient_light_conditions: Optional[str] = None
    room_temperature: Optional[float] = None
    humidity: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class PatientClinicalData:
    """Patient clinical and epidemiological data."""
    # Demographics
    age: Optional[int] = None  # Age in years
    sex: Optional[str] = None  # "M", "F", "O", "U"
    ethnicity: Optional[str] = None
    race: Optional[str] = None
    
    # Systemic conditions
    diabetes: Optional[bool] = None
    diabetes_type: Optional[str] = None  # "Type 1", "Type 2", etc.
    diabetes_duration_years: Optional[int] = None
    hba1c: Optional[float] = None  # Glycemic control
    
    hypertension: Optional[bool] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    
    hyperlipidemia: Optional[bool] = None
    cholesterol_level: Optional[float] = None
    
    # Physical metrics
    bmi: Optional[float] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    
    # Renal function (relevant for DM complications)
    eGFR: Optional[float] = None
    creatinine: Optional[float] = None
    
    # Ocular measurements
    intraocular_pressure_od: Optional[float] = None  # mmHg
    intraocular_pressure_os: Optional[float] = None
    visual_acuity_od: Optional[str] = None  # e.g., "20/20", "20/200"
    visual_acuity_os: Optional[str] = None
    axial_length_od: Optional[float] = None  # mm (from IOLMaster or similar)
    axial_length_os: Optional[float] = None
    keratometry_od: Optional[float] = None  # Corneal power
    keratometry_os: Optional[float] = None
    
    # Medications
    medications: List[str] = field(default_factory=list)  # Current medications
    insulin_dependent: Optional[bool] = None
    
    # Lifestyle/risk factors
    smoking_status: Optional[str] = None  # "current", "former", "never"
    alcohol_use: Optional[str] = None
    exercise_hours_per_week: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class HarmonizedRecord:
    """
    Comprehensive canonical schema for harmonized ophthalmology dataset records.
    
    This is an enterprise-grade schema designed to capture data across all major ophthalmic
    imaging modalities (fundus, OCT, slit-lamp, etc.) and all disease categories with
    support for clinical findings, patient demographics, device information, and quality tracking.
    
    CORE STRUCTURE:
    ===============
    Identifiers:
        image_id: Unique per-image identifier (required)
        dataset_source: Source dataset name (required)
        patient_id: De-identified patient identifier
        visit_number: Sequential visit number for longitudinal studies
        
    IMAGE METADATA:
        modality: Type of imaging (Fundus, OCT, etc.) - required
        laterality: Eye being imaged (OD/OS/OU)
        view_type: Specific anatomical view (macula, optic_disc, etc.)
        image_path: File path or filename
        image_metadata: ImageMetadata object with technical specs
        
    DIAGNOSIS & CLINICAL:
        diagnosis_raw: Original label from dataset
        diagnosis_category: Standardized diagnosis
        diagnosis_confidence: Auto-detection confidence (0.0-1.0)
        multiple_diagnoses: List of secondary diagnoses
        severity: Primary severity grade
        clinical_findings: ClinicalFindings object
        
        disease_specific_fields: Dict for condition-specific data
            DR: dr_severity (ICDR scale), dme_present, dme_severity
            AMD: amd_type (dry/wet), amd_stage (early/intermediate/advanced)
            Glaucoma: cup_disc_ratio, glaucoma_stage, perimetric
            Cataract: cataract_type, cataract_density, cataract_location
            
    PATIENT DATA:
        patient_clinical: PatientClinicalData object with demographics,
                         systemic conditions, medications, vital signs
        
    DEVICE INFO:
        device_and_acquisition: DeviceAndAcquisition with scanner specs,
                               acquisition parameters, software versions
        
    STUDY/VISIT CONTEXT:
        exam_date: Date of examination (YYYY-MM-DD)
        exam_time: Time of examination (HH:MM:SS)
        facility_name: Imaging center/hospital
        visit_number: Sequential visit number
        follow_up_recommended: Boolean for follow-up status
        
    QUALITY & PROVENANCE:
        quality_flags: List of detected issues
        is_valid: Whether record passes baseline validation
        validation_notes: Validation error messages
        annotation_quality: Expert/clinician/crowd annotation
        data_source_reliability: Clinical trial/hospital/crowdsourced
        internal_consistency_check: Passed automated checks
        
    EXTENSIBILITY:
        extra_json: Dict for non-standard unmapped fields
        created_at: ISO timestamp of record creation
    """
    
    # === REQUIRED CORE IDENTIFIERS ===
    image_id: str  # Unique per-image identifier (REQUIRED)
    dataset_source: str  # Source dataset (REQUIRED)
    
    # === OPTIONAL IDENTIFIERS ===
    patient_id: Optional[str] = None  # De-identified patient ID
    visit_number: Optional[int] = None  # For longitudinal tracking (1, 2, 3, ...)
    
    # === IMAGE CHARACTERISTICS (MOSTLY REQUIRED) ===
    modality: str = "Unknown"  # Type of imaging (REQUIRED for analysis)
    laterality: Optional[str] = None  # OD/OS/OU
    view_type: Optional[str] = None  # "macula", "optic_disc", "full_field", "disc_and_macula"
    image_path: Optional[str] = None  # File path or URL
    
    # === DIAGNOSIS & SEVERITY ===
    diagnosis_raw: Optional[str] = None  # Original diagnosis from dataset
    diagnosis_category: Optional[str] = None  # Standardized diagnosis
    diagnosis_confidence: Optional[float] = None  # 0.0-1.0 confidence
    multiple_diagnoses: List[str] = field(default_factory=list)  # Secondary diagnoses
    severity: Optional[str] = None  # Severity grade
    
    # === CLINICAL FINDINGS (RICH STRUCTURED DATA) ===
    clinical_findings: ClinicalFindings = field(default_factory=ClinicalFindings)
    
    # === DISEASE-SPECIFIC FIELDS ===
    disease_specific_fields: Dict[str, Any] = field(default_factory=dict)
    # Examples:
    #   DR: {"dr_severity_icdr": "Severe NPDR", "dme_present": True}
    #   AMD: {"amd_type": "wet", "amd_stage": "advanced"}
    #   Glaucoma: {"cup_disc_ratio": 0.75, "glaucoma_stage": "advanced"}
    #   Cataract: {"cataract_type": "nuclear", "cataract_density": "2.5"}
    
    # === PATIENT DATA ===
    patient_clinical: PatientClinicalData = field(default_factory=PatientClinicalData)
    
    # === DEVICE & ACQUISITION ===
    device_and_acquisition: DeviceAndAcquisition = field(default_factory=DeviceAndAcquisition)
    image_metadata: ImageMetadata = field(default_factory=ImageMetadata)
    
    # === STUDY/EXAM CONTEXT ===
    exam_date: Optional[str] = None  # ISO format YYYY-MM-DD
    exam_time: Optional[str] = None  # ISO format HH:MM:SS
    facility_name: Optional[str] = None  # Imaging center name
    follow_up_recommended: Optional[bool] = None
    
    # === DATA QUALITY & VALIDATION ===
    quality_flags: List[str] = field(default_factory=list)  # Issues detected
    is_valid: bool = True  # Passes basic validation
    validation_notes: Optional[str] = None  # Validation errors
    
    # === PROVENANCE & ANNOTATION ===
    annotation_quality: Optional[str] = None  # "Expert", "Clinician", "Automated", etc.
    data_source_reliability: Optional[str] = None  # "Clinical Trial", "Hospital", etc.
    internal_consistency_check: Optional[bool] = None  # Passed automated checks
    
    # === EXTENSIBILITY ===
    extra_json: Dict[str, Any] = field(default_factory=dict)  # Unmapped fields
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary, serializing nested objects."""
        data = {
            'image_id': self.image_id,
            'dataset_source': self.dataset_source,
            'patient_id': self.patient_id,
            'visit_number': self.visit_number,
            'modality': self.modality,
            'laterality': self.laterality,
            'view_type': self.view_type,
            'image_path': self.image_path,
            'diagnosis_raw': self.diagnosis_raw,
            'diagnosis_category': self.diagnosis_category,
            'diagnosis_confidence': self.diagnosis_confidence,
            'multiple_diagnoses': json.dumps(self.multiple_diagnoses),
            'severity': self.severity,
            'clinical_findings': json.dumps(self.clinical_findings.to_dict()),
            'disease_specific_fields': json.dumps(self.disease_specific_fields),
            'patient_clinical': json.dumps(self.patient_clinical.to_dict()),
            'device_and_acquisition': json.dumps(self.device_and_acquisition.to_dict()),
            'image_metadata': json.dumps(self.image_metadata.to_dict()),
            'exam_date': self.exam_date,
            'exam_time': self.exam_time,
            'facility_name': self.facility_name,
            'follow_up_recommended': self.follow_up_recommended,
            'quality_flags': json.dumps(self.quality_flags),
            'is_valid': self.is_valid,
            'validation_notes': self.validation_notes,
            'annotation_quality': self.annotation_quality,
            'data_source_reliability': self.data_source_reliability,
            'internal_consistency_check': self.internal_consistency_check,
            'extra_json': json.dumps(self.extra_json) if self.extra_json else None,
            'created_at': self.created_at,
        }
        return data
    
    def add_quality_flag(self, flag: str) -> None:
        """Add a quality flag to the record."""
        if flag not in self.quality_flags:
            self.quality_flags.append(flag)
    
    def add_diagnosis(self, diagnosis: str, position: str = "secondary") -> None:
        """Add a secondary diagnosis to the record."""
        if position == "primary":
            self.diagnosis_category = diagnosis
        else:
            if diagnosis not in self.multiple_diagnoses:
                self.multiple_diagnoses.append(diagnosis)
    
    def set_disease_field(self, field_name: str, value: Any) -> None:
        """Set a disease-specific field."""
        self.disease_specific_fields[field_name] = value
    
    def get_disease_field(self, field_name: str, default: Any = None) -> Any:
        """Get a disease-specific field."""
        return self.disease_specific_fields.get(field_name, default)
    
    def validate(self) -> bool:
        """Comprehensive validation of record integrity."""
        errors = []
        
        # Check required fields
        if not self.image_id or not self.dataset_source:
            errors.append("Missing required fields: image_id or dataset_source")
        
        # Validate age
        if self.patient_clinical.age is not None:
            if not 0 <= self.patient_clinical.age <= 150:
                self.add_quality_flag("age_out_of_reasonable_range")
                errors.append(f"Invalid age: {self.patient_clinical.age}")
        
        # Validate confidence scores
        if self.diagnosis_confidence is not None:
            if not 0.0 <= self.diagnosis_confidence <= 1.0:
                self.add_quality_flag("invalid_confidence_score")
                errors.append("Confidence score not in [0.0, 1.0]")
        
        # Validate clinical measurements
        if self.clinical_findings.cup_to_disc_ratio is not None:
            if not 0.0 <= self.clinical_findings.cup_to_disc_ratio <= 1.0:
                self.add_quality_flag("invalid_cup_disc_ratio")
                errors.append("Cup-to-disc ratio not in [0.0, 1.0]")
        
        if self.patient_clinical.bmi is not None:
            if not 10 <= self.patient_clinical.bmi <= 60:
                self.add_quality_flag("bmi_out_of_reasonable_range")
                errors.append(f"Unusual BMI: {self.patient_clinical.bmi}")
        
        if self.patient_clinical.intraocular_pressure_od is not None:
            if not 5 <= self.patient_clinical.intraocular_pressure_od <= 80:
                self.add_quality_flag("iop_od_out_of_range")
                errors.append("IOP OD out of range")
        
        if self.patient_clinical.intraocular_pressure_os is not None:
            if not 5 <= self.patient_clinical.intraocular_pressure_os <= 80:
                self.add_quality_flag("iop_os_out_of_range")
                errors.append("IOP OS out of range")
        
        # Set validation status
        self.is_valid = len(errors) == 0
        if errors:
            self.validation_notes = "; ".join(errors)
        
        return self.is_valid


def create_schema_columns() -> List[str]:
    """Return list of canonical schema column names for DataFrame export."""
    return [
        # Identifiers
        'image_id',
        'dataset_source',
        'patient_id',
        'visit_number',
        
        # Imaging
        'modality',
        'laterality',
        'view_type',
        'image_path',
        
        # Diagnosis
        'diagnosis_raw',
        'diagnosis_category',
        'diagnosis_confidence',
        'multiple_diagnoses',
        'severity',
        'clinical_findings',
        'disease_specific_fields',
        
        # Patient
        'patient_clinical',
        
        # Device
        'device_and_acquisition',
        'image_metadata',
        
        # Exam context
        'exam_date',
        'exam_time',
        'facility_name',
        'follow_up_recommended',
        
        # Quality
        'quality_flags',
        'is_valid',
        'validation_notes',
        'annotation_quality',
        'data_source_reliability',
        'internal_consistency_check',
        
        # Extensibility
        'extra_json',
        'created_at',
    ]


def get_enum_values(enum_class) -> List[str]:
    """Get all values from an Enum class."""
    return [item.value for item in enum_class]


def create_harmonized_record_template(**kwargs) -> HarmonizedRecord:
    """
    Create a HarmonizedRecord with specified values.
    
    Args:
        image_id (str): Unique image identifier (required)
        dataset_source (str): Source dataset (required)
        **kwargs: Additional fields to populate
        
    Returns:
        HarmonizedRecord: Populated record
    """
    return HarmonizedRecord(**kwargs)


# Field mapping helpers for common dataset column names
COMMON_IMAGE_ID_PATTERNS = [
    'image_id', 'image_ID', 'ImageID', 'id', 'ID', 
    'sample_id', 'file_name', 'filename', 'file_path', 'filepath'
]

COMMON_DIAGNOSIS_PATTERNS = [
    'diagnosis', 'label', 'class', 'target', 'finding',
    'disease', 'condition', 'pathology', 'result'
]

COMMON_AGE_PATTERNS = [
    'age', 'Age', 'patient_age', 'age_years', 'age_at_visit'
]

COMMON_SEX_PATTERNS = [
    'sex', 'Sex', 'gender', 'Gender', 'patient_sex'
]

COMMON_MODALITY_PATTERNS = [
    'modality', 'Modality', 'imaging_type', 'image_type', 'image_modality'
]

COMMON_LATERALITY_PATTERNS = [
    'laterality', 'Laterality', 'eye', 'Eye', 'left_right', 'OD_OS'
]
