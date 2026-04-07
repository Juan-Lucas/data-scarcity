# Business Understanding (CRISP-DM - Phase 1)

## 1. Contexte métier

Ce projet vise l’optimisation de la supply chain dans des contextes contraints en données (PME, nouveaux produits, marchés émergents).

Dans ces contextes, les décisions de stock et d’approvisionnement sont souvent prises avec peu d’historique fiable, ce qui augmente:
- le risque de rupture,
- le surstock,
- les coûts opérationnels,
- l’incertitude dans la planification.

Le projet propose une approche hybride combinant:
- le transfert d’apprentissage (Transfer Learning),
- la modélisation probabiliste (quantification de l’incertitude).

## 2. Problème métier

Les approches classiques de prévision de demande demandent généralement des volumes de données importants. Lorsque les données sont rares, ces modèles sur-apprennent et produisent des prédictions fragiles.

Le besoin métier est de fournir des prévisions exploitables même en faible volume de données, avec une estimation explicite du niveau de confiance pour améliorer les décisions de stock.

## 3. Objectifs métier

### 3.1 Objectif principal

Améliorer la qualité des décisions supply chain (stock, approvisionnement, planification) dans les environnements data-scarce.

### 3.2 Objectifs spécifiques

- Concevoir une approche de prévision adaptée aux faibles volumes de données.
- Réduire les erreurs de prévision par rapport à une baseline classique.
- Produire des sorties probabilistes (intervalles/quantiles) pour piloter le risque.
- Démontrer la valeur de l’approche sur un scénario réaliste de PME ou de marché émergent.

## 4. Critères de succès métier

Les critères de succès métier pour la première itération sont:

- Réduction mesurable de l’erreur de prévision versus baseline.
- Amélioration de la robustesse des décisions en présence d’incertitude.
- Capacité à prioriser des décisions prudentes quand l’incertitude augmente.
- Clarté des résultats pour une interprétation par des profils non experts IA.

## 5. Critères de succès data science (liés au métier)

- Performance supérieure à une baseline simple (ex: modèle classique non transféré).
- Qualité de calibration des prédictions probabilistes.
- Stabilité du modèle quand la taille du dataset cible est très faible.
- Reproductibilité des résultats (pipeline, paramètres, protocoles).

## 6. Périmètre du projet

### Inclus

- Prévision de demande sur jeux de données retail/supply chain.
- Scénario de transfert: grand dataset source vers petit dataset cible.
- Estimation de l’incertitude via approche probabiliste.
- Comparaison avec baseline.

### Exclu (phase actuelle)

- Déploiement production temps réel.
- Optimisation multi-échelons complète de bout en bout.
- Intégration ERP/WMS opérationnelle.

## 7. Hypothèses de travail

- Un dataset source plus large peut transférer une information utile vers le dataset cible.
- Le dataset cible représente un contexte local pertinent mais faible en volume.
- La quantification d’incertitude apporte une valeur décisionnelle supérieure à une simple prédiction ponctuelle.

## 8. Contraintes

- Données limitées et potentiellement bruitées.
- Hétérogénéité entre domaine source et domaine cible.
- Temps et ressources de calcul raisonnables (cadre académique/prototypage).
- Exigence de lisibilité scientifique pour article workshop.

## 9. Risques et plans de mitigation

- Risque: transfert négatif (source trop différente du cible).
  - Mitigation: tester plusieurs stratégies de fine-tuning et comparer à baseline.

- Risque: overfitting sur le petit dataset cible.
  - Mitigation: validation stricte, régularisation, early stopping, simplification modèle.

- Risque: incertitude mal calibrée.
  - Mitigation: évaluer calibration (couverture d’intervalles, métriques dédiées).

- Risque: dataset cible insuffisant pour conclure.
  - Mitigation: protocoles de sous-échantillonnage contrôlés et analyse de sensibilité.

## 10. Parties prenantes

- Équipe projet (modélisation, expérimentation, rédaction).
- Encadrant(s) académique(s).
- Communauté workshop AI2M4RI.
- Cible d’impact: PME et organisations opérant en contexte data-scarce.

## 11. Valeur attendue

- Méthodologie réplicable pour contextes à faibles ressources.
- Meilleure prise de décision sous incertitude.
- Contribution scientifique appliquée au thème AI + méthodes mathématiques à impact réel.

## 12. Livrables de la phase Business Understanding

- Définition claire du problème métier et des objectifs.
- Critères de succès métier et data science.
- Périmètre, hypothèses, contraintes, risques.
- Cadre d’évaluation orienté impact opérationnel.

## 13. Décision de passage à la phase suivante (Data Understanding)

Le passage en phase 2 CRISP-DM est validé si:
- le problème métier est correctement formulé,
- les critères de succès sont mesurables,
- le périmètre est clair,
- les risques principaux sont identifiés avec un plan de mitigation.
