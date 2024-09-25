from operator import attrgetter
import pytest
from returns.maybe import Nothing
from returns.result import Failure
from repository.database import create_tables, drop_tables
from repository.movie_repository import insert_movie, find_movie_by_id, delete_movie, update_movie, \
    find_movies_by_movie_gener, find_movie_by_movie_year, find_rentals_of_movie_by_id
from models import Movie
import toolz as t
from operator import eq

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    insert_movie(Movie(movie_title='Shais movie', movie_gener='shais comedy', movie_year=1998))
    yield
    drop_tables()

def test_insert_movie(setup_database):
    movie = insert_movie(Movie(movie_title='Shais movie 2', movie_gener='shais comedy', movie_year=2000))
    assert movie.unwrap().id is not None

def test_find_user_by_id(setup_database):
    movie = find_movie_by_id(1)
    assert movie.unwrap().movie_title == 'Shais movie'
    movie = find_movie_by_id(-1)
    assert movie is Nothing

def test_find_movies_by_movie_gener(setup_database):
    movies = find_movies_by_movie_gener('shais comedy')
    assert len(movies) > 0
    movies = find_movies_by_movie_gener('')
    assert len(movies) == 0

def test_find_movie_by_movie_year(setup_database):
    movies = find_movie_by_movie_year(1998)
    assert len(movies) > 0
    movies = find_movie_by_movie_year(0)
    assert len(movies) == 0

def test_delete_movie(setup_database):
    deleted_movie =  delete_movie(1)
    assert (deleted_movie
             .map(attrgetter("id"))
             .map(t.partial(eq, 1))
             .value_or(False))

    assert isinstance(delete_movie(1), Failure)

def test_update_movie(setup_database):
    movie = update_movie(1, Movie(movie_year=1999))
    assert movie.unwrap().id == 1
    assert movie.unwrap().movie_title == 'Shais movie'
    assert movie.unwrap().movie_year == 1999
    assert isinstance(update_movie(2, Movie()), Failure)

def test_find_rentals_of_movie_by_id(setup_database):
    rentals = find_rentals_of_movie_by_id(1)
    assert len(rentals) == 0
