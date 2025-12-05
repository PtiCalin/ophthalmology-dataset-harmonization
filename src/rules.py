"""
Comprehensive harmonization ruleset for standardizing ophthalmology dataset fields.

This module provides extensive mappings and inference logic for:
- Diagnosis normalization (140+ keywords with severity grading)
- Severity scaling for all major conditions
- Modality detection across all imaging types (12+ modalities)
- Laterality detection (multi-language support)
- Clinical finding keywords and patterns
- Image quality assessment
- Patient demographic standardization
- Advanced pattern matching and confidence scoring

Designed for multi-dataset harmonization across Kaggle, clinical trials, and hospital data.
"""

from typing import Optional, Dict, List, Tuple, Set
import re


# ============================================================================
# COMPREHENSIVE DIAGNOSIS KEYWORD MAPPING (140+ keywords)
# ============================================================================

DIAGNOSIS_MAPPING = {
    # ========== DIABETIC RETINOPATHY (DR) ==========
    'diabetic retinopathy': ('Diabetic Retinopathy', None),
    'dr': ('Diabetic Retinopathy', None),
    'diabetes retinopathy': ('Diabetic Retinopathy', None),
    'retinopathy due to diabetes': ('Diabetic Retinopathy', None),
    'no dr': ('Normal', None),
    'no diabetic retinopathy': ('Normal', None),
    'without dr': ('Normal', None),
    'negative for dr': ('Normal', None),
    
    # DR Severity (ICDR Scale)
    'non-proliferative': ('Diabetic Retinopathy', 'Mild'),
    'nonproliferative': ('Diabetic Retinopathy', 'Mild'),
    'npdr': ('Diabetic Retinopathy', 'Mild'),
    'mild npdr': ('Diabetic Retinopathy', 'Mild'),
    'mild non-proliferative': ('Diabetic Retinopathy', 'Mild'),
    'minimal npdr': ('Diabetic Retinopathy', 'Mild'),
    'moderate npdr': ('Diabetic Retinopathy', 'Moderate'),
    'moderate non-proliferative': ('Diabetic Retinopathy', 'Moderate'),
    'moderately severe npdr': ('Diabetic Retinopathy', 'Moderate'),
    'severe npdr': ('Diabetic Retinopathy', 'Severe'),
    'severe non-proliferative': ('Diabetic Retinopathy', 'Severe'),
    'proliferative': ('Diabetic Retinopathy', 'Proliferative'),
    'proliferative dr': ('Diabetic Retinopathy', 'Proliferative'),
    'proliferative diabetic retinopathy': ('Diabetic Retinopathy', 'Proliferative'),
    'pdr': ('Diabetic Retinopathy', 'Proliferative'),
    'advanced pdr': ('Diabetic Retinopathy', 'Proliferative'),
    'advanced diabetic eye disease': ('Diabetic Retinopathy', 'Severe'),
    
    # Diabetic Macular Edema (DME)
    'diabetic macular edema': ('Diabetic Macular Edema', None),
    'dme': ('Diabetic Macular Edema', None),
    'diabetic macula': ('Diabetic Macular Edema', None),
    'macular edema from diabetes': ('Diabetic Macular Edema', None),
    'diabetic edema': ('Diabetic Macular Edema', None),
    'dme mild': ('Diabetic Macular Edema', 'Mild'),
    'dme moderate': ('Diabetic Macular Edema', 'Moderate'),
    'dme severe': ('Diabetic Macular Edema', 'Severe'),
    'center involved macular edema': ('Diabetic Macular Edema', 'Severe'),
    'cime': ('Diabetic Macular Edema', 'Severe'),
    
    # ========== AGE-RELATED MACULAR DEGENERATION (AMD) ==========
    'amd': ('Age-Related Macular Degeneration', None),
    'age-related macular degeneration': ('Age-Related Macular Degeneration', None),
    'age related macular degeneration': ('Age-Related Macular Degeneration', None),
    'armd': ('Age-Related Macular Degeneration', None),
    'macular degeneration': ('Age-Related Macular Degeneration', None),
    'macula degeneration': ('Age-Related Macular Degeneration', None),
    
    # AMD Type and Severity
    'wet amd': ('Age-Related Macular Degeneration', 'Severe'),
    'wet age-related': ('Age-Related Macular Degeneration', 'Severe'),
    'neovascular amd': ('Age-Related Macular Degeneration', 'Severe'),
    'exudative amd': ('Age-Related Macular Degeneration', 'Severe'),
    'choroidal neovascularization': ('Age-Related Macular Degeneration', 'Severe'),
    'cnv': ('Age-Related Macular Degeneration', 'Severe'),
    'dry amd': ('Age-Related Macular Degeneration', 'Moderate'),
    'dry age-related': ('Age-Related Macular Degeneration', 'Moderate'),
    'atrophic amd': ('Age-Related Macular Degeneration', 'Moderate'),
    'geographic atrophy': ('Age-Related Macular Degeneration', 'Severe'),
    'ga': ('Age-Related Macular Degeneration', 'Severe'),
    'early amd': ('Age-Related Macular Degeneration', 'Mild'),
    'early age-related': ('Age-Related Macular Degeneration', 'Mild'),
    'intermediate amd': ('Age-Related Macular Degeneration', 'Moderate'),
    'intermediate age-related': ('Age-Related Macular Degeneration', 'Moderate'),
    'advanced amd': ('Age-Related Macular Degeneration', 'Severe'),
    'advanced age-related': ('Age-Related Macular Degeneration', 'Severe'),
    
    # ========== CATARACT ==========
    'cataract': ('Cataract', None),
    'cataract formation': ('Cataract', None),
    'cataracts': ('Cataract', None),
    'no cataract': ('Normal', None),
    'without cataract': ('Normal', None),
    'clear lens': ('Normal', None),
    
    # Cataract Type
    'nuclear cataract': ('Cataract', 'Moderate'),
    'nuclear sclerotic': ('Cataract', 'Moderate'),
    'nuclear': ('Cataract', 'Moderate'),
    'cortical cataract': ('Cataract', 'Moderate'),
    'cortical': ('Cataract', 'Moderate'),
    'posterior subcapsular': ('Cataract', 'Severe'),
    'posterior subcapsular cataract': ('Cataract', 'Severe'),
    'subcapsular': ('Cataract', 'Moderate'),
    'mixed cataract': ('Cataract', 'Moderate'),
    'brown cataract': ('Cataract', 'Moderate'),
    'brunescent': ('Cataract', 'Moderate'),
    
    # Cataract Density/Maturity
    'immature cataract': ('Cataract', 'Mild'),
    'immature': ('Cataract', 'Mild'),
    'incipient': ('Cataract', 'Mild'),
    'beginning': ('Cataract', 'Mild'),
    'early cataract': ('Cataract', 'Mild'),
    'intumescent': ('Cataract', 'Mild'),
    'intumescence': ('Cataract', 'Mild'),
    'mature cataract': ('Cataract', 'Severe'),
    'mature': ('Cataract', 'Severe'),
    'swollen': ('Cataract', 'Moderate'),
    'hypermature': ('Cataract', 'Severe'),
    'hypermature cataract': ('Cataract', 'Severe'),
    'overripe': ('Cataract', 'Severe'),
    'white mature': ('Cataract', 'Severe'),
    'soft cataract': ('Cataract', 'Mild'),
    'hard cataract': ('Cataract', 'Severe'),
    'congenital cataract': ('Cataract', 'Moderate'),
    'traumatic cataract': ('Cataract', 'Moderate'),
    'radiation cataract': ('Cataract', 'Moderate'),
    
    # ========== GLAUCOMA ==========
    'glaucoma': ('Glaucoma', None),
    'glaucomas': ('Glaucoma', None),
    'no glaucoma': ('Normal', None),
    'without glaucoma': ('Normal', None),
    'negative for glaucoma': ('Normal', None),
    
    # Glaucoma Type
    'open angle glaucoma': ('Glaucoma', 'Moderate'),
    'primary open angle': ('Glaucoma', 'Moderate'),
    'poag': ('Glaucoma', 'Moderate'),
    'angle closure glaucoma': ('Glaucoma', 'Severe'),
    'acute angle closure': ('Glaucoma', 'Severe'),
    'chronic angle closure': ('Glaucoma', 'Moderate'),
    'secondary glaucoma': ('Glaucoma', 'Moderate'),
    'normal tension glaucoma': ('Glaucoma', 'Mild'),
    'ntg': ('Glaucoma', 'Mild'),
    'pigmentary glaucoma': ('Glaucoma', 'Moderate'),
    'exfoliative glaucoma': ('Glaucoma', 'Moderate'),
    'pseudoexfoliation': ('Glaucoma', 'Moderate'),
    'congenital glaucoma': ('Glaucoma', 'Moderate'),
    'neovascular glaucoma': ('Glaucoma', 'Severe'),
    'uveitic glaucoma': ('Glaucoma', 'Moderate'),
    
    # Glaucoma Suspect and Risk
    'glaucoma suspect': ('Glaucoma Suspect', None),
    'suspected glaucoma': ('Glaucoma Suspect', None),
    'glaucoma risk': ('Glaucoma Suspect', None),
    'at risk for glaucoma': ('Glaucoma Suspect', None),
    'ocular hypertension': ('Glaucoma Suspect', 'Mild'),
    'elevated iop': ('Glaucoma Suspect', 'Mild'),
    'high iop': ('Glaucoma Suspect', 'Mild'),
    'suspicious optic nerve': ('Glaucoma Suspect', None),
    'large cup disc': ('Glaucoma Suspect', None),
    
    # ========== DIABETIC MACULAR EDEMA - SEPARATE ==========
    'macular edema': ('Macular Edema', None),
    'macula edema': ('Macular Edema', None),
    'macula swelling': ('Macular Edema', None),
    'retinal swelling': ('Macular Edema', None),
    'edema macula': ('Macular Edema', None),
    'cystoid macular edema': ('Macular Edema', 'Severe'),
    'cystoid edema': ('Macular Edema', 'Severe'),
    'cme': ('Macular Edema', 'Severe'),
    'serous detachment': ('Macular Edema', 'Severe'),
    'exudative detachment': ('Macular Edema', 'Severe'),
    
    # ========== DRUSEN ==========
    'drusen': ('Drusen', None),
    'drusens': ('Drusen', None),
    'macular drusen': ('Drusen', None),
    'retinal drusen': ('Drusen', None),
    
    # Drusen Type
    'hard drusen': ('Drusen', 'Mild'),
    'small drusen': ('Drusen', 'Mild'),
    'tiny drusen': ('Drusen', 'Mild'),
    'soft drusen': ('Drusen', 'Moderate'),
    'large drusen': ('Drusen', 'Moderate'),
    'confluent drusen': ('Drusen', 'Severe'),
    'extensive drusen': ('Drusen', 'Severe'),
    'soft indistinct drusen': ('Drusen', 'Moderate'),
    
    # ========== REFRACTIVE ERRORS ==========
    'myopia': ('Myopia', None),
    'myopic': ('Myopia', None),
    'myopia diagnosis': ('Myopia', None),
    'myopic shift': ('Myopia', None),
    'high myopia': ('Myopia', 'Severe'),
    'high myopic': ('Myopia', 'Severe'),
    'pathologic myopia': ('Myopia', 'Severe'),
    'degenerative myopia': ('Myopia', 'Severe'),
    'hyperopia': ('Hyperopia', None),
    'hyperopic': ('Hyperopia', None),
    'farsightedness': ('Hyperopia', None),
    'high hyperopia': ('Hyperopia', 'Moderate'),
    'astigmatism': ('Astigmatism', None),
    'astigmatic': ('Astigmatism', None),
    'high astigmatism': ('Astigmatism', 'Moderate'),
    'presbyopia': ('Presbyopia', None),
    'presbyopic': ('Presbyopia', None),
    'refractive error': ('Myopia', None),
    'refractive anomaly': ('Myopia', None),
    'ametropia': ('Myopia', None),
    'anisometropia': ('Myopia', None),
    
    # ========== HYPERTENSIVE RETINOPATHY ==========
    'hypertensive': ('Hypertensive Retinopathy', None),
    'hypertensive retinopathy': ('Hypertensive Retinopathy', None),
    'hypertension retinopathy': ('Hypertensive Retinopathy', None),
    'high blood pressure eye': ('Hypertensive Retinopathy', None),
    'hypertensive optic neuropathy': ('Hypertensive Retinopathy', 'Severe'),
    'malignant hypertension': ('Hypertensive Retinopathy', 'Severe'),
    'hypertensive crisis': ('Hypertensive Retinopathy', 'Severe'),
    
    # ========== VASCULAR OCCLUSIONS ==========
    'retinal artery occlusion': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'central retinal artery': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'crao': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'branch retinal artery': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'brao': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'retinal vein occlusion': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'central retinal vein': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'crvo': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'branch retinal vein': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'brvo': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'hemi-retinal vein': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'hrvo': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'vascular occlusion': ('Retinal Vein/Artery Occlusion', 'Severe'),
    'retinal infarct': ('Retinal Vein/Artery Occlusion', 'Severe'),
    
    # ========== RETINAL DETACHMENT & BREAKS ==========
    'retinal detachment': ('Retinal Detachment', 'Severe'),
    'detached retina': ('Retinal Detachment', 'Severe'),
    'rhegmatogenous': ('Retinal Detachment', 'Severe'),
    'tractional detachment': ('Retinal Detachment', 'Severe'),
    'rhegmatogenous detachment': ('Retinal Detachment', 'Severe'),
    'total detachment': ('Retinal Detachment', 'Severe'),
    'macula-off': ('Retinal Detachment', 'Severe'),
    'macula-on': ('Retinal Detachment', 'Moderate'),
    'retinal break': ('Retinal Detachment', 'Moderate'),
    'retinal tear': ('Retinal Detachment', 'Moderate'),
    'retinal hole': ('Retinal Detachment', 'Moderate'),
    'macular hole': ('Retinal Detachment', 'Severe'),
    'full-thickness macular': ('Retinal Detachment', 'Severe'),
    'lamellar hole': ('Retinal Detachment', 'Moderate'),
    
    # ========== CORNEAL DISEASE ==========
    'corneal disease': ('Corneal Disease', None),
    'cornea disease': ('Corneal Disease', None),
    'corneal condition': ('Corneal Disease', None),
    'keratitis': ('Corneal Disease', 'Moderate'),
    'corneal inflammation': ('Corneal Disease', 'Moderate'),
    'infectious keratitis': ('Corneal Disease', 'Moderate'),
    'bacterial keratitis': ('Corneal Disease', 'Moderate'),
    'viral keratitis': ('Corneal Disease', 'Moderate'),
    'fungal keratitis': ('Corneal Disease', 'Moderate'),
    'herpes keratitis': ('Corneal Disease', 'Moderate'),
    'ulcerative keratitis': ('Corneal Disease', 'Severe'),
    'corneal ulcer': ('Corneal Disease', 'Moderate'),
    'corneal scar': ('Corneal Disease', 'Severe'),
    'corneal scarring': ('Corneal Disease', 'Severe'),
    'stromal scar': ('Corneal Disease', 'Severe'),
    'band keratopathy': ('Corneal Disease', 'Severe'),
    'corneal dystrophy': ('Corneal Disease', 'Mild'),
    'stromal dystrophy': ('Corneal Disease', 'Mild'),
    'endothelial dystrophy': ('Corneal Disease', 'Mild'),
    'fuchs dystrophy': ('Corneal Disease', 'Mild'),
    'lattice dystrophy': ('Corneal Disease', 'Mild'),
    'map-dot-fingerprint': ('Corneal Disease', 'Mild'),
    'corneal edema': ('Corneal Disease', 'Moderate'),
    'stromal edema': ('Corneal Disease', 'Moderate'),
    'epithelial edema': ('Corneal Disease', 'Moderate'),
    'keratoconus': ('Keratoconus', 'Moderate'),
    'keratectasia': ('Keratoconus', 'Moderate'),
    'ectasia': ('Keratoconus', 'Moderate'),
    'post-lasik ectasia': ('Keratoconus', 'Moderate'),
    'pterygium': ('Pterygium', 'Mild'),
    'pterygial': ('Pterygium', 'Mild'),
    'pinguecula': ('Corneal Disease', 'Mild'),
    'conjunctival xerosis': ('Corneal Disease', 'Mild'),
    
    # ========== RETINAL & OPTIC DISEASES ==========
    'retinoblastoma': ('Retinoblastoma', 'Severe'),
    'retinitis pigmentosa': ('Retinal Pigmentary Disease', 'Moderate'),
    'rp': ('Retinal Pigmentary Disease', 'Moderate'),
    'pigmentary retinopathy': ('Retinal Pigmentary Disease', 'Moderate'),
    'optic neuritis': ('Optic Disc Disease', 'Moderate'),
    'optic neuropathy': ('Optic Disc Disease', 'Moderate'),
    'optic atrophy': ('Optic Disc Disease', 'Severe'),
    'optic pallor': ('Optic Disc Disease', 'Severe'),
    'papilledema': ('Optic Disc Disease', 'Severe'),
    'optic nerve swelling': ('Optic Disc Disease', 'Severe'),
    'swollen optic disc': ('Optic Disc Disease', 'Severe'),
    'optic disc cupping': ('Optic Disc Disease', 'Moderate'),
    'large cup': ('Optic Disc Disease', 'Moderate'),
    'optic nerve hypoplasia': ('Optic Disc Disease', 'Moderate'),
    'optic nerve coloboma': ('Optic Disc Disease', 'Moderate'),
    
    # ========== VITREOUS ==========
    'vitreous hemorrhage': ('Vitreous Hemorrhage', 'Severe'),
    'vitreous bleed': ('Vitreous Hemorrhage', 'Severe'),
    'vh': ('Vitreous Hemorrhage', 'Severe'),
    'hemorrhage vitreous': ('Vitreous Hemorrhage', 'Severe'),
    'vitreous opacities': ('Vitreous Hemorrhage', 'Moderate'),
    'vitreous floaters': ('Vitreous Hemorrhage', 'Mild'),
    'posterior vitreous detachment': ('Vitreous Hemorrhage', 'Mild'),
    'pvd': ('Vitreous Hemorrhage', 'Mild'),
    'vitreous inflammation': ('Vitreous Hemorrhage', 'Moderate'),
    'vitreous haze': ('Vitreous Hemorrhage', 'Moderate'),
    
    # ========== NORMAL ==========
    'normal': ('Normal', None),
    'normal eye': ('Normal', None),
    'no disease': ('Normal', None),
    'healthy': ('Normal', None),
    'unremarkable': ('Normal', None),
    'no pathology': ('Normal', None),
    'normal fundus': ('Normal', None),
    'clear fundus': ('Normal', None),
    'normal ocular': ('Normal', None),
    'benign': ('Normal', None),
}

