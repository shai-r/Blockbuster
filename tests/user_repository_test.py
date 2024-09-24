from operator import attrgetter
import pytest
from returns.maybe import Nothing
from returns.result import Failure
from repository.database import create_tables, drop_tables
from repository.user_repository import insert_user, find_user_by_id, find_users_by_user_name, find_user_by_email, \
    delete_user, update_user, find_subscriptions_of_user_by_id
from models import User
import toolz as t
from operator import eq

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    insert_user(User(user_name='Shai', user_email='shai@gmail.com', user_phone='0551234567'))
    yield
    drop_tables()

def test_insert_user(setup_database):
    user = insert_user(User(user_name='Shalom', user_email='shalom@gmail.com', user_phone='055234561'))
    assert user.unwrap().id is not None

def test_find_user_by_id(setup_database):
    user = find_user_by_id(1)
    assert user.unwrap().user_name == 'Shai'
    user = find_user_by_id(-1)
    assert user is Nothing

def test_find_users_by_user_name(setup_database):
    users = find_users_by_user_name('Shai')
    assert len(users) > 0
    users = find_users_by_user_name('')
    assert len(users) == 0

def test_find_user_by_email(setup_database):
    user = find_user_by_email('shai@gmail.com')
    assert user.unwrap().id == 1
    user = find_user_by_email('')
    assert user is Nothing

def test_delete_user(setup_database):
    deleted_user =  delete_user(1)
    assert (deleted_user
             .map(attrgetter("id"))
             .map(t.partial(eq, 1))
             .value_or(False))

    assert isinstance(delete_user(1), Failure)

def test_update_user(setup_database):
    user = update_user(1, User(user_name='Shai Reiner'))
    assert user.unwrap().id == 1
    assert user.unwrap().user_name == 'Shai Reiner'
    assert user.unwrap().user_email == 'shai@gmail.com'
    assert isinstance(update_user(2, User()), Failure)

def test_find_subscriptions_of_user_by_id(setup_database):
    subscription = find_subscriptions_of_user_by_id(1)
    assert len(subscription) == 0
