# Rules & Harmonization Logic

Complete documentation of diagnosis mapping, severity grading, modality inference, and harmonization rules.

---

## Overview

The `src/rules.py` module provides comprehensive harmonization rules for:
- **269+ diagnosis keywords** → 28 standardized categories + severity
- **8+ severity grading systems** (ICDR for DR, stages for AMD, etc.)
- **150+ modality patterns** across 12 imaging types
- **Multi-language laterality detection** (English, French, Spanish)
- **37+ clinical finding types** detection
- **Image quality assessment** (5 levels)
- **Patient demographic standardization**

---

## Diagnosis Mapping (269+ Keywords)

Maps raw diagnosis text to standardized (category, severity) tuples.

### Diabetic Retinopathy (36 keywords)
```python
'diabetic retinopathy' → ('Diabetic Retinopathy', None)
'dr' → ('Diabetic Retinopathy', None)

# Severity (ICDR Scale)
'mild npdr' → ('Diabetic Retinopathy', 'Mild')
'moderate npdr' → ('Diabetic Retinopathy', 'Moderate')
'severe npdr' → ('Diabetic Retinopathy', 'Severe')
'proliferative dr' → ('Diabetic Retinopathy', 'Proliferative')
'pdr' → ('Diabetic Retinopathy', 'Proliferative')
```

### Diabetic Macular Edema (10+ keywords)
```python
'diabetic macular edema' → ('Diabetic Macular Edema', None)
'dme' → ('Diabetic Macular Edema', None)
'macular thickening' → ('Diabetic Macular Edema', None)
```

### AMD (36 keywords)
```python
'age-related macular degeneration' → ('Age-Related Macular Degeneration', None)
'amd' → ('Age-Related Macular Degeneration', None)

# Wet/Dry distinction
'wet amd' → ('Age-Related Macular Degeneration', 'Severe')
'dry amd' → ('Age-Related Macular Degeneration', 'Mild')
'neovascular amd' → ('Age-Related Macular Degeneration', 'Severe')
'geographic atrophy' → ('Age-Related Macular Degeneration', 'Severe')
```

### Cataract (50+ keywords)
```python
'cataract' → ('Cataract', None)

# Type-based severity
'nuclear cataract' → ('Cataract', 'Moderate')
'cortical cataract' → ('Cataract', 'Moderate')
'posterior subcapsular' → ('Cataract', 'Severe')

# Density-based severity
'immature cataract' → ('Cataract', 'Mild')
'mature cataract' → ('Cataract', 'Moderate')
'hypermature cataract' → ('Cataract', 'Severe')
```

### Glaucoma (40+ keywords)
```python
'glaucoma' → ('Glaucoma', None)
'open angle glaucoma' → ('Glaucoma', None)
'angle closure' → ('Glaucoma', None)
'normal tension glaucoma' → ('Glaucoma', None)
'secondary glaucoma' → ('Glaucoma', None)
```

### Corneal Disease (40+ keywords)
```python
'corneal disease' → ('Corneal Disease', None)
'corneal scar' → ('Corneal Disease', None)
'keratoconus' → ('Corneal Disease', None)
'pterygium' → ('Corneal Disease', None)
'corneal ulcer' → ('Corneal Disease', None)
```

### Vascular Occlusions (20+ keywords)
```python
'central retinal artery occlusion' → ('Vascular Occlusion', None)
'crao' → ('Vascular Occlusion', None)
'branch retinal vein occlusion' → ('Vascular Occlusion', None)
'brvo' → ('Vascular Occlusion', None)
'hemi-retinal artery occlusion' → ('Vascular Occlusion', None)
```

### Retinal Detachment (15+ keywords)
```python
'retinal detachment' → ('Retinal Detachment', None)
'rhegmatogenous' → ('Retinal Detachment', None)
'tractional' → ('Retinal Detachment', None)
'macula-on' → ('Retinal Detachment', None)
'macula-off' → ('Retinal Detachment', None)
```

### Plus 14+ More Categories
- Myopia, Hyperopia, Astigmatism, Presbyopia
- Macular Edema (non-diabetic)
- Drusen
- Hypertensive Retinopathy
- Refractive Errors
- Optic Disc Disease
- Vitreous Disease
- Retinoblastoma
- Cotton Wool Spots
- Hard Exudates
- Microaneurysms
- Hemorrhages
- Neovascularization

---

## Severity Grading (8+ Systems)

Specialized severity scales for each condition.

### Diabetic Retinopathy (ICDR)
```python
0: 'None'
1: 'Mild'      # Mild NPDR
2: 'Moderate'  # Moderate NPDR
3: 'Severe'    # Severe NPDR
4: 'Proliferative'
```

### AMD
```python
0: 'None'
1: 'Early'
2: 'Intermediate'
3: 'Advanced'
```

