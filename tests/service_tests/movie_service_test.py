import pytest
from repository.database import create_tables, drop_tables
from repository.movie_repository import insert_movie
from models import Movie
import toolz as t
from operator import eq

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    insert_movie(Movie(movie_title='Shais movie', movie_gener='shais comedy', movie_year=1998))
    insert_movie(Movie(movie_title='Shais movie', movie_gener='shais comedy', movie_year=1998))
    insert_movie(Movie(movie_title='Shais movie', movie_gener='shais drama', movie_year=1998))
    yield
    drop_tables()

# def test_(setup_database):
#     most_common_genre
