import sqlite3

DB_PATH = 'netflix.db'


def find_film_by_title(title):

    """**Шаг 1**
Реализуйте поиск по названию. Если таких фильмов несколько, выведите самый свежий.
Создайте представление для роута `/movie/title` , который бы выводил данные про фильм"""

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title = {title}
                ORDER BY release_year
                LIMIT 1
        """
        cursor.execute(query)
        row_data = cursor.fetchone()
        data = {
            "title": row_data[0],
            "country": row_data[1],
            "release_year": row_data[2],
            "genre": row_data[3],
            "description": row_data[4]
        }
        return data


def find_film_by_two_years(year_1, year_2):

    """**Шаг 2**

Сделайте поиск по диапазону лет выпуска. Фильмов будет много, так что ограничьте вывод 100 тайтлами.
Создайте представление для роута `/movie/year`, который бы выводил список словарей"""

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT title, release_year
                from netflix
                WHERE release_year BETWEEN {year_1} AND {year_2}
                limit 100
        """
        cursor.execute(query)
        row_data = cursor.fetchall()
        data = []
        for i in row_data:
            k = {
                "title": i[0],
                "release_year": i[1]
            }
            data.append(k)

        return data


def find_film_by_rating(rating):
    """**Шаг 3**

Реализуйте поиск по рейтингу. Определите группы: для детей, для семейного просмотра, для взрослых.

    :param rating:
    children - G
    family - PG, PG-13
    adult - R, NC-17
    :return:
    """
    if rating == 'children':
        rating_for_query = 'G'
    elif rating == 'family':
        rating_for_query = 'PG' + "'" + ',' + "'" + 'PG-13'
    elif rating == 'adult':
        rating_for_query = 'R' + "'" + ',' + "'" + 'NC-17'
    else:
        return 'error: incorrect rating'

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating in ('{rating_for_query}')
        """
        cursor.execute(query)
        row_data = cursor.fetchall()
        data = []
        for i in row_data:
            k = {
                "title": i[0],
                "rating": i[1],
                "description": i[2]
            }
            data.append(k)
        return data


def find_fresh10_films_by_genre(genre):

    """**Шаг 4**

Напишите функцию, которая получает название жанра в качестве аргумента и возвращает 10
самых свежих фильмов в формате json. В результате должно содержаться название и описание каждого фильма."""

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT title, description from netflix 
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY date_added DESC 
                limit 10
        """
        cursor.execute(query)
        row_data = cursor.fetchall()
        data = []
        for i in row_data:
            k = {
                "title": i[0],
                "description": i[1]
            }
            data.append(k)

        return data


def find_actors(first_actor, second_actor):

    """**Шаг 5**

Напишите функцию, которая получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
и возвращает список тех, кто играет с ними в паре больше 2 раз. В качестве теста можно передать:
Rose McIver и Ben Lamb, Jack Black и Dustin Hoffman."""

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT GROUP_CONCAT("cast", ',') as "cast" from netflix 
                WHERE "cast" LIKE '%{first_actor}%' AND "cast" LIKE '%{second_actor}%'
        """
        cursor.execute(query)
        row_data = cursor.fetchone()
        actors_list = row_data[0].split(', ')
        actors_list_unique = set(actors_list)
        actors_list_unique.remove(first_actor)
        actors_list_unique.remove(second_actor)
        actors_list_unique = str(actors_list_unique)
        actors_list_unique = actors_list_unique.replace('{', '')
        actors_list_unique = actors_list_unique.replace('}', '')
        actors_list_unique = actors_list_unique.replace("'", '')

        data = {
            "actors_list": actors_list_unique
        }

        return data


def find_films_by_type_year_genre(type_film, year, genre):

    """**Шаг 6**

Напишите функцию, с помощью которой можно будет передавать тип картины (фильм или сериал), год выпуска и ее жанр
в БД с помощью SQL-запроса и получать на выходе список названий картин с их описаниями в JSON."""

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f"""
        SELECT title, description
        from netflix
        WHERE "type" = '{type_film}'
        AND release_year = '{year}'
        AND listed_in LIKE '%{genre}%'
"""


        cursor.execute(query)
        row_data = cursor.fetchall()
        data = []
        for i in row_data:
            k = {
                "title": i[0],
                "description": i[1]
            }
            data.append(k)

        return data


#print(find_films_by_type_year_genre('TV Show', '2020', 'drama'))