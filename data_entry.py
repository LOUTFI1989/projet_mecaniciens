import sqlite3
import json

# Connexion à la base de données (crée le fichier s'il n'existe pas)
conn = sqlite3.connect('mec.db')  # Change le nom de la base de données si nécessaire
cursor = conn.cursor()


# Charger les données JSON depuis le fichier
try:
    with open('data/mecaniciens.json', encoding='utf-8') as f:
        data = json.load(f)
        print(data)  # Vérifie le contenu de data
except FileNotFoundError:
    print("Le fichier JSON n'a pas été trouvé. Vérifiez le chemin.")
    conn.close()
    exit()

# Insérer les données JSON dans la table
for entry in data['mechaniciens'].values():  # Accède à chaque mécanicien
    nom = entry.get('nom')
    zone = entry.get('zone')
    specialites = entry.get('specialites')
    adresse = entry.get('Adresse')  # Remarquez ici que vous utilisez 'Adresse' avec un A majuscule
    notation = entry.get('notation')

    # Vérification de la validité des champs et transformation de la liste specialites en chaîne de caractères
    if nom and zone and specialites and adresse and notation is not None:
        if isinstance(specialites, list):
            specialites = ', '.join(specialites)  # Convertir la liste en une chaîne de caractères
        cursor.execute('''
            INSERT INTO mecaniciens (nom, zone, specialites, adresse, notation)
            VALUES (?, ?, ?, ?, ?)
        ''', (nom, zone, specialites, adresse, notation))
    else:
        print(f"Données manquantes pour l'entrée: {entry}")

# Valider les modifications
conn.commit()

# Vérifier les données insérées
cursor.execute('SELECT * FROM mecaniciens')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fermer la connexion
conn.close()
