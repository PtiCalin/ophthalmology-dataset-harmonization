# Documentation Index

Your project documentation has been consolidated into **6 core files** totaling ~64 KB.

---

## Quick Navigation

All documentation lives under the docs folder. Data-processing references are under docs/data-processing.

### 📖 **README.md**
**Start here!** Project overview, quick start guide, and architecture.

**Includes:**

**Best for:** First-time users, developers, stakeholders


### 🧭 **METHODOLOGY.md**
**Methodological foundations and validation framework** for the harmonization approach.

**Includes:**
- Theoretical frameworks (FAIR, TDQM, clinical standards)
- Harmonization process architecture
- Rule-based inference design
- Quality assurance and validation strategy

**Best for:** Researchers, academics, technical reviewers

---

### 📋 **SCHEMA.md**
**Complete field reference** for the 122-field data structure.

**Includes:**
  - ClinicalFindings (25 fields)
  - PatientClinicalData (35 fields)
  - DeviceAndAcquisition (12 fields)
  - ImageMetadata (20 fields)

**Best for:** Data engineers, schema users, field validation

**Location:** docs/data-processing/SCHEMA.md


### 📐 **RULES.md**
**Harmonization logic documentation** for all inference functions.

**Includes:**
- Complete diagnosis mapping (269+ keywords → 28 categories + severity)
- All 8+ severity grading systems
- Modality inference (150+ patterns across 12 types)
- Laterality detection (English, French, Spanish, filename patterns)
- Clinical findings detection (37 types)
- Image quality assessment (5 levels)
- Patient demographic standardization
- All core functions with examples
- Pattern matching strategy
- Validation confidence scoring

**Best for:** Data harmonization, diagnosis mapping, field inference

**Location:** docs/data-processing/RULES.md

---

### 📚 **CODEBOOK.md**
**Data dictionary and enumeration reference** for all standardized values.

**Includes:**
- Modality enumeration (12 values + examples)
- Laterality codes (3 values + variants)
- Diagnosis categories (28 values + SNOMED/ICD-10)
- Severity levels (6 generic + condition-specific)
- Sex/Gender codes (4 values)
- Diabetes types (5 values)
- DR severity ICDR scale (international standard)
- Annotation quality (6 levels)
- Data source types (7 values)
- Image quality levels (5 + artifact types)
- Age groups (reference table)
- Ethnicity/Race (8 values)
- Clinical finding types (37 values)
- Modality pattern quick reference
- Column name detection guide
- Validation ranges for all numeric fields

**Best for:** Data validation, coding, field mapping, reference

**Location:** docs/data-processing/CODEBOOK.md

---

### 📖 **UPDATES.md**
**Release notes, enhancement history, and future roadmap.**

**Includes:**
- Current version (v2.0 Production) status
- Major enhancements summary:
  - Diagnosis mapping expansion (50 → 269+ keywords)
  - Severity grading systems (8+ systems)
  - Modality patterns (150+ patterns)
  - Clinical findings (37 types)
  - New functions (15+)
  - File growth statistics
- Version 1.0 baseline (archived)
- Future roadmap (Phases 3-7)
- Known issues & limitations
- Performance metrics
- Dependency versions
- Backward compatibility matrix
- Changelog by date
- Project statistics summary

**Best for:** Project history, roadmap planning, version tracking, statistics

**Location:** docs/UPDATES.md

---

## File Information

| File | Size | Lines | Focus |
|------|------|-------|-------|
| README.md | 6.8 KB | ~200 | Quick start & overview |
| METHODOLOGY.md | 8.5 KB | ~280 | Methodological framework |
| SCHEMA.md | 11.2 KB | ~350 | Field reference |
| RULES.md | 12.7 KB | ~400 | Harmonization logic |
| CODEBOOK.md | 12.7 KB | ~400 | Data dictionary |
| UPDATES.md | 12.4 KB | ~400 | Release notes |
| **Total** | **64.3 KB** | **~2,030** | **Complete reference** |

---

## Reading Paths by Role

### 👨‍💻 Software Developer
1. README.md → Architecture section
2. SCHEMA.md → Field definitions & examples
3. RULES.md → Function signatures & logic
4. CODEBOOK.md → As needed for enumerations

### 📊 Data Analyst / Data Engineer
1. README.md → Schema overview
2. CODEBOOK.md → All enumerations & validation
3. SCHEMA.md → Patient clinical data fields
4. RULES.md → Diagnosis mapping & inference

### 🔬 Researcher / ML Engineer
1. METHODOLOGY.md → Theoretical frameworks & validation
2. UPDATES.md → Project history & enhancement roadmap
3. RULES.md → Diagnosis mapping (269+ keywords)
4. SCHEMA.md → Feature engineering (clinical findings)
5. README.md → Architecture & performance metrics

### 📚 New User / Student
1. README.md → Introduction (read carefully!)
2. Follow architecture guide in README.md
3. SCHEMA.md → Field by field exploration
4. CODEBOOK.md → Reference for values
5. RULES.md → Deep dive into harmonization

### 👨‍💼 Project Manager / Stakeholder
1. README.md → Project description & status
2. UPDATES.md → Current version & statistics
3. UPDATES.md → Roadmap for planning

