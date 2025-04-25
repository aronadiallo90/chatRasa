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
# mysql -h 127.0.0.1 -P 3306 -u root -p