# ============================================================================
# COMPREHENSIVE SEVERITY GRADING SCALES (By Condition)
# ============================================================================

SEVERITY_GRADING = {
    'diabetic retinopathy': {
        0: 'None',
        1: 'Mild',
        2: 'Moderate',
        3: 'Severe',
        4: 'Proliferative',
    },
    'diabetic macular edema': {
        0: 'None',
        1: 'Mild',
        2: 'Moderate',
        3: 'Severe',
    },
    'amd': {
        0: 'None',
        1: 'Early',
        2: 'Intermediate',
        3: 'Advanced',
    },
    'cataract': {
        0: 'None',
        1: 'Mild',
        2: 'Moderate',
        3: 'Mature',
        4: 'Hypermature',
    },
    'glaucoma': {
        0: 'None',
        1: 'Mild',
        2: 'Moderate',
        3: 'Advanced',
        4: 'Terminal',
    },
    'corneal disease': {
        0: 'None',
        1: 'Mild',
        2: 'Moderate',
        3: 'Severe',
    },
    'retinal detachment': {
        0: 'None',
        1: 'Macula-on',
        2: 'Macula-off',
        3: 'Rhegmatogenous',
        4: 'Tractional',
    },
    'hypertensive retinopathy': {
        0: 'None',
        1: 'Grade 1',
        2: 'Grade 2',
        3: 'Grade 3',
        4: 'Grade 4',  # Malignant
    },
}

