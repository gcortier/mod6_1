# Contribution & Validation du Code

Avant chaque commit, push ou pull request, merci de respecter les règles suivantes :

1. **Vérification syntaxique et logique**
   - Vérifie la structure, l’indentation et la cohérence des blocs (async/await, switch, etc.)
   - Assure-toi qu’il n’y a pas de doublons, de code mort ou d’appels asynchrones incorrects

2. **Validation automatique**
   - Lance le linter (ex : ESLint pour JS) et corrige toutes les erreurs
   - Exécute les tests unitaires et d’intégration si disponibles
   - Si possible, utilise un outil d’analyse statique pour détecter les erreurs

3. **Correction avant soumission**
   - Corrige toutes les erreurs détectées avant de soumettre le code
   - Ajoute un commentaire dans la PR ou le commit si une règle ne peut pas être respectée

4. **Rappel pour Copilot et assistants IA**
   - Ajoute l’instruction suivante à chaque demande :
     > “Après chaque modification, vérifie la validité syntaxique et logique du code, corrige les erreurs avant de rendre la main.”

---

Ces règles garantissent la qualité et la robustesse du code pour tous les contributeurs.
