# Plan du projet et méthodologie CRISP-DM

## 1. Objectif du projet

Ce projet vise à optimiser la supply chain dans un contexte de lancement de nouveau produit retail avec peu d’historique, en combinant:
- le Transfer Learning pour réutiliser les connaissances d’un modèle entraîné sur un grand jeu de données,
- la modélisation probabiliste pour représenter l’incertitude et prendre des décisions plus prudentes.

Le but final est de produire un article scientifique court, structuré selon le template AI2M4RI / Procedia Computer Science, avec une expérimentation crédible sur un cas de lancement (simulation low-data sur M5).

## 2. Structure du projet

Le dépôt suit une organisation de type data science project:

- `data/` : données brutes, intermédiaires, traitées et externes.
- `data_scarcity/` : code Python du projet.
- `docs/` : documents de cadrage, de suivi et de méthodologie.
- `models/` : modèles entraînés et artefacts de prédiction.
- `notebooks/` : exploration, préparation, entraînement et analyse.
- `reports/` : template LaTeX, figures et livrables de rédaction.
- `tests/` : tests automatiques et vérifications minimales.

## 3. Méthodologie CRISP-DM

Le projet suit les 6 étapes CRISP-DM. Pour chaque phase, on précise l’objectif, les actions prévues et les livrables attendus.

### 3.1 Business Understanding

Objectif: comprendre le problème métier et définir ce que le projet doit résoudre.

Actions prévues:
- Décrire le problème du lancement de nouveau produit avec historique très court.
- Clarifier les impacts métier: rupture de stock, surstock, coûts, niveau de service, incertitude.
- Définir les objectifs scientifiques et opérationnels.
- Identifier les critères de succès et les contraintes.

Livrables:
- cadrage du problème,
- objectifs métier,
- hypothèses,
- critères de succès,
- risques principaux.

Correspondance Trello:
- `Section 1 - Introduction`
- `Section Contexte Supply Chain`
- `Check "Anonymous Submission"`
- `Vérification du format Vancouver`
- `Nomenclature & Glossaire`

### 3.2 Data Understanding

Objectif: comprendre les données disponibles, leur qualité et leur pertinence.

Actions prévues:
- Identifier un grand dataset source et un petit dataset cible.
- Explorer les variables, la structure temporelle et les manques de données.
- Vérifier la cohérence entre domaine source et domaine cible.
- Étudier la taille minimale de données utile pour les expériences de démarrage produit.

Livrables:
- inventaire des datasets,
- description des variables,
- premier diagnostic qualité,
- hypothèses sur le transfert entre domaines.

Correspondance Trello:
- `Recherche de Datasets`
- `Préparation du Dataset Scarce`
- `Dossier Drive`
- `Section 2 - Related Work (État de l'art)`

### 3.3 Data Preparation

Objectif: préparer les données pour l’entraînement et l’évaluation.

Actions prévues:
- Nettoyer les données.
- Construire des sous-ensembles expérimentaux de petite taille simulant les premières semaines d’un nouveau produit.
- Créer les variables nécessaires pour le modèle.
- Séparer correctement les jeux d’entraînement, validation et test.
- Préparer les entrées du modèle source et du modèle cible.

Livrables:
- datasets préparés,
- scripts ou notebooks de préparation,
- pipeline reproductible de transformation.

Correspondance Trello:
- `Préparation du Dataset Scarce`
- `Adaptation au Small Data`
- `Nomenclature & Glossaire`
- `Section Méthodologie`

### 3.4 Modeling

Objectif: construire les modèles et comparer les approches.

Actions prévues:
- Entraîner un modèle source sur un gros dataset.
- Appliquer le transfert d’apprentissage vers le petit dataset cible (nouveau produit).
- Ajouter une couche ou un cadre probabiliste pour quantifier l’incertitude.
- Construire une baseline classique sans transfert.
- Comparer les performances des approches.

Livrables:
- modèle source,
- modèle transféré,
- baseline,
- protocole expérimental,
- métriques de comparaison.

