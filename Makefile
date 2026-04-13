PROJECT_NAME = data-scarcity
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python

.PHONY: requirements clean lint format test create_environment \
	dataset features train predict compare_models run_experiment plot pipeline help

requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

clean:
	$(PYTHON_INTERPRETER) -c "import pathlib, shutil; p=pathlib.Path('.'); [f.unlink() for f in p.rglob('*.pyc') if f.exists()]; [f.unlink() for f in p.rglob('*.pyo') if f.exists()]; [shutil.rmtree(d, ignore_errors=True) for d in p.rglob('__pycache__')]"

lint:
	ruff check .
	black --check .

format:
	ruff check . --fix
	black .

test:
	$(PYTHON_INTERPRETER) -m pytest tests

create_environment:
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> conda env created. Activate with: conda activate $(PROJECT_NAME)"

dataset: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.dataset --input-path data/raw/m5/sales_train_validation.csv --max-series 250 --max-days 365

features: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.features --lag-count 7 --target-test-fraction 0.3

train: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.modeling.train --transfer-lambda 10 --ridge-lambda 0.001 --quantiles "0.1,0.5,0.9"

predict: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.modeling.predict --features-path data/processed/target_test_features.csv --alpha 0.1

compare_models: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.modeling.compare_models --quantiles "0.1,0.5,0.9" --ridge-alpha 0.001 --transfer-lambda 10

run_experiment: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.modeling.run_experiment --sales-input-path data/raw/m5/sales_train_validation.csv --history-grid "0.1,0.2,0.3" --lambda-grid "1,10,50" --lag-count 7 --target-test-fraction 0.3 --quantiles "0.1,0.5,0.9" --alpha 0.1 --max-series 250 --max-days 365

plot: requirements
	cmd /c cls
	$(PYTHON_INTERPRETER) -m data_scarcity.plots --features-path data/processed/target_test_features.csv --predictions-path data/processed/model_comparison_predictions.csv --output-path reports/figures/test_series_confidence_band.png --model-name ridge_transfer

pipeline: dataset features train predict
	@echo "Pipeline standard termine."

help:
	@echo "Commandes disponibles :"
	@echo "  make requirements     # Installer les dependances Python"
	@echo "  make dataset          # Construire source/target (low-data)"
	@echo "  make features         # Generer les features et split temporel"
	@echo "  make train            # Entrainer baseline/target/transfer"
	@echo "  make predict          # Predire et evaluer"
	@echo "  make compare_models   # Comparer plusieurs modeles"
	@echo "  make run_experiment   # Lancer la grille d'experiences"
	@echo "  make plot             # Generer la figure de confiance"
	@echo "  make pipeline         # Enchainement dataset -> features -> train -> predict"
	@echo "  make lint             # Verifier Ruff + Black"
	@echo "  make format           # Corriger format/lint automatiquement"
	@echo "  make test             # Lancer les tests"
	@echo "  make clean            # Supprimer caches Python"