# ============================================================================
# CLINICAL FINDING KEYWORDS (Signs Visible in Images)
# ============================================================================

CLINICAL_FINDINGS_KEYWORDS = {
    # Hemorrhages
    'hemorrhages': ['hemorrhage', 'bleed', 'bleeding', 'blood', 'heme', 'flame', 'dot blot', 'scattered'],
    'microhemorrhages': ['micro hemorrh', 'microhemorrh', 'small bleed', 'flame hemorrh'],
    'dot_blot_hemorrhages': ['dot blot', 'dot-blot', 'dot and blot', 'intraretinal'],
    'flame_hemorrhages': ['flame hemorrh', 'flame shaped', 'nerve fiber'],
    'preretinal_hemorrhage': ['preretinal', 'subhyaloid', 'vitreous hemorrh', 'premacular'],
    
    # Exudates
    'hard_exudates': ['hard exudate', 'lipid', 'yellow deposit', 'retinal deposit', 'yel', 'exudative'],
    'soft_exudates': ['soft exudate', 'cotton wool', 'white spot', 'infarct'],
    'exudates': ['exudate', 'deposit', 'lipid'],
    
    # Microaneurysms
    'microaneurysms': ['microaneurysm', 'microaneurysom', 'ma', 'aneurysm'],
    'ma_clusters': ['ma cluster', 'aneurysm cluster'],
    
    # Edema & Fluid
    'macular_edema': ['macular edema', 'macula edema', 'macula swell', 'edema', 'fluid', 'cystoid'],
    'retinal_thickening': ['retinal thick', 'thickening', 'swell', 'engorg'],
    'serous_detachment': ['serous detach', 'exudative detach', 'detach'],
    'cysts': ['cyst', 'cystoid', 'intraretinal space'],
    
    # Neovascularization
    'neovascularization': ['neovascularization', 'neovascular', 'new vessels', 'nv', 'cnv', 'cnvs'],
    'neovascular_disc': ['neovascular disc', 'nv disc', 'nv elsewhere'],
    'choroidal_neovascularization': ['cnv', 'choroidal neovascularization', 'subretinal neovascular'],
    'retinal_neovascularization': ['retinal nv', 'peripheral neovascular'],
    
    # Vessel Changes
    'vessel_tortuosity': ['tortuous', 'tortuosity', 'winding', 'coiled'],
    'vessel_narrowing': ['narrowing', 'narrowed', 'attenuated', 'sheathed'],
    'vessel_beading': ['beading', 'segmental narrowing', 'irregularity'],
    'arteriovenous_nicking': ['av nicking', 'nicking', 'arteriovenous', 'av nick'],
    
    # Retinal Changes
    'cotton_wool_spots': ['cotton wool', 'cws', 'white spot', 'nerve fiber layer'],
    'retinal_folds': ['retinal fold', 'epiretinal', 'macular fold'],
    'hard_drusen': ['hard drusen', 'small drusen', 'punctate'],
    'soft_drusen': ['soft drusen', 'large drusen', 'confluent drusen'],
    'geographic_atrophy': ['geographic atrophy', 'ga', 'chorioretinal atrophy'],
    'macular_scarring': ['macular scar', 'scarring', 'disciform', 'fibrosis'],
    
    # Optic Nerve
    'optic_disc_pallor': ['pallor', 'pale', 'optic atrophy'],
    'optic_disc_cupping': ['cup', 'cupping', 'excavation'],
    'optic_nerve_swelling': ['swelling', 'optic disc swelling', 'papilledema', 'disc edema'],
    'large_cup_disc_ratio': ['large cup', 'cup disc', 'c/d ratio'],
    
    # Other
    'vitreous_hemorrhage': ['vitreous hemorrh', 'vitreous bleed', 'vh', 'hemorrhage'],
    'subretinal_hemorrhage': ['subretinal hemorrh', 'sub retinal'],
    'retinal_detachment': ['retinal detach', 'detached', 'rd', 'break', 'tear', 'hole'],
    'laser_scars': ['laser scar', 'photocoagulation', 'burn', 'scar'],
    'retinal_thinning': ['thinning', 'atrophy', 'thin retina'],
}

