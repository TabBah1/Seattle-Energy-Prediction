## Présentation du Projet

La ville de Seattle s'est fixée un objectif ambitieux : **atteindre la neutralité carbone d'ici 2050**. 

Pour y parvenir, l'équipe municipale doit comprendre et optimiser la consommation énergétique des bâtiments non résidentiels (bureaux, hôpitaux, commerces, etc.).

### Problématique

Notre mission : **prédire la consommation d'énergie** des bâtiments pour lesquels les mesures n'ont pas encore été effectuées, en utilisant uniquement leurs caractéristiques structurelles.

### Données disponibles

- **Source** : Seattle Building Energy Benchmarking 2016
- **Année** : 2016
- **Type** : Bâtiments non résidentiels de Seattle
- **Variables** : Caractéristiques structurelles (taille, âge, usage) + Consommations énergétiques

### Technologies utilisées

- **Analyse de données** : Pandas, Numpy, Matplotlib, Seaborn
- **Machine Learning** : Scikit-Learn (SVR, GridSearchCV, Pipeline)
- **Déploiement API** : BentoML
- **Validation de données** : Pydantic

### Objectifs de ce notebook

1. **Analyse Exploratoire** : Comprendre la structure des données, traiter les valeurs manquantes et identifier les variables discriminantes.

2. **Energie & Corrélations** : Analyser la distribution de la variable cible et étudier les relations entre les caractéristiques physiques (surface, âge, usage) et la consommation

3. **Nettoyage & Feature Engineering** : Filtrage des outliers et Creation des variables pertinentes pour la modélisation , Transformation logarithmique des variables asymétriques pour stabiliser la variance, et Encodage des variables catégorielles

4. **Préparation des données pour la modélisation** : Standardisation des données et comparaison de modèles de référence (Régression Linéaire, SVR, Random Forest) via validation croisée.

5. **Optimisation du modele selectionné** : Recherche des meilleurs hyperparamètres pour le modèle SVR via GridSearchCV.

6. **Evaluation Finale et Analyse des résidus** : Vérification des performances sur le jeu de test et analyse de la distribution des erreurs pour valider la robustesse du modèle.

7. **Etude de l'Energy Star Score** : Évaluer l'apport de cette variable sur la précision du modèle et discuter de son coût d'obtention par rapport au gain de performance.

8. **Conclusion générale** : Synthèse des résultats et recommandations métier pour la ville de Seattle.

---

## Structure du Dépôt

```text
P6_SEATTLE_ENERGY/
├── api/
│   ├── __init__.py        # Package Python
│   ├── app.py             # Script de service BentoML
│   └── validation.py      # Schémas de données Pydantic
├── data/
│   └── 2016_Building_Energy_Benchmarking.csv  # Données brutes
├── notebook/
│   ├── Bah_Abdoulaye_notebook_012026.ipynb    # Analyse & Modélisation
│   ├── features_list.pkl  # Liste des colonnes utilisées
│   ├── model_svr_seattle.pkl   # Modèle SVR entraîné
│   └── scaler_seattle.pkl      # Scaler pour la normalisation
├── .gitignore             # Fichiers exclus de Git
├── bentofile.yaml         # Configuration du build BentoML
├── readme.md              # Documentation du projet
└── requirements.txt       # Dépendances Python
```
## Installation et Utilisation

1. Préparation de l'environnement:

Assurez-vous d'avoir Anaconda ou Miniconda installé.

#### Création de l'environnement
``` conda create -n p6_seattle python=3.10 -y 
    conda activate p6_seattle 
```

#### Installation des dépendances
``` pip install -r requirements.txt 
```

2. Entraînement et Analyse:

Le processus complet (Nettoyage, EDA, Feature Engineering et Modélisation) est détaillé dans le notebook : Bah_Abdoulaye_notebook_012026.ipynb

3. Déploiement de l'API (BentoML):

Pour construire et lancer l'API de prédiction :

#### Build du Bento
bentoml build

