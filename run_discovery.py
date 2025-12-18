#!/usr/bin/env python3
"""
Automated Dataset Discovery Runner
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    parser = argparse.ArgumentParser(description="Run automated dataset discovery")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")

    args = parser.parse_args()

    try:
        # Import and run discovery
        from pipeline.simple_discovery import discover_and_document

        new_datasets = discover_and_document(dry_run=args.dry_run)

        if args.dry_run:
            print(f"Dry run: Would process {len(new_datasets)} datasets")
        else:
            print(f"Processed {len(new_datasets)} new datasets")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())