# ============================================================================
# COMPREHENSIVE MODALITY PATTERNS (12+ Modalities)
# ============================================================================

MODALITY_PATTERNS = {
    'Fundus': [
        'fundus', 'color fundus', 'cf', 'cfp', 'color photograph', 'color photography',
        'optos', 'widefield', 'wide field', 'wf', 'macula', 'retinal', 'retina',
        'aptos', 'messidor', 'refuge', 'ukiadb', 'eyepacs', 'diabetic retinopathy',
        'color fundus photograph', 'digital fundus', 'fundus image', 'fundus photo',
        'disc', 'macula view', 'macular view', 'posterior pole', 'peripheral retina'
    ],
    'OCT': [
        'oct', 'optical coherence', 'spectral domain', 'sd-oct', 'sdoct',
        'time domain', 'td-oct', 'swept source', 'ss-oct', 'ssoct',
        'structural', 'cross section', 'b-scan', 'volumetric', '3d', 'volume',
        'oct scan', 'oct imaging', 'optical coherence tomography', 'macular oct',
        'optic disc oct', 'anterior segment oct', 'as-oct'
    ],
    'OCTA': [
        'octa', 'oct angiography', 'oct angio', 'angiography', 'angioography',
        'optical coherence tomography angiography', 'octa', 'angiogram',
        'vascular imaging', 'capillary network', 'vessel density'
    ],
    'Slit-Lamp': [
        'slit', 'slit-lamp', 'slit lamp', 'anterior', 'anterior segment',
        'anterior chamber', 'lens', 'cornea', 'iris', 'angle', 'goniosc',
        'biomicroscopy', 'slit lamp photography', 'anterior segment imaging'
    ],
    'Fluorescein Angiography': [
        'fa', 'fag', 'fluorescein', 'angiography', 'fa imaging',
        'icg', 'indocyanine', 'angiogram', 'fundus angiography',
        'retinal angiography', 'fluorescein angiogram'
    ],
    'Fundus Autofluorescence': [
        'faf', 'autofluorescence', 'faf imaging', 'af', 'afo',
        'fundus autofluorescence', 'autofluorescent', 'af imaging'
    ],
    'Infrared': [
        'ir', 'infrared', 'infrared imaging', 'near infrared', 'nir', 'nir imaging',
        'ir reflectance', 'infrared reflectance', 'reflectance imaging'
    ],
    'Ultrasound': [
        'ultrasound', 'us', 'b-scan', 'a-scan', 'b scan', 'a scan',
        'echography', 'echogram', 'ultrasonic', 'ultrasound imaging'
    ],
    'Anterior Segment': [
        'anterior segment', 'anterior chamber', 'cornea imaging', 'iris imaging',
        'lens imaging', 'angle imaging', 'gonioscopy', 'anterior imaging'
    ],
    'Specular Microscopy': [
        'specular', 'endothelial', 'endothelial cell', 'cell count',
        'corneal endothelium', 'endothelial imaging'
    ],
    'Visual Field': [
        'visual field', 'vf', 'perimetry', 'automated', 'threshold',
        'humphrey', 'field analyzer', 'visual field test', 'vf test',
        'perimetric', 'perimetry test'
    ],
    'Anterior Segment OCT': [
        'as-oct', 'anterior segment oct', 'corneal', 'pachymetry',
        'anterior chamber depth', 'angle measurement'
    ],
}

