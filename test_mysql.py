import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    try:
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
           host='127.0.0.1',
            port=3307,
            user='root',
            password='adieadie',
            database='PGDEPGDE'
        )

        if connection.is_connected():
            print("Connexion réussie à la base de données MySQL")

            # Récupérer et afficher les utilisateurs
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM mysql.user")
            users = cursor.fetchall()

            print("Liste des utilisateurs :")
            for user in users:
                print(user[0])

    except Error as e:
        print(f"Erreur de connexion MySQL : {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Connexion fermée.")

if __name__ == "__main__":
    test_mysql_connection()
# ssh  -L 3307:127.0.0.1:3306 adminadie@10.121.220.44 -p 3333
# ssh   adminadie@10.121.221.75 -p 3333
# mysql -h 127.0.0.1 -P 3306 -u root -p

# sudo systemctl enable ssh-tunnel.service
# sudo systemctl start ssh-tunnel.service

# verifier
# sudo systemctl status ssh-tunnel.service

# sudo nano /etc/systemd/system/ssh-tunnel.service
# sudo nano /etc/systemd/system/rasa-api.service





# sudo systemctl daemon-reexec
# sudo systemctl daemon-reload
# sudo systemctl enable ssh-tunnel.service
# sudo systemctl start ssh-tunnel.service
# sudo systemctl status ssh-tunnel.service




# desactiver les tunnel ssh : 
# Trouve tous les PID liés à autossh
# ps aux | grep autossh | awk '{print $2}' | xargs sudo kill -9
# # Trouve tous les PID liés à ssh (optionnel si tu sais que ça ne dérange pas)
# ps aux | grep '[s]sh -L 3307' | awk '{print $2}' | xargs sudo kill -9



# la commande autossh qui marche
# autossh -M 0 -f -L 3307:127.0.0.1:3306 adminadie@10.121.220.44 -p 3333 -N \
# -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes

