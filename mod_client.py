import requests

import requests

# URL de l'API
api_uri = 'http://localhost:5609/api/mecaniciens'


# Ajouter un mécanicien
def ajouter_mecanicien():
    nom = input('Saisir le nom du mécanicien: ')
    zone = input('Saisir la zone du mécanicien: ')
    specialites = input('Saisir les spécialités du mécanicien (séparées par des virgules): ').split(',')
    adresse = input('Saisir l\'adresse du mécanicien: ')

    while True:
        try:
            notation = float(input('Saisir la note du mécanicien (nombre valide): '))
            break
        except ValueError:
            print("Erreur : veuillez entrer un nombre valide pour la notation.")

    demande = {
        'nom': nom,
        'zone': zone,
        'specialites': [s.strip() for s in specialites],  # Retirer les espaces en trop
        'adresse': adresse,
        'notation': notation
    }

    try:
        # Effectuer la requête POST à l'API
        response = requests.post(api_uri, json=demande)

        # Afficher le statut de la réponse
        print(f'Statut de la réponse: {response.status_code}')

        if response.status_code == 201:
            print('Mécanicien ajouté avec succès!')
        else:
            # Afficher plus d'informations sur l'erreur
            print(f'Erreur: {response.status_code} - {response.text}')
    except requests.exceptions.RequestException as e:
        # Gestion des erreurs de connexion ou autres exceptions liées aux requêtes
        print(f'Erreur lors de la connexion à l\'API: {str(e)}')


# Récupérer tous les mécaniciens
def afficher_mecaniciens():
    response = requests.get(api_uri)
    if response.status_code == 200:
        mecaniciens = response.json().get('mecaniciens', [])
        if mecaniciens:
            print('Liste des mécaniciens :')
            for mecanicien in mecaniciens:
                print(f"ID: {mecanicien['id']}, Nom: {mecanicien['nom']}, Zone: {mecanicien['zone']}, "
                      f"Spécialités: {mecanicien['specialites']}, Adresse: {mecanicien['adresse']}, "
                      f"Notation: {mecanicien['notation']}")
        else:
            print("Aucun mécanicien trouvé.")
    else:
        print(f'Erreur: {response.status_code} - {response.text}')

# Mettre à jour un mécanicien
def modifier_mecanicien():
    mecanicien_id = input('Saisir l\'ID du mécanicien à modifier: ')
    nom = input('Saisir le nom du mécanicien: ')
    zone = input('Saisir la zone du mécanicien: ')
    specialites = input('Saisir les spécialités du mécanicien (séparées par des virgules): ').split(',')
    adresse = input('Saisir l\'adresse du mécanicien: ')

    while True:
        try:
            notation = float(input('Saisir la note du mécanicien (nombre valide): '))
            break
        except ValueError:
            print("Erreur : veuillez entrer un nombre valide pour la notation.")

    demande = {'nom': nom, 'zone': zone, 'specialites': specialites, 'adresse': adresse, 'notation': notation}

    response = requests.put(f"{api_uri}/{mecanicien_id}", json=demande)
    if response.status_code == 200:
        print(f'Mécanicien avec ID {mecanicien_id} mis à jour avec succès.')
    else:
        print(f'Erreur: {response.status_code} - {response.text}')

# Supprimer un mécanicien
def supprimer_mecanicien():
    mecanicien_id = input('Saisir l\'ID du mécanicien à supprimer: ')
    response = requests.delete(f"{api_uri}/{mecanicien_id}")
    if response.status_code == 200:
        print(f'Mécanicien avec ID {mecanicien_id} supprimé avec succès.')
    else:
        print(f'Erreur: {response.status_code} - {response.text}')

# Menu des opérations
def menu():
    while True:
        print("\n1. Ajouter un mécanicien")
        print("2. Afficher tous les mécaniciens")
        print("3. Modifier un mécanicien")
        print("4. Supprimer un mécanicien")
        print("5. Quitter")

        choix = input("Choisir une option: ")
        if choix == '1':
            ajouter_mecanicien()
        elif choix == '2':
            afficher_mecaniciens()
        elif choix == '3':
            modifier_mecanicien()
        elif choix == '4':
            supprimer_mecanicien()
        elif choix == '5':
            break
        else:
            print("Option invalide.")

# Exécution du menu
if __name__ == '__main__':
    menu()
