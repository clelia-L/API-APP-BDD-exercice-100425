import requests
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000/api/"


def afficher_menu():
    print("\n=== GESTION MEUBLES (Laragon) ===")
    print("1. Lister les produits")
    print("2. Ajouter un produit")
    print("3. Quitter")


def lister_produits():
    try:
        response = requests.get(urljoin(BASE_URL, "produits"))
        if response.status_code == 200:
            print("\n=== PRODUITS ===")
            for prod in response.json():
                print(f"{prod['id']} | {prod['nom']} | {prod['prix']}€ | Stock: {prod['stock']}")
        else:
            print(f"Erreur API: {response.status_code}")
            print(response.json().get('error', ''))
    except requests.exceptions.ConnectionError:
        print("Serveur API indisponible - Lancez api.py d'abord")


def ajouter_produit():
    try:
        data = {
            'nom': input("Nom du produit: "),
            'prix': float(input("Prix: ")),
            'stock': int(input("Stock (optionnel): ") or 0)
        }
        response = requests.post(urljoin(BASE_URL, "produits"), json=data)

        if response.status_code == 201:
            print("Produit ajouté avec succès!")
        else:
            print("Erreur:", response.json().get('error', 'Inconnue'))
    except ValueError:
        print("Saisie invalide")


if __name__ == "__main__":
    print("Connexion à MySQL via Laragon (localhost:3309)")
    while True:
        afficher_menu()
        choix = input("> ")

        if choix == '1':
            lister_produits()
        elif choix == '2':
            ajouter_produit()
        elif choix == '3':
            break
