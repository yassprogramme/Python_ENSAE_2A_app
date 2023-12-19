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


if __name__ == '__main__':
    app.run_server(debug=True)
