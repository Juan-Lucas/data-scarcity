import csv
from collections import defaultdict
from pathlib import Path

from loguru import logger
import typer

from data_scarcity.config import PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    source_input_path: Path = PROCESSED_DATA_DIR / "source_dataset.csv",
    target_input_path: Path = PROCESSED_DATA_DIR / "target_dataset.csv",
    source_features_path: Path = PROCESSED_DATA_DIR / "source_features.csv",
    target_train_features_path: Path = PROCESSED_DATA_DIR / "target_train_features.csv",
    target_test_features_path: Path = PROCESSED_DATA_DIR / "target_test_features.csv",
    series_col: str = "series_id",
    time_col: str = "timestamp",
    target_col: str = "y",
    lag_count: int = 3,
    target_test_fraction: float = 0.3,
):
    """Create lagged features and target temporal split for train/test."""
    if lag_count < 1:
        raise ValueError("lag_count must be >= 1")
    if not (0 < target_test_fraction < 1):
        raise ValueError("target_test_fraction must be in (0, 1)")

    source_rows = _read_rows(source_input_path)
    target_rows = _read_rows(target_input_path)

    source_features = _build_lag_features(source_rows, series_col, time_col, target_col, lag_count)
    target_features = _build_lag_features(target_rows, series_col, time_col, target_col, lag_count)

    target_train, target_test = _split_target_temporal(
        target_features,
        series_col=series_col,
        time_col=time_col,
        test_fraction=target_test_fraction,
    )

    output_fields = [
        series_col,
        time_col,
        *[f"lag_{k}" for k in range(1, lag_count + 1)],
        "y",
    ]
    _write_rows(source_features_path, output_fields, source_features)
    _write_rows(target_train_features_path, output_fields, target_train)
    _write_rows(target_test_features_path, output_fields, target_test)

    logger.success(
        "Features generated. Source train rows: {}, Target train rows: {}, Target test rows: {}",
        len(source_features),
        len(target_train),
        len(target_test),
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _build_lag_features(
    rows: list[dict[str, str]],
    series_col: str,
    time_col: str,
    target_col: str,
    lag_count: int,
) -> list[dict[str, str]]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[series_col]].append(row)

    out: list[dict[str, str]] = []
    for sid, srows in grouped.items():
        ordered = sorted(srows, key=lambda r: _time_sort_key(r[time_col]))
        y_values = [float(r[target_col]) for r in ordered]

        for idx in range(lag_count, len(ordered)):
            item = {
                series_col: sid,
                time_col: ordered[idx][time_col],
                "y": str(y_values[idx]),
            }
            for k in range(1, lag_count + 1):
                item[f"lag_{k}"] = str(y_values[idx - k])
            out.append(item)

    return out


def _split_target_temporal(
    rows: list[dict[str, str]],
    series_col: str,
    time_col: str,
    test_fraction: float,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[series_col]].append(row)

    train_rows: list[dict[str, str]] = []
    test_rows: list[dict[str, str]] = []

    for sid, srows in grouped.items():
        ordered = sorted(srows, key=lambda r: _time_sort_key(r[time_col]))
        n = len(ordered)
        n_test = max(1, int(n * test_fraction))
        if n - n_test < 1:
            n_test = max(1, n - 1)

        split_idx = n - n_test
        train_rows.extend(ordered[:split_idx])
        test_rows.extend(ordered[split_idx:])

    return train_rows, test_rows


def _write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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
