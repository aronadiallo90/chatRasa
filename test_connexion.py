import pyodbc
# 10.42.3.49
#AdieAdie2
# Configuration de la connexion
server = "10.4.116.87,1433"
database = "referentiel_fudpe_new"
username = "sa"
password = "AdieAdie1"

# Matricule de l'agent à tester
matricule = "654986B"  # Remplace par un matricule valide

try:
    # Connexion à la base de données
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    cursor = conn.cursor()
    
    # Définition de la requête SQL
    query = """
        SELECT 
            a.agt_nom,
            a.agt_prenom,
            ac.act_numero_projet,
            ac.act_numero_acte,
            ea.eta_act_code AS etat_projet,
            ta.tac_libelle AS type_projet
        FROM 
            referentiel_fudpe_new.dbo.agent a
        INNER JOIN 
            referentiel_fudpe_new.dbo.acte_agent aa ON aa.act_agt_agt_id = a.agt_id
        INNER JOIN 
            referentiel_fudpe_new.dbo.acte ac ON ac.act_id = aa.act_agt_act_id
        LEFT JOIN 
            referentiel_fudpe_new.dbo.etat_acte ea ON ea.eta_act_id = ac.act_etat_id
        LEFT JOIN 
            referentiel_fudpe_new.dbo.type_acte ta ON ta.tac_id = ac.act_tac_id
        WHERE 
            a.agt_matricule_solde = ?
            AND ac.act_is_projet = 1;
    """

    # Exécution de la requête avec le matricule
    cursor.execute(query, (matricule,))
    results = cursor.fetchall()

    # Vérification et affichage des résultats
    if results:
        print("✅ Résultats trouvés :")
        for row in results:
            print(f"👤 {row.agt_nom} {row.agt_prenom}")
            print(f"📜 Numéro projet : {row.act_numero_projet}")
            print(f"📄 Numéro acte : {row.act_numero_acte}")
            print(f"📌 État du projet : {row.etat_projet}")
            print(f"🔹 Type de projet : {row.type_projet}")
            print("-" * 40)
    else:
        print("⚠️ Aucun projet trouvé pour ce matricule.")

    # Fermeture de la connexion
    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Erreur lors de l'exécution de la requête :", e)