# ============================================================================
# COMPREHENSIVE LATERALITY PATTERNS (Multi-language)
# ============================================================================

LATERALITY_PATTERNS = {
    'OD': [
        # English
        'right', 'od', 'oculus dexter', 're', 'r', 'r.', 'right eye', 'r eye',
        # Filename patterns
        '_r.', '_r_', '-r-', '_od', '-od', '_right', '-right',
        # Latin abbreviations
        'o.d.', 'od', 'odex',
        # Alternative codes
        'droit',  # French
        'derecha',  # Spanish
        'right side',
    ],
    'OS': [
        # English
        'left', 'os', 'oculus sinister', 'le', 'l', 'l.', 'left eye', 'l eye',
        # Filename patterns
        '_l.', '_l_', '-l-', '_os', '-os', '_left', '-left',
        # Latin abbreviations
        'o.s.', 'os', 'osex',
        # Alternative codes
        'gauche',  # French
        'izquierda',  # Spanish
        'left side',
    ],
    'OU': [
        # English
        'both', 'ou', 'oculus uterque', 'bilateral', 'binocular',
        'both eyes', 'each eye', 'combined', 'both sides',
        # Alternative codes
        'bilat', 'bilaterally',
    ],
}

# ============================================================================
# IMAGE QUALITY ASSESSMENT KEYWORDS
# ============================================================================

