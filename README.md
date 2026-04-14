# Data Scarcity - Transfer Learning & Probabilistic Modeling for Demand Forecasting

Ce projet met en place un pipeline reproductible pour la prevision de demande en contexte de data scarcity (cold-start produit), avec transfer learning et modelisation probabiliste.

Le workflow couvre la preparation des donnees, l'entrainement des modeles, l'evaluation probabiliste, la comparaison inter-modeles, puis la generation des artefacts pour l'article AI2M4RI.

## Architecture globale

```text
┌────────────────────────────────────────────────────────────────────────────┐
│            Pipeline Data Scarcity (Forecasting / AI2M4RI)                 │
│                                                                            │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Construction source/target (dataset.py)                   │            │
│  │ data/raw -> data/processed/source_dataset.csv             │            │
│  │           -> data/processed/target_dataset.csv            │            │
│  └────────────────────────────────────────────────────────────┘            │
│         ↓                                                                  │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Feature engineering (features.py)                         │            │
│  │ lag features + split temporel train/test                  │            │
│  └────────────────────────────────────────────────────────────┘            │
│         ↓                                                                  │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Training (modeling/train.py)                              │            │
│  │ baseline + target_only + transfer + quantiles             │            │
│  └────────────────────────────────────────────────────────────┘            │
│         ↓                                                                  │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Inference & metrics (modeling/predict.py)                 │            │
│  │ MAE/RMSE + pinball + coverage + interval width            │            │
│  └────────────────────────────────────────────────────────────┘            │
│         ↓                                                                  │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Comparaison modeles (modeling/compare_models.py)          │            │
│  │ Ridge vs Random Forest vs Gradient Boosting               │            │
│  └────────────────────────────────────────────────────────────┘            │
│         ↓                                                                  │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Figure article (plots.py)                                 │            │
│  │ bande de confiance 10%-90% -> reports/figures             │            │
│  └────────────────────────────────────────────────────────────┘            │
└────────────────────────────────────────────────────────────────────────────┘
```

## Installation et utilisation

### Prerequis
- Python 3.11
- pip

### Installation
```bash
git clone https://github.com/Juan-Lucas/data-scarcity.git
cd data-scarcity
pip install -r requirements.txt
```

### Execution du pipeline complet (commandes Python)

```bash
# 1) Construire source/target low-data
python -m data_scarcity.dataset --input-path data/raw/m5/sales_train_validation.csv --max-series 250 --max-days 365

# 2) Generer les features + split temporel
python -m data_scarcity.features --lag-count 7 --target-test-fraction 0.3

# 3) Entrainer les modeles
python -m data_scarcity.modeling.train --transfer-lambda 10 --ridge-lambda 0.001 --quantiles "0.1,0.5,0.9"

# 4) Predire et evaluer
python -m data_scarcity.modeling.predict --features-path data/processed/target_test_features.csv --alpha 0.1

# 5) Comparer plusieurs modeles
python -m data_scarcity.modeling.compare_models --quantiles "0.1,0.5,0.9" --ridge-alpha 0.001 --transfer-lambda 10

# 6) Generer la figure de confiance pour l'article
python -m data_scarcity.plots --features-path data/processed/target_test_features.csv --predictions-path data/processed/model_comparison_predictions.csv --output-path reports/figures/test_series_confidence_band.png --model-name ridge_transfer
```

### Execution du pipeline complet (via Makefile)

```bash
# Installation des dependances
make requirements

# Pipeline standard: dataset -> features -> train -> predict
make pipeline

# Etapes complementaires
make compare_models
make plot
make metrics_plots

# Variante grille d'experiences
make run_experiment
```

### Utilisation du Makefile (optionnel)

```bash
make requirements    # Installer les dependances
make dataset         # Construire source/target low-data
make features        # Generer les features et split temporel
make train           # Entrainer baseline/target/transfer
make predict         # Predire et evaluer
make compare_models  # Comparer plusieurs modeles
make run_experiment  # Lancer la grille d'experiences
make plot            # Generer la figure de confiance
make metrics_plots   # Generer 3 graphiques de metriques
make pipeline        # Enchainement standard du pipeline
make lint            # Verifier le style
make format          # Formatter le code
make test            # Lancer les tests
make clean           # Supprimer caches Python
```

Voir `make help` pour la liste complete des cibles.

## Sorties principales

- `data/processed/source_dataset.csv`
- `data/processed/target_dataset.csv`
- `data/processed/source_features.csv`
- `data/processed/target_train_features.csv`
- `data/processed/target_test_features.csv`
- `data/processed/test_predictions.csv`
- `data/processed/test_metrics.json`
- `data/processed/model_comparison_results.csv`
- `data/processed/model_comparison_predictions.csv`
- `reports/figures/test_series_confidence_band.png`
- `reports/figures/model_metrics_bars.png`
- `reports/figures/transfer_gain_heatmap.png`
- `reports/figures/coverage_width_tradeoff.png`
- `reports/AI2M4RI_PROCS_Template/AI2M4RI_PROCS_Template.tex`

## Organisation du projet

```text
data/
  raw/
  interim/
  processed/
data_scarcity/
  modeling/
docs/
models/
notebooks/
references/
reports/
tests/
```

## Auteur

Jean-Luc Mupasa Kalunga, 
Lucianne Kalubi, 
Ulysse Mwanza

## Licence

Projet sous licence MIT. Voir `LICENSE`.
