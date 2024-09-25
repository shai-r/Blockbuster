from operator import attrgetter
from returns.maybe import Maybe, Nothing
from returns.result import Result, Success, Failure
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from config.base import session_factory
from models import Movie, Rental

def insert_movie(movie: Movie) -> Result[Movie, str]:
    with session_factory() as session:
        try:
            session.add(movie)
            session.commit()
            session.refresh(movie)
            return Success(movie)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_movie_by_id(m_id: int) -> Maybe[Movie]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Movie)
            .filter(Movie.id == m_id)
            .first()
        )

def find_movies_by_movie_gener(m_gener :str) -> List[Movie]:
    with session_factory() as session:
        return session.query(Movie).filter(Movie.movie_gener == m_gener).all()

def find_movie_by_movie_year(m_year :int) -> List[Movie]:
    with session_factory() as session:
        return session.query(Movie).filter(Movie.movie_year == m_year).all()

def delete_movie(m_id: int) -> Result[Movie, str]:
    with session_factory() as session:
        try:
            maybe_movie = find_movie_by_id(m_id)
            if maybe_movie is Nothing:
                return Failure(f"No movie by the id {m_id}")
            movie_to_delete = maybe_movie.unwrap()
            session.delete(movie_to_delete)
            session.commit()
            return Success(movie_to_delete)
        except SQLAlchemyError as e:
            return Failure(str(e))

def update_movie(m_id: int, movie: Movie) -> Result[Movie, str]:
    with session_factory() as session:
        try:
            maybe_movie = find_movie_by_id(m_id)
            if maybe_movie is Nothing:
                return Failure(f"No movie by the id {m_id}")
            movie_to_update = session.merge(maybe_movie.unwrap())
            movie_to_update.movie_gener = movie.movie_gener or movie_to_update.movie_gener
            movie_to_update.movie_year = movie.movie_year or movie_to_update.movie_year
            movie_to_update.movie_title = movie.movie_title or movie_to_update.movie_title
            session.commit()
            session.refresh(movie_to_update)
            return Success(movie_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_rentals_of_movie_by_id(m_id:int) -> List[Rental]:
    with session_factory() as session:
        return (find_movie_by_id(m_id)
                .map(session.merge)
                .map(attrgetter("rentals"))
                .value_or([])
        )