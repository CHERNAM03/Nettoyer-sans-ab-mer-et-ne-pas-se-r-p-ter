# Le directeur marketing voudrait connaitre les canaux  les moins utilisés par les 
# les clients pour effectuer une reservation.

# Le responsable voudrait connaitre  le canal qui rapporte le moins et pourquoi ?

# Ce que j'ai compris de sa question

# ce qui est ambigue

# Ma requete





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
from datetime import date
aujourdhui = date.today().strftime("%Y-%m-%d")


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

rapports = {
    f"classement_reservation1_{aujourdhui}.csv": """
        SELECT reservation_id, montant_total, 
            CASE WHEN montant_total < 300 THEN 'Petite'
                 WHEN montant_total BETWEEN 300 AND 800 THEN 'Moyenne'
                 ELSE 'Grosse'
            END AS Classement
        FROM reservations
        LIMIT 15;
    """,
    f"nb_reservation_clts_htl_{aujourdhui}.csv": """
        SELECT 
            h.hotel_id,
            COUNT(*) AS nb_de_reservation,
            COUNT(DISTINCT r.client_id) AS nb_clts_diffe
        FROM hotels h 
        JOIN chambres c ON h.hotel_id = c.hotel_id
        JOIN reservations r ON c.chambre_id = r.chambre_id
        GROUP BY h.hotel_id;
    """,
    f"tarif_moyen_htl_ch_{aujourdhui}.csv": """
        SELECT 
            hotel_id,
            COUNT(*) AS nb,
            ROUND(AVG(tarif_standard), 2) AS tarif_moyen_hotel
        FROM chambres c 
        GROUP BY hotel_id;
    """,
    f"nb_reservations_clts_etr_{aujourdhui}.csv": """
        SELECT 
           c.pays,
           c.segment_client,
           COUNT(*) AS nb_reservation_horsFR
        FROM clients c 
        JOIN reservations r ON c.client_id = r.client_id 
        WHERE c.pays != 'France'
        GROUP BY c.pays, c.segment_client;
    """,
    f"nb_reservations_qdep_mttMoyen_{aujourdhui}.csv": """
           select reservation_id, canal_reservation, statut, montant_total
            from reservations r 
           WHERE montant_total > (SELECT avg(montant_total) FROM reservations)
            order by montant_total  desc
            limit 10;
        """
}
for nom_fichier, requete in rapports.items():
 tableau = pd.read_sql(requete, connexion)
 tableau.to_csv(nom_fichier, 
                sep=";",
                decimal=",",
                 index=False, 
                encoding="utf-8-sig")
 print(nom_fichier, )

# Avec la boucle je suis passé de 45 lignes à 31, cela allége le code
# --- 3. LE RESULTAT ----------------------------------------------------
# pandas execute la requete et range le resultat dans un "DataFrame",
# c'est-a-dire un tableau, avec des lignes et des colonnes.
#tableau = pd.read_sql(requete, connexion)

#print(f"\nLe resultat contient {len(tableau)} lignes et {len(tableau.columns)} colonnes.")
#print("\nVoici les 5 premieres lignes :\n")
#print(tableau.head(5).to_string(index=False))


# --- 4. LE FICHIER -----------------------------------------------------
# Trois reglages, et chacun resout un vrai probleme :
#   sep=";"               Excel en francais separe les colonnes par des points-virgules
#   decimal=","           sinon Excel lit 159567.68 comme du TEXTE, pas comme un nombre
#   encoding="utf-8-sig"  sinon les accents s'affichent en caracteres bizarres
#print(tableau.shape) # combien de lignes et de colonnes
#print(tableau.columns) # les noms des colonnes
#print(tableau.head(3)) # les 3 premières lignes
#print(tableau.tail(3)) # les 3 dernières lignes

#tableau.to_csv(f"classement_reservation1{aujourdhui}.csv", sep=";", decimal=",",
 #              index=False, encoding="utf-8-sig")
#print(f"\nFichier ecrit : classement_reservation1{aujourdhui}.csv")
#print("Ouvre-le : il est a cote de ce script.")

#tableau.to_csv(f"nb_reservation_clts_htl{aujourdhui}.csv", sep=";", decimal=",",
#               index=False, encoding="utf-8-sig")
#print(f"\nFichier ecrit : nb_reservation_clts_htl{aujourdhui}.csv")
#print("Ouvre-le : il est a cote de ce script.")

#tableau.to_csv(f"tarif_moyen_htl_ch{aujourdhui}.csv", sep=";", decimal=",",
               #index=False, encoding="utf-8-sig")
#print(f"\nFichier ecrit : tarif_moyen_htl_ch.csv{aujourdhui}.csv")
#print("Ouvre-le : il est a cote de ce script.")

#print(tableau["type_chambre"].value_counts())
connexion.close()



##  Ce rapport permet au responsable de prendre connaissance du canal le moins important en terme de
## chiffre d'affaires en valeur absolue. Ainsi les reservations par telephone représentent à peu prés
## 10 % du chiffre d'affaires... Mes recommnandations :

## Exercice 6 — Ce que ça vous a vraiment donné 

# La principale différence entre faire tes requêtes séparément et utiliser une boucle réside dans 
# la maintenance, la longueur du code et le principe DRY (Don't Repeat Yourself ou "Ne te répète pas").

##  En résumé
#### Sans boucle : Tu fais du copier-coller de code, c'est fastidieux à maintenir.

#### Avec la boucle : Tu automatises, ton code est plus court, plus propre et beaucoup plus facile à modifier ou à faire grandir.