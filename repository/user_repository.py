from operator import attrgetter
from returns.maybe import Maybe, Nothing
from returns.result import Result, Success, Failure
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from config.base import session_factory
from models import User, Subscriber

def insert_user(user: User) -> Result[User, str]:
    with session_factory() as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return Success(user)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def get_all_users():
    with session_factory() as session:
        return session.query(User).all()

def find_user_by_id(u_id: int) -> Maybe[User]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(User)
            .filter(User.id == u_id)
            .first()
        )

def find_user_by_email(u_email :str) ->Maybe[User]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(User)
            .filter(User.user_email == u_email)
            .first()
        )

def find_users_by_user_name(u_name :str) -> List[User]:
    with session_factory() as session:
        return session.query(User).filter(User.user_name == u_name).all()

def delete_user(u_id: int) -> Result[User, str]:
    with session_factory() as session:
        try:
            maybe_user = find_user_by_id(u_id)
            if maybe_user is Nothing:
                return Failure(f"No user by the id {u_id}")
            user_to_delete = maybe_user.unwrap()
            session.delete(user_to_delete)
            session.commit()
            return Success(user_to_delete)
        except SQLAlchemyError as e:
            return Failure(str(e))

def update_user(u_id: int, user: User) -> Result[User, str]:
    with session_factory() as session:
        try:
            maybe_user = find_user_by_id(u_id)
            if maybe_user is Nothing:
                return Failure(f"No user by the id {u_id}")
            user_to_update = session.merge(maybe_user.unwrap())
            user_to_update.user_name = user.user_name or user_to_update.user_name
            user_to_update.user_email = user.user_email or user_to_update.user_email
            user_to_update.user_phone = user.user_phone or user_to_update.user_phone
            session.commit()
            session.refresh(user_to_update)
            return Success(user_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))

def find_subscriptions_of_user_by_id(u_id:int) -> List[Subscriber]:
    with session_factory() as session:
        return (find_user_by_id(u_id)
                .map(session.merge)
                .map(attrgetter("subscribers"))
                .value_or([])
        )