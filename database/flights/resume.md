La régression linéaire est nécessaire lorsque la variable cible à prédire est continue, c’est-à-dire qu’elle peut prendre une infinité de valeurs numériques (et pas seulement 0 ou 1).

Exemple typique : Prédire le retard d’un vol en minutes (DEP_DELAY ou ARR_DELAY), c’est-à-dire la valeur exacte du retard (par exemple : 0, 5, 12.3, -3, etc.).



Voici la signification des métriques du rapport de classification :

precision : proportion de prédictions positives correctes parmi toutes les prédictions positives faites par le modèle.
(Ex : sur 100 prédictions « retard », si 90 sont vraiment des retards, la précision est 0.90)

recall (rappel) : proportion de vrais positifs détectés parmi tous les cas réellement positifs.
(Ex : sur 100 vrais retards, si le modèle en détecte 80, le rappel est 0.80)

f1-score : moyenne harmonique entre précision et rappel, utile quand il faut un compromis entre les deux.
(F1 = 2 × (precision × recall) / (precision + recall))

support : nombre d’exemples réels de chaque classe dans le jeu de test.
(Ex : si 200 vols sont « retard », le support pour la classe « retard » est 200)

AUC score (LogisticRegression) : 0.9471
Classification LogisticRegression : 
              precision    recall  f1-score   support

           0      0.878     0.924     0.900      1514
           1      0.918     0.869     0.893      1486

    accuracy                          0.897      3000
   macro avg      0.898     0.896     0.897      3000
weighted avg      0.898     0.897     0.897      3000

AUC score : 0.8530
Classification DecisionTreeClassifier : 
              precision    recall  f1-score   support

           0      0.855     0.854     0.854      1514
           1      0.851     0.852     0.852      1486

    accuracy                          0.853      3000
   macro avg      0.853     0.853     0.853      3000
weighted avg      0.853     0.853     0.853      3000

AUC moyen : 0.9609
Classification RandomForestClassifier :               
                precision    recall  f1-score   support

           0      0.881     0.933     0.906     14906
           1      0.930     0.876     0.902     15094

    accuracy                          0.904     30000
   macro avg      0.905     0.904     0.904     30000
weighted avg      0.906     0.904     0.904     30000

AUC score (LightGBM) : 0.9567
Classification LightGBM : 
              precision    recall  f1-score   support

           0      0.877     0.931     0.903      1514
           1      0.925     0.867     0.895      1486

    accuracy                          0.899      3000
   macro avg      0.901     0.899     0.899      3000
weighted avg      0.901     0.899     0.899      3000





# Les principaux types de modèles de machine learning pour données tabulaires

## 1. Arbres de décision et modèles ensemblistes
- **Arbre de décision** : Modèle simple, facile à interpréter, qui segmente les données en fonction de règles ("si... alors...").
- **Random Forest** : Ensemble d'arbres de décision entraînés sur des sous-échantillons des données. Plus robuste et performant qu'un arbre seul.
- **Gradient Boosting (XGBoost, LightGBM, CatBoost)** : Entraîne des arbres de façon séquentielle pour corriger les erreurs des précédents. Très performant sur les données tabulaires.

## 2. Réseaux de neurones (Deep Learning)
- **Réseau de neurones dense (MLP)** : Empilement de couches de neurones. Puissant pour des données complexes, mais souvent moins performant que les arbres pour des données tabulaires classiques.
- **Réseaux spécialisés** : CNN pour images, RNN/LSTM pour séquences, etc.

## 3. Modèles linéaires
- **Régression linéaire/logistique** : Simple, rapide, interprétable. Efficace si la relation entre variables est linéaire.

## 4. Autres modèles
- **SVM (Support Vector Machine)** : Efficace pour des petits jeux de données, moins utilisé pour de grandes bases tabulaires.
- **K plus proches voisins (KNN)** : Simple, mais peu efficace sur de grands volumes.

## En résumé
- Pour des données tabulaires, les modèles d'arbres (RandomForest, LightGBM, XGBoost) sont souvent les plus efficaces.
- Les réseaux de neurones sont surtout utiles pour des données non structurées (images, texte, son).
- Les modèles linéaires restent utiles pour leur simplicité et leur interprétabilité.