#%%
import requests
import json
import time
import pandas as pd

# Votre clé d'API TMDb
api_key = '28c6630049f5d468217e4f34963c03a6'

# URL de base de l'API TMDb pour les films populaires
base_url_popular = 'https://api.themoviedb.org/3/movie/popular'

# Nombre total de films à récupérer
total_movies = 10000

# Nombre de films à récupérer par requête
movies_per_request = 20

# Champs de base pour les films
fields = 'id'  # Ajoutez les champs que vous souhaitez récupérer ici

# Liste pour stocker tous les films avec leurs détails
all_movies_details = []

# Nombre de requêtes nécessaires pour obtenir le nombre total de films
num_requests = total_movies // movies_per_request

# Effectuer les requêtes pour récupérer les films
for page in range(1, num_requests + 1):
    params = {
        'api_key': api_key,
        'page': page,
        'fields': fields
    }
    response = requests.get(base_url_popular, params=params)#, timeout=10)  # Définir un délai d'attente de 10 secondes

    if response.status_code == 200:
        movies_data = response.json()
        movies_reco = movies_data.get('results', [])

            # Pour chaque film, récupérer les détails supplémentaires
        for movie in movies_reco:
            movie_id = movie['id']
            movie_details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits,keywords'
            movie_details_response = requests.get(movie_details_url)
            if movie_details_response.status_code == 200:
                movie_details = movie_details_response.json()
                all_movies_details.append(movie_details)
                print(f"Film {movie['title']} récupéré avec détails supplémentaires.")
            else:
                print(f"Erreur lors de la récupération des détails pour {movie['title']}. Statut : {movie_details_response.status_code}")
        print(f"Page {page} récupérée. Total de films récupérés : {len(all_movies_details)}")

    else:
        print(f"Erreur lors de la requête pour la page {page}. Statut : {response.status_code}")


    if len(all_movies_details) >= total_movies:
        break

# Enregistrer les données complètes dans un fichier JSON
with open('movies_data_complete.json', 'w', encoding='utf-8') as f:
    json.dump(all_movies_details, f, ensure_ascii=False, indent=4)

print("Récupération des films avec détails complets terminée. Les données ont été enregistrées dans movies_data_complete.json.")