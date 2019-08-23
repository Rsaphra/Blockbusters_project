import mysql.connector
from mysql.connector import errorcode
import re
import config
import requests
import json
import time
import omdb_functions
import db_functions
import tmdb_functions


def get_genres():
    """This function retrieves a list of a dictionary 
    containing a list of all genres and their ids."""

    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={config.api_key}'
    headers = {'api_key': config.api_key}

    params = {'language': ''}
    response = requests.get(url, params=params)
    genres = response.json()['genres']
    # returns list of dictionaries, each containing
    # key and value
    return genres


def omdb_api(movies):
    """This function retrieves the movie deatils for list 
    of given movies using omdb api"""
    movies_details = []
    for title in movies:
        title.replace(" ", "+")
        url = f'http://www.omdbapi.com/?apikey={config.omdb_api}&t={title}'
        response = requests.get(url)
        movie = response.json()
        # check to make sure each key is always in the dict
        necessary_fields = ['Director', 'BoxOffice', 'Ratings', 'Title']
        if check_data_fields(movie, necessary_fields):
            # 4 necessary fields, title is important for the insert statement query later
            movie_dict = {'director': movie['Director'],
                          'boxoffice': convert_to_int(movie['BoxOffice']),
                          'rt_rating': rt_rating(movie),
                          'title': movie['Title']}
            movies_details.append(movie_dict)
        time.sleep(.2)

    return movies_details


def top_rated(pages):
    """This function retrieves the top rated movies from the movie db using their api.
       The user is required to give it a list of the pages they want to obtain from the db"""

    url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={config.api_key}'
    top_rated = []
    for page in pages:
        # updating the 'page' paramater
        params = {'language': '', 'page': page}
        response = requests.get(url, params=params)
        json_response = response.json()
        # making sure we have data before going on
        if 'results' in json_response:
            top_rated.append(json_response['results'])
        # considering movieDB limit for requests
        time.sleep(4)
    # returns a list of dictionary. each page on a different dictionary.
    reducted_data = arrange_data(top_rated)
    #tupple_data = multiple_tuples(reducted_data)
    return reducted_data
