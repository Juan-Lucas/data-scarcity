import csv
from dataclasses import dataclass
import math
from pathlib import Path

from loguru import logger
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
import typer

from data_scarcity.config import PROCESSED_DATA_DIR

app = typer.Typer()


@dataclass
class ModelResult:
    name: str
    mae: float
    rmse: float
    pinball_loss: float
    interval_coverage: float
    interval_avg_width: float


@app.command()
def main(
    source_features_path: Path = PROCESSED_DATA_DIR / "source_features.csv",
    target_train_features_path: Path = PROCESSED_DATA_DIR / "target_train_features.csv",
    target_test_features_path: Path = PROCESSED_DATA_DIR / "target_test_features.csv",
    results_csv_path: Path = PROCESSED_DATA_DIR / "model_comparison_results.csv",
    predictions_csv_path: Path = PROCESSED_DATA_DIR
    / "model_comparison_predictions.csv",
    quantiles: str = "0.1,0.5,0.9",
    ridge_alpha: float = 1e-3,
    transfer_lambda: float = 10.0,
    random_state: int = 42,
):
    """Compare Ridge, Random Forest, Gradient Boosting, and Ridge-transfer on the target test set."""
    q_levels = sorted({float(q.strip()) for q in quantiles.split(",") if q.strip()})
    if not q_levels:
        raise ValueError("At least one quantile is required")

    feature_cols_s, x_source, y_source = _read_xy(source_features_path)
    feature_cols_t, x_target_train, y_target_train = _read_xy(
        target_train_features_path
    )
    feature_cols_te, x_target_test, y_target_test = _read_xy(target_test_features_path)

    if feature_cols_s != feature_cols_t or feature_cols_s != feature_cols_te:
        raise ValueError("Feature columns do not match across splits")

    source_weights = _fit_ridge(x_source, y_source, ridge_alpha)
    ridge_target_weights = _fit_ridge(x_target_train, y_target_train, ridge_alpha)
    ridge_transfer_weights = _fit_transfer_ridge(
        x_target_train,
        y_target_train,
        prior_weights=source_weights,
        ridge_alpha=ridge_alpha,
        transfer_lambda=transfer_lambda,
    )

    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1,
    )
    rf.fit(x_target_train, y_target_train)

    gbr = GradientBoostingRegressor(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=3,
        random_state=random_state,
        loss="squared_error",
    )
    gbr.fit(x_target_train, y_target_train)

    models = {
        "ridge_target_only": (ridge_target_weights, _predict_linear),
        "ridge_transfer": (ridge_transfer_weights, _predict_linear),
        "random_forest": (rf, _predict_sklearn),
        "gradient_boosting": (gbr, _predict_sklearn),
    }

    results: list[ModelResult] = []

    predictions_by_model: dict[str, list[float]] = {}
    interval_bounds_by_model: dict[str, tuple[list[float], list[float]]] = {}

    for model_name, (model_obj, predictor) in models.items():
        train_pred = [predictor(model_obj, x) for x in x_target_train]
        test_pred = [predictor(model_obj, x) for x in x_target_test]
        residuals = [y - yhat for y, yhat in zip(y_target_train, train_pred)]
        residual_q = {q: _quantile(residuals, q) for q in q_levels}

        lo_q = _closest_level(q_levels, 0.1)
        hi_q = _closest_level(q_levels, 0.9)
        lower = [p + residual_q[lo_q] for p in test_pred]
        upper = [p + residual_q[hi_q] for p in test_pred]

        result = ModelResult(
            name=model_name,
            mae=_mae(y_target_test, test_pred),
            rmse=_rmse(y_target_test, test_pred),
            pinball_loss=_pinball_multi(
                y_target_test,
                {q: [p + residual_q[q] for p in test_pred] for q in q_levels},
            ),
            interval_coverage=_coverage(y_target_test, lower, upper),
            interval_avg_width=_avg_width(lower, upper),
        )
        results.append(result)
        predictions_by_model[model_name] = test_pred
        interval_bounds_by_model[model_name] = (lower, upper)

    _write_results(results_csv_path, results)
    _write_predictions(
        predictions_csv_path,
        feature_cols_te,
        x_target_test,
        y_target_test,
        predictions_by_model,
        interval_bounds_by_model,
        list(models.keys()),
    )

    logger.success(
        "Model comparison complete. Results saved to {} and {}",
        results_csv_path,
        predictions_csv_path,
    )


def _read_xy(path: Path) -> tuple[list[str], list[list[float]], list[float]]:
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        feature_cols = sorted(
            [c for c in fieldnames if c.startswith("lag_")], key=_lag_sort_key
        )
        if not feature_cols:
            raise ValueError(f"No lag features found in {path}")

        x: list[list[float]] = []
        y: list[float] = []
        for row in reader:
            x.append([float(row[col]) for col in feature_cols])
            y.append(float(row["y"]))

    return feature_cols, x, y


