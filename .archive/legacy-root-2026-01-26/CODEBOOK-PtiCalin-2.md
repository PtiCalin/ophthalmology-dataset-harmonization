# Codebook

Data dictionary and enumeration reference for all standardized values.

---

## Design Principles

### Standardization Rationale

**Clinical Standards Alignment:** Values based on established medical classifications (SNOMED-CT, ICD-10, ICDR scales).

**Interoperability:** Consistent coding enables data exchange across systems and institutions.

**Research Compatibility:** Standardized categories support meta-analysis and comparative studies.

**Extensibility:** Framework allows addition of new values without breaking existing implementations.

### Validation Approach

**Enum Constraints:** Restricted to predefined values prevents data entry errors.

**Case-Insensitive Matching:** Accommodates varied input formats while ensuring consistency.

**Alias Support:** Multiple representations (abbreviations, translations) increase compatibility.

## Modality (12 Values)

| Code | Name | Description | Example Modalities |
|------|------|-------------|-------------------|
| Fundus | Color Fundus Photography | Standard retinal imaging | CFP, Optos, Widefield |
| OCT | Optical Coherence Tomography | Structural imaging | SD-OCT, SS-OCT, 3D |
| OCTA | OCT Angiography | Vascular imaging | Vascular networks |
| Slit-Lamp | Slit-Lamp Biomicroscopy | Anterior segment | Anterior chamber |
| Fluorescein Angiography | Fundus Angiography | Dye studies | FA, ICG |
| Fundus Autofluorescence | FAF | Autofluorescence | FAF imaging |
| Infrared | Infrared Reflectance | Reflectance imaging | Near-infrared |
| Ultrasound | Ultrasound Imaging | Acoustic imaging | A-scan, B-scan |
| Anterior Segment | Anterior Imaging | Front of eye | Corneal, iris |
| Specular Microscopy | Endothelial Imaging | Corneal cells | Cell count |
| Visual Field | Perimetry | Visual testing | Automated, threshold |
| Unknown | Unknown | Unidentified | Default |

**Rationale:** Comprehensive coverage of ophthalmology imaging modalities used in clinical practice and research.

---

## Laterality (3 Values)

| Code | Name | English | French | Spanish | Codes |
|------|------|---------|--------|---------|-------|
| OD | Right Eye | right, re, r | droit | derecha | od, oculus dexter |
| OS | Left Eye | left, le, l | gauche | izquierda | os, oculus sinister |
| OU | Both Eyes | both, bilateral | les deux | ambos | ou, oculus uterque |

**Filename Patterns:**

- OD: `_r.`, `-r-`, `_od`, `-od`, `_right`, `-right`
- OS: `_l.`, `-l-`, `_os`, `-os`, `_left`, `-left`

**Rationale:** Multi-language support enables processing of international datasets. Filename pattern recognition handles automated data ingestion from various sources.

---

## Diagnosis Category (28 Values)

| Category | SNOMED-CT Equivalents | Related ICD-10 | Severity Scale |
|----------|----------------------|-----------------|-----------------|
| Normal | Normal | Z01.00 | None |
| Diabetic Retinopathy | Diabetic retinopathy | E11.3xx | ICDR (5 grades) |
| Diabetic Macular Edema | DME | E11.35 | 4-level |
| AMD | Age-related macular degeneration | H35.3 | 3-level |
| Cataract | Cataract | H25-H26 | 5-level (by type) |
| Glaucoma | Glaucoma | H40 | 5-level (by stage) |
| Glaucoma Suspect | Glaucoma suspect | H40.00 | None |

