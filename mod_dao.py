# Fonction pour créer la table mecaniciens si elle n'existe pas déjà
import sqlite3


def creer_table():
    cde_ddl = '''CREATE TABLE IF NOT EXISTS mecaniciens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        zone TEXT NOT NULL,
        specialites TEXT NOT NULL,
        adresse TEXT NOT NULL,
        notation REAL NOT NULL
    )'''
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute(cde_ddl)
    con.commit()
    con.close()
# Créer la table au démarrage
creer_table()