#### Lancement du serveur local
bentoml serve energy_prediction_service:latest

- L'interface interactive Swagger UI sera accessible à l'adresse : http://localhost:3000

#### Exemple de Test API
Pour tester la prédiction, vous pouvez envoyer le JSON suivant dans Swagger :

```json
{
  "data": {
    "PropertyGFATotal": 50000,
    "BuildingAge": 90,
    "NumberofFloors": 15,
    "HasGas": 1,
    "PrimaryPropertyType": "Office"
  }
}
```
## Méthodologie & Résultats

### Nettoyage des données

 - Filtrage des bâtiments non-résidentiels uniquement.

 - Suppression des données aberrantes (Outliers) sur les surfaces et consommations.

 - Création de variables (Feature Engineering) : Âge du bâtiment, types d'usage.

### Modélisation

 - Modèle retenu : SVR (Support Vector Regression).

 - Transformation de la cible : Logarithmique (pour stabiliser la variance).

 - Optimisation : Recherche par grille (GridSearchCV).

### Validation des données

L'API utilise Pydantic pour garantir que les données envoyées au modèle respectent le format attendu (types, plages de valeurs), évitant ainsi les erreurs en production.


## Conclusion générale et recommandations stratégiques

Ce projet avait pour objectif de prédire la consommation énergétique des
bâtiments non résidentiels de la ville de Seattle à partir de leurs seules
caractéristiques structurelles, dans un contexte de transition énergétique
et de neutralité carbone à l’horizon 2050.

**Synthèse de la Modélisation**
Nous avons testé trois approches algorithmiques pour répondre à cette problématique :La Régression Linéaire : Servait de baseline stable mais trop simple pour capturer la complexité des données.

La Random Forest : A montré un sur-apprentissage (overfitting) massif ($R^2$ Train 0.92 vs Test 0.43), prouvant qu'un modèle complexe n'est pas toujours le meilleur s'il ne généralise pas.

Le SVR (Support Vector Regressor) : S'est révélé être le modèle le plus robuste. Après optimisation des hyperparamètres par GridSearchCV, il a atteint un R2 final de 0.6938 sur le jeu de test.


**Performance du modèle**
Avec près de 70% de la variance expliquée, le modèle SVR optimisé est un outil fiable pour estimer la consommation d'énergie des bâtiments n'ayant pas encore réalisé d'audit complet. L'erreur moyenne (MAE) est maîtrisée, ce qui permet une planification budgétaire énergétique cohérente pour la ville.

**L'intérêt de l'ENERGY STAR Score**
Notre test comparatif a montré que l'intégration de l'ENERGY STAR Score fait progresser la précision du modèle de 10.4% (le R² passant de 0.53 à 0.58 en validation croisée).
Ce score apporte une valeur ajoutée réelle. Cependant, le modèle reste performant même sans lui, offrant ainsi une alternative gratuite et rapide pour une première estimation.

## Recommandations pour la Ville de Seattle

**Déploiement du modèle SVR Optimisé**
Le modèle développé permet d'expliquer près de 70% de la consommation sans nécessiter d'audit technique complexe.

- Action : Utiliser ce modèle pour identifier les bâtiments dont la consommation réelle dépasse largement la prédiction. Ces "bâtiments anormaux" doivent être les cibles prioritaires pour des inspections de rénovation énergétique.

**Ciblage par type d'usage**
L'importance des variables a montré que l'Usage (Hôtels, Entrepôts, Bureaux) est le deuxième facteur le plus impactant après la surface.

- Action : Créer des programmes de sensibilisation spécifiques par secteur. Un hôtel et un entrepôt de même surface n'ont pas les mêmes leviers d'économie (isolation vs gestion du chauffage/climatisation).

**Focus sur le parc ancien**
L'âge du bâtiment est un prédicteur significatif de la consommation.

- Recommandation : Soutenir financièrement la rénovation thermique des bâtiments construits avant les années 80, car ils présentent le plus gros potentiel d'économie d'énergie selon les tendances capturées par le modèle.