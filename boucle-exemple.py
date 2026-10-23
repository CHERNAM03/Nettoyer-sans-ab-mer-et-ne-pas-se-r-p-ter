# -*- coding: utf-8 -*-
# S43 - jeudi 22 octobre
# Trois choses que tu utilises depuis lundi sans les avoir nommees.
# Ce fichier ne se connecte a rien. Lance-le, lis la sortie, puis modifie-le.

print("=" * 55)
print(" 1. LA LISTE  -  plusieurs valeurs, dans l'ordre")
print("=" * 55)

officiels = ["Site web", "Booking", "Agence", "Téléphone"]

officiels.append("Passage")

print("la liste entiere  :", officiels)
print("combien de valeurs:", len(officiels))
print("la premiere       :", officiels[0])      # on compte a partir de ZERO
print("la deuxieme       :", officiels[1])
print("la derniere       :", officiels[-1])     # -1 = la derniere
print("la troixieme       :", officiels[2])     # troisiéme
print("la cinquieme       :", officiels[4])     # cinquiéme
#print("la dixieme       :", officiels[9])       # dixiéme

officiels.append("Partenaire")                   # ajouter une valeur a la fin
print("apres append      :", officiels)


print()
print("=" * 55)
print(" 2. LE DICTIONNAIRE  -  une cle, une valeur")
print("=" * 55)

correspondances = {"site web": "Site web",
                   "BOOKING":  "Booking",
                   "Telephone":"Téléphone"}


correspondances["Passage"]="Walkin"
print("le dictionnaire   :", correspondances)
print("combien de paires :", len(correspondances))
print("valeur de 'BOOKING' :", correspondances["BOOKING"])
print("toutes les cles   :", list(correspondances.keys()))
print("toutes les valeurs:", list(correspondances.values()))

correspondances["AGENCE"] = "Agence"             # ajouter une paire
print("apres ajout       :", correspondances)

print(correspondances["Passage"])

print()
print("=" * 55)
print(" 3. LA BOUCLE  -  faire la meme chose pour chaque valeur")
print("=" * 55)

print("\n-- sur une liste --")
for canal in officiels:
    print("   je traite :", canal)

print("\n-- sur un dictionnaire : il faut .items() --")
for mal_ecrit, correct in correspondances.items():
    print("  ", mal_ecrit, "devient", correct)


print()
print("=" * 55)
print(" 4. CE QUE LA BOUCLE REMPLACE")
print("=" * 55)

# AVANT : on ecrit la meme ligne trois fois
print("\nAVANT (ce que tu as fait mardi) :")
print("   rapport 1 : ca_par_hotel.csv")
print("   rapport 2 : ca_par_canal.csv")
print("   rapport 3 : ca_par_segment.csv")

# APRES : on ecrit la ligne UNE fois
print("\nAPRES :")
fichiers = ["ca_par_hotel.csv", "ca_par_canal.csv", "ca_par_segment.csv"]
for nom_fichier in fichiers:
    print("   rapport  :", nom_fichier)

print("\n-> Ajouter un quatrieme rapport coute maintenant UNE ligne,")
print("   dans la liste. Pas trois lignes de plus dans le script.")

# Ajoutez votre propre canal à la liste officiels avec append , et relancez. Où apparaît-il ?
## J'ai ajouté mon propre canal, appelé Passage , qui est à la derniére position sur ma liste,
## grace à la methode .append

# Affichez la troisième valeur de la liste. Puis la cinquième. Puis la dixième — et lisez 
# le message d’erreur avec la méthode du mémo : dernière ligne, lignede votre fichier, chevron.

## On a une erreur de type IndexError, au niveau de la ligne 21 et concernant officiels[9]
# Ajoutez une paire au dictionnaire, et affichez-la par sa clé.
# j'ai ajouté une paire "Passage" : "Walkin" et je l'ai affiché par la clé, j'ai le resultat suivant:
## le dictionnaire   : {'site web': 'Site web', 'BOOKING': 'Booking', 'Telephone': 'Téléphone', 'Passage': 'Walkin'}
## Walkin


# Supprimez .items() dans la dernière boucle, relancez, lisez l’erreur, remettez
## On a une erreur de type ValueError, au niveau de la,ligne 59 et concerne mal_ecrit, correct