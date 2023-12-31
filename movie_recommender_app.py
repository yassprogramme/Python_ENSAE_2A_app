import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pickle
import pandas as pd

similarity = pickle.load(open("similarity.pkl", "rb"))
movies_details = pickle.load(open("movies_details.pkl","rb"))
movies_details = pd.DataFrame(movies_details)
movies_details["poster_path"]="https://image.tmdb.org/t/p/w500/" + movies_details["poster_path"]


genre_options = [genre for genre in movies_details['genres'].explode().unique()]

def recommend(movie, selected_genres=None):
    index = movies_details[movies_details['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    k = 1
    
    for i in distances[1::]:
        if k < 6:
            movie_id = movies_details.iloc[i[0]]["id"]
            movie_genres = movies_details.iloc[i[0]]["genres"] 
            # On vérifie si le film a le genre sélectionné (s'il y a un genre sélectionné)
            if selected_genres is None or any(genre in movie_genres for genre in selected_genres):
                recommended_movies.append(movies_details.iloc[i[0]].title)
                recommended_movies_posters.append(movies_details[movies_details["id"] == movie_id]["poster_path"].values[0])
                k += 1
        else:
            break
    
    return recommended_movies, recommended_movies_posters


def extract(list):
    S=""
    for x in list:
        S+=x+" "
    return S

           
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            html.H1("MOVIE RECOMMENDATION", style={'text-align': 'center', 'font-family': 'Source Sans Pro', 'font-weight': 'bold'}),
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        ),
        dcc.Dropdown( #c'est la première barre de recherche
            id='movie-dropdown',
            options=[{'label': title, 'value': title} for title in movies_details['title']],
            placeholder='Search...', # Texte affiché par défaut sur la barre de recherche
            value=""  # C'est la première valeur par défaut
        ),
        dcc.Dropdown(# c'est le filtre sur le genre
            id='genre-dropdown',
            options=genre_options,
            multi=True,
            placeholder='Filter by Genre'
        ),
        html.Button('Recommend', id='recommend-button', n_clicks=0),
        html.Div(id='output-recommendation')
    ],
    style={'backgroundColor': '#00008080'}  # Utilisation du code hexadécimal pour un bleu foncé semi-transparent en fond d'application
)

