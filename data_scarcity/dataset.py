import csv
import json
import random
from collections import defaultdict
from pathlib import Path

from loguru import logger
import typer

from data_scarcity.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "m5" / "sales_train_validation.csv",
    source_output_path: Path = PROCESSED_DATA_DIR / "source_dataset.csv",
    target_output_path: Path = PROCESSED_DATA_DIR / "target_dataset.csv",
    metadata_output_path: Path = PROCESSED_DATA_DIR / "experimental_setup_metadata.json",
    series_col: str = "series_id",
    time_col: str = "timestamp",
    target_col: str = "y",
    target_ratio: float = 0.2,
    target_history_fraction: float = 0.25,
    min_points_per_series: int = 20,
    max_series: int = 250,
    max_days: int = 365,
    seed: int = 42,
):
    """Build source/target datasets and simulate launch-phase low-data on target."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    if not (0 < target_ratio < 1):
        raise ValueError("target_ratio must be in (0, 1)")
    if not (0 < target_history_fraction <= 1):
        raise ValueError("target_history_fraction must be in (0, 1]")

    logger.info("Loading raw dataset from {}", input_path)
    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

    if "id" in header and any(name.startswith("d_") for name in header):
        _process_m5_stream(
            input_path=input_path,
            source_output_path=source_output_path,
            target_output_path=target_output_path,
            metadata_output_path=metadata_output_path,
            target_ratio=target_ratio,
            target_history_fraction=target_history_fraction,
            min_points_per_series=min_points_per_series,
            max_series=max_series,
            max_days=max_days,
            seed=seed,
        )
        return

    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    required = {series_col, time_col, target_col}
    missing = required.difference(fieldnames)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    grouped = defaultdict(list)
    for row in rows:
        grouped[row[series_col]].append(row)

    # Keep only series with enough history for lagged features and split.
    valid_grouped = {
        sid: sorted(srows, key=lambda r: _time_sort_key(r[time_col]))
        for sid, srows in grouped.items()
        if len(srows) >= min_points_per_series
    }
    if len(valid_grouped) < 2:
        raise ValueError("Need at least 2 valid series after filtering to form source and target sets")

    series_ids = sorted(valid_grouped)
    rng = random.Random(seed)
    n_target = max(1, int(len(series_ids) * target_ratio))
    n_target = min(n_target, len(series_ids) - 1)
    target_ids = set(rng.sample(series_ids, k=n_target))
    source_ids = [sid for sid in series_ids if sid not in target_ids]

    source_rows: list[dict[str, str]] = []
    target_rows: list[dict[str, str]] = []
    truncation_info: dict[str, dict[str, int]] = {}

    for sid in source_ids:
        source_rows.extend(valid_grouped[sid])

    for sid in sorted(target_ids):
        full_rows = valid_grouped[sid]
        full_n = len(full_rows)
        kept_n = max(8, int(full_n * target_history_fraction))
        kept_n = min(kept_n, full_n)
        target_rows.extend(full_rows[:kept_n])
        truncation_info[sid] = {"original_points": full_n, "kept_points": kept_n}

    source_output_path.parent.mkdir(parents=True, exist_ok=True)
    target_output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_output_path.parent.mkdir(parents=True, exist_ok=True)

    with source_output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(source_rows)

    with target_output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(target_rows)

    metadata = {
        "input_path": str(input_path),
        "source_output_path": str(source_output_path),
        "target_output_path": str(target_output_path),
        "series_col": series_col,
        "time_col": time_col,
        "target_col": target_col,
        "n_series_total": len(series_ids),
        "n_series_source": len(source_ids),
        "n_series_target": len(target_ids),
        "target_ratio": target_ratio,
        "target_history_fraction": target_history_fraction,
        "truncation_per_target_series": truncation_info,
        "seed": seed,
    }
    with metadata_output_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.success(
        "Dataset setup complete. Source rows: {}, Target rows (low-data): {}",
        len(source_rows),
        len(target_rows),
    )


def _process_m5_stream(
    input_path: Path,
    source_output_path: Path,
    target_output_path: Path,
    metadata_output_path: Path,
    target_ratio: float,
    target_history_fraction: float,
    min_points_per_series: int,
    max_series: int,
    max_days: int,
    seed: int,
) -> None:
    rng = random.Random(seed)

    source_output_path.parent.mkdir(parents=True, exist_ok=True)
    target_output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["series_id", "timestamp", "y"]
    truncation_info: dict[str, dict[str, int]] = {}
    n_source_series = 0
    n_target_series = 0
    n_source_rows = 0
    n_target_rows = 0
    processed_series = 0

    with (
        input_path.open("r", newline="", encoding="utf-8") as fin,
        source_output_path.open("w", newline="", encoding="utf-8") as fs,
        target_output_path.open("w", newline="", encoding="utf-8") as ft,
    ):
        reader = csv.DictReader(fin)
        all_day_cols = [c for c in (reader.fieldnames or []) if c.startswith("d_")]
        day_cols = sorted(all_day_cols, key=_time_sort_key)
        if max_days > 0:
            day_cols = day_cols[-max_days:]

        sw = csv.DictWriter(fs, fieldnames=fieldnames)
        tw = csv.DictWriter(ft, fieldnames=fieldnames)
        sw.writeheader()
        tw.writeheader()

        for row in reader:
            if max_series > 0 and processed_series >= max_series:
                break

            sid = row["id"]
            series_pairs = [(d, row[d]) for d in day_cols]
            if len(series_pairs) < min_points_per_series:
                continue

            processed_series += 1
            is_target = rng.random() < target_ratio

            if is_target:
                kept_n = max(8, int(len(series_pairs) * target_history_fraction))
                kept_n = min(kept_n, len(series_pairs))
                for d, y in series_pairs[:kept_n]:
                    tw.writerow({"series_id": sid, "timestamp": d, "y": y})
                    n_target_rows += 1
                n_target_series += 1
                truncation_info[sid] = {
                    "original_points": len(series_pairs),
                    "kept_points": kept_n,
                }
            else:
                for d, y in series_pairs:
                    sw.writerow({"series_id": sid, "timestamp": d, "y": y})
                    n_source_rows += 1
                n_source_series += 1

    # Guarantee both domains have at least one series.
    if n_source_series == 0 or n_target_series == 0:
        raise ValueError(
            "M5 split failed (empty source or target). Increase max_series or adjust target_ratio."
        )

    metadata = {
        "input_path": str(input_path),
        "source_output_path": str(source_output_path),
        "target_output_path": str(target_output_path),
        "n_series_total": n_source_series + n_target_series,
        "n_series_source": n_source_series,
        "n_series_target": n_target_series,
        "n_rows_source": n_source_rows,
        "n_rows_target": n_target_rows,
        "target_ratio": target_ratio,
        "target_history_fraction": target_history_fraction,
        "max_series": max_series,
        "max_days": max_days,
        "seed": seed,
        "truncation_per_target_series": truncation_info,
    }
    with metadata_output_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.success(
        "M5 setup complete. Source series: {} | Target series: {} | Source rows: {} | Target rows: {}",
        n_source_series,
        n_target_series,
        n_source_rows,
        n_target_rows,
    )


def _time_sort_key(value: str) -> float | str:
    if value.startswith("d_"):
        suffix = value[2:]
        if suffix.isdigit():
            return float(int(suffix))
    try:
        return float(value)
    except ValueError:
        return value


if __name__ == "__main__":
    app()
