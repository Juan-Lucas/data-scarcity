# Plan de rédaction et méthodologie CRISP-DM

Ce document sert de feuille de route pour l’article et pour le projet complet. Il combine:
- les règles de soumission AI2M4RI / EasyChair,
- la structure imposée par le template Procedia Computer Science,
- la méthodologie CRISP-DM,
- la répartition des tâches du Trello.

## 1. Cadre général

Le projet traite de l’optimisation de la supply chain pour un cas précis: lancement de nouveau produit retail avec historique très court.

L’idée centrale est de comparer:
- une approche classique sans transfert,
- une approche hybride combinant Transfer Learning et modélisation probabiliste.

Le scénario expérimental de référence repose sur M5 avec sous-échantillonnage contrôlé pour simuler les premières semaines de vie d’un nouveau produit.

Le manuscrit final doit rester court, clair, anonyme à la soumission initiale, et tenir dans la limite de 6 pages, références comprises.

## 1.1 Structure du dépôt (fichiers utiles)

- `reports/AI2M4RI_PROCS_Template/AI2M4RI_PROCS_Template.tex` : fichier principal de rédaction de l’article.
- `docs/business_understanding_crisp_dm.md` : cadrage métier (phase 1 CRISP-DM).
- `docs/glossaire.md` : terminologie et cohérence des notations.
- `notebooks/` et `data_scarcity/` : expérimentations et implémentation.

## 2. Contraintes de rédaction imposées par EasyChair

Les règles principales à respecter sont:
- format Procedia Computer Science (Elsevier),
- soumission initiale anonyme: pas de noms d’auteurs ni d’affiliations,
- PDF obligatoire pour la soumission,
- longueur maximale: 6 pages, figures, tableaux et références inclus,
- dépôt avant la date limite EasyChair,
- version finale enrichie des noms et affiliations seulement après acceptation.

## 3. Structure de l’article

Le papier suivra la structure suivante:

1. `Front matter`
   - titre,
   - résumé,
   - mots-clés,
   - sans auteurs ni affiliations pour la première soumission.

2. `Main Text`
   - introduction,
   - état de l’art,
   - méthodologie,
   - expérimentation,
   - résultats et discussion.

3. `Acknowledgements`
   - uniquement dans la version finale si nécessaire.

4. `Appendix`
   - seulement si des détails complémentaires doivent être ajoutés.

5. `References`
   - bibliographie au style attendu par le template.

## 3.1 Règles de rédaction conformes au template AI2M4RI_PROCS_Template.tex

- Écrire le manuscrit directement dans `reports/AI2M4RI_PROCS_Template/AI2M4RI_PROCS_Template.tex`.
- Compiler avec PDFLaTeX en priorité.
- Ne pas modifier la mise en forme du template (styles, marges, logique du document).
- Conserver le format de soumission anonyme pour la version EasyChair.
- Respecter strictement la limite de 6 pages, références et figures incluses.
- Intégrer les tableaux et figures dans le texte avec légendes conformes.
- Vérifier la cohérence citations <-> bibliographie avant export PDF.

## 3.2 Structure détaillée recommandée pour cet article

1. `Front matter`
   - titre,
   - version anonyme à la soumission,
   - résumé,
   - mots-clés.

2. `Main Text`
   - Introduction (problème métier et contributions),
   - Related Work,
   - Mathematical Framework,
   - Proposed Architecture / Methodology,
   - Experimental Setup,
   - Results and Discussion,
   - Conclusion.

3. `Acknowledgements`
   - en version finale uniquement si nécessaire.

4. `References`
   - style conforme au template.

5. `Appendix`
   - seulement si indispensable.

## 4. Méthodologie CRISP-DM

### 4.1 Business Understanding

But: définir le problème métier, les objectifs et les critères de succès.

À faire:
- expliquer le cas de lancement de nouveau produit et son historique limité,
- définir le besoin de prévision sous incertitude sur les 8 à 12 premières semaines,
- préciser les risques métier: rupture, surstock, niveau de service, décision imprécise,
- fixer les critères de succès métier et scientifique.

Livrables:
- cadrage du projet,
- objectifs,
- hypothèses,
- contraintes,
- risques.

### 4.2 Data Understanding

But: explorer les données source et cible.

À faire:
- sélectionner un grand dataset source,
- sélectionner ou construire un petit dataset cible simulant un produit nouvellement lancé,
- examiner les variables et la qualité des données,
- vérifier les écarts entre domaine source et domaine cible.

Livrables:
- description des datasets,
- diagnostic qualité,
- premiers constats sur la faisabilité du transfert.

### 4.3 Data Preparation