@app.callback(
    Output('output-recommendation', 'children'),
    Input('recommend-button', 'n_clicks'),
    [Input('movie-dropdown', 'value')],
    [Input('genre-dropdown', 'value')]  # Ajout de la valeur du filtre de genre comme entrée du callback
)
def update_output(n_clicks, selected_movie_name,selected_genre):
    if not selected_movie_name or selected_movie_name=="":  # Si aucun film n'est sélectionné
                #Si aucun genre n'est selectionné, on affiche les 20 films populaires du moment
            if not selected_genre:
                top_20_popular_movies = movies_details.sort_values('popularity', ascending=False).head(20)
            else:
                #Sinon, on affiche les 20 films populaires du moment en prenant en compte la liste des genres selectionnés.
                filtered_movies = movies_details[movies_details['genres'].apply(lambda x: any(item in x for item in selected_genre))]
                top_20_popular_movies = filtered_movies.sort_values('popularity', ascending=False).head(20)

            popular_movies_divs = []
            movies_per_row = 5  # Nombre de films par lignes
            rows_count = len(top_20_popular_movies) // movies_per_row  # Nombre de lignes
            popular_movies_divs.append(html.H2("The Popular Movies of the Moment"))  # Titre  

            for row in range(rows_count):
                start_idx = row * movies_per_row
                end_idx = start_idx + movies_per_row
                row_movies = top_20_popular_movies.iloc[start_idx:end_idx]
                
                # On crée une ligne horizontale pour chaque série de 5 films populaires
                movie_row = html.Div([
                    html.Div([
                        html.Div(row_movies.iloc[i]["title"] + ", Note : " + str(row_movies.iloc[i]["vote_average"].round(1)) + "/10"),
                        html.Img(src=row_movies.iloc[i]["poster_path"], style={'width': '100%', 'height': '15%'})
                    ], style={'width': '20%', 'text-align': 'center', 'margin-right': '10px'})
                    for i in range(movies_per_row)
                ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
                
                # On ajoute la ligne horizontale des films populaires à la liste
                popular_movies_divs.append(movie_row)
            
            return popular_movies_divs  # On affiche le nom des films ainsi que leur poster
    else: # Si on selectionne un film, on affiche le poster du film et des informations sur le film
        selected_movie = movies_details[movies_details['title'] == selected_movie_name]
        selected_movie_div = html.Div([
            html.H2(selected_movie['title'].values[0]),
            html.Div([
                html.Img(src=selected_movie['poster_path'].values[0], style={'width': '20%', 'height': 'auto'}),
                html.Div([
                    html.P([html.Strong(html.Span("Director:  ", style={'text-decoration': 'underline'})), selected_movie['crew'].values[0][0]], style={'text-align': 'left', 'margin-left': '10px'}),
                    html.P([html.Strong(html.Span("Genres:  ", style={'text-decoration': 'underline'})), extract(selected_movie['genres'].values[0])], style={'text-align': 'left', 'margin-left': '10px'}),
                    html.P([html.Strong(html.Span("Production:  ", style={'text-decoration': 'underline'})), selected_movie['production_companies'].values[0]], style={'text-align': 'left', 'margin-left': '10px'}), 
                    html.P([html.Strong(html.Span("Note:  ", style={'text-decoration': 'underline'})), str(selected_movie['vote_average'].values[0].round(1))+"/10"], style={'text-align': 'left', 'margin-left': '10px'}), 
                    html.P([html.Strong(html.Span("Released in:  ", style={'text-decoration': 'underline'})), selected_movie['release_year'].values[0]], style={'text-align': 'left', 'margin-left': '10px'}),
                    html.P([html.Strong(html.Span("Runtime:  ", style={'text-decoration': 'underline'})),str(selected_movie['runtime'].values[0])+"min"], style={'text-align': 'left', 'margin-left': '10px'}),
                    html.P([html.Strong(html.Span("Synopsis:  ", style={'text-decoration': 'underline'})), selected_movie['overview'].values[0]], style={'text-align': 'left', 'margin-left': '10px'})  # Synopsis
                ], style={'margin-left': '5px', 'display': 'flex', 'flex-direction': 'column'})  # Nouvelle ligne pour le synopsis
            ], style={'display': 'flex', 'align-items': 'stretch'})
        ])
        if selected_genre:#Si des genres sont renseignés
            recommended_movies, recommended_movies_posters = recommend(selected_movie_name, selected_genre)
        else:#Si aucun genre n'est renseigné en plus, on applique la même fontion en sachant que par défaut selected_genre=genres_options
            recommended_movies, recommended_movies_posters = recommend(selected_movie_name)
        
        recommendations = []
        posters_per_row = 5  # Nombre de posters par ligne
        rows_count = len(recommended_movies_posters) // posters_per_row  # Nombre de lignes complètes
        I=movies_details[movies_details['title'] == selected_movie_name].index[0]
        for row in range(rows_count):
            start_idx = row * posters_per_row
            end_idx = start_idx + posters_per_row
            row_posters = recommended_movies_posters[start_idx:end_idx]
            row_names = recommended_movies[start_idx:end_idx]
        
        # On crée une ligne horizontale de posters centrée
            poster_row = html.Div([
    html.Div([
        html.Div(
            row_names[i]+" , Recommandé à " + str(int(similarity[I, movies_details[movies_details['title'] == row_names[i]].index[0]].round(2)*100))+"%"),
        html.Img(src=row_posters[i], style={'width': '90%', 'height': '10%'}),
        ", Note : " + str(movies_details[movies_details['title'] == row_names[i]]['vote_average'].values[0].round(1)) + "/10"
    ])
    for i in range(posters_per_row)
], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})

        
            # On ajoute la ligne horizontale de posters à la liste des recommandations
            recommendations.append(poster_row)

        return [selected_movie_div] + recommendations 

if __name__ == '__main__':
    app.run_server(debug=True)