import csv
from pathlib import Path

from loguru import logger
import matplotlib.pyplot as plt
import typer

from data_scarcity.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    model_results_path: Path = PROCESSED_DATA_DIR / "model_comparison_results.csv",
    experiment_grid_path: Path = PROCESSED_DATA_DIR / "experiment_results_grid.csv",
    output_dir: Path = FIGURES_DIR,
):
    """Generate 3 additional performance visualizations for the article."""
    if not model_results_path.exists():
        raise FileNotFoundError(f"Model comparison file not found: {model_results_path}")
    if not experiment_grid_path.exists():
        raise FileNotFoundError(f"Experiment grid file not found: {experiment_grid_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    model_rows = _read_rows(model_results_path)
    grid_rows = _read_rows(experiment_grid_path)

    _plot_model_metric_bars(model_rows, output_dir / "model_metrics_bars.png")
    _plot_transfer_gain_heatmap(grid_rows, output_dir / "transfer_gain_heatmap.png")
    _plot_coverage_width_tradeoff(model_rows, output_dir / "coverage_width_tradeoff.png")

    logger.success("Additional metrics figures generated in {}", output_dir)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _plot_model_metric_bars(rows: list[dict[str, str]], output_path: Path) -> None:
    models = [r["model"] for r in rows]
    maes = [float(r["MAE"]) for r in rows]
    rmses = [float(r["RMSE"]) for r in rows]
    pinballs = [float(r["pinball_loss"]) for r in rows]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    metrics = [("MAE", maes), ("RMSE", rmses), ("Pinball", pinballs)]

    for ax, (title, values) in zip(axes, metrics):
        ax.bar(models, values, color="#2563eb", alpha=0.85)
        ax.set_title(title)
        ax.set_xlabel("Model")
        ax.tick_params(axis="x", rotation=25)
        for idx, value in enumerate(values):
            ax.text(idx, value, f"{value:.3f}", ha="center", va="bottom", fontsize=8)

    fig.suptitle("Model Comparison Across Core Error Metrics")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_transfer_gain_heatmap(rows: list[dict[str, str]], output_path: Path) -> None:
    history_vals = sorted({float(r["target_history_fraction"]) for r in rows})
    lambda_vals = sorted({float(r["transfer_lambda"]) for r in rows})

    value_grid: list[list[float]] = []
    for h in history_vals:
        line: list[float] = []
        for lam in lambda_vals:
            match = next(
                r
                for r in rows
                if float(r["target_history_fraction"]) == h
                and float(r["transfer_lambda"]) == lam
            )
            gain = float(match["rmse_target_only"]) - float(match["rmse_transfer"])
            line.append(gain)
        value_grid.append(line)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    im = ax.imshow(value_grid, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(len(lambda_vals)))
    ax.set_yticks(range(len(history_vals)))
    ax.set_xticklabels([str(int(v)) if v.is_integer() else str(v) for v in lambda_vals])
    ax.set_yticklabels([str(v) for v in history_vals])
    ax.set_xlabel("Transfer lambda")
    ax.set_ylabel("Target history fraction")
    ax.set_title("RMSE Gain of Transfer vs Target-only")

    for i in range(len(history_vals)):
        for j in range(len(lambda_vals)):
            ax.text(j, i, f"{value_grid[i][j]:.4f}", ha="center", va="center", fontsize=8)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("RMSE gain (positive is better)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_coverage_width_tradeoff(rows: list[dict[str, str]], output_path: Path) -> None:
    models = [r["model"] for r in rows]
    coverages = [float(r["interval_coverage"]) for r in rows]
    widths = [float(r["interval_avg_width"]) for r in rows]
    pinballs = [float(r["pinball_loss"]) for r in rows]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for model, cov, width, pin in zip(models, coverages, widths, pinballs):
        ax.scatter(width, cov, s=120, alpha=0.85)
        ax.text(width, cov, f" {model}\n p={pin:.3f}", fontsize=8, va="bottom")

    ax.axhline(0.8, color="#dc2626", linestyle="--", linewidth=1.5, label="Target coverage = 0.8")
    ax.set_xlabel("Average interval width")
    ax.set_ylabel("Interval coverage")
    ax.set_title("Uncertainty Trade-off: Coverage vs Width")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    app()
