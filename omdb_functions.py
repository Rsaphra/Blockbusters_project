import api_connections
import db_functions
import mysql.connector
from mysql.connector import errorcode
import re
import config
import requests
import json
import time
import tmdb_functions
# omdbi api helper functions


def convert_to_int(string):
    '''This function tries to convert a string into an integer, if it fails
       it will return "null"'''
    try:
        clean_string = re.sub('\W+', '', string)
        clean_string = int(clean_string)
    except:
        clean_string = "NULL"
    return clean_string


def rt_rating(movie):
    """This function is able to access the inner dictionary from each movie
       json file to retrieve it rotten tomatoes score"""
    for rating in movie['Ratings']:
        if rating['Source'] == "Rotten Tomatoes":
            rt_v = rating['Value']
            return convert_to_int(rt_v)


def convert_list_from_tuples(tuple_list):
    """The movie titles are retrieved as a list of tupes, 
    return instead a list with just the title from the first half of each tuple"""
    title_list = []
    for item in tuple_list:
        title_list.append(item[0])
    return title_list


def get_movie_names():
    '''This function grabs the title from inside
       the "movies" table in movie db'''
    name_q = """
            SELECT title
            FROM movies"""
    cnx, c = connect_to_db()
    c.execute(name_q)
    results = c.fetchall()
    cnx.close()
    c.close()
    title_list = convert_list_from_tuples(results)
    return title_list


def get_all_movie_info():
    '''This function grabs all the data from inside
       the "movies" table in movie db'''
    select_q = """
                SELECT *
                FROM movies
                """
    cnx, c = connect_to_db()
    c.execute(q)
    results = c.fetchall()
    cnx.close()
    c.close()
    return results


def check_data_fields(data, list_of_fields):
    """Takes in a dictionary and a list of all keys that must be in that dictionary
        returns false if any of those keys are not contained"""
    exists = True
    for field in list_of_fields:
        if field not in data:
            exists = False
    return exists


def add_omdb_values_to_movies():
    """Add box office, director and rotten tomatoes rating 
    from the omdb to our pre-existing movies DB"""

    # retrieve all movie names and pass to omdb_api to get a
    # list of dictionaries with values of directora nd box_office and rating
    all_titles = get_movie_names()
    omdb_values = omdb_api(all_titles)
    return omdb_values


# to account for when rt_rating or box_office
# doesn't exist, we have different sql statements for each case
def determing_insert_query(values):
    director = values[0]
    box_office = values[1]
    rt_rating = values[2]
    title = values[3]
    # both box office and rating are absent
    if box_office == "NULL" and rt_rating == None:
        return f"""UPDATE movies
                    SET 
                        director = "{director}"
                    WHERE title = "{title}";"""
    # box office is absent
    elif box_office == 'NULL':
        return f"""UPDATE movies
                    SET 
                        director = "{director}", 
                        rt_ratings = '{rt_rating}'
                    WHERE title = "{title}";"""
    #rating is absent
    elif rt_rating == None:
        return f"""UPDATE movies
                    SET 
                        director = "{director}", 
                        box_office = '{box_office}'
                    WHERE title = "{title}";"""
    # all accounted for
    else:
        return f"""UPDATE movies
                    SET 
                        director = "{director}", 
                        box_office = '{box_office}', 
                        rt_ratings = '{rt_rating}'
                    WHERE title = "{title}";"""


def insert_omdb_values(values):
    '''This function inserts the values "director", 
       "box_office" (revenue), and rt_ratings into the db'''
    insert_q = determing_insert_query(values)
    cnx, c = connect_to_db()
    c.execute(insert_q)
    cnx.commit()
    c.close
    cnx.close


def check_data_fields(data, list_of_fields):
    """Takes in a dictionary and a list of all keys that must be in that dictionary
        returns false if any of those keys are not contained"""
    exists = True
    for field in list_of_fields:
        if field not in data:
            exists = False
    return exists


# to test to see if title = {title}
# actually matches anything
def check_title_match(values):
    title = values[3]
    insert_q = f"""SELECT title, movie_id
            FROM movies
            WHERE title = "{title}";"""
    cnx, c = connect_to_db()
    c.execute(insert_q)
    result = c.fetchall()
    c.close
    cnx.close
    return result
