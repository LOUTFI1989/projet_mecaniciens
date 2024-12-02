
from flasgger import Swagger
import requests
from flask import Flask, request, jsonify

#http://localhost:5603/apidocs/

app = Flask(__name__)
swagger = Swagger(app)  # Initialisation de Swagger
api_sql_uri = 'http://localhost:5003/api/mecaniciens'

@app.route('/api/mecaniciens', methods=['POST'])
def ajouter_mecanicien():
    """
    Ajouter un mécanicien
    ---
    parameters:
      - name: nom
        in: body
        required: true
        type: string
        description: Nom du mécanicien
      - name: zone
        in: body
        required: true
        type: string
        description: Zone d'intervention du mécanicien
      - name: specialite
        in: body
        required: true
        type: string
        description: Spécialité du mécanicien
    responses:
      200:
        description: Mécanicien ajouté avec succès
        schema:
          id: Mecanicien
          properties:
            id:
              type: integer
              description: Identifiant du mécanicien
            nom:
              type: string
              description: Nom du mécanicien
            zone:
              type: string
              description: Zone d'intervention
            specialite:
              type: string
              description: Spécialité du mécanicien
      400:
        description: Mauvaise requête (données invalides)
    """
    data = request.get_json()
    response = requests.post(f'{api_sql_uri}/ajouter', json=data)

    if response.status_code in [200, 201]:
        return jsonify(response.json()), response.status_code
    else:
        print(f'Erreur lors de l\'ajout du mécanicien: {response.status_code} - {response.text}')
        return jsonify({'error': 'Erreur lors de l\'ajout du mécanicien.'}), response.status_code


@app.route('/api/mecaniciens', methods=['GET'])
def afficher_mecaniciens():
    """
    Récupérer tous les mécaniciens
    ---
    responses:
      200:
        description: Liste de tous les mécaniciens
        schema:
          type: array
          items:
            id: Mecanicien
            properties:
              id:
                type: integer
                description: Identifiant du mécanicien
              nom:
                type: string
                description: Nom du mécanicien
              zone:
                type: string
                description: Zone d'intervention
              specialite:
                type: string
                description: Spécialité du mécanicien
    """
    response = requests.get(f'{api_sql_uri}/select')
    return jsonify(response.json()), response.status_code




# GET - Récupérer un mécanicien par ID
@app.route('/api/mecaniciens/id/<int:id>', methods=['GET'])
def afficher_mecanicien_par_id(id):

    response = requests.get(f'{api_sql_uri}/id/{id}')
    return jsonify(response.json()), response.status_code

# GET - Récupérer un mécanicien par adresse
@app.route('/api/mecaniciens/adresse/<string:adresse>', methods=['GET'])
def afficher_mecanicien_par_adresse(adresse):
    response = requests.get(f'{api_sql_uri}/adresee/{adresse}')
    return jsonify(response.json()), response.status_code

# GET - Récupérer un mécanicien par adresse
@app.route('/api/mecaniciens/notation/<string:notation>', methods=['GET'])
def afficher_mecanicien_par_notation(notation):
    response = requests.get(f'{api_sql_uri}/notation/{notation}')
    return jsonify(response.json()), response.status_code

@app.route('/api/mecaniciens/zone/<string:zone>', methods=['GET'])
def afficher_mecanicien_par_zone(zone):

 try:
    response = requests.get(f"{api_sql_uri}/zone/{zone}")
    if response.status_code == 200:
        return jsonify(response.json()), response.status_code
    else:
        return jsonify({"error": "Erreur lors de la récupération des mécaniciens par zone."}), response.status_code

 except requests.RequestException as e:
        return jsonify({"message": f"Erreur de connexion à l'API: {str(e)}"}), 500


@app.route('/api/mecaniciens/specialite/<string:specialite>', methods=['GET'])
def afficher_mecanicien_par_specialite(specialite):
    try:
        response = requests.get(f'{api_sql_uri}/specialite/{specialite}')
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"message": "Erreur lors de la récupération des mécaniciens par spécialité."}), response.status_code
    except requests.RequestException as e:
        return jsonify({"message": f"Erreur de connexion à l'API: {str(e)}"}), 500

@app.route('/api/mecaniciens/nom/<string:nom>', methods=['GET'])
def afficher_mecanicien_par_nom(nom):
        try:
            response = requests.get(f'{api_sql_uri}/nom/{nom}')
            if response.status_code == 200:
                return jsonify(response.json()), 200
            else:
                return jsonify(
                    {"message": "Erreur lors de la récupération des mécaniciens par nom."}), response.status_code
        except requests.RequestException as e:
            return jsonify({"message": f"Erreur de connexion à l'API: {str(e)}"}), 500

# PUT - Modifier un mécanicien
@app.route('/api/mecaniciens/<int:id>', methods=['PUT'])
def modifier_mecanicien(id):
    data = request.get_json()
    response = requests.put(f'{api_sql_uri}/{id}', json=data)
    return jsonify(response.json()), response.status_code

# DELETE - Supprimer un mécanicien
@app.route('/api/mecaniciens/<int:id>', methods=['DELETE'])
def supprimer_mecanicien(id):
    response = requests.delete(f'{api_sql_uri}/{id}')
    return jsonify(response.json()), response.status_code

# Démarrer le serveur
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5609)
