from fastapi import FastAPI
import pandas as pd
import io
import json
import re
from datetime import datetime
import requests
from typing import List
from io import StringIO
app = FastAPI()
url = 'https://raw.githubusercontent.com/NicolasTablon/Proyecto_Individual/main/Csv_Proyecto_Terminado.csv'

# Descargar el archivo CSV
response = requests.get(url)
response.raise_for_status()

# Leer el archivo CSV
df = pd.read_csv(io.BytesIO(response.content), encoding="UTF-8", delimiter=",", error_bad_lines=False)

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes):
    mes = mes.lower()
    peliculas_mes = df[df["month"] == mes]
    cantidad = len(peliculas_mes)
    
    mensaje = f"{cantidad} cantidad de películas fueron estrenadas en el mes {mes.capitalize()}."
    
    return mensaje

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia):
    dia = dia.lower()
    filmaciones_dia = df[df["nombre_dia_espanol"].str.lower() == dia]
    cantidad = len(filmaciones_dia)
    
    mensaje = f"{cantidad} cantidad de películas fueron estrenadas en el día {dia.capitalize()}."
    
    return mensaje

@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion):
    pelicula = df[df["title"] == titulo_de_la_filmacion]
    
    if pelicula.empty:
        return "No se encontró la filmación en el dataset."
    
    titulo = pelicula["title"].iloc[0]
    ano_estreno = pelicula["release_year"].iloc[0]
    score = pelicula["popularity"].iloc[0]
    
    mensaje = f"La película {titulo} fue estrenada en el año {ano_estreno} con un score/popularidad de {score}."
    
    return mensaje

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo_de_la_filmacion):
    pelicula = df[df["title"] == titulo_de_la_filmacion]
    
    if pelicula.empty:
        return "No se encontró la filmación en el dataset."
    
    cantidad_votos = pelicula["vote_count"].iloc[0]
    
    if cantidad_votos < 2000:
        return "La filmación no cumple con la cantidad mínima de valoraciones."
    
    promedio_votos = pelicula["vote_average"].iloc[0]
    mensaje = f"La película {titulo_de_la_filmacion} fue estrenada en el año {pelicula['release_year'].iloc[0]}. Cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}."
    
    return mensaje

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor):
    actor_df = df[df["actors"].str.contains(nombre_actor, case=False, na=False)]
    actor_df["return"] = actor_df["revenue"] - actor_df["budget"]
    
    cantidad_peliculas = len(actor_df)
    retorno_total = actor_df["return"].sum()
    promedio_retorno = actor_df["return"].mean()
    
    mensaje = f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas. Ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por película."
    
    return mensaje

@app.get('/get_director/{director}')
def get_director(director: str):
    df1 = df[df["director"].notna() & df["director"].str.contains(director)]
    df1["ganancia"] = df1["revenue"] - df1["budget"]
    retorno_director = df1["return"].sum()
    resp = df1[["title", "release_year", "return", "budget", "ganancia"]]

    return [director, retorno_director, resp]


@app.get('/recomendacion')
async def recomendacion(titulo: str) -> List[str]:
    # Convertir el título proporcionado a minúsculas
    titulo = titulo.lower()

    # Obtener la fila correspondiente al título proporcionado
    pelicula = df.loc[df['title'].str.lower() == titulo]

    if pelicula.empty:
        return []

    # Obtener la puntuación de la película
    puntuacion = pelicula['vote_average'].values[0]

    # Encontrar películas similares según la puntuación
    peliculas_similares = df.loc[df['vote_average'] >= puntuacion].sort_values('vote_average', ascending=False)

    # Obtener los títulos de las 5 películas con mayor puntuación
    recomendaciones = peliculas_similares['title'].head(5).tolist()

    return recomendaciones

if __name__ == '__main__':
    app.run()

@app.get("/inicio")
async def ruta_prueba():
    return "Hola"
