# Commandes a taper

Ce fichier regroupe les commandes utiles pour executer le pipeline Experimental Setup.

## 1) Se placer a la racine du projet

```bash
cd c:/Devs/python/Researchs/Article_2/data-scarcity
```

## 2) Installer les dependances

```bash
pip install -r requirements.txt
```

## 3) Pipeline complet (ordre recommande)

### Etape A - Construire source/target low-data

```bash
python -m data_scarcity.dataset --input-path data/raw/m5/sales_train_validation.csv --max-series 250 --max-days 365
```

### Etape B - Generer les features et split temporel target train/test

```bash
python -m data_scarcity.features --lag-count 7 --target-test-fraction 0.3
```

### Etape C - Entrainer baseline + target_only + transfer + quantiles

```bash
python -m data_scarcity.modeling.train --transfer-lambda 10 --ridge-lambda 0.001 --quantiles "0.1,0.5,0.9"
```

### Etape D - Predire et evaluer

```bash
python -m data_scarcity.modeling.predict --features-path data/processed/target_test_features.csv --alpha 0.1
```

## 4) Verifier les sorties

```bash
ls data/processed
ls models
```

Fichiers attendus:

- data/processed/source_dataset.csv
- data/processed/target_dataset.csv
- data/processed/experimental_setup_metadata.json
- data/processed/source_features.csv
- data/processed/target_train_features.csv
- data/processed/target_test_features.csv
- data/processed/test_predictions.csv
- data/processed/test_metrics.json
- data/processed/article_results_single_run.csv
- models/experimental_model.json

## 5) Lancer avec un autre niveau de rarete

Exemple: garder seulement 15% d'historique sur la cible.

```bash
python -m data_scarcity.dataset --input-path data/raw/m5/sales_train_validation.csv --target-history-fraction 0.15 --max-series 250 --max-days 365
python -m data_scarcity.features --lag-count 7 --target-test-fraction 0.3
python -m data_scarcity.modeling.train --transfer-lambda 10 --ridge-lambda 0.001 --quantiles "0.1,0.5,0.9"
python -m data_scarcity.modeling.predict --features-path data/processed/target_test_features.csv --alpha 0.1
```

## 6) Variante quantiles

```bash
python -m data_scarcity.modeling.train --transfer-lambda 10 --quantiles "0.05,0.1,0.5,0.9,0.95"
```

## 7) Debug rapide

### Voir les metriques

```bash
cat data/processed/test_metrics.json
```

### Voir quelques predictions

```bash
python -c "import csv; p='data/processed/test_predictions.csv'; r=list(csv.DictReader(open(p, encoding='utf-8'))); print('rows=', len(r)); print(r[:3])"
```

## 8) Commande unique pour produire un tableau de resultats article

Cette commande lance une grille d'experiences (plusieurs niveaux de rarete et de regularisation) et genere un CSV comparatif pret a inserer dans l'article.

```bash
python -m data_scarcity.modeling.run_experiment --sales-input-path data/raw/m5/sales_train_validation.csv --history-grid "0.1,0.2,0.3" --lambda-grid "1,10,50" --lag-count 7 --target-test-fraction 0.3 --quantiles "0.1,0.5,0.9" --alpha 0.1 --max-series 250 --max-days 365
```

Sortie principale:

- data/processed/experiment_results_grid.csv

## 9) Comparer plusieurs modeles (Ridge vs Random Forest vs Gradient Boosting)

Cette commande compare directement un modele lineaire, un modele random forest et un modele de gradient boosting sur la meme base de test.

```bash
python -m data_scarcity.modeling.compare_models --quantiles "0.1,0.5,0.9" --ridge-alpha 0.001 --transfer-lambda 10
```

Sorties principales:

- data/processed/model_comparison_results.csv
- data/processed/model_comparison_predictions.csv

## 10) Generer la figure de confiance pour l'article

Cette commande trace une serie test reelle avec la bande de confiance 10%-90% et enregistre l'image dans le dossier des figures.

```bash
python -m data_scarcity.plots --features-path data/processed/target_test_features.csv --predictions-path data/processed/model_comparison_predictions.csv --output-path reports/figures/test_series_confidence_band.png --model-name ridge_transfer
```

Sortie principale:

- reports/figures/test_series_confidence_band.png
