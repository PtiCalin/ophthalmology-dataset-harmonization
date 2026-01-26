# REFUGE2 Raw Data Directory

This directory should contain the raw REFUGE2 dataset files downloaded from Kaggle.

## Expected Files

### Clinical Data
- `clinical_annotations.csv` - Clinical measurements and diagnoses
- `patient_demographics.csv` - Patient demographic information
- `image_metadata.csv` - Image acquisition details

### Image Data
- `images/` - Directory containing retinal fundus images
  - `training/` - Training set images
  - `validation/` - Validation set images
  - `test/` - Test set images

### Ground Truth
- `ground_truth.csv` - Expert annotations for glaucoma classification
- `segmentation_masks/` - Pixel-level segmentation masks (if available)

## Download Instructions

1. Visit: https://www.kaggle.com/datasets/ferencjuhsz/refuge2-and-refuge2cross-dataset
2. Download all files
3. Extract to this directory maintaining the original structure
4. Ensure all CSV files are properly formatted and encoded

## Data Verification

After download, verify:
- All expected CSV files are present
- Image directories contain the expected number of files
- File sizes match the dataset description
- No corruption in downloaded archives

## Notes

- Images are typically in high-resolution format (e.g., 2124x2056 pixels)
- Total dataset size: ~2GB
- Maintain original file names and directory structure for proper integration