def _fit_ridge(x: list[list[float]], y: list[float], ridge_alpha: float) -> list[float]:
    phi = [[1.0, *row] for row in x]
    p = len(phi[0])

    a = [[0.0 for _ in range(p)] for _ in range(p)]
    b = [0.0 for _ in range(p)]

    for r, yi in zip(phi, y):
        for i in range(p):
            b[i] += r[i] * yi
            for j in range(p):
                a[i][j] += r[i] * r[j]

    for i in range(1, p):
        a[i][i] += ridge_alpha

    return _solve_linear_system(a, b)


def _fit_transfer_ridge(
    x: list[list[float]],
    y: list[float],
    prior_weights: list[float],
    ridge_alpha: float,
    transfer_lambda: float,
) -> list[float]:
    phi = [[1.0, *row] for row in x]
    p = len(phi[0])

    a = [[0.0 for _ in range(p)] for _ in range(p)]
    b = [0.0 for _ in range(p)]

    for r, yi in zip(phi, y):
        for i in range(p):
            b[i] += r[i] * yi
            for j in range(p):
                a[i][j] += r[i] * r[j]

    for i in range(p):
        if i > 0:
            a[i][i] += ridge_alpha
        a[i][i] += transfer_lambda
        b[i] += transfer_lambda * prior_weights[i]

    return _solve_linear_system(a, b)


def _solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-12:
            continue
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]

        pivot_val = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= pivot_val

        for r in range(n):
            if r == col:
                continue
            factor = m[r][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                m[r][j] -= factor * m[col][j]

    return [m[i][n] for i in range(n)]


def _predict_linear(weights: list[float], x: list[float]) -> float:
    return weights[0] + sum(w * xi for w, xi in zip(weights[1:], x))


def _predict_sklearn(model, x: list[float]) -> float:
    return float(model.predict([x])[0])


def _mae(y_true: list[float], y_pred: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)


def _rmse(y_true: list[float], y_pred: list[float]) -> float:
    mse = sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)
    return math.sqrt(mse)


def _pinball(y: float, qhat: float, tau: float) -> float:
    u = y - qhat
    return u * (tau - (1.0 if u < 0 else 0.0))


def _pinball_multi(y_true: list[float], q_preds: dict[float, list[float]]) -> float:
    total = 0.0
    n = len(y_true)
    levels = sorted(q_preds)
    for q in levels:
        qh = q_preds[q]
        total += sum(_pinball(y, p, q) for y, p in zip(y_true, qh)) / n
    return total / len(levels)


def _coverage(y_true: list[float], lower: list[float], upper: list[float]) -> float:
    return sum(1 for y, lo, hi in zip(y_true, lower, upper) if lo <= y <= hi) / len(
        y_true
    )


def _avg_width(lower: list[float], upper: list[float]) -> float:
    return sum(hi - lo for lo, hi in zip(lower, upper)) / len(lower)


def _quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]

    pos = (len(ordered) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


def _closest_level(levels: list[float], target: float) -> float:
    return min(levels, key=lambda q: abs(q - target))


def _write_results(path: Path, results: list[ModelResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "model",
                "MAE",
                "RMSE",
                "pinball_loss",
                "interval_coverage",
                "interval_avg_width",
            ],
        )
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    "model": row.name,
                    "MAE": row.mae,
                    "RMSE": row.rmse,
                    "pinball_loss": row.pinball_loss,
                    "interval_coverage": row.interval_coverage,
                    "interval_avg_width": row.interval_avg_width,
                }
            )


def _write_predictions(
    path: Path,
    feature_cols: list[str],
    x_test: list[list[float]],
    y_test: list[float],
    predictions_by_model: dict[str, list[float]],
    interval_bounds_by_model: dict[str, tuple[list[float], list[float]]],
    model_names: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["y"] + [f"lag_{i}" for i in range(1, len(feature_cols) + 1)]
    for name in model_names:
        fieldnames.extend([f"{name}_pred", f"{name}_lo", f"{name}_hi"])

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(x_test):
            out = {"y": y_test[idx]}
            for i, value in enumerate(row, start=1):
                out[f"lag_{i}"] = value
            for name in model_names:
                pred = predictions_by_model[name][idx]
                lo, hi = interval_bounds_by_model[name]
                out[f"{name}_pred"] = pred
                out[f"{name}_lo"] = lo[idx]
                out[f"{name}_hi"] = hi[idx]
            writer.writerow(out)


def _lag_sort_key(name: str) -> int:
    suffix = name.split("_", maxsplit=1)[1]
    return int(suffix) if suffix.isdigit() else 10**9


if __name__ == "__main__":
    app()