**Rationale:** Categories based on clinical classifications with standardized coding systems. Severity scales derived from validated clinical guidelines and research standards.
| Corneal Disease | Corneal disease | H16-H19 | 4-level |
| Retinoblastoma | Retinoblastoma | C69 | 5-level (Murphree) |
| Macular Edema | Macular edema (non-diabetic) | H35.81 | 4-level |
| Drusen | Drusen | H35.36 | 3-level |
| Myopia | Myopia | H52.1 | 5-level |
| Hyperopia | Hyperopia | H52.0 | 5-level |
| Astigmatism | Astigmatism | H52.2 | 5-level |
| Presbyopia | Presbyopia | H52.4 | None |
| Hypertensive Retinopathy | Hypertensive retinopathy | H35.0 | 4-level (Grade 1-4) |
| Retinal Detachment | Retinal detachment | H33 | 4-level |
| Retinal Vein Occlusion | Central/branch RVO | H34.8 | None |
| Retinal Artery Occlusion | Central/branch RAO | H34.1 | None |
| Optic Disc Disease | Optic disc disorders | H47.2 | None |
| Vitreous Hemorrhage | Vitreous hemorrhage | H43.1 | 3-level |
| Keratoconus | Keratoconus | H18.6 | 4-level |
| Pterygium | Pterygium | H11.0 | 3-level |
| Cotton Wool Spots | Cotton wool spots | H35.81 | None |
| Hard Exudates | Retinal exudates | H35.81 | None |
| Microaneurysms | Microaneurysm | H35.81 | None |
| Hemorrhages | Retinal hemorrhage | H35.81 | 3-level |
| Neovascularization | Neovascular | H35.81 | None |
| Other | Other condition | None | None |

---

## Severity Levels (6 Values)

### Generic Scale (Used by Multiple Conditions)

```txt
None         - No disease present
Mild         - Minimal or early changes
Moderate     - Noticeable disease, functionally significant
Severe       - Advanced disease, visual impact likely
Proliferative - Most severe form (neovascular/proliferative)
Very Severe  - Terminal/worst-case scenario
```

### Diabetic Retinopathy (ICDR Scale) [International Standard]

```txt
0: No DR                   - No disease detected
1: Mild NPDR              - Microaneurysms only or hemorrhages only
2: Moderate NPDR          - Microaneurysms + hemorrhages + hard exudates
3: Severe NPDR            - Severe intraretinal hemorrhages, beading, shunts
4: Proliferative DR (PDR) - Neovascularization of disc or elsewhere
```

### AMD (3-Level)

```txt
0: None           - No macular disease
1: Early          - Small drusen, pigment changes
2: Intermediate   - Intermediate drusen or geographic atrophy
3: Advanced       - Geographic atrophy or choroidal neovascularization
```

### Cataract (5-Level by Density)

```txt
0: None       - No lens opacity
1: Mild       - Immature, minimal opacity
2: Moderate   - Some vision impact
3: Mature     - Dense opacity, significant vision loss
4: Hypermature - Over-mature, may be brunescent or require urgent surgery
```

### Glaucoma (5-Level by Stage)

```txt
0: None       - No glaucoma
1: Mild       - Early structural/functional changes
2: Moderate   - Mid-stage disease
3: Advanced   - Significant field loss or cup-disc ratio >0.8
4: Terminal   - Near-total vision loss
```

### Hypertensive Retinopathy (4-Level, Keith-Wagener)

```txt
0: None       - No hypertensive retinopathy
1: Grade 1    - Arteriovenous nicking, vasoconstriction
2: Grade 2    - Grade 1 + flame hemorrhages, cotton wool spots
3: Grade 3    - Grade 2 + papilledema, Roth spots
4: Grade 4 (Malignant) - Grade 3 + optic disc swelling, microinfarcts
```

---

## Sex (4 Values)

| Code | Name | Variants | Notes |
|------|------|----------|-------|
| M | Male | male, man, masculino, homme, herr | Biological male |
| F | Female | female, woman, femenino, femme, frau | Biological female |
| O | Other | other, non-binary, prefer not to say | Other/non-binary |
| U | Unknown | unknown, unclear, not specified, n/a | Not reported |

---

## Diabetes Type (5 Values)

