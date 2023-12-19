import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pickle
import pandas as pd

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_details = pd.read_json("movies_data_complete.json")
movies["poster_path"] = "https://image.tmdb.org/t/p/w500/" + movies_details["poster_path"]
movies_details["poster_path"]="https://image.tmdb.org/t/p/w500/" + movies_details["poster_path"]
top_20_popular_movies = movies_details.sort_values('popularity', ascending=False).head(20)
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]["id"]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(movies_details[movies_details["id"] == movie_id]["poster_path"].values[0])
    return recommended_movies, recommended_movies_posters

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            html.H1("MOVIE RECOMMENDATION", style={'text-align': 'center', 'font-family': 'Source Sans Pro', 'font-weight': 'bold'}),
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        ),
        dcc.Dropdown(
            id='movie-dropdown',
            options=[{'label': title, 'value': title} for title in movies['title']],
            placeholder='Search...', # Texte affiché par défaut
            value=""  # Mettez la première valeur par défaut
        ),
        html.Button('Recommend', id='recommend-button', n_clicks=0),
        html.Div(id='output-recommendation')
    ],
    style={'backgroundColor': '#00008080'}  # Utilisation du code hexadécimal pour un bleu foncé semi-transparent
)

@app.callback(
    Output('output-recommendation', 'children'),
    Input('recommend-button', 'n_clicks'),
    [Input('movie-dropdown', 'value')]
)
def update_output(n_clicks, selected_movie_name):
    if not selected_movie_name or selected_movie_name==" ":  # Si aucun film n'est sélectionné
            # Créer une liste pour stocker les divs des 20 films populaires, 5 par ligne
            popular_movies_divs = []
            movies_per_row = 5  # Nombre de films par ligne
            rows_count = len(top_20_popular_movies) // movies_per_row  # Nombre de lignes complètes
            
            for row in range(rows_count):
                start_idx = row * movies_per_row
                end_idx = start_idx + movies_per_row
                row_movies = top_20_popular_movies.iloc[start_idx:end_idx]
                
                # Créer une ligne horizontale pour chaque série de 5 films populaires
                movie_row = html.Div([
                    html.Div([
                        html.Div(row_movies.iloc[i]["title"]),  # Afficher le nom du film
                        html.Img(src=row_movies.iloc[i]["poster_path"], style={'width': '100%', 'height': '15%'})
                    ], style={'width': '20%', 'text-align': 'center', 'margin-right': '10px'})
                    for i in range(movies_per_row)
                ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
                
                # Ajouter la ligne horizontale des films populaires à la liste
                popular_movies_divs.append(movie_row)
            
            return popular_movies_divs  # Affiche le nom des films ainsi que leur poster
    else:
        # Afficher le film sélectionné
        selected_movie = movies_details[movies_details['title'] == selected_movie_name]
        selected_movie_div = html.Div([
            html.H2(selected_movie['title'].values[0]),
            html.Img(src=selected_movie['poster_path'].values[0], style={'width': '20%', 'height': 'auto'}),
            html.P(selected_movie['overview'].values[0])
        ])

        # Afficher les films similaires
        recommended_movies, recommended_movies_posters = recommend(selected_movie_name)

        recommendations = []
        posters_per_row = 5  # Nombre de posters par ligne
        rows_count = len(recommended_movies_posters) // posters_per_row  # Nombre de lignes complètes
        
        for row in range(rows_count):
            start_idx = row * posters_per_row
            end_idx = start_idx + posters_per_row
            row_posters = recommended_movies_posters[start_idx:end_idx]
            row_names = recommended_movies[start_idx:end_idx]
        
        # Créer une ligne horizontale de posters centrée
            poster_row = html.Div([
                html.Div([
                    html.Div(row_names[i]),
                    html.Img(src=row_posters[i], style={'width': '100%', 'height': 'auto'})
                ], style={'width': '20%', 'text-align': 'center', 'margin-right': '10px'})
                for i in range(posters_per_row)
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        
            # Ajouter la ligne horizontale de posters à la liste des recommandations
            recommendations.append(poster_row)

        return [selected_movie_div] + recommendations  # Retourner la div du film sélectionné avec les films similaires

if __name__ == '__main__':
    app.run_server(debug=True)
