import unicodedata

def normaliser_nom(nom):
    # Supprimer les accents
    nom = unicodedata.normalize('NFKD', nom).encode('ASCII', 'ignore').decode('utf-8')
    # Nettoyer les espaces inutiles
    nom = ' '.join(nom.strip().split())
    # Capitaliser chaque mot
    return ' '.join([mot.capitalize() for mot in nom.split()])

def nettoyer_fichier_noms(fichier_source, fichier_sortie):
    noms_set = set()

    # Lire et nettoyer les noms
    with open(fichier_source, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            nom = ligne.strip()
            if nom:  # Ignorer les lignes vides
                nom_nettoye = normaliser_nom(nom)
                if nom_nettoye:
                    noms_set.add(nom_nettoye)

    # Trier les noms
    noms_final = sorted(noms_set)

    # Écrire dans le nouveau fichier
    with open(fichier_sortie, 'w', encoding='utf-8') as sortie:
        for nom in noms_final:
            sortie.write(f"- {nom}\n")

    print(f"{len(noms_final)} noms nettoyés enregistrés dans '{fichier_sortie}'.")

# Exemple d'utilisation
if __name__ == "__main__":
    nettoyer_fichier_noms("nom.txt", "noms_nettoyes.txt")