| Type | Description | HbA1c Typical | Risk Factors |
|------|-------------|---------------|--------------|
| Type 1 | Insulin-dependent | Variable | Autoimmune, young onset |
| Type 2 | Non-insulin initially | 5-10% | Age, obesity, family history |
| Gestational | Pregnancy-related | Variable | Pregnancy, BMI >25 |
| Unknown | Type not specified | Unknown | Missing data |
| No Diabetes | No diabetes present | <5.7% | Non-diabetic |

---

## DR Severity (ICDR Scale) [Validated International Standard]

| Grade | Name | ETDRS Code | Microaneurysms | Hemorrhages | Hard Exudates | Signs |
|-------|------|-----------|----------------|-------------|---------------|-------|
| 0 | No DR | 10 | Absent | Absent | Absent | None |
| 1 | Mild NPDR | 20 | Present (>1) OR | Only dots/blots | Absent | Microaneurysms only |
| 2 | Moderate NPDR | 35 | Present | Present | May be present | Venous beading? Shunts? |
| 3 | Severe NPDR | 43-47 | Many | Extensive | Present | ≥1 severity sign* |
| 4 | PDR | 53-61 | Many | Many | May be present | New vessels |

*Severity signs: Extensive hemorrhages (4 quadrants), venous beading (2 quadrants), intraretinal microvascular abnormalities (1 quadrant)

---

## Annotation Quality (6 Values)

| Level | Expertise | Validation | Error Rate | Best For |
|-------|-----------|-----------|-----------|----------|
| Expert | Ophthalmology subspecialist | Gold standard | <2% | Research, validation |
| Clinician | General eye care provider | Trained | 3-5% | Clinical use |
| Consensus | 3+ independent graders agree | Majority vote | 2-4% | AI training |
| Crowd-sourced | Community contributed | Crowd review | 5-10% | Large-scale annotation |
| Automated | AI/algorithmic | No human review | 5-15% | Speed/scale |
| Unverified | Not validated | No validation | Unknown | Data exploration |

---

## Data Source (7 Values)

| Source | Setting | Bias Considerations | Use Case |
|--------|---------|-------------------|----------|
| Clinical Trial | Research study | Selection bias, high-quality imaging | Validation, benchmarking |
| Hospital Records | Clinical practice | Referral bias, variable quality | Real-world performance |
| Telehealth | Remote settings | Compressed imaging, lighting issues | Practical deployment |
| Research Study | University/institute | Well-controlled, screened | Algorithm development |
| Public Dataset | Kaggle/public repo | Mixed quality, distribution shift | Training/learning |
| Crowdsourced | Online platforms | High variability | Data augmentation |
| Synthetic Data | Generated | Artificial | Edge case testing |

---

## Image Quality (5 Levels)

| Level | Sharpness | Illumination | Artifacts | Usability |
|-------|-----------|--------------|-----------|-----------|
| Excellent | Perfect focus | Optimal | None | Fully gradable |
| Good | Very clear | Adequate | Minor | Fully gradable |
| Moderate | Acceptable | Fair | Some | Gradable with care |
| Poor | Blurry | Dim/bright | Moderate | Difficult to grade |
| Ungradable | Not focused | Inadequate | Extensive | Cannot assess |

**Artifact Types:**

- Motion blur
- Media opacity (cataract, corneal)
- Inadequate illumination
- Eyelash/lid occlusion
- Specular glare
- Out of focus
- Noise/interference

---

## Age Groups (Reference)

| Category | Age Range | Description |
|----------|-----------|-------------|
| Infant | 0-2 | Newborn to toddler |
| Toddler | 2-5 | Early childhood |
| Child | 5-13 | School age |
| Adolescent | 13-18 | Teenage |
| Adult | 18-65 | Working age |
| Elderly | 65-130 | Senior/geriatric |

**Valid range: 0-130 years**

---

## Ethnicity/Race (8 Values)

