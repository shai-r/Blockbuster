from operator import attrgetter
from returns.maybe import Maybe, Nothing
from returns.result import Result, Success, Failure
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from config.base import session_factory
from models import Subscriber, Store, Rental


def insert_subscriber(subscriber: Subscriber) -> Result[Subscriber, str]:
    with session_factory() as session:
        try:
            session.add(subscriber)
            session.commit()
            session.refresh(subscriber)
            return Success(subscriber)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_subscriber_by_id(s_id: int) -> Maybe[Subscriber]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Subscriber)
            .filter(Subscriber.id == s_id)
            .first()
        )

def find_all_subscribers_who_owe_more_than(debt :float) -> List[Subscriber]:
    with session_factory() as session:
        return session.query(Subscriber).filter(Subscriber.total_payment > debt).all()

def delete_subscriber(s_id: int) -> Result[Subscriber, str]:
    with session_factory() as session:
        try:
            maybe_subscriber = find_subscriber_by_id(s_id)
            if maybe_subscriber is Nothing:
                return Failure(f"No subscription by the id {s_id}")
            subscriber_to_delete = maybe_subscriber.unwrap()
            session.delete(subscriber_to_delete)
            session.commit()
            return Success(subscriber_to_delete)
        except SQLAlchemyError as e:
            return Failure(str(e))

def update_subscriber(s_id: int, total_payment: float) -> Result[Subscriber, str]:
    with session_factory() as session:
        try:
            maybe_subscription = find_subscriber_by_id(s_id)
            if maybe_subscription is Nothing:
                return Failure(f"No subscription by the id {s_id}")
            subscriber_to_update = session.merge(maybe_subscription.unwrap())
            subscriber_to_update.total_payment = total_payment
            session.commit()
            session.refresh(subscriber_to_update)
            return Success(subscriber_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_rentals_of_subscriber_by_id(m_id:int) -> List[Rental]:
    with session_factory() as session:
        return (find_subscriber_by_id(m_id)
                .map(session.merge)
                .map(attrgetter("rentals"))
                .value_or([])
                )