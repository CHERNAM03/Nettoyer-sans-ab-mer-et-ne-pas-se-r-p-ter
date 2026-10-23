# =====================================================================
#  VERIFICATION DE L'INSTALLATION  -  lundi 19 octobre, 10 minutes
#
#  Ce script ne fait rien d'autre que verifier que tout est en place.
#  Lance-le, et lis le resultat ligne par ligne.
#
#  Dans VS Code : clic droit dans le fichier -> "Executer le fichier Python
#  dans le terminal".  Ou bien, dans le terminal :  python verifier_installation.py
# =====================================================================

print("=" * 55)
print(" VERIFICATION DE VOTRE INSTALLATION")
print("=" * 55)

tout_va_bien = True

# --- 1. Python ---
import sys
print(f"\n[1] Python        : version {sys.version.split()[0]}  -> OK")

# --- 2. pandas ---
try:
    import pandas as pd
    print(f"[2] pandas        : version {pd.__version__}  -> OK")
except ImportError:
    print("[2] pandas        : ABSENT")
    print("    -> dans le terminal :  pip install pandas")
    tout_va_bien = False

# --- 3. psycopg2 (le pont entre Python et PostgreSQL) ---
try:
    import psycopg2
    print(f"[3] psycopg2      : version {psycopg2.__version__.split()[0]}  -> OK")
except ImportError:
    print("[3] psycopg2      : ABSENT")
    print("    -> dans le terminal :  pip install psycopg2-binary")
    tout_va_bien = False

# --- 4. La base de donnees repond-elle ? ---
if tout_va_bien:
    from getpass import getpass
    print("\n[4] Connexion a PostgreSQL")
    mot_de_passe = getpass("    Mot de passe PostgreSQL : ")
    try:
        conn = psycopg2.connect(host="localhost", port=5432, dbname="Urbanstay",
                                user="postgres", password=mot_de_passe)
        curseur = conn.cursor()
        curseur.execute("SELECT count(*) FROM reservations")
        nb = curseur.fetchone()[0]
        print(f"    Connexion etablie. La table reservations contient {nb} lignes.")
        if nb == 2000:
            print("    -> OK, c'est le bon nombre.")
        else:
            print(f"    -> ATTENTION : on attendait 2000 lignes, il y en a {nb}.")
            print("       Previens le formateur.")
            tout_va_bien = False
        curseur.close(); conn.close()
    except Exception as erreur:
        print(f"    ECHEC : {erreur}")
        print("    -> Verifie que PostgreSQL est demarre, et le mot de passe.")
        tout_va_bien = False

print("\n" + "=" * 55)
if tout_va_bien:
    print(" TOUT EST EN PLACE. Tu peux commencer.")
else:
    print(" IL MANQUE QUELQUE CHOSE. Lis les lignes ci-dessus,")
    print(" puis appelle le formateur en lui disant QUEL numero a echoue.")
print("=" * 55)