| Category | Variants | Notes |
|----------|----------|-------|
| Caucasian | White, European, Anglo | European descent |
| African | Black, African American, Afro-Caribbean | African descent |
| Asian | East Asian, South Asian, Indian, Chinese, Japanese | Asian descent |
| Hispanic | Latino, Latin American, Spanish | Spanish/Portuguese speaking |
| Middle Eastern | Arab, Persian, Turkish | Middle Eastern/North African |
| Pacific Islander | Hawaiian, Pacific Islander | Pacific Island descent |
| Mixed | Multiracial, Biracial | Multiple ethnicities |
| Other | Other, prefer not to say, unknown | Not classified |

---

## Clinical Finding Types (37 Values)

### Hemorrhage Subtypes (5)
- Hemorrhages (general)
- Microhemorrhages (tiny)
- Dot-blot hemorrhages (intraretinal)
- Flame hemorrhages (nerve fiber layer)
- Preretinal hemorrhage (subhyaloid)

### Exudate Subtypes (3)
- Hard exudates (lipid, yellow)
- Soft exudates (cotton wool, white spots)
- Exudates (general)

### Microstructure (3)
- Microaneurysms
- Microaneurysm clusters
- Dot-blot lesions

### Edema & Fluid (4)
- Macular edema
- Retinal thickening
- Serous detachment
- Cystoid cysts

### Neovascularization (4)
- Neovascularization (general)
- Neovascular disc (NVD)
- Choroidal neovascularization (CNV)
- Retinal neovascularization

### Vascular Changes (4)
- Vessel tortuosity
- Vessel narrowing
- Vessel beading
- Arteriovenous nicking

### Retinal Changes (7)
- Cotton wool spots
- Retinal folds
- Hard drusen
- Soft drusen
- Geographic atrophy
- Macular scarring
- Retinal thinning

### Optic Nerve (4)
- Optic disc pallor
- Optic disc cupping
- Optic nerve swelling
- Large cup-disc ratio

### Other (6)
- Vitreous hemorrhage
- Subretinal hemorrhage
- Retinal detachment
- Laser scars
- Myelin sheath
- Shunt vessels

---

## Modality Pattern Examples

**Quick Reference for Common Patterns:**

| Modality | Top Patterns |
|----------|--------------|
| Fundus | fundus, cfp, messidor, optos, eyepacs |
| OCT | oct, sd-oct, swept source, 3d, volume |
| OCTA | octa, angiography, vessel density |
| Slit-Lamp | slit, anterior, cornea, iris |
| FA | fa, fluorescein, angiography |
| FAF | faf, autofluorescence |
| Infrared | infrared, ir, nir |
| Ultrasound | ultrasound, b-scan, a-scan |

---

## Quick Reference: Field Mapping

**Common column name → Field type:**

| Pattern | Detects As |
|---------|-----------|
| diagnosis, label, disease, condition | diagnosis |
| image_id, filename, file_name, img_id | image_id |
| path, image, img, photo | image_path |
| eye, side, laterality, od, os | laterality |
| modality, imaging, type, technique | modality |
| age, patient_age | patient_age |
| sex, gender, patient_sex | patient_sex |
| resolution, pixel, dpi | resolution |

---

## Validation Ranges

| Field | Min | Max | Unit | Notes |
|-------|-----|-----|------|-------|
| Age | 0 | 150 | years | Strict bounds |
| IOP | 5 | 80 | mmHg | Both eyes |
| BMI | 10 | 60 | kg/m² | Adult range |
| Systolic BP | 80 | 200 | mmHg | Reasonable range |
| Diastolic BP | 40 | 120 | mmHg | Reasonable range |
| eGFR | 0 | 150 | mL/min/1.73m² | Kidney function |
| Creatinine | 0 | 10 | mg/dL | General range |
| Cup-disc ratio | 0.0 | 1.0 | ratio | Normalized |
| Confidence | 0.0 | 1.0 | proportion | Normalized |
| HbA1c | 4 | 15 | % | Typical range |

---
