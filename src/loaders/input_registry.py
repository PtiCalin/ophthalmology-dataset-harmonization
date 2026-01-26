"""
Auto-detected dataset loaders for all INPUT datasets.

This module discovers datasets in the INPUT folder, loads metadata or images,
constructs per-dataset loader configs, and harmonizes them via UniversalLoader.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import logging

import pandas as pd

from .universal_loader import UniversalLoader

logger = logging.getLogger(__name__)

IMAGE_PATTERNS = ["*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff", "*.bmp"]
META_PATTERNS = ["*.csv", "*.parquet"]


@dataclass
class DatasetConfig:
    name: str
    data_dir: Path
    column_mapping: Optional[Dict[str, str]] = None
    enabled: bool = True


@dataclass
class DatasetLoadResult:
    name: str
    dataframe: pd.DataFrame
    loader: UniversalLoader
    report: Dict


def _list_files(base_dir: Path, patterns: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        files.extend(base_dir.rglob(pattern))
    return [p for p in files if p.is_file()]


def _choose_data_dir(dataset_dir: Path) -> Optional[Path]:
    raw_dir = dataset_dir / "raw"
    if raw_dir.exists() and any(raw_dir.rglob("*")):
        return raw_dir

    if any(_list_files(dataset_dir, META_PATTERNS)) or any(_list_files(dataset_dir, IMAGE_PATTERNS)):
        return dataset_dir

    return None


def load_dataset_from_path(dataset_dir: Path) -> Optional[pd.DataFrame]:
    """Load a dataset from a folder by detecting CSV/Parquet or images."""
    dataset_dir = Path(dataset_dir)
    if not dataset_dir.exists():
        logger.warning("Dataset dir not found: %s", dataset_dir)
        return None

    csv_files = _list_files(dataset_dir, ["*.csv"])
    parquet_files = _list_files(dataset_dir, ["*.parquet"])

    meta_candidates = csv_files + parquet_files
    if meta_candidates:
        meta_candidates.sort(key=lambda p: p.stat().st_size, reverse=True)
        meta_file = meta_candidates[0]
        try:
            if meta_file.suffix.lower() == ".csv":
                df = pd.read_csv(meta_file)
            else:
                df = pd.read_parquet(meta_file)
            logger.info("Loaded metadata: %s (%s)", meta_file, df.shape)
            return df
        except Exception as exc:
            logger.warning("Failed to load metadata %s: %s", meta_file, exc)

    image_files = _list_files(dataset_dir, IMAGE_PATTERNS)
    if image_files:
        df = pd.DataFrame({
            "image_path": [str(p.relative_to(dataset_dir)) for p in image_files],
            "filename": [p.name for p in image_files],
        })
        logger.info("Built image-only dataframe: %s (%s)", dataset_dir, df.shape)
        return df

    return None


def build_dataset_registry(
    input_root: Path = Path("..") / "INPUT",
    overrides: Optional[Dict[str, Dict]] = None,
) -> List[DatasetConfig]:
    """Create a registry of dataset configs from INPUT folder.

    overrides can include per-dataset options:
    { "dataset_name": {"column_mapping": {...}, "enabled": True, "data_dir": "path"} }
    """
    overrides = overrides or {}
    input_root = Path(input_root)

    if not input_root.exists():
        logger.warning("INPUT root not found: %s", input_root)
        return []

    configs: List[DatasetConfig] = []

    for dataset_dir in sorted([p for p in input_root.iterdir() if p.is_dir()]):
        if dataset_dir.name.startswith("."):
            continue

        override = overrides.get(dataset_dir.name, {})
        enabled = override.get("enabled", True)

        data_dir = override.get("data_dir")
        if data_dir:
            data_dir = Path(data_dir)
        else:
            data_dir = _choose_data_dir(dataset_dir)

        if data_dir is None:
            logger.warning("No usable data found for %s", dataset_dir.name)
            continue

        column_mapping = override.get("column_mapping")

        configs.append(
            DatasetConfig(
                name=dataset_dir.name,
                data_dir=data_dir,
                column_mapping=column_mapping,
                enabled=enabled,
            )
        )

    return configs


def load_and_harmonize_inputs(
    input_root: Path = Path("..") / "INPUT",
    overrides: Optional[Dict[str, Dict]] = None,
) -> Tuple[List[pd.DataFrame], List[DatasetLoadResult], List[str]]:
    """Load and harmonize all auto-detected INPUT datasets."""
    configs = build_dataset_registry(input_root=input_root, overrides=overrides)
    harmonized_frames: List[pd.DataFrame] = []
    results: List[DatasetLoadResult] = []
    failed: List[str] = []

    for config in configs:
        if not config.enabled:
            logger.info("Skipping disabled dataset: %s", config.name)
            continue

        df = load_dataset_from_path(config.data_dir)
        if df is None or df.empty:
            logger.warning("No data loaded for %s", config.name)
            failed.append(config.name)
            continue

        loader = UniversalLoader(config.name, column_mapping=config.column_mapping or {})
        try:
            harmonized_df = loader.load_and_harmonize(df)
            if harmonized_df.empty:
                failed.append(config.name)
                continue

            harmonized_frames.append(harmonized_df)
            results.append(DatasetLoadResult(
                name=config.name,
                dataframe=harmonized_df,
                loader=loader,
                report=loader.get_load_report(),
            ))
        except Exception as exc:
            logger.warning("Failed to harmonize %s: %s", config.name, exc)
            failed.append(config.name)

    return harmonized_frames, results, failed
