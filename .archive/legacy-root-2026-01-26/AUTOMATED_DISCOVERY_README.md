# Automated Dataset Discovery

This system automatically discovers new datasets from your Kaggle "Ophthalmology" collection and creates the necessary documentation structure for integration into the harmonization pipeline.

## Overview

The automated discovery system consists of:

- **Dataset Search**: Searches Kaggle for ophthalmology-related datasets
- **Intelligent Filtering**: Uses keywords to identify relevant datasets
- **Documentation Generation**: Creates DESCRIPTION.md, CODEBOOK.md, and INTEGRATION.md files
- **Registry Updates**: Automatically updates INPUT.md with new datasets

## Setup

### Prerequisites

1. **Kaggle API Access**:

   ```bash
   # Install kagglehub
   pip install kagglehub

   # Set up API token (optional, improves rate limits)
   export KAGGLE_API_TOKEN="your_api_token"
   ```

2. **Python Dependencies**:

   ```bash
   pip install requests pandas
   ```

### Configuration

Edit `src/pipeline/config.py` to customize:

- **Kaggle Username**: Set your Kaggle username
- **Keywords**: Add ophthalmology-related search terms
- **Templates**: Customize documentation templates

## Usage

### One-time Discovery

Run the discovery script:

```bash
# From project root
python run_discovery.py
```

### Dry Run

See what would be discovered without making changes:

```bash
python run_discovery.py --dry-run
```

### Custom User

Search datasets from a different Kaggle user:

```bash
python run_discovery.py --user other_username
```

### Programmatic Usage

```python
from src.pipeline.enhanced_discovery import discover_and_document

# Discover and document new datasets
new_datasets = discover_and_document()

print(f"Processed {len(new_datasets)} new datasets")
```

## Scheduling

### Windows Task Scheduler

Create a daily task:

```powershell
schtasks /create /tn "Kaggle Dataset Discovery" /tr "python C:\path\to\project\run_discovery.py" /sc daily /st 09:00
```

### Linux Cron

Add to crontab:

```bash
# Edit crontab
crontab -e

# Add line for daily execution at 9 AM
0 9 * * * cd /path/to/project && python run_discovery.py
```

### Python Script

```python
import schedule
import time
from run_discovery import discover_and_document

# Schedule daily discovery
schedule.every().day.at("09:00").do(discover_and_document)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

## How It Works

### 1. Dataset Discovery

The system searches Kaggle using:

- User-specific dataset search
- Keyword filtering for ophthalmology terms
- Relevance scoring and ranking

### 2. Filtering

Datasets are filtered using:

- **Include Keywords**: ophthalmology, retina, fundus, OCT, eye, etc.
- **Exclude Keywords**: non-medical, synthetic, test data, etc.

### 3. Documentation Generation

For each new dataset, the system creates:

- **DESCRIPTION.md**: Dataset overview and clinical context
- **CODEBOOK.md**: Field definitions and validation rules
- **INTEGRATION.md**: Loading instructions and harmonization steps
- **raw/**: Directory for raw dataset files

### 4. Registry Updates

New datasets are automatically added to `INPUT/INPUT.md` in the "Documentation Pending" section.

## Output Structure

```txt
INPUT/
├── new-dataset-slug/
│   ├── DESCRIPTION.md    # Auto-generated overview
│   ├── CODEBOOK.md       # Field specifications
│   ├── INTEGRATION.md    # Loading instructions
│   └── raw/             # Raw data directory
└── INPUT.md             # Updated registry
```

## Customization

### Adding Keywords

Edit `src/pipeline/config.py`:

```python
KAGGLE_CONFIG = {
    "collection_keywords": [
        "ophthalmology", "retina", "fundus", "oct", "eye",
        "diabetic retinopathy", "glaucoma", "macular degeneration",
        "retinal", "optical coherence tomography",
        "YOUR_NEW_KEYWORD"  # Add here
    ]
}
```

### Modifying Templates

Update the template strings in `config.py` to customize the generated documentation.

### Custom Filtering

Extend `OphthalmologyDatasetFilter` class for more sophisticated filtering logic.

## Troubleshooting

### No Datasets Found

- Check your Kaggle username in config
- Verify internet connection
- Check Kaggle API status

### Permission Errors

- Ensure write access to INPUT/ directory
- Check file permissions

### Import Errors

- Install missing dependencies: `pip install kagglehub requests`
- Ensure Python path includes src/: `export PYTHONPATH=$PYTHONPATH:./src`

### Rate Limiting

- Kaggle API has rate limits
- Add delays between requests if needed
- Use API token for higher limits

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Daily Dataset Discovery
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
  workflow_dispatch:

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run discovery
        run: python run_discovery.py
        env:
          KAGGLE_API_TOKEN: ${{ secrets.KAGGLE_API_TOKEN }}
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add INPUT/
          git commit -m "Auto-discover new datasets" || echo "No changes to commit"
          git push
```

## Security Notes

- API tokens are sensitive; use environment variables
- Generated documentation is templates; manual review required
- Automatic commits should be reviewed before merging

## Contributing

To extend the discovery system:

1. **New Data Sources**: Add support for other platforms beyond Kaggle
2. **Better Filtering**: Improve relevance algorithms
3. **Enhanced Templates**: Create dataset-type-specific templates
4. **Quality Checks**: Add automatic quality validation

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review logs for error messages
3. Verify configuration settings
4. Test with `--dry-run` flag 

</content>
    <parametername="filePath">c:\Users\charl\OneDrive\Projets\ophthalmology-dataset-harmonization\AUTOMATED_DISCOVERY_README.md