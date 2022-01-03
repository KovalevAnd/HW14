from flask import Flask, jsonify
from func import find_film_by_title, find_film_by_two_years, find_film_by_rating, find_fresh10_films_by_genre, \
    find_actors, find_films_by_type_year_genre

app = Flask(__name__)


@app.route('/movie/<title>')
def page_by_title(title):
    movie = find_film_by_title(title)
    return jsonify(movie)


@app.route('/movie/year/<year_from>/to/<year_to>')
def page_by_two_years(year_from, year_to):
    movie = find_film_by_two_years(year_from, year_to)
    return jsonify(movie)


@app.route('/rating/<rating_group>')
def page_by_rating(rating_group):
    movie = find_film_by_rating(rating_group)
    return jsonify(movie)


@app.route('/genre/<genre>')
def page_by_genre(genre):
    movie = find_fresh10_films_by_genre(genre)
    return jsonify(movie)


@app.route('/actors/<actor_first>/<actor_second>')
def page_by_actor(actor_first, actor_second):
    movie = find_actors(actor_first, actor_second)
    return jsonify(movie)


@app.route('/multifind/<type_film>/<year>/<genre>')
def page_multifind(type_film, year, genre):
    movie = find_films_by_type_year_genre(type_film, year, genre)
    return jsonify(movie)


app.run()
