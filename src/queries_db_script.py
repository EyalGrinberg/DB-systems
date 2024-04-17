
import mysql.connector
import os


def get_query_as_text(path):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, path)
    query_list = open(my_file, "r").read()
    query = "".join(query_list)
    return query


def query_1(title):
    # pick_by_movie
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg', port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_1.txt') % title)
    results = []
    for result in cursor.fetchall():
        results.append({"Title":result[0], "Overview":result[1], "Rating":result[2], "Runtime":result[3], "language":result[4], "release date":result[5]})

    return results


def query_2(name):
    # pick_by_actor
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_2.txt') % name)
    results = []
    for result in cursor.fetchall():
        results.append({"Title": result[0], "Overview": result[1]})

    return results

def query_3(genre):
    # pick_by_genre
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_3.txt') % genre)
    results = []
    for result in cursor.fetchall():
        results.append({"Title": result[0], "Revenue": result[1]})
    return results


def query_4():
    # top_films_by_year
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_4.txt'))
    results = []
    for result in cursor.fetchall():
        results.append({"Title":result[0], "Movie Rating":result[1], "Genre":result[2], "Year's avg rating":result[3], "Genre Rating":result[4]})
    return results



def query_5(genre, length, movie_language):
    # pick_by_criteria
    if length == "short":
        min_runtime = 60
        max_runtime = 90
    elif length == "medium":
        min_runtime = 90
        max_runtime = 120
    elif length == "long":
        min_runtime = 120
        max_runtime = 200
    else:
        problem = None
        min_runtime = None
        max_runtime = None

    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_5.txt') % (genre, min_runtime, max_runtime, movie_language))
    results = []
    for result in cursor.fetchall():
        results.append({"Title": result[0], "Overview": result[1], "Rating": result[2], "Runtime": result[3],
                        "language": result[4], "release date": result[5]})

    return results


def query_6():
    # mean_rev_by_genre
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_6.txt'))
    results = []
    for result in cursor.fetchall():
        results.append({"Genre": result[0], "Mean Revenue": result[1]})
    return results


def query_7(name):
    # top_characters_by_actor
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_7.txt') % name)
    results = []
    for result in cursor.fetchall():
        results.append({"Name": result[0], "Movie Title": result[1]})
    return results


def query_8(language):
    # top_by_language
    cnx = mysql.connector.connect(host='127.0.0.1', user='eyalgrinberg', password='eyalgrinb66437', db='eyalgrinberg',
                                  port=3305)
    cursor = cnx.cursor()
    cursor.execute(get_query_as_text('queries/query_8.txt') % language)
    results = []
    for result in cursor.fetchall():
        results.append({"Title": result[0], "Rating": result[1]})
    return results


def print_result(movies):
    for movie in movies:
        for attr in movie:
            print(attr, ": ", movie[attr])
        print('\n')

