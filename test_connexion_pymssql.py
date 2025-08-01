import pymssql
import sys

# Configuration de la connexion
server = "10.42.3.49"
database = "referentiel_fudpe_new"
username = "sa"
password = "AdieAdie2"
port = 1433
#pip install pymssql

# Matricule de l'agent à tester
matricule = "654986B"  # Remplacez par un matricule valide

print("🔄 Tentative de connexion à la base de données...")
print(f"Serveur: {server}:{port}")
print(f"Base de données: {database}")
print(f"Utilisateur: {username}")
print("-" * 50)

try:
    # Connexion à la base de données avec pymssql
    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        port=port,
        timeout=30,  # Timeout de 30 secondes
        login_timeout=30  # Timeout de connexion
    )
    
    print("✅ Connexion à la base de données réussie !")
    
    cursor = conn.cursor()
    
    # Test simple de connexion
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()
    print(f"📊 Version SQL Server: {version[0][:50]}...")
    
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
            a.agt_matricule_solde = %s
            AND ac.act_is_projet = 1;
    """

    print(f"🔍 Recherche des projets pour le matricule: {matricule}")
    
    # Exécution de la requête avec le matricule
    cursor.execute(query, (matricule,))
    results = cursor.fetchall()

    # Vérification et affichage des résultats
    if results:
        print(f"✅ {len(results)} résultat(s) trouvé(s) :")
        print("=" * 50)
        for i, row in enumerate(results, 1):
            print(f"📋 Résultat {i}:")
            print(f"👤 Nom complet: {row[0]} {row[1]}")
            print(f"📜 Numéro projet: {row[2] if row[2] else 'N/A'}")
            print(f"📄 Numéro acte: {row[3] if row[3] else 'N/A'}")
            print(f"📌 État du projet: {row[4] if row[4] else 'N/A'}")
            print(f"🔹 Type de projet: {row[5] if row[5] else 'N/A'}")
            print("-" * 40)
    else:
        print("⚠️ Aucun projet trouvé pour ce matricule.")
        print("💡 Vérifiez que:")
        print("   - Le matricule existe dans la base")
        print("   - L'agent a des projets associés")
        print("   - La colonne 'act_is_projet' est bien à 1")

    # Test pour vérifier si le matricule existe
    cursor.execute("SELECT COUNT(*) FROM referentiel_fudpe_new.dbo.agent WHERE agt_matricule_solde = %s", (matricule,))
    count = cursor.fetchone()[0]
    print(f"🔍 Nombre d'agents trouvés avec ce matricule: {count}")

    # Fermeture de la connexion
    cursor.close()
    conn.close()
    print("✅ Connexion fermée proprement.")

except pymssql.Error as e:
    print(f"❌ Erreur SQL Server: {e}")
    print("💡 Vérifiez:")
    print("   - Les paramètres de connexion")
    print("   - Que SQL Server accepte les connexions TCP/IP")
    print("   - Que le port 1433 est ouvert")
except Exception as e:
    print(f"❌ Erreur générale: {e}")
    print("💡 Vérifiez:")
    print("   - La connectivité réseau")
    print("   - Les permissions d'accès")
    sys.exit(1)
