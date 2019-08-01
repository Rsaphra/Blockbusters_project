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


def convert_to_int(string):
    '''This function tries to convert a string into an integer, if it fails
       it will return "null"'''
    try:
        clean_string = re.sub('\W+','', string)
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


def check_data_fields(data, list_of_fields):
    """Takes in a dictionary and a list of all keys that must be in that dictionary
        returns false if any of those keys are not contained"""
    exists = True
    for field in list_of_fields:
        if field not in data:
            exists = False        
    return exists

def omdb_api(movies):
    """This function retrieves the movie deatils for list of given movies using omdb api"""
    movies_details = []
    for title in movies:
        title.replace(" ", "+")
        url = f'http://www.omdbapi.com/?apikey={config.omdb_api}&t={title}'
        response = requests.get(url)
        movie = response.json()
        #check to make sure each key is always in the dict
        necessary_fields = ['Director', 'BoxOffice', 'Ratings', 'Title']
        if check_data_fields(movie, necessary_fields):
            #4 necessary fields, title is important for the insert statement query later
            movie_dict = {'director': movie['Director'],
                          'boxoffice': convert_to_int(movie['BoxOffice']),
                          'rt_rating': rt_rating(movie),
                          'title': movie['Title']}
            movies_details.append(movie_dict)
        time.sleep(.2)
        
    
    return movies_details 


def add_omdb_values_to_movies():
    """Add box office, director and rotten tomatoes rating 
    from the omdb to our pre-existing movies DB"""
    
    #retrieve all movie names and pass to omdb_api to get a 
    #list of dictionaries with values of directora nd box_office and rating
    all_titles = get_movie_names()
    omdb_values = omdb_api(all_titles)
    return omdb_values



#to account for when rt_rating or box_office doesn't exist, we have different sql statements for each case
def determing_insert_query(values):
    director = values[0]
    box_office = values[1]
    rt_rating = values[2]
    title = values[3]
    #both box office and rating are absent
    if box_office == "NULL" and rt_rating == None:
        return f"""UPDATE movies
                    SET 
                        director = "{director}"
                    WHERE title = "{title}";"""
    #box office is absent
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
    #all accounted for
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


#to test to see if title = {title} actually matches anything
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


#################################################################################
#TMDb_api helper functions   

#parse through the data and retrieve only what I need
def arrange_data(data):
    """This function receives the raw data that we pulled. that is saved in a list of pages.
       each page contains a list of movies for every movie """
    new_list = []
    for page in data:
        for dictionary in page:
            #save the values we want for each title
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

###############################
#these two functions make sure our data is in tuple form
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

#'movies' table insertion function
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
        #updating the 'page' paramater
        params = {'language': '', 'page': page}
        response = requests.get(url, params=params)
        json_response = response.json()
        #making sure we have data before going on
        if 'results' in json_response:
            top_rated.append(json_response['results'])
        #considering movieDB limit for requests
        time.sleep(4)
    #returns a list of dictionary. each page on a different dictionary.
    reducted_data = arrange_data(top_rated)
    #tupple_data = multiple_tuples(reducted_data)
    return  reducted_data


def populate_movies_table(data):
    cnx, cursor = connect_to_db()
    #the query we use to insert
    insert_movies_q = ("""INSERT INTO movies 
                     (movie_id, title, popularity, 
                     release_date, vote_count, vote_avg)
                     VALUES (%s, %s, %s, %s, %s, %s)""")

    #get the full list of all values to be inserted
    tupled_data = multiple_tuples(data)
    # insert the business data ito db
    db_insertion(insert_movies_q, tupled_data)

    # make sure the connection is closed.
    cursor.close()
    cnx.close()


#helper functiosn in populating the genre instances table
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
        