Correspondance Trello:
- `Entraînement du Modèle Source`
- `Implémentation Transfer Learning`
- `Adaptation au Small Data`
- `Formalisation Mathématique`
- `Section 3 - Mathematical Framework`
- `Diagramme d'Architecture`

### 3.5 Evaluation

Objectif: vérifier si la solution répond réellement au besoin métier et scientifique.

Actions prévues:
- Mesurer l’erreur de prévision.
- Comparer IA classique vs IA avec transfert + probabilités.
- Évaluer la robustesse sur peu de données.
- Analyser la calibration ou l’incertitude si applicable.
- Vérifier l’impact potentiel sur les décisions de stock (rupture, surstock, niveau de service).

Livrables:
- tableaux de résultats,
- figures de comparaison,
- analyse des performances,
- interprétation métier.

Correspondance Trello:
- `Tests de performance :`
- `Génération des Figures (Format PNG/PDF)`
- `Section 5 - Results & Discussion`
- `Résultats & Discussion (Équipe)`

### 3.6 Deployment

Objectif: rendre le projet publiable et partageable dans le cadre du workshop.

Actions prévues:
- Finaliser le papier au format AI2M4RI.
- Vérifier le format anonyme.
- Contrôler le respect de la limite de 6 pages.
- Vérifier les références au format Vancouver.
- Préparer la soumission sur EasyChair.

Livrables:
- PDF final anonyme,
- version prête pour soumission,
- dépôt GitHub propre,
- support Overleaf finalisé.

Correspondance Trello:
- `Setup Overleaf [URGENT]`
- `Vérification de la limite de 6 pages (Lucianne).`
- `Correction Anglais / Plagiat (Jean-Luc).`
- `Relecture Prof. Merlec (Lui envoyer le lien pour validation finale).`
- `Check "Anonymous Submission"`
- `Soumission EasyChair`
- `Upload EasyChair.`
- `Génération du PDF Final Anonyme (Sans les noms des auteurs selon le CFP).`

## 4. Répartition générale des travaux

### Phase 1: cadrage et bibliographie

- définir le problème,
- lire et résumer les articles clés,
- préciser les notations mathématiques,
- préparer le glossaire et la nomenclature.

### Phase 2: expérimentation

- préparer les données,
- entraîner le modèle source,
- simuler un scénario de lancement via sous-échantillonnage M5,
- implémenter le transfert et la couche probabiliste,
- produire les premières figures.

### Phase 3: rédaction

- rédiger l’introduction,
- rédiger l’état de l’art,
- écrire la méthodologie,
- présenter les résultats et discussion.

### Phase 4: revue et soumission

- vérifier le style du template,
- contrôler l’anonymat,
- corriger l’anglais,
- vérifier la bibliographie,
- générer le PDF final et soumettre.

## 5. Livrables attendus par phase

- **CRISP-DM 1 - Business Understanding**: cadrage du cas "lancement nouveau produit" et objectifs.
- **CRISP-DM 2 - Data Understanding**: inventaire source/cible et diagnostic pour simulation low-data.
- **CRISP-DM 3 - Data Preparation**: données nettoyées et sous-échantillonnage contrôlé des premières semaines.
- **CRISP-DM 4 - Modeling**: baseline, transfert et modèle probabiliste.
- **CRISP-DM 5 - Evaluation**: résultats, calibration, impact métier (rupture/surstock/service).
- **CRISP-DM 6 - Deployment**: article final et soumission.

## 6. Fichier de référence

Les éléments de rédaction et de mise en page s’appuient sur:
- le template AI2M4RI / Procedia Computer Science,
- le README principal du projet,
- le fichier de cadrage business understanding,
- le glossaire.

## 7. Conclusion

Ce document sert de feuille de route du projet. Il relie la structure du dépôt, les tâches du Trello et la logique CRISP-DM pour que chaque étape du travail soit claire, traçable et orientée vers la soumission finale.
