# KERMANY2018-DATASET Raw Data Directory

This directory should contain the raw kermany2018-dataset dataset files downloaded from Kaggle.

## Expected Files

### Clinical Data
- clinical_annotations.csv - Clinical measurements and diagnoses
- patient_demographics.csv - Patient demographic information
- image_metadata.csv - Image acquisition details

### Image Data
- images/ - Directory containing retinal images
  - 	raining/ - Training set images
  - alidation/ - Validation set images
  - 	est/ - Test set images

### Ground Truth
- ground_truth.csv - Expert annotations
- segmentation_masks/ - Pixel-level segmentation masks (if available)

## Download Instructions

1. Visit the Kaggle dataset URL
2. Download all files to this directory
3. Extract archives maintaining directory structure
4. Ensure all CSV files are properly formatted and encoded

## Data Verification

After download, verify:
- All expected CSV files are present
- Image directories contain expected number of files
- File sizes match dataset description
- No corruption in downloaded archives

## Notes

- Images are typically in high-resolution format
- Dataset size varies by collection
- Maintain original file names and directory structure for proper integration
