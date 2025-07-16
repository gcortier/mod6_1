# Projet : Conteneur Docker pour base de données SQLite (jeu de données Adult)

## Résumé
Ce projet vise à :
- Construire un conteneur Docker qui héberge une base de données SQLite alimentée par les fichiers `adult.data` et `adult.test`.
- Utiliser la description du dataset dans `adult.names` pour modéliser la base.
- Concevoir le système de façon modulaire et maintenable (système "meurice pure").

## Structure des données
- **Source** : Fichiers `adult.data` (train) et `adult.test` (test)
- **Description** : Voir `adult.names` pour le détail des colonnes et des valeurs possibles.
- **Colonnes principales** :
  - age, workclass, fnlwgt, education, education-num, marital-status, occupation, relationship, race, sex, capital-gain, capital-loss, hours-per-week, native-country, income

## Plan d'action

1. **Analyse et modélisation**
   - Lire `adult.names` pour comprendre les champs et types.
   - Définir un schéma relationnel (table principale + tables annexes si normalisation souhaitée).

2. **Préparation des données**
   - Nettoyer et convertir les fichiers `adult.data` et `adult.test` en CSV standard si besoin.
   - Gérer les valeurs manquantes et les types.

3. **Création de la base SQLite**
   - Écrire un script (Python recommandé) pour créer la base et importer les données.
   - Générer le fichier `.db` prêt à l'emploi.

4. **Création du conteneur Docker**
   - Écrire un `Dockerfile` pour un conteneur léger (ex : basé sur Python ou Alpine).
   - Copier la base SQLite dans le conteneur.
   - Prévoir un point d'entrée pour servir la base (API REST, ou accès direct à la base selon besoin).

5. **Système modulaire et maintenable**
   - Séparer clairement les scripts de transformation, d'import, et de service.
   - Documenter chaque étape et chaque module.

6. **Tests et validation**
   - Vérifier l'intégrité de la base et la cohérence des données importées.
   - Tester l'accès à la base dans le conteneur.

## Pour aller plus loin
- Possibilité d'ajouter une API REST (ex : Flask/FastAPI) pour exposer les données.
- Ajouter des scripts de migration ou d'évolution du schéma.
- Prévoir des tests automatisés pour la chaîne d'import et de service.

---

**Voir `adult.names` pour toute question sur la signification des champs.**
