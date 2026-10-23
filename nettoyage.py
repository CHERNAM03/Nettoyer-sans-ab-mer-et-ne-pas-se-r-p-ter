# =====================================================================
#  MERCREDI  -  Nettoyer avec Python, et garder la trace
#
#  Aucune nouveaute de langage dans ce script. Rien que des lignes
#  que tu sais deja lire :
#       quelque_chose = autre_chose        on range une valeur
#       print(...)                         on affiche
#       tableau["colonne"]                 on designe une colonne
#       .str.strip()                       on demande une action a la colonne
# =====================================================================

import warnings, psycopg2, pandas as pd
from getpass import getpass
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

mot_de_passe = getpass("Mot de passe PostgreSQL : ")
connexion = psycopg2.connect(host="localhost", port=5432, dbname="Urbanstay",
                             user="postgres", password=mot_de_passe)

reservations = pd.read_sql("SELECT * FROM reservations", connexion)
connexion.close()
print(f"Lu : {len(reservations)} reservations\n")


# --- D'ABORD : combien de valeurs sont REELLEMENT fausses ? ------------
# Les quatre libelles officiels d'UrbanStay, ecrits une fois pour toutes.
officiels = ["Site web", "Booking", "Agence", "Téléphone"]

mal_ecrites = reservations[~reservations["canal_reservation"].isin(officiels)]
print(f"Valeurs reellement mal ecrites : {len(mal_ecrites)}")
print("Lesquelles :")
print(mal_ecrites["canal_reservation"].value_counts().to_string())


# --- LA REGLE 1 : enlever les espaces au debut et a la fin -------------
avant_1 = reservations["canal_reservation"]
apres_1 = avant_1.str.strip()
nb_1 = (avant_1 != apres_1).sum()
reservations["canal_reservation"] = apres_1
print(f"\nRegle 1 - espaces supprimes          : {nb_1} valeur(s) modifiee(s)")


# --- LA REGLE 2 : reconnaitre, puis CHOISIR le bon libelle -------------
# On ne FABRIQUE pas le libelle avec une fonction : on le CHOISIT.
# A gauche : ce qu'on peut rencontrer.  A droite : le libelle officiel.
#correspondances = {
 #   "site web":  "Site web",   "SITE WEB":  "Site web",
  #  "booking":   "Booking",    "BOOKING":   "Booking",
  #  "agence":    "Agence",     "AGENCE":    "Agence",
  #  "Telephone": "Téléphone",  "TELEPHONE": "Téléphone",
#}

#avant_2 = reservations["canal_reservation"]
#apres_2 = avant_2.replace(correspondances)
#nb_2 = (avant_2 != apres_2).sum()
#reservations["canal_reservation"] = apres_2
#print(f"Regle 2 - libelles officiels choisis : {nb_2} valeur(s) modifiee(s)")


# --- LE CONTROLE : le nettoyage est-il fini ? --------------------------
print("\nApres nettoyage :")
print(reservations["canal_reservation"].value_counts().to_string())

restantes = reservations[~reservations["canal_reservation"].isin(officiels)]
print(f"\nValeurs encore hors de la liste officielle : {len(restantes)}")
if len(restantes) == 0:
    print("-> Le nettoyage est termine.")
else:
    print("-> LE NETTOYAGE N'EST PAS FINI. Il reste :")
    print(restantes["canal_reservation"].value_counts().to_string())


# --- LA TRACE : le journal part dans un fichier ------------------------
journal = pd.DataFrame({
    "regle":             ["espaces supprimes", "libelles officiels choisis"],
    "colonne":           ["canal_reservation", "canal_reservation"],
    "valeurs_modifiees": [nb_1, 0],
})
journal.to_csv("journal_nettoyage.csv", sep=";", index=False, encoding="utf-8-sig")
print("\nJournal ecrit : journal_nettoyage.csv")
print("C'est lui qu'on montre le jour ou quelqu'un conteste un chiffre.")