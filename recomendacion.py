import pandas as pd

def recomendacion(titulo):
    # Descargar el archivo CSV
response = requests.get(url)
response.raise_for_status()

# Leer el archivo CSV
df = pd.read_csv(io.BytesIO(response.content), encoding="UTF-8", delimiter=",", error_bad_lines=False)

    # Normalizar los títulos de las películas en la columna "title"
    df_movies['title'] = df_movies['title'].str.lower().str.strip()

    # Filtrar por el título de la película ingresada
    selected_movie = df_movies[df_movies['title'] == titulo.lower().strip()]

    if selected_movie.empty:
        return "La película no se encuentra en la base de datos."

    # Calcular la similitud de puntuación entre la película ingresada y el resto de películas
    similarity_scores = df_movies[['title', 'vote_average']].corrwith(selected_movie['vote_average'])

    # Ordenar las películas según el score de similitud en orden descendente
    similar_movies = similarity_scores.sort_values(ascending=False)

    # Obtener los nombres de las películas recomendadas (excluyendo la película ingresada)
    recommended_movies = similar_movies.index[1:6].tolist()

    return recommended_movies