---

## Key Statistics

### Schema Coverage
- **Total Fields:** 122 (30 top-level + 92 nested)
- **Nested Objects:** 4 dataclasses
- **Enumerations:** 9 types with 45+ values
- **Validation Rules:** 10+
- **Supported Modalities:** 12
- **Supported Disease Categories:** 28

### Rules Coverage
- **Diagnosis Keywords:** 269+ (5.4× expansion)
- **Severity Systems:** 8+
- **Modality Patterns:** 150+ (10× expansion)
- **Clinical Finding Types:** 37
- **Inference Functions:** 15+

### Testing & Quality
- **Test Cases:** 18+ (all passing ✅)
- **Code Files:** src/schema.py (643 lines), src/rules.py (1,020+ lines)
- **Documentation Lines:** 2,030+
- **Fully Type-Annotated:** Yes

---

## Cross-References Quick Index

**Looking for...? Try this file:**

| Topic | File | Section |
|-------|------|---------|
| Field definitions | SCHEMA.md | Top-Level Columns / Nested Objects |
| Enum values | CODEBOOK.md | Modality / Laterality / Diagnosis |
| Severity grading | RULES.md / CODEBOOK.md | Severity Grading Systems |
| Diagnosis mapping | RULES.md | Diagnosis Mapping |
| Laterality patterns | RULES.md | Laterality Detection |
| Modality patterns | RULES.md / CODEBOOK.md | Modality Inference |
| Validation rules | SCHEMA.md / CODEBOOK.md | Validation Rules / Ranges |
| Clinical findings | RULES.md / CODEBOOK.md | Clinical Findings Detection |
| Patient demographics | SCHEMA.md | PatientClinicalData |
| Image quality | RULES.md / CODEBOOK.md | Image Quality Assessment |
| Enhancement history | UPDATES.md | Major Enhancements |
| Roadmap | UPDATES.md | Roadmap |
| Performance | README.md / UPDATES.md | Performance Metrics |
| Architecture | README.md | Architecture |
| Quick start | README.md | Quick Start |

---

## Recent Consolidation

Documentation was recently consolidated from **11 files → 6 files** (45% reduction in file count while preserving 100% of information).

**Original 11 Files:**
- README.md
- PROJECT_STRUCTURE.md
- QUICK_START.md
- SCHEMA_REFERENCE.md (1000+ lines)
- SCHEMA_STATISTICS.md
- SCHEMA_ENHANCEMENT_COMPLETE.md
- ROBUST_SCHEMA_SUMMARY.md
- ENHANCEMENT_SUMMARY.md
- ENHANCEMENTS_COMPLETED.md
- DELIVERY_SUMMARY.md
- NOTEBOOK_GUIDE.md

**Consolidated to 6 Files:**
- README.md (quick start + architecture)
- METHODOLOGY.md (methodological foundations)
- SCHEMA.md (complete field reference)
- RULES.md (harmonization logic)
- CODEBOOK.md (data dictionary)
- UPDATES.md (release notes + roadmap)

See **CONSOLIDATION_SUMMARY.md** for detailed mapping.

---

## Common Questions

**Q: Where do I start?**  
A: Read **README.md** first. It has quick start instructions and a project overview.

**Q: What fields are in the schema?**  
A: See **SCHEMA.md** for complete field-by-field documentation with 122 total fields.

**Q: How does diagnosis mapping work?**  
A: See **RULES.md** → Diagnosis Mapping section (269+ keywords to 28 categories).

**Q: What are the valid values for [field]?**  
A: Check **CODEBOOK.md** for enumerations and validation ranges.

**Q: What's been enhanced in v2.0?**  
A: See **UPDATES.md** → Major Enhancements (Phase 2) section.

**Q: How do I use a specific inference function?**  
A: See **RULES.md** → Core Functions section.

**Q: What validation rules apply?**  
A: See **SCHEMA.md** → Validation Rules section and **CODEBOOK.md** → Validation Ranges.

**Q: How do I extend the rules?**  
A: See **RULES.md** → Pattern Matching Strategy section.

---

## File Versions

| File | Version | Updated | Status |
|------|---------|---------|--------|
| README.md | 2.0 | Dec 2025 | ✅ Current |
| SCHEMA.md | 2.0 | Dec 2025 | ✅ Current |
| RULES.md | 2.0 | Dec 2025 | ✅ Current |
| CODEBOOK.md | 2.0 | Dec 2025 | ✅ Current |
| UPDATES.md | 2.0 | Dec 2025 | ✅ Current |

---

## Getting Help

**For technical questions:**
- See **README.md** → Architecture section
- See **SCHEMA.md** → Complete reference
- See **RULES.md** → Function documentation

**For data questions:**
- See **CODEBOOK.md** → Data dictionary
- See **SCHEMA.md** → Field definitions
- See **RULES.md** → Inference logic

**For project questions:**
- See **README.md** → Project overview
- See **UPDATES.md** → Enhancement history
- See **UPDATES.md** → Roadmap & future plans

---

**Happy harmonizing! 🏥**
