from datetime import date
from operator import attrgetter
from returns.maybe import Maybe, Nothing
from returns.result import Result, Success, Failure
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from config.base import session_factory
from models import Rental


def insert_rental(rental: Rental) -> Result[Rental, str]:
    with session_factory() as session:
        try:
            session.add(rental)
            session.commit()
            session.refresh(rental)
            return Success(rental)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def get_all_rentals():
    with session_factory() as session:
        return session.query(Rental).all()

def find_rental_by_id(r_id: int) -> Maybe[Rental]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Rental)
            .filter(Rental.id == r_id)
            .first()
        )

def find_all_rentals_by_rental_date(rental_date :date) -> List[Rental]:
    with session_factory() as session:
        return session.query(Rental).filter(Rental.rental_date == rental_date).all()

def find_all_rentals_by_return_date(return_date :date) -> List[Rental]:
    with session_factory() as session:
        return session.query(Rental).filter(Rental.return_date == return_date).all()

def delete_rental(r_id: int) -> Result[Rental, str]:
    with session_factory() as session:
        try:
            maybe_rental = find_rental_by_id(r_id)
            if maybe_rental is Nothing:
                return Failure(f"No rental by the id {r_id}")
            rental_to_delete = maybe_rental.unwrap()
            session.delete(rental_to_delete)
            session.commit()
            return Success(rental_to_delete)
        except SQLAlchemyError as e:
            return Failure(str(e))

def update_rental(r_id: int, rental: Rental) -> Result[Rental, str]:
    with session_factory() as session:
        try:
            maybe_rental = find_rental_by_id(r_id)
            if maybe_rental is Nothing:
                return Failure(f"No rental by the id {r_id}")
            rental_to_update = session.merge(maybe_rental.unwrap())
            rental_to_update.rental_date = rental.rental_date or rental_to_update.rental_date
            rental_to_update.return_date = rental.return_date or rental_to_update.return_date
            session.commit()
            session.refresh(rental_to_update)
            return Success(rental_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
