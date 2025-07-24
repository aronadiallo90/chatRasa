def nettoyer_et_formater_noms(fichier_entree, fichier_sortie):
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    noms_formats = []
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne:
            # Nettoyage : suppression des espaces multiples et capitalisation
            mots = ligne.split()
            mots = [mot.capitalize() for mot in mots]
            nom_formate = ' '.join(mots)
            noms_formats.append(nom_formate)

    # Tri optionnel (tu peux commenter cette ligne si tu veux garder l'ordre original)
    noms_formats.sort()

    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        for nom in noms_formats:
            f.write(f"- {nom}\n")

# Exemple d'utilisation
nettoyer_et_formater_noms("nom copy.txt", "noms_formates.txt")
