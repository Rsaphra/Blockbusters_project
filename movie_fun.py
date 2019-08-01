import mysql.connector
from mysql.connector import errorcode
import re
import config
import requests
import json
import time


#################################################################################
# genre db functions


# connection to db function
def connect_to_db():
    '''This function opens a connection and creates a cursor
       to the movie database'''
    cnx = mysql.connector.connect(
        host=config.host, user=config.user, passwd=config.password, database=config.DB_NAME)
    cursor = cnx.cursor()
    return cnx, cursor


# drops movies, genres and genre_instances if the tables already exist in the DB
def drop_all_current_tables():
    cnx, cursor = connect_to_db()
    d1 = "DROP TABLE IF EXISTS movies;"
    d2 = "DROP TABLE IF EXISTS genres;"
    d3 = "DROP TABLE IF EXISTS genre_instances;"
    cursor.execute(d3)
    cursor.execute(d2)
    cursor.execute(d1)
    cnx.close()
    cursor.close()


# returns a dictionary containing the necessary SQL queries to create each respective Table
def get_create_queries():
    TABLES = {}
    # movie_id through vote average is pulled from themoviedb, director through
    TABLES['movies'] = """
                        CREATE TABLE movies (
                            movie_id varchar(24) NOT NULL,
                            title varchar(256) NOT NULL,
                            popularity float(24) ,
                            release_date VARCHAR(12),
                            vote_count int(24),
                            vote_avg float(12), 
                            director varchar(24),
                            box_office FLOAT(32),
                            rt_ratings INTEGER,
                            PRIMARY KEY (movie_id)
                        ) ENGINE=InnoDB
                        """

    TABLES['genres'] = """
                        CREATE TABLE genres(
                            genre_id varchar(24) NOT NULL,
                            name VARCHAR(24),
                            PRIMARY KEY(genre_id)
                            )
                            """

    TABLES['genre_instances'] = """
                                CREATE TABLE genre_instances (
                                    genre_instance_id INTEGER AUTO_INCREMENT,
                                    movie_id VARCHAR(24),
                                    genre_id VARCHAR(24),
                                    PRIMARY KEY (genre_instance_id),
                                    CONSTRAINT fk_movie_id
                                    FOREIGN KEY fk_movie_id(movie_id)
                                    REFERENCES movies(movie_id) ON DELETE CASCADE,
                                    FOREIGN KEY fk_genre_id(genre_id)
                                    REFERENCES genres(genre_id) ON DELETE CASCADE
                                    )
                                """
    return TABLES


# create the tables using the pre defined queries
def create_tables():
    # drop current_tables if they exist
    drop_all_current_tables()
    # creating the queries for the actual tables setting business id as a primary key and a foreign key

    cnx, cursor = connect_to_db()

    TABLES = get_create_queries()
    # create the table using
    for table_name in TABLES:
        create_table_q = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(create_table_q)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()


# helper method, executes a sql query and returns the fetchall results
def execute_query(query):
    cnx, c = connect_to_db
    c.execute(query)
    result = c.fetchall()
    # close
    c.close()
    cnx.close()
    return result


# inserting genre instances based on the genre_ids in a movie_data and relating them to genre_data
def insert_genre_instances(movie_data):
    cnx, cursor = connect_to_db()
    # first iterate through each movie data
    for movie in movie_data:
        # then iterate through each 'genres' list
        genres = movie['genres']
        movie_id = movie['movie_id']
        # create row where movie_id = movie_id and genre_id = genre_id
        for genre in genres:
            insert_gi_q = f"""INSERT INTO genre_instances (movie_id, genre_id)
                             VALUES('{movie_id}', '{genre}')"""
            cursor.execute(insert_gi_q)

    cursor.close()
    cnx.close()


# takes a list of dicts as genres as data
def insert_genres(genre_data):
    cnx, cursor = connect_to_db()
    # go through list of genres and insert genre_id and name into DB
    for genre in genre_data:
        name = genre['name']
        genre_id = genre['id']
        insert_g_query = f"""INSERT INTO genres
                            (genre_id, name)
                            VALUES ('{genre_id}', '{name}')"""
        cursor.execute(insert_g_query)
        cnx.commit()
    cnx.close()
    cursor.close()


def get_genres():
    """This function retrieves a list of a dictionary containing a list of all genres and their ids."""

    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={config.api_key}'
    headers = {'api_key': config.api_key}

    params = {'language': ''}
    response = requests.get(url, params=params)
    genres = response.json()['genres']
    # returns list of dictionaries, each containing key and value
    return genres

#################################################################################

# omdbi api helper functions