### Cataract
```python
0: 'None'
1: 'Mild'
2: 'Moderate'
3: 'Mature'
4: 'Hypermature'
```

### Glaucoma
```python
0: 'None'
1: 'Mild'
2: 'Moderate'
3: 'Advanced'
4: 'Terminal'
```

### Corneal Disease
```python
0: 'None'
1: 'Mild'
2: 'Moderate'
3: 'Severe'
```

### Hypertensive Retinopathy
```python
0: 'None'
1: 'Grade 1'
2: 'Grade 2'
3: 'Grade 3'
4: 'Grade 4' (Malignant)
```

### Retinal Detachment
```python
0: 'None'
1: 'Macula-on'
2: 'Macula-off'
3: 'Rhegmatogenous'
4: 'Tractional'
```

### Diabetic Macular Edema
```python
0: 'None'
1: 'Mild'
2: 'Moderate'
3: 'Severe'
```

---

## Modality Inference (150+ Patterns, 12 Modalities)

Auto-detects imaging type from dataset name or image description.

### Fundus Camera
**30+ patterns:**
fundus, color fundus, cfp, optos, widefield, messidor, eyepacs, aptos, refuge, color fundus photograph, digital fundus, fundus image, fundus photo, disc, macula view, macular view, posterior pole, peripheral retina

**Example:**
```python
infer_modality("Messidor", None) → "Fundus"
infer_modality("color_fundus_photo", None) → "Fundus"
```

### OCT
**25+ patterns:**
oct, optical coherence, spectral domain, sd-oct, sdoct, time domain, td-oct, swept source, ss-oct, ssoct, structural, cross section, b-scan, volumetric, 3d, volume, oct scan, oct imaging, macular oct, optic disc oct, anterior segment oct, as-oct

**Example:**
```python
infer_modality("OCT_scan", None) → "OCT"
infer_modality("spectral domain OCT", None) → "OCT"
```

### OCTA (OCT Angiography)
**15+ patterns:**
octa, oct angiography, oct angio, vascular imaging, capillary network, vessel density

**Example:**
```python
infer_modality("OCTA", None) → "OCTA"
infer_modality("oct angiography", None) → "OCTA"
```

### Slit-Lamp
**20+ patterns:**
slit, slit-lamp, slit lamp, anterior, anterior segment, anterior chamber, lens, cornea, iris, angle, goniosc, biomicroscopy, slit lamp photography, anterior segment imaging

### Fluorescein Angiography
**15+ patterns:**
fa, fag, fluorescein, angiography, fa imaging, icg, indocyanine, angiogram, fundus angiography, retinal angiography, fluorescein angiogram

### Plus 7 More Modalities
- Fundus Autofluorescence (FAF)
- Infrared Reflectance
- Ultrasound (A/B-scan)
- Anterior Segment
- Specular Microscopy
- Visual Field (Perimetry)
- Anterior Segment OCT

---

## Laterality Detection (Multi-Language)

Infers eye side from various input formats.

### English
**Right (OD):**
right, od, oculus dexter, re, r, r., right eye, r eye, o.d., odex

**Left (OS):**
left, os, oculus sinister, le, l, l., left eye, l eye, o.s., osex

**Both (OU):**
both, ou, oculus uterque, bilateral, binocular, both eyes, combined

### Filename Patterns
```python
infer_laterality("image_r.jpg") → "OD"
infer_laterality("image_l.jpg") → "OS"
infer_laterality("exam_od_2024") → "OD"
infer_laterality("scan-os-final") → "OS"
```

### French
```python
infer_laterality("droit") → "OD"      # Right
infer_laterality("gauche") → "OS"     # Left
```

### Spanish
```python
infer_laterality("derecha") → "OD"    # Right
infer_laterality("izquierda") → "OS"  # Left
```

---

## Clinical Findings Detection (37 Types)

Auto-detects clinical signs from diagnosis or notes text.

### Hemorrhages (5 types)
- hemorrhages
- microhemorrhages
- dot_blot_hemorrhages
- flame_hemorrhages
- preretinal_hemorrhage

### Exudates (3 types)
- hard_exudates
- soft_exudates
- exudates

### Edema & Fluid (4 types)
- macular_edema
- retinal_thickening
- serous_detachment
- cysts

### Neovascularization (4 types)
- neovascularization
- neovascular_disc
- choroidal_neovascularization
- retinal_neovascularization

### Vessel Changes (4 types)
- vessel_tortuosity
- vessel_narrowing
- vessel_beading
- arteriovenous_nicking

### Retinal Changes (7 types)
- cotton_wool_spots
- retinal_folds
- hard_drusen
- soft_drusen
- geographic_atrophy
- macular_scarring
- retinal_thinning