But: préparer les données pour l’entraînement.

À faire:
- nettoyage,
- sélection des variables utiles,
- création des sous-ensembles de faible taille (fenêtres de démarrage produit),
- séparation train / validation / test,
- préparation du pipeline de transformation.

Livrables:
- datasets prêts à l’emploi,
- scripts ou notebooks de préparation,
- pipeline reproductible.

### 4.4 Modeling

But: entraîner et comparer les modèles.

À faire:
- entraîner un modèle source,
- transférer l’apprentissage vers le petit dataset,
- ajouter une couche probabiliste ou un cadre bayésien,
- construire une baseline sans transfert,
- comparer les performances.

Livrables:
- baseline,
- modèle transféré,
- modèle probabiliste,
- métriques de comparaison.

### 4.5 Evaluation

But: valider la pertinence du modèle proposé.

À faire:
- comparer les erreurs,
- analyser l’impact du faible volume de données,
- vérifier la robustesse,
- évaluer la calibration des intervalles probabilistes,
- relier les résultats aux KPI métier (rupture, surstock, niveau de service),
- interpréter les résultats sous l’angle métier.

Livrables:
- tableaux de résultats,
- figures,
- interprétation technique et métier.

### 4.6 Deployment

But: préparer la soumission et la version finale.

À faire:
- intégrer le contenu dans le template LaTeX,
- vérifier l’anonymat,
- contrôler la longueur du papier,
- vérifier les références,
- générer le PDF final,
- soumettre sur EasyChair.

Livrables:
- article final,
- PDF anonyme,
- version prête pour soumission.

## 5. Plan de travail relié au Trello

### Phase 1 - Cadrage & bibliographie

Objectif: définir le sujet et la base théorique.

Cartes associées:
- `Section 1 - Introduction`
- `Section 2 - Related Work (État de l'art)`
- `Formalisation Mathématique`
- `Nomenclature & Glossaire`
- `Recherche de Datasets`

### Phase 2 - Développement & expérimentation

Objectif: construire le modèle et les expériences.

Cartes associées:
- `Entraînement du Modèle Source`
- `Adaptation au Small Data`
- `Implémentation Transfer Learning`
- `Diagramme d'Architecture`
- `Tests de performance :`
- `Génération des Figures (Format PNG/PDF)`

### Phase 3 - Rédaction

Objectif: rédiger l’article dans le template.

Cartes associées:
- `Section 1 - Introduction`
- `Section 2 - Related Work (État de l'art)`
- `Section 3 - Mathematical Framework`
- `Section 4 - Proposed Architecture`
- `Section 5 - Results & Discussion`
- `Section Contexte Supply Chain`

### Phase 4 - Revue & soumission

Objectif: finaliser le papier et soumettre.

Cartes associées:
- `Check "Anonymous Submission"`
- `Vérification du format Vancouver`
- `Vérification de la limite de 6 pages`
- `Correction Anglais / Plagiat`
- `Relecture Prof. Merlec`
- `Soumission EasyChair`
- `Upload EasyChair.`
- `Génération du PDF Final Anonyme`

## 6. Répartition des livrables par étape

- **CRISP-DM 1**: problème métier lancement produit, objectifs, contraintes, risques.
- **CRISP-DM 2**: datasets source/cible, qualité des données, faisabilité transfert.
- **CRISP-DM 3**: nettoyage, préparation, sous-échantillonnage des premières semaines.
- **CRISP-DM 4**: baseline, transfert, modèle probabiliste.
- **CRISP-DM 5**: résultats, discussion, calibration, impact rupture/surstock/service.
- **CRISP-DM 6**: mise en forme finale et soumission.

## 7. Ordre recommandé de rédaction

1. Finaliser le cadrage métier.
2. Valider les datasets.
3. Produire les expériences et figures.
4. Rédiger l’introduction et l’état de l’art.
5. Rédiger la méthodologie.
6. Rédiger résultats et discussion.
7. Vérifier anonymat, longueur et références.
8. Générer et soumettre le PDF.

## 8. Résultat attendu

À la fin du projet, le dépôt doit contenir:
- le template de l’article rempli,
- les scripts ou notebooks de préparation et d’entraînement,
- les figures finales,
- les documents de cadrage CRISP-DM,
- le PDF final prêt pour EasyChair.

## 9. Checklist finale avant soumission

- PDF final en 6 pages maximum (références et figures incluses).
- Version anonyme pour EasyChair (pas de noms d’auteurs/affiliations).
- Figures et tableaux lisibles, légendes conformes, insertion dans le texte.
- Toutes les citations du texte présentes dans la bibliographie.
- Compilation LaTeX sans erreur bloquante.
