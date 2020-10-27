import requests_with_caching
import json


# Função recebe uma string com um nome de filme e 
# retorna 5 filmes relacionados ao título fornecido.
# As informações são disponibilizadas pela API
def get_movies_from_tastedive(movie_name):
    parameters = {"q": movie_name, "type":"movies", "limit": 5}
    
    results = requests_with_caching.get("https://tastedive.com/api/similar", params = parameters)
    
    return results.json()



#Função que extrai somente os títulos
# dos filmes retornados por get_movies_from_tastedive
def extract_movie_titles(movies_d):
    movie_names = []
    
    for movie in movies_d["Similar"]["Results"]:
        movie_names.append(movie["Name"])
        
    return movie_names



# Recebe uma lista de filmes, pega 5 filmes relacionados para cada um deles
# e separa somente os títulos destes filmes em uma lista sem repetição
def get_related_titles(movies_list):
    related_titles_list = []
    
    for movie in movies_list:
        movie_name = extract_movie_titles(get_movies_from_tastedive(movie))
        
        for name in movie_name:
            if name not in related_titles_list:
                related_titles_list.append(name)
            
    return related_titles_list


# Função usa o nome de um filme e retorna um dicionário com informações relacionados ao filme
# as informações são extraídas da API
def get_movie_data(movie_name):
    parameters = {"t": movie_name, "r":"json", "apikey":""}
    
    results = requests_with_caching.get("http://www.omdbapi.com/", params = parameters)
    
    return results.json()



# Recebe o dicionário de informações sobre um filme e retorna o rating no Rotten Tomatoes
def get_movie_rating(omdb_dic):
    rating_value = 0
    
    for item in omdb_dic["Ratings"]:
        if item["Source"] == "Rotten Tomatoes":
                rating_value = int(item["Value"].replace("%", ""))
                break
    
    return rating_value


# Tem uma lista de filmes como entrada,
# retorna outra lista com cinco filmes relacionados a cada um
# esta é ordenada(do maior para o menor rating no Rotten Tomatoes)
def get_sorted_recommendations(movie_titles_list):
    result_list  = []
    related_title_list = get_related_titles(movie_titles_list)
    
    result_list = sorted(related_title_list, reverse = True, key = lambda movie_name: (get_movie_rating(get_movie_data(movie_name)), movie_name))
    
    return result_list