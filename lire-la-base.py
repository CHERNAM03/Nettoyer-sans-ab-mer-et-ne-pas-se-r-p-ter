# =====================================================================
#  LUNDI  -  Le script qui va chercher les donnees tout seul
#
#  Ce que fait ce script, en quatre temps :
#    1. il se connecte a la base
#    2. il execute UNE REQUETE SQL  -  celle que tu connais deja
#    3. il recoit le resultat sous forme de tableau
#    4. il ecrit ce tableau dans un fichier que tu peux ouvrir dans Excel
#
#  Tu n'apprends pas une nouvelle facon de poser des questions.
#  Tu apprends a mettre TES questions dans un fichier qui se relance tout seul.
# =====================================================================

import warnings
import psycopg2
import pandas as pd
from getpass import getpass

# pandas affiche un avertissement sans consequence quand on lui passe une
# connexion psycopg2. Cette ligne le masque -- volontairement, et on sait pourquoi.
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")


# --- 1. LA CONNEXION ---------------------------------------------------
# Le mot de passe n'est JAMAIS ecrit dans le fichier : on le demande a chaque fois.
mot_de_passe = getpass("Mot de passe PostgreSQL : ")

connexion = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="Urbanstay",
    user="postgres",
    password=mot_de_passe,
)
print("Connecte a la base.")


# --- 2. LA REQUETE -----------------------------------------------------
# C'est du SQL. Exactement celui de la semaine derniere.
# Les trois guillemets permettent d'ecrire la requete sur plusieurs lignes.
requete = """
    SELECT h.nom_hotel,
           count(*)                        AS nb_reservations,
           round(sum(r.montant_total), 2)  AS chiffre_affaires
    FROM reservations r
    JOIN chambres c ON r.chambre_id = c.chambre_id
    JOIN hotels h   ON c.hotel_id   = h.hotel_id
    GROUP BY h.nom_hotel
    ORDER BY chiffre_affaires DESC
"""
requete = """
    select 
    segment_client,
    count(*) as nb_clients,
    MAX(date_inscription)
 from clients c 
 group by segment_client;
"""
requete = """
    SELECT * FROM chambres
"""

# --- 3. LE RESULTAT ----------------------------------------------------
# pandas execute la requete et range le resultat dans un "DataFrame",
# c'est-a-dire un tableau, avec des lignes et des colonnes.
tableau = pd.read_sql(requete, connexion)

print(f"\nLe resultat contient {len(tableau)} lignes et {len(tableau.columns)} colonnes.")
print("\nVoici les 5 premieres lignes :\n")
print(tableau.head(5).to_string(index=False))


# --- 4. LE FICHIER -----------------------------------------------------
# Trois reglages, et chacun resout un vrai probleme :
#   sep=";"               Excel en francais separe les colonnes par des points-virgules
#   decimal=","           sinon Excel lit 159567.68 comme du TEXTE, pas comme un nombre
#   encoding="utf-8-sig"  sinon les accents s'affichent en caracteres bizarres

print(tableau.shape) # combien de lignes et de colonnes
print(tableau.columns) # les noms des colonnes
print(tableau.head(3)) # les 3 premières lignes
print(tableau.tail(3)) # les 3 dernières lignes
tableau.to_csv("chambres.csv", sep=";", decimal=",",
               index=False, encoding="utf-8-sig")
print("\nFichier ecrit : chambres.csv")
print("Ouvre-le : il est a cote de ce script.")

print(tableau["type_chambre"].value_counts())

connexion.close()


### Exercice 1 — La chasse aux cinq formes · 40 min ####

## Trouvez trois variables :
# 1. La variable "connexion" : elle contient l'objet de liaison établi avec la base de données PostgreSQL. ligne 28
# 2. La variable "requete" : elle contient le texte de la requête SQL à exécuter. Ligne 41
# 3. La variable "tableau" : elle contient le DataFrame Pandas qui stocke les lignes et colonnes renvoyées par la base.
# Ligne 56


## Trouvez l’appel à to_csv :
# Ligne : tableau.to_csv("ca_par_hotel.csv", sep=";", decimal=",", index=False, encoding="utf-8-sig")
# On lui donne 4 réglages principaux (en plus du nom du fichier) :
# - sep=";" : sépare les colonnes par un point-virgule (indispensable pour Excel en français).
# - decimal="," : utilise la virgule comme séparateur décimal pour éviter que les nombres soient lus comme du texte.
# - index=False : évite d'ajouter une colonne supplémentaire pour l'index numérique des lignes.
# - encoding="utf-8-sig" : garantit que les accents s'affichent correctement.


## Trouvez trois méthodes :
# 1. tableau.head(5) -> On demande au tableau d'extraire ses 5 premières lignes. Ligne 60
# 2. tableau.to_csv(...) -> On demande au tableau de s'exporter sous forme de fichier CSV. Ligne 68
# 3. connexion.close() -> On demande à la connexion de se fermer proprement. Ligne 73


## Le script contient une ligne qui masque un avertissement.
# Laquelle, et pourquoi est-elle là ?
# Ligne : warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
# Elle est là pour masquer l'avertissement inoffensif que Pandas envoie lorsqu'on utilise 
# une connexion brute "psycopg2" au lieu de SQLAlchemy, afin de garder un terminal propre et lisible.

## Exercice 4 — Interroger le tableau :
# « tableau.shape affiche deux nombres :
# Dans le résultat que vous obtenez : (6, 3) :
#  Le premier nombre (6) correspond au nombre de lignes de notre tableau.
#  Le second nombre (3) correspond au nombre de colonnes de votre tableau 
#  (ici : segment_client, nb_clients et max).   
# Ce que chaque ligne de notre terminal a affiché :
# (6, 3) :
#  Le résultat de print(tableau.shape) (dimensions du tableau).  
#  Index(['segment_client', 'nb_clients', 'max'], dtype='str') : 
# Le résultat de print(tableau.columns) qui liste le nom exact des colonnes.
#  Les 3 premières lignes (via head(3)) : Les segments Loisirs et Groupe.  
#  Les 3 dernières lignes (via tail(3)) : Les lignes du segment Business. 


##### Exercice 5 — Compter sans SQL ###############
# Pour cette question, on a trouvé exactement les memes chiffres que la semaine passée. c'est à dire 
# On a les memes resultats, cela ne pourrait pas etre le cas, car on s'est connecté sur la meme base de
# données. MAIS.....
# En cas d'écart inattendu entre un résultat SQL et un traitement Python, 
# la base de données SQL fait toujours foi.
# Piste de vérification : Pour trancher, comparez systématiquement le nombre total de lignes (len() vs COUNT(*)) 
# et surveillez la présence de valeurs nulles ou d'espaces invisibles.


