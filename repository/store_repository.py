from operator import attrgetter
from returns.maybe import Maybe, Nothing
from returns.result import Result, Success, Failure
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from config.base import session_factory
from models import Store, Subscriber

def insert_store(store: Store) -> Result[Store, str]:
    with session_factory() as session:
        try:
            session.add(store)
            session.commit()
            session.refresh(store)
            return Success(store)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_store_by_id(s_id: int) -> Maybe[Store]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Store)
            .filter(Store.id == s_id)
            .first()
        )

def find_stores_by_store_name(s_name :str) -> List[Store]:
    with session_factory() as session:
        return session.query(Store).filter(Store.store_name == s_name).all()

def find_store_by_store_state(s_state :str) -> List[Store]:
    with session_factory() as session:
        return session.query(Store).filter(Store.store_state == s_state).all()

def delete_store(s_id: int) -> Result[Store, str]:
    with session_factory() as session:
        try:
            maybe_store = find_store_by_id(s_id)
            if maybe_store is Nothing:
                return Failure(f"No store by the id {s_id}")
            store_to_delete = maybe_store.unwrap()
            session.delete(store_to_delete)
            session.commit()
            return Success(store_to_delete)
        except SQLAlchemyError as e:
            return Failure(str(e))

def update_store(s_id: int, store: Store) -> Result[Store, str]:
    with session_factory() as session:
        try:
            maybe_store = find_store_by_id(s_id)
            if maybe_store is Nothing:
                return Failure(f"No store by the id {s_id}")
            store_to_update = session.merge(maybe_store.unwrap())
            store_to_update.store_name = store.store_name or store_to_update.store_name
            store_to_update.store_state = store.store_state or store_to_update.store_state
            store_to_update.store_city = store.store_city or store_to_update.store_city
            store_to_update.store_address = store.store_address or store_to_update.store_address
            store_to_update.rental_fee = store.rental_fee or store_to_update.rental_fee
            store_to_update.late_fee = store.late_fee or store_to_update.late_fee
            session.commit()
            session.refresh(store_to_update)
            return Success(store_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_subscriptions_of_store_by_id(s_id:int) -> List[Subscriber]:
    with session_factory() as session:
        return (find_store_by_id(s_id)
                .map(session.merge)
                .map(attrgetter("subscribers"))
                .value_or([])
        )