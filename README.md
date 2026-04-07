# Supply Chain Optimization under Data Scarcity

Projet de recherche sur l’optimisation de la supply chain dans des contextes où les données historiques sont rares, par exemple pour des PME, des marchés émergents ou le lancement d’un nouveau produit.

L’approche combine deux briques principales:

- `Transfer Learning` pour réutiliser un modèle pré-entraîné sur un grand jeu de données source.
- `Probabilistic Modeling` pour quantifier l’incertitude et produire des décisions prudentes quand l’historique est limité.

## Pourquoi ce sujet

Le problème central est la rareté des données. Dans ce contexte, les modèles classiques sur-apprennent vite et généralisent mal. L’objectif du projet est donc de montrer qu’un modèle hybride, adapté à peu de données, peut mieux soutenir des décisions de prévision de demande, de stock et d’approvisionnement.

Ce sujet est bien aligné avec le workshop `AI & Mathematical Methods for Real-world Impact`, car il vise explicitement des environnements à ressources et données limitées.

## Idée méthodologique

- `Source domain`: grand dataset logistique ou de demande, utilisé pour apprendre des représentations générales.
- `Target domain`: petit dataset local ou réduit, utilisé pour simuler la rareté des données.
- `Côté maths`: cadre bayésien ou autre modèle probabiliste pour estimer une distribution de sortie plutôt qu’une valeur unique.

## Datasets à explorer

Pistes utiles pour démarrer:

- Jeux de données de demande ou de ventes retail sur Kaggle ou UCI.
- `M5 Forecasting - Walmart` comme grand dataset source pour simuler le transfert d’apprentissage.
- Un petit dataset local ou un sous-échantillon pour reproduire le cas `data-scarce`.

Mots-clés de recherche:

- `demand forecasting small dataset`
- `supply chain inventory data sparse`
- `transfer learning for time series forecasting`

## Structure visée de l’article

Le template AI2M4RI suit une structure simple: `Front matter`, `Main Text`, `Acknowledgements`, `Appendix`, puis `References`.

Pour cet article, la trame utile est la suivante:

1. `Title`, auteurs, affiliations, abstract et keywords.
2. `Main Text` avec:
	- `Introduction`
	- `Structure` ou contexte du problème
	- `Tables` si nécessaire pour résumer les données ou résultats
	- `Figures/Illustrations` pour les schémas du pipeline
	- `Equations` pour le cadre probabiliste
	- `Section headings` pour organiser la méthodologie et les expériences
3. `Acknowledgements` pour remercier les contributeurs ou sources de données.
4. `Appendix` si des détails techniques ou supplémentaires doivent être ajoutés.
5. `References` au format numérique du template.

## Organisation du dépôt

```text
data/
data_scarcity/
docs/
models/
notebooks/
reports/
tests/
```
