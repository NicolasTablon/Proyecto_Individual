import pandas as pd

   
url = 'https://raw.githubusercontent.com/NicolasTablon/Proyecto_Individual/main/Csv_Proyecto_Terminado.csv'
# Descargar el archivo CSV
response = requests.get(url)
response.raise_for_status()

# Leer el archivo CSV
df_movies = pd.read_csv(io.BytesIO(response.content), encoding="UTF-8", delimiter=",", error_bad_lines=False)

 @app.route('/recomendacion', methods=['GET'])
def recomendacion():
    titulo = request.args.get('titulo')  # Obtener el parámetro 'titulo' de la solicitud GET
    
    # Filtrar las películas similares basadas en el título proporcionado
    pelicula_actual = df[df['title'] == titulo]
    puntajes_similares = df[df['vote_average'] >= pelicula_actual['vote_average'].values[0]]
    peliculas_similares = puntajes_similares.sort_values(by='vote_average', ascending=False)['title'].tolist()
    
    # Devolver una lista de 5 películas recomendadas en formato JSON
    recomendaciones = peliculas_similares[:5]
    return jsonify(recomendaciones)

if __name__ == '__main__':
    app.run()

    return recommended_movies