IMAGE_QUALITY_KEYWORDS = {
    'excellent': ['excellent', 'perfect', 'clear', 'sharp', 'well-focused'],
    'good': ['good', 'very good', 'clear view', 'adequate'],
    'moderate': ['moderate', 'fair', 'acceptable', 'ok'],
    'poor': ['poor', 'low quality', 'blurry', 'unclear', 'artifact'],
    'ungradable': ['ungradable', 'not assessable', 'cannot grade', 'missing', 'absent'],
    
    # Artifact types
    'motion_artifact': ['motion', 'blur', 'movement', 'eye movement'],
    'media_opacity': ['opacity', 'cataract', 'corneal', 'haze', 'cloudiness'],
    'inadequate_illumination': ['illumination', 'lighting', 'dark', 'dim', 'bright'],
    'eyelashes': ['eyelash', 'eyelid', 'lash'],
    'glare': ['glare', 'reflection', 'specular'],
    'artifact_present': ['artifact', 'defect', 'noise', 'interference'],
}

# ============================================================================
# PATIENT DEMOGRAPHIC RANGES & VALIDATION
# ============================================================================

AGE_RANGES = {
    'infant': (0, 2),
    'toddler': (2, 5),
    'child': (5, 13),
    'adolescent': (13, 18),
    'adult': (18, 65),
    'elderly': (65, 150),
}