### Optic Nerve (4 types)
- optic_disc_pallor
- optic_disc_cupping
- optic_nerve_swelling
- large_cup_disc_ratio

### Other (6 types)
- vitreous_hemorrhage
- subretinal_hemorrhage
- retinal_detachment
- laser_scars
- microaneurysms
- myelin_sheath

**Example:**
```python
findings = find_clinical_findings("Hemorrhage, exudates, and edema visible")
# Result: ['hemorrhages', 'hard_exudates', 'macular_edema']
```

---

## Image Quality Assessment

Maps quality descriptors to standardized levels.

### Quality Levels
```python
'Excellent'   # Perfect focus, clear view
'Good'        # Very good, adequate for analysis
'Moderate'    # Fair, acceptable
'Poor'        # Low quality, artifacts present
'Ungradable'  # Cannot assess
```

**Example:**
```python
assess_image_quality("Excellent quality, perfect focus") → "Excellent"
assess_image_quality("Poor quality with motion blur") → "Poor"
```

### Artifact Detection
```python
detect_artifacts("Motion blur and media opacity present")
# Result: ['motion_artifact', 'media_opacity']
```

**Artifact Types:**
- motion_artifact
- media_opacity
- inadequate_illumination
- eyelashes
- glare
- artifact_present

---

## Patient Demographic Standardization

Standardizes age, sex, and ethnicity fields.

### Age Normalization
```python
standardize_age(45) → 45
standardize_age("67.5") → 67
standardize_age(200) → None    # Out of range
standardize_age(None) → None

# Valid range: 0-150 years
```

### Sex Standardization
```python
standardize_sex('M') → 'M'
standardize_sex('male') → 'M'
standardize_sex('F') → 'F'
standardize_sex('female') → 'F'
standardize_sex('O') → 'O'      # Other
standardize_sex('U') → 'U'      # Unknown
```

### Ethnicity Standardization
```python
standardize_ethnicity('Caucasian') → 'Caucasian'
standardize_ethnicity('White') → 'Caucasian'
standardize_ethnicity('Asian') → 'Asian'
standardize_ethnicity('Black') → 'African'
standardize_ethnicity('Hispanic') → 'Hispanic'

# Categories: Caucasian, African, Asian, Hispanic, 
#             Middle Eastern, Pacific Islander, Mixed, Other
```

---

## Core Functions

### normalize_diagnosis(diagnosis_text)
```python
Returns: (category, severity) tuple
Example: normalize_diagnosis("moderate npdr") 
         → ('Diabetic Retinopathy', 'Moderate')
```

### infer_modality(dataset_name, image_description)
```python
Returns: Modality name or None
Example: infer_modality("Messidor", "fundus_image.jpg")
         → "Fundus"
```

### infer_laterality(value)
```python
Returns: 'OD', 'OS', 'OU', or None
Example: infer_laterality("right eye")
         → "OD"
```

### infer_severity_from_diagnosis(diagnosis_text, diagnosed_condition)
```python
Returns: Severity level or None
Example: infer_severity_from_diagnosis("severe glaucoma", "Glaucoma")
         → "Severe"
```

### find_clinical_findings(text)
```python
Returns: List of finding types
Example: find_clinical_findings("hemorrhage and edema")
         → ['hemorrhages', 'macular_edema']
```

### assess_image_quality(quality_text, has_artifacts)
```python
Returns: Quality level ('Excellent', 'Good', 'Moderate', 'Poor', 'Ungradable')
Example: assess_image_quality("excellent quality")
         → "Excellent"
```

### detect_column_role(column_name)
```python
Returns: Field type ('diagnosis', 'modality', 'laterality', etc.) or None
Priority: diagnosis → image_id → image_path → laterality → 
          modality → patient_age → patient_sex → resolution
```

### harmonize_column_value(field_type, value, context)
```python
Returns: Harmonized value
Example: harmonize_column_value('diagnosis', 'dr', {})
         → 'Diabetic Retinopathy'
```

---

## Pattern Matching Strategy

All inference uses **longest-match-first** strategy for robustness:

1. Normalize input (lowercase, remove punctuation)
2. Sort patterns by length (longest first)
3. Match in order (most specific first)
4. Return first match found

**Example:**
```python
# Text: "oct angiography"
# Patterns sorted: ["oct angiography", "angiography", "octa", "oct"]
# Result: Matches "oct angiography" → OCTA
```

---

## Validation Confidence

All inferences include optional confidence scoring.

**High confidence (>0.85):**
- Exact keyword match
- Specific pattern match
- Standard codes (ICD-10, ICDR)

**Medium confidence (0.5-0.85):**
- Partial string match
- Inferred from context
- Secondary pattern

**Low confidence (<0.5):**
- Ambiguous keywords
- Fallback inference
- Missing data

---

