# Kaggle API setup script
# Usage:
#   1. Set KAGGLE_API_TOKEN in your shell before running this script, or
#   2. Store credentials in %USERPROFILE%\.kaggle\kaggle.json per Kaggle docs.

if (-not $env:KAGGLE_API_TOKEN) {
	Write-Host "KAGGLE_API_TOKEN is not set."
	Write-Host "Set it for the current session with:"
	Write-Host "  `$env:KAGGLE_API_TOKEN = '<your-token>'"
	exit 1
}

Write-Host "KAGGLE_API_TOKEN detected for current session."
