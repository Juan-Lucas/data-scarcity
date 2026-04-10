# Business Understanding (CRISP-DM - Phase 1)

## 1. Contexte métier

Le projet est ancre sur un cas d’usage unique: lancement de nouveau produit dans une chaine retail.

Au demarrage d’un lancement, l’historique du nouveau produit est quasi nul (quelques semaines), alors que les decisions d’achat fournisseur doivent etre prises immediatement.

Les consequences metier sont directes:
- rupture en rayon si la demande est sous-estimee,
- surstock et demarque si la demande est surestimee,
- immobilisation de tresorerie sur un produit encore incertain,
- degradation du taux de service lors des premieres semaines critiques.

L’idee est d’exploiter les donnees de produits similaires (source) pour ameliorer la prevision du nouveau produit (cible), via:
- transfert d’apprentissage (Transfer Learning),
- modelisation probabiliste (quantification de l’incertitude).

## 2. Problème métier

Les modeles classiques de prevision de demande supposent un historique suffisamment long. Dans un lancement de nouveau produit, cette hypothese est violee.

Le probleme metier a resoudre est:
- fournir des previsions exploitables avec tres peu d’observations,
- estimer explicitement l’incertitude (intervalle/quantiles),
- transformer cette incertitude en decisions de stock prudentes et actionnables.

Le besoin prioritaire n’est pas seulement d’avoir une prediction ponctuelle, mais d’aider a decider le niveau de stock initial et son ajustement hebdomadaire pendant les 8 a 12 premieres semaines.

## 3. Objectifs métier

### 3.1 Objectif principal

Ameliorer la qualite des decisions de stock et d’approvisionnement pour un nouveau produit en phase de lancement, malgre un historique limite.

### 3.2 Objectifs spécifiques

- Concevoir une approche adaptee au regime low-data des premieres semaines de vie produit.
- Reduire l’erreur de prevision vs baseline non transferee.
- Produire des previsions probabilistes (quantiles/intervalle) utilisables pour definir un stock de securite.
- Demontrer la pertinence sur un protocole reproductible de type M5: produit cible sous-echantillonne simulant un lancement.

## 4. Critères de succès métier

Les criteres de succes metier pour la premiere iteration sont:

- Reduction mesurable de l’erreur de prevision vs baseline sur la fenetre de lancement.
- Baisse du risque de rupture pendant les premieres semaines.
- Baisse du surstock moyen et de la demarque associee.
- Regles de decision claires pour profils metier non experts IA (ex: quantile 0.8 pour reappro prudent).

## 5. Critères de succès data science (liés au métier)

- Performance superieure a une baseline non transferee (MAE, RMSE, ou WAPE selon setup).
- Bonne calibration probabiliste (couverture des intervalles proche du niveau nominal).
- Stabilite lorsque le nombre de points cibles est fortement reduit.
- Reproductibilite complete (pipeline, seeds, protocole de sous-echantillonnage).

## 6. Périmètre du projet

### Inclus

- Prevision de demande d’un nouveau produit sur horizon court (lancement).
- Transfert de connaissances depuis produits/categories similaires vers produit cible.
- Estimation d’incertitude pour piloter stock de securite et niveau de service.
- Evaluation comparative baseline vs transfert vs transfert probabiliste.
- Reproduction experimentale sur M5 avec sous-echantillonnage controle du produit cible.

### Exclu (phase actuelle)

- Deploiement temps reel en production.
- Optimisation end-to-end de tout le reseau multi-echelon.
- Integration operationnelle ERP/WMS.
- Pricing, promotion planning, et contraintes marketing avancees.

## 7. Hypothèses de travail

- Des series de produits similaires contiennent des patterns transferables utiles au nouveau produit.
- Le transfert reduit l’erreur plus vite qu’un apprentissage uniquement sur le faible historique cible.
- La quantification d’incertitude ameliore la decision de stock vs prediction ponctuelle seule.
- Le protocole de sous-echantillonnage M5 approxime de facon acceptable un contexte de lancement reel.

## 8. Contraintes

- Historique cible tres court, potentiellement bruite et non stationnaire.
- Risque d’ecart de distribution entre produits source et produit cible.
- Budget de calcul limite (cadre academique, prototypage rapide).
- Contraintes de publication workshop: anonymat, 6 pages, reproductibilite et clarte.

## 9. Risques et plans de mitigation

- Risque: transfert negatif (produits source trop differents du produit lance).
  - Mitigation: selection de groupes source par similarite + ablations + comparaison stricte a baseline.

- Risque: overfitting sur les premieres semaines du produit cible.
  - Mitigation: validation temporelle, regularisation, early stopping, modeles plus simples en reference.

- Risque: incertitude mal calibree donc decisions de stock trompeuses.
  - Mitigation: evaluation de calibration (coverage, interval score) et recalibration si necessaire.

- Risque: protocole de simulation trop eloigne du reel.
  - Mitigation: multiplier les scenarios de sous-echantillonnage (fenetre courte, bruit, chocs) et rapporter robustesse.

## 10. Parties prenantes

- Equipe projet (modelisation, experimentation, redaction).
- Encadrant(s) academique(s).
- Role metier simule: demand planner / approvisionneur retail.
- Communaute workshop AI2M4RI.

## 11. Valeur attendue

- Cadre replicable pour prevoir un nouveau produit avec peu de donnees.
- Reduction conjointe du risque de rupture et du surstock au lancement.
- Contribution scientifique sur transfer learning probabiliste en contexte data-scarce.

## 12. Livrables de la phase Business Understanding

- Formulation du cas d’usage cible: lancement nouveau produit retail.
- Definition des KPI metier (rupture, surstock, niveau de service) et data science (erreur, calibration).
- Hypotheses et risques relies explicitement au transfert et a l’incertitude.
- Protocole d’evaluation preliminaire sur M5 sous-echantillonne.

## 13. Décision de passage à la phase suivante (Data Understanding)

Le passage en phase 2 CRISP-DM est validé si:
- le cas d’usage lancement est formule de maniere non ambigue,
- les KPI metier et data science sont mesurables et relies aux decisions,
- le protocole de simulation low-data sur M5 est defini,
- les risques critiques (transfert negatif, calibration, overfitting) ont un plan de mitigation testable.
