Exercice 1 — Terminer la fiche des règles

SOUS Dbeaver on a utilisé fonctions suivantes pour nettoyer les fichier de données :
- On a créé une vue
- Une copie
- La fonction Update pour mettre à jour avec set 
- Dans la condition CASE WHEN on a utilisé les fonctions :
----- UPPER  pour harmoniser certains mots en majuscules
----- TRIM pour enlever les espaces parasites
----- initcap pour mettre la premiére lettre d'un mot en majsucule
- 
Sous Python on a utilié d'autres methode pour la meme tache, c'est à dire nettoyage du fichier
- on a d'abord commencé par calculer  combien de valeurs sont REELLEMENT fausses en utilisant
----- les fonctions isin et len de python
- Ensuite on a enlevé les espaces au debut et a la fin avec les fonctions :
------ STRIP est une fonction intégrée aux chaînes de caractères (str) qui permet de supprimer des caractères spécifiques (par défaut, les espaces, tabulations et retours à la ligne) situés au début et à la fin d'une chaîne.  ------- et la fonction SUM de python
   _____  la règle 1 modifie zéro valeur :Par ce qu'elle compte les lignes et enlève les espaces au début et à la   fin et n'agit pas sur l'orthographe pour le moment
   _____ Valeurs réellement mal écrites sont au nombre de  30 et concernent le canal réservations:
canal_reservation
Téléphone    9
booking      9
site web     7
BOOKING      5
   ______ Règle 1 - espaces supprimes          : 0 valeur(s) modifiée(s)
          Règle 2 - libelles officiels choisis : 30 valeur(s) modifiée(s)

Apres nettoyage :
canal_reservation
Site web     779
Booking      609
Agence       405
Téléphone    207

Valeurs encore hors de la liste officielle : 0
-> Le nettoyage est termine.

------ les LISTES comme sequence de données bien ordonnées
- On a reconnu , puis choisi le bon libelle avec les fonctions et methode python :
------ des dictionnaires avec des clés et des valeurs 
------ les methodes:
 -------- REPLACE() permet de remplacer une ou plusieurs occurrences d'une sous-chaîne (ou d'un caractère) 
          par une autre dans une chaîne de caractères. 
 -------- et la fonction SUM() qui permet de calculer la somme


#### Avec lequel des trois outils feriez-vous ce nettoyage dans une vraie entreprise, et pourquoi ?

je le ferai avec Python, vu que cela permet d'automatiser les taches, un gain de temps colossal, et produit un 
journal des faits dans un fichier csv. Anisi, cela va garder des traces.