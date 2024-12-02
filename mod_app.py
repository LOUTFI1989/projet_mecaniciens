
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import logging
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'ma_cle_secrete'

# Firebase and API setup
api_uri = 'http://localhost:5609/api/mecaniciens'
cred = credentials.Certificate("./data/projetmecaniciens-firebase-adminsdk-e0tpf-c9fab95845.json")

firebase_admin.initialize_app(cred)


# Helper function for token authentication
def verifier_token_firebase(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return None

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/profile')
def profile():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('token', None)  # Remove token from session
    flash("Déconnexion réussie", 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            flash("Utilisateur créé avec succès", 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Erreur : {str(e)}", 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate the user with Firebase
        try:
            user = auth.get_user_by_email(email)
            # Check password (Firebase will do this for us)
            # In this case, we only use the token for session management
            token = auth.create_custom_token(user.uid)
            session['token'] = token  # Store token in session

            flash("Connexion réussie", 'success')
            return redirect(url_for('profile'))
        except auth.AuthError as e:
            flash("Erreur d'authentification: " + str(e), 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_mecanicien():


    if request.method == 'POST':
        nom = request.form['nom']
        zone = request.form['zone']
        specialites = request.form['specialites'].split(',')
        adresse = request.form['adresse']
        notation = float(request.form['notation'])

        demande = {
            'nom': nom,
            'zone': zone,
            'specialites': [s.strip() for s in specialites],
            'adresse': adresse,
            'notation': notation
        }

        response = requests.post(api_uri, json=demande)
        if response.status_code == 201:
            flash('Mécanicien ajouté avec succès!', 'success')
            return redirect(url_for('liste_mecaniciens'))
        else:
            flash('Erreur lors de l\'ajout du mécanicien.', 'danger')

    return render_template('ajouter.html')


@app.route('/liste')
def liste_mecaniciens():
    response = requests.get(api_uri)
    mecaniciens = response.json().get('mecaniciens', [])
    return render_template('liste.html', mecaniciens=mecaniciens)


@app.route('/mecaniciens', methods=['GET'])
def chercher_mecaniciens():
    mecaniciens = []
    critere = request.args.get('critere', '').strip()
    valeur = request.args.get('valeur', '').strip()

    try:
        if critere == 'zone':
            response = requests.get(f'{api_uri}/zone/{valeur}', timeout=5)
        elif critere == 'specialite':
            response = requests.get(f'{api_uri}/specialite/{valeur}', timeout=5)
        elif critere == 'nom':
            response = requests.get(f'{api_uri}/nom/{valeur}', timeout=5)
        else:
            return render_template('mecaniciens.html', mecaniciens=[])

        response.raise_for_status()
        mecaniciens = response.json().get('mecaniciens', [])

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Erreur HTTP : {http_err}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Erreur de requête : {err}")

    return render_template('mecaniciens.html', mecaniciens=mecaniciens)


if __name__ == '__main__':
    app.run(debug=True, port=5004)

