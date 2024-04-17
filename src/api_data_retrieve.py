# imports
import mysql.connector
import requests
import time
from create_db_script import create_tables




def retrieve_movies():
    # init variables
    added_genres = set()
    problematics = set()
    added_movies = 0


    # insert movies from API
    cnx = mysql.connector.connect(host=hostname, user=username, password=password, db=database, port=port)
    cursor = cnx.cursor()

    # insert queries templates
    insert_movie_stmt = (
        "INSERT INTO movies (id, title, release_date, rate, revenue, spoken_language, runtime, overview) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )

    insert_genre_stmt = (
        "INSERT INTO genres (id, name) "
        "VALUES (%s, %s)"
    )

    insert_movie_genre_stmt = (
        "INSERT INTO movies_genres (movie_id, genre_id) "
        "VALUES (%s, %s)"
    )

    insert_movie_no_release = (
        "INSERT INTO movies (id, title, rate, revenue, spoken_language, runtime, overview) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )

    start_time = time.time()

    for movie_id in range(150000, 220000):

        if added_movies >= 5000:
            break

        try:
            # get data from the api
            response = requests.get(
                "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=56bcaf59a960c93b3e74daf8b8c937f2")
            if (response.status_code == 404):
                continue

            data = response.json()

            movie_id = data["id"]
            title = data["title"]
            rate = data["vote_average"]
            revenue = data["revenue"]
            release_date = data["release_date"]
            overview = data["overview"]
            runtime = data["runtime"]
            lang = data["spoken_languages"][0]["english_name"]

            # handle the case when there is no release date
            if release_date == '':
                release_date = None
                movie_data = (movie_id, title, rate, revenue, lang, runtime, overview)
                stmt = insert_movie_no_release
            else:
                movie_data = (movie_id, title, release_date, rate, revenue, lang, runtime, overview)
                stmt = insert_movie_stmt

            # insert generes into genres table and movie_genre table
            genres = data["genres"]

            # exeute queries
            try:
                cursor.execute(stmt, movie_data)
                added_movies += 1
            except:
                continue

            for genre in genres:
                if genre["id"] not in added_genres:
                    genre_data = (genre["id"], genre["name"])
                    try:
                        cursor.execute(insert_genre_stmt, genre_data)
                        added_genres.add(genre["id"])
                    except:
                        continue

                movie_genre_data = (movie_id, genre["id"])
                try:
                    cursor.execute(insert_movie_genre_stmt, movie_genre_data)
                except:
                    continue

            # commit 100 movies each time
            if added_movies % 100 == 0:
                cnx.commit()

        # handle errors
        except Exception as e:
            print("Error!", movie_id, "\n", e)
            problematics.add(movie_id)


    cursor.close()
    cnx.commit()
    cnx.close()

    print("!!!!!!!!!!!!finish all movies!!!!!!!!!!!")

# insert actors from API

def retrieve_actors():
    added_actors = 0
    problematics = set()
    cnx = mysql.connector.connect(host=hostname, user=username, password=password, db=database, port=port)
    cursor = cnx.cursor()

    # insert queries templates
    insert_actor_stmt = (
        "INSERT INTO actors (id, name, popularity) "
        "VALUES (%s, %s, %s)"
    )

    for actor_id in range(1, 220000):
        if added_actors >= 5000:
            break

        try:
            # get data from the api
            response = requests.get(
                "https://api.themoviedb.org/3/person/" + str(actor_id) + "?api_key=4dec3d85d9e68720edcce937fca2f95c")

            if (response.status_code == 404):
                continue
            elif response.json()["known_for_department"] != "Acting":
                continue

            data = response.json()

            actor_id = data["id"]
            name = data["name"]

            actor_data = (actor_id, name)

            # insert actors data to DB
            cursor.execute(insert_actor_stmt, actor_data)
            added_actors += 1

            # commit 100 movies each time
            if added_actors % 100 == 0:
                cnx.commit()

        # handle errors
        except Exception as e:
            print("Error!", e)
            problematics.add(actor_id);

    print("added_actors", added_actors)
    print(problematics)

    cursor.close()
    cnx.commit()
    cnx.close()

    print("!!!!!!!!!!!!finish all actors!!!!!!!!!!!")


def retrieve_characters():
    # get all actors ids
    problematics = set()
    cnx = mysql.connector.connect(host=hostname, user=username, password=password, db=database, port=port)

    cursor = cnx.cursor()
    select_stmt = (
        "select id from eyalgrinberg.actors"
    )

    cursor.execute(select_stmt)
    results = [result[0] for result in cursor.fetchall()]
    results = sorted(results)
    print(len(results))
    print(results[:5])

    cursor.close()
    cnx.close()



    # insert characters from API
    cnx = mysql.connector.connect(host=hostname, user=username, password=password, db=database, port=port)
    cursor = cnx.cursor()

    added_actors = 0

    insert_character_stmt = (
        "INSERT INTO characters (actor_id, movie_id, name) "
        "VALUES (%s, %s, %s)"
    )


    for person_id in results:

        try:
            # get data from the api
            response = requests.get("https://api.themoviedb.org/3/person/" + str(
                person_id) + "/credits?api_key=4dec3d85d9e68720edcce937fca2f95c")
            if (response.status_code == 404):
                continue

            characters = response.json()

            # go over all actor's characters
            for data in characters["cast"]:

                name = data["character"]
                if name == "" or name is None:
                    continue

                movie_id = data["id"]
                character_data = (person_id, movie_id, name)
                try:

                    # execute the query and insert the character data into character table
                    cursor.execute(insert_character_stmt, character_data)
                except:
                    continue

            added_actors += 1

            # commit 100 actors each time
            if added_actors % 100 == 0:
                cnx.commit()

        # handle errors
        except Exception as e:
            print("Error! with ", person_id, "\n", e)
            problematics.add((person_id, name))

    cursor.close()
    cnx.commit()
    cnx.close()

    print("!!!!!!!!!!!!finish all characters!!!!!!!!!!!")


if __name__ == '__main__':
    hostname = '127.0.0.1'
    username = 'eyalgrinberg'
    password = 'eyalgrinb66437'
    database = 'eyalgrinberg'
    port = 3305

    '''To build the DB run following lines: 
    marked as comment because the DB already exists'''
    # create_tables()
    # retrieve_movies()
    # retrieve_actors()
    # retrieve_characters()