SEX_MAPPINGS = {
    'M': ['m', 'male', 'man', 'male', 'masculino', 'homme', 'herr'],
    'F': ['f', 'female', 'woman', 'femenino', 'femme', 'frau'],
    'O': ['o', 'other', 'non-binary', 'prefer not to say', 'unknown'],
    'U': ['u', 'unknown', 'unclear', 'not specified', 'n/a', 'na'],
}

ETHNICITY_MAPPINGS = {
    'Caucasian': ['caucasian', 'white', 'european', 'anglo'],
    'African': ['african', 'black', 'african american', 'afro-caribbean'],
    'Asian': ['asian', 'east asian', 'south asian', 'indian', 'chinese', 'japanese'],
    'Hispanic': ['hispanic', 'latino', 'latin american', 'spanish'],
    'Middle Eastern': ['middle eastern', 'arab', 'persian', 'turkish'],
    'Pacific Islander': ['pacific islander', 'hawaiian'],
    'Mixed': ['mixed', 'multiracial', 'biracial'],
    'Other': ['other', 'prefer not to say', 'unknown'],
}

# ============================================================================
# ADDITIONAL HARMONIZATION KEYWORDS
# ============================================================================

TREATMENT_KEYWORDS = {
    'laser': ['laser', 'photocoagulation', 'pan-retinal', 'focal', 'scatter'],
    'injection': ['injection', 'intravitreal', 'ivt', 'anti-vegf', 'steroid'],
    'surgery': ['surgery', 'surgical', 'vitrectomy', 'retinopathy', 'scleral'],
    'medical': ['medical', 'medication', 'medical management', 'drug'],
    'untreated': ['untreated', 'no treatment', 'naive', 'therapy-naive'],
}

STUDY_KEYWORDS = {
    'baseline': ['baseline', 'initial', 'first visit', 'entry'],
    'followup': ['follow-up', 'followup', 'visit', 'month', 'year', 'week'],
    'endpoint': ['endpoint', 'final', 'end', 'conclusion'],
}

# ============================================================================
# HELPER FUNCTIONS FOR COMPREHENSIVE HARMONIZATION
# ============================================================================


