import api_connections
import db_functions
import mysql.connector
from mysql.connector import errorcode
import re
import config
import requests
import json
import time
import omdb_functions


# TMDb_api helper functions

# parse through the data and retrieve only what I
# need
def arrange_data(data):
    """This function receives the raw data that we pulled. that is saved in a list of pages.
       each page contains a list of movies for every movie """
    new_list = []
    for page in data:
        for dictionary in page:
            # save the values we want for each title
            new_dictionary = {}
            for k, v in dictionary.items():
                if k == 'id':
                    new_dictionary[k] = v
                if k == 'title':
                    new_dictionary[k] = v
                if k == 'popularity':
                    new_dictionary[k] = v
                if k == 'release_date':
                    new_dictionary[k] = v
                if k == 'vote_count':
                    new_dictionary[k] = v
                if k == 'vote_average':
                    new_dictionary[k] = v
                if k == 'genre_ids':
                    new_dictionary[k] = v
            new_list.append(new_dictionary)
    return new_list


##############################
# these two functions make sure our data
# is in tuple form
def create_tuple(reducted_data):
    data = (reducted_data['id'], reducted_data['title'],
            reducted_data['popularity'], reducted_data['release_date'],
            reducted_data['vote_count'], reducted_data['vote_average'])

    return data


def multiple_tuples(reducted_data):
    list_tuples = []
    for movie in reducted_data:
        list_tuples.append(create_tuple(movie))
    return list_tuples
################################

# 'movies' table insertion function


def db_insertion(query, data):
    '''This function inserts one instance of data into our db'''
    try:
        for datum in data:
            # Make sure data is committed to the database
            cursor.execute(query, datum)
            cnx.commit()
    except:
        print(f"{datum} already exists!")
    pass


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


def populate_movies_table(data):
    cnx, cursor = connect_to_db()
    # the query we use to insert
    insert_movies_q = ("""INSERT INTO movies 
                     (movie_id, title, popularity, 
                     release_date, vote_count, vote_avg)
                     VALUES (%s, %s, %s, %s, %s, %s)""")

    # get the full list of all values to be inserted
    tupled_data = multiple_tuples(data)
    # insert the business data ito db
    db_insertion(insert_movies_q, tupled_data)

    # make sure the connection is closed.
    cursor.close()
    cnx.close()


# helper functiosn in populating the genre
# instances table
def create_genre_tuple(reducted_data):
    data = (reducted_data['id'], reducted_data['genre_ids'])
    return data


def genres_tuples(reducted_data):
    list_tuples = []
    for movie in reducted_data:
        list_tuples.append(create_genre_tuple(movie))
    return list_tuples


def genre_instances_insertion(query, data):
    for datum in data:
        movie_id = datum[0]
        for genre_id in datum[1]:
            cursor.execute(query, (movie_id, genre_id))
            cnx.commit()
