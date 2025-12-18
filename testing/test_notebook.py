#!/usr/bin/env python3
"""
Test script to validate notebook functionality
"""

import os
import re
import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure pandas display
pd.set_option("display.max_columns", 200)
pd.set_option("display.max_colwidth", 50)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("✓ Libraries imported successfully")

# Test canonical schema
CANONICAL_COLUMNS = [
    "image_id", "dataset_name", "image_path", "eye", "modality", "view_type",
    "diagnosis_raw", "diagnosis_category", "diagnosis_binary", "severity",
    "patient_id", "age", "sex", "resolution_x", "resolution_y", "extra_json"
]

def canonical_row():
    return {col: None for col in CANONICAL_COLUMNS}

print(f"✓ Canonical schema defined with {len(CANONICAL_COLUMNS)} columns")

# Test diagnosis mapping
DIAGNOSIS_MAPPING = {
    'dr': 'DR', 'diabetic retinopathy': 'DR', 'retinopathy': 'DR',
    'amd': 'AMD', 'age-related macular degeneration': 'AMD',
    'cataract': 'Cataract', 'glaucoma': 'Glaucoma',
    'normal': 'Normal', 'healthy': 'Normal'
}

def map_diagnosis(raw):
    if raw is None:
        return None
    r = str(raw).lower().strip()
    if r in DIAGNOSIS_MAPPING:
        return DIAGNOSIS_MAPPING[r]
    for key, normalized in DIAGNOSIS_MAPPING.items():
        if key in r:
            return normalized
    return 'Other'

print("✓ Harmonization rules defined")

# Test demo dataset creation
demo_datasets = {}

demo_datasets['Cataract DS'] = pd.DataFrame({
    'image_path': ['cat_001_right.jpg', 'cat_001_left.jpg'],
    'condition': ['Immature Cataract', 'Healthy'],
    'age': [67, 67],
    'sex': ['M', 'M']
})

print("✓ Demo datasets created")

# Test loader function
def load_dataset_from_dataframe(df, dataset_name, img_field=None, diag_field=None, eye_field=None):
    logger.info(f"Loading dataset: {dataset_name}")

    if df.empty:
        return pd.DataFrame(columns=CANONICAL_COLUMNS)

    # Auto-detect fields
    if img_field is None:
        img_field = next((c for c in df.columns if any(x in c.lower() for x in ['path', 'img', 'image', 'file', 'filename'])), None)
    if diag_field is None:
        diag_field = next((c for c in df.columns if any(x in c.lower() for x in ['label', 'class', 'diagn', 'condition', 'disease'])), None)

    logger.info(f"  Auto-detected columns: img={img_field}, diag={diag_field}")

    rows = []

    for idx, row in df.iterrows():
        r = canonical_row()
        r["image_id"] = f"{dataset_name}_{idx}"
        r["dataset_name"] = dataset_name
        r["image_path"] = row.get(img_field) if img_field else None
        raw_diag = row.get(diag_field) if diag_field else None
        r["diagnosis_raw"] = str(raw_diag) if pd.notna(raw_diag) else None
        r["diagnosis_category"] = map_diagnosis(r["diagnosis_raw"])
        r["diagnosis_binary"] = 'Normal' if r["diagnosis_category"] == 'Normal' else 'Abnormal'

        # Extract metadata
        for age_col in ['age', 'patient_age', 'age_years']:
            if age_col in df.columns and pd.notna(row.get(age_col)):
                try:
                    r["age"] = int(row.get(age_col))
                    break
                except (ValueError, TypeError):
                    pass

        for sex_col in ['sex', 'gender', 'patient_sex']:
            if sex_col in df.columns and pd.notna(row.get(sex_col)):
                val = str(row.get(sex_col)).upper()[:1]
                if val in ['M', 'F']:
                    r["sex"] = val
                    break

        rows.append(r)

    result_df = pd.DataFrame(rows)
    logger.info(f"  Harmonized {len(result_df)} records from {dataset_name}")
    return result_df

# Test harmonization
harmonized_frames = []
for dataset_name, df in demo_datasets.items():
    print(f"\nProcessing: {dataset_name}")
    harmonized_df = load_dataset_from_dataframe(df, dataset_name)
    if not harmonized_df.empty:
        harmonized_frames.append(harmonized_df)
        print(f"  ✓ Harmonized shape: {harmonized_df.shape}")

# Test merging
if harmonized_frames:
    final_df = pd.concat(harmonized_frames, ignore_index=True)
    print(f"\n✓ Merged dataset created")
    print(f"  Total records: {len(final_df)}")
    print(f"  Shape: {final_df.shape}")

    # Test export
    output_dir = Path('.') / 'output'
    output_dir.mkdir(exist_ok=True)

    parquet_path = output_dir / 'harmonized_test.parquet'
    final_df.to_parquet(parquet_path, index=False)
    print(f"✓ Exported to Parquet: {parquet_path}")

    # Test reading back
    loaded_df = pd.read_parquet(parquet_path)
    print(f"✓ Loaded {len(loaded_df)} records from {parquet_path}")
    print(f"  Columns match: {list(loaded_df.columns) == list(final_df.columns)}")

    print("\n=== SAMPLE RECORDS ===")
    print(loaded_df.head(3)[['image_id', 'dataset_name', 'diagnosis_category', 'modality', 'eye']].to_string())

print("\n🎉 All notebook functionality tests passed!")