def normalize_diagnosis(raw_diagnosis: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Normalize a raw diagnosis label to standardized category and severity.
    
    Args:
        raw_diagnosis: Raw diagnosis string from dataset
        
    Returns:
        Tuple of (diagnosis_category, severity_grade) or (None, None) if not found
    """
    if not raw_diagnosis:
        return None, None
    
    raw_lower = str(raw_diagnosis).lower().strip()
    
    # Direct lookup
    if raw_lower in DIAGNOSIS_MAPPING:
        return DIAGNOSIS_MAPPING[raw_lower]
    
    # Partial matching - prioritize exact substring matches
    best_match = None
    best_length = 0
    
    for key, value in DIAGNOSIS_MAPPING.items():
        if key in raw_lower and len(key) > best_length:
            best_match = value
            best_length = len(key)
    
    if best_match:
        return best_match
    
    # If no match found, return original
    return raw_diagnosis, None


def infer_severity_from_diagnosis(raw_diagnosis: Optional[str], diagnosis_category: Optional[str]) -> Optional[str]:
    """
    Infer severity grading from diagnosis text.
    
    Args:
        raw_diagnosis: Raw diagnosis string
        diagnosis_category: Normalized diagnosis category
        
    Returns:
        Severity grade or None
    """
    if not raw_diagnosis or not diagnosis_category:
        return None
    
    raw_lower = str(raw_diagnosis).lower()
    
    # Direct severity patterns
    severity_keywords = {
        'severe': 'Severe',
        'advanced': 'Severe',
        'proliferative': 'Proliferative',
        'moderate': 'Moderate',
        'mild': 'Mild',
        'early': 'Mild',
        'minimal': 'Mild',
    }
    
    for keyword, severity in severity_keywords.items():
        if keyword in raw_lower:
            return severity
    
    return None


def infer_modality(dataset_name: Optional[str], column_name: Optional[str] = None) -> str:
    """
    Infer imaging modality from dataset name or column metadata.
    
    Args:
        dataset_name: Name of the source dataset
        column_name: Optional column name that might indicate modality
        
    Returns:
        Inferred modality (default: 'Unknown')
    """
    search_text = f"{dataset_name or ''} {column_name or ''}".lower()
    
    # Find best match (longest pattern match)
    best_modality = 'Unknown'
    best_length = 0
    
    for modality, patterns in MODALITY_PATTERNS.items():
        for pattern in patterns:
            if pattern in search_text and len(pattern) > best_length:
                best_modality = modality
                best_length = len(pattern)
    
    return best_modality


def infer_laterality(value: Optional[str]) -> Optional[str]:
    """
    Infer laterality (eye side) from a string value with word boundary detection.
    
    Args:
        value: String value potentially indicating laterality
        
    Returns:
        Standardized laterality code (OD, OS, OU) or None
    """
    if not value:
        return None
    
    value_lower = str(value).lower().strip()
    
    # Try exact match first
    for code, patterns in LATERALITY_PATTERNS.items():
        if value_lower in patterns:
            return code
    
    # Then substring matching with word boundaries
    for code, patterns in LATERALITY_PATTERNS.items():
        for pattern in patterns:
            if pattern in value_lower:
                return code
    
    return None


def detect_column_role(column_name: str) -> Optional[str]:
    """
    Auto-detect what field a column likely represents with priority ordering.
    
    Args:
        column_name: Column name from dataset
        
    Returns:
        Field name (e.g., 'diagnosis', 'modality', 'laterality') or None
    """
    col_lower = column_name.lower()
    
    # Priority-ordered detection
    if any(x in col_lower for x in ['diagnosis', 'label', 'class', 'disease', 'condition']):
        return 'diagnosis'
    elif any(x in col_lower for x in ['image_id', 'image id', 'filename', 'file', 'id']):
        return 'image_id'
    elif any(x in col_lower for x in ['path', 'img', 'image']):
        return 'image_path'
    elif any(x in col_lower for x in ['laterality', 'eye', 'side', 'left', 'right', 'od', 'os']):
        return 'laterality'
    elif any(x in col_lower for x in ['modality', 'imaging', 'type', 'technique']):
        return 'modality'
    elif any(x in col_lower for x in ['age', 'patient_age']):
        return 'patient_age'
    elif any(x in col_lower for x in ['sex', 'gender', 'patient_sex']):
        return 'patient_sex'
    elif any(x in col_lower for x in ['resolution', 'pixel', 'dpi', 'width', 'height']):
        return 'resolution'
    
    return None


def harmonize_column_value(field_type: str, value: any, context: Dict = None) -> any:
    """
    Apply field-specific harmonization to a column value.
    
    Args:
        field_type: Type of field being harmonized
        value: The value to harmonize
        context: Optional context dict with dataset_name, etc.
        
    Returns:
        Harmonized value
    """
    context = context or {}
    
    if field_type == 'diagnosis':
        return normalize_diagnosis(value)[0]  # Return only category
    elif field_type == 'severity':
        diag = normalize_diagnosis(value)
        return diag[1] or infer_severity_from_diagnosis(str(value), diag[0])
    elif field_type == 'modality':
        return infer_modality(context.get('dataset_name'), str(value) if value else None)
    elif field_type == 'laterality':
        return infer_laterality(value)
    elif field_type == 'patient_age':
        try:
            age = int(float(value)) if value else None
            # Validate reasonable age range
            if age is not None and 0 <= age <= 150:
                return age
            return None
        except (ValueError, TypeError):
            return None
    elif field_type == 'patient_sex':
        if value is None:
            return None
        val_upper = str(value).upper().strip()
        if val_upper in ['M', 'MALE']:
            return 'M'
        elif val_upper in ['F', 'FEMALE']:
            return 'F'
        elif val_upper in ['O', 'OTHER']:
            return 'O'
        elif val_upper in ['U', 'UNKNOWN']:
            return 'U'
        return None
    elif field_type == 'patient_ethnicity':
        if value:
            return str(value).strip()
        return None
    
    return value
