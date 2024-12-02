import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/mecaniciens/ajouter', methods=['POST'])
def inserer_mecanicien():
    data = request.get_json()

    try:
        # Utilisation de "with" pour ouvrir et fermer automatiquement la connexion
        with sqlite3.connect('mec.db', timeout=10) as con:
            curseur = con.cursor()

            # Préparation de la commande d'insertion
            cde_insert = '''INSERT INTO mecaniciens (nom, zone, specialites, adresse, notation)
                            VALUES (?, ?, ?, ?, ?)'''
            specialites_str = ','.join(data['specialites'])  # Conversion des spécialités en chaîne de caractères

            # Exécution de l'insertion
            curseur.execute(cde_insert, (data['nom'], data['zone'], specialites_str, data['adresse'], data['notation']))

            # Aucune nécessité de faire con.commit() ici, car "with" gère cela automatiquement

            return jsonify({'message': 'Mécanicien ajouté avec succès!'}), 201
    except sqlite3.DatabaseError as e:
        # Gestion des erreurs de la base de données
        return jsonify({'error': f'Erreur lors de l\'ajout du mécanicien : {str(e)}'}), 500

# GET - Récupérer tous les mécaniciens
@app.route('/api/mecaniciens/select', methods=['GET'])
def select_tous_les_mecaniciens():
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('SELECT * FROM mecaniciens')
    mecaniciens = curseur.fetchall()
    con.close()

    mecaniciens_list = [
        {'id': m[0], 'nom': m[1], 'zone': m[2], 'specialites': m[3], 'adresse': m[4], 'notation': m[5]}
        for m in mecaniciens
    ]

    return jsonify({'mecaniciens': mecaniciens_list}), 200

@app.route('/api/mecaniciens/nom/<string:nom>', methods=['GET'])
def select_mecanicien_par_nom(nom):
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('SELECT * FROM mecaniciens WHERE nom LIKE ?', (f'%{nom}%',))
    mecaniciens = curseur.fetchall()
    con.close()

    mecaniciens_list = [
        {'id': m[0], 'nom': m[1], 'zone': m[2], 'specialites': m[3], 'adresse': m[4], 'notation': m[5]}
        for m in mecaniciens
    ]

    if mecaniciens_list:
        return jsonify({'mecaniciens': mecaniciens_list}), 200
    else:
        return jsonify({'message': 'Aucun mécanicien trouvé avec ce nom.'}), 404

# GET - Récupérer des mécaniciens par zone
@app.route('/api/mecaniciens/zone/<string:zone>', methods=['GET'])
def select_mecanicien_par_zone(zone):
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('SELECT * FROM mecaniciens WHERE LOWER(zone) LIKE LOWER(?)', (f'%{zone}%',))
    mecaniciens = curseur.fetchall()
    con.close()

    mecaniciens_list = [
        {'id': m[0], 'nom': m[1], 'zone': m[2], 'specialites': m[3], 'adresse': m[4], 'notation': m[5]}
        for m in mecaniciens
    ]

    if mecaniciens_list:
        return jsonify({'mecaniciens': mecaniciens_list}), 200
    else:
        return jsonify({'message': 'Aucun mécanicien trouvé dans cette zone.'}), 404

    # GET - Récupérer des mécaniciens par zone


@app.route('/api/mecaniciens/adresse/<string:adresse>', methods=['GET'])
def select_mecanicien_par_adresse(adresse):
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('SELECT * FROM mecaniciens WHERE LOWER(adresse) LIKE LOWER(?)', (f'%{adresse}%',))
    mecaniciens = curseur.fetchall()
    con.close()

    mecaniciens_list = [
        {'id': m[0], 'nom': m[1], 'zone': m[2], 'specialites': m[3], 'adresse': m[4], 'notation': m[5]}
        for m in mecaniciens
    ]

    if mecaniciens_list:
        return jsonify({'mecaniciens': mecaniciens_list}), 200
    else:
        return jsonify({'message': 'Aucun mécanicien trouvé dans cette adresse.'}), 404

@app.route('/api/mecaniciens/notation/<string:notation>', methods=['GET'])
def select_mecanicien_par_notation(notation):
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('SELECT * FROM mecaniciens WHERE LOWER(notation) LIKE LOWER(?)', (f'%{notation}%',))
    mecaniciens = curseur.fetchall()
    con.close()

    mecaniciens_list = [
        {'id': m[0], 'nom': m[1], 'zone': m[2], 'specialites': m[3], 'adresse': m[4], 'notation': m[5]}
        for m in mecaniciens
    ]

    if mecaniciens_list:
        return jsonify({'mecaniciens': mecaniciens_list}), 200
    else:
        return jsonify({'message': 'Aucun mécanicien trouvé dans cette notation.'}), 404

# GET - Récupérer des mécaniciens par spécialité
@app.route('/api/mecaniciens/specialite/<string:specialite>', methods=['GET'])
def select_mecanicien_par_specialite(specialite):
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('SELECT * FROM mecaniciens WHERE specialites LIKE ?', (f'%{specialite}%',))
    mecaniciens = curseur.fetchall()
    con.close()

    mecaniciens_list = [
        {'id': m[0], 'nom': m[1], 'zone': m[2], 'specialites': m[3], 'adresse': m[4], 'notation': m[5]}
        for m in mecaniciens
    ]

    if mecaniciens_list:
        return jsonify({'mecaniciens': mecaniciens_list}), 200
    else:
        return jsonify({'message': 'Aucun mécanicien trouvé avec cette spécialité.'}), 404

# PUT - Modifier un mécanicien
@app.route('/api/mecaniciens/<int:id>', methods=['PUT'])
def modifier_mecanicien(id):
    data = request.get_json()
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    cde_update = '''UPDATE mecaniciens SET nom = ?, zone = ?, specialites = ?, adresse = ?, notation = ?
                    WHERE id = ?'''
    curseur.execute(cde_update, (data['nom'], data['zone'], data['specialites'], data['adresse'], data['notation'], id))
    con.commit()
    con.close()
    return jsonify({'message': 'Mécanicien mis à jour avec succès!'}), 200

# DELETE - Supprimer un mécanicien
@app.route('/api/mecaniciens/<int:id>', methods=['DELETE'])
def supprimer_mecanicien(id):
    con = sqlite3.connect('mec.db')
    curseur = con.cursor()
    curseur.execute('DELETE FROM mecaniciens WHERE id = ?', (id,))
    con.commit()
    con.close()
    return jsonify({'message': 'Mécanicien supprimé avec succès!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)
