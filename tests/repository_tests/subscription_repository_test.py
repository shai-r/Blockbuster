from operator import attrgetter
import pytest
from returns.maybe import Nothing
from returns.result import Failure
from repository.database import create_tables, drop_tables
from repository.store_repository import insert_store
from repository.subscriber_repository import insert_subscriber, find_subscriber_by_id, \
    find_all_subscribers_who_owe_more_than, delete_subscriber, update_subscriber, find_rentals_of_subscriber_by_id
from models import Subscriber, User, Store
import toolz as t
from operator import eq

from repository.user_repository import insert_user


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    insert_user(User(user_name='Shai', user_email='shai@gmail.com', user_phone='0551234567'))
    insert_store(Store(store_name='Shai store', store_state='NY', store_city='NY',
                       store_address='Kadachat 6', rental_fee=70.4, late_fee=7.04))
    insert_subscriber(Subscriber(user_id=1, store_id=1, total_payment=55.5))
    yield
    drop_tables()

def test_insert_subscription(setup_database):
    subscription = insert_subscriber(Subscriber(user_id=1, store_id=1, total_payment=66.539))
    assert subscription.unwrap().id is not None

def test_find_subscription_by_id(setup_database):
    subscription = find_subscriber_by_id(1)
    assert subscription.unwrap().total_payment == 55.5
    subscription = find_subscriber_by_id(-1)
    assert subscription is Nothing

def test_find_all_subscribers_who_owe_more_than(setup_database):
    subscribers = find_all_subscribers_who_owe_more_than(10)
    assert len(subscribers) > 0
    subscribers = find_all_subscribers_who_owe_more_than(10000000)
    assert len(subscribers) == 0

def test_delete_subscriber(setup_database):
    deleted_subscriber =  delete_subscriber(1)
    assert (deleted_subscriber
             .map(attrgetter("id"))
             .map(t.partial(eq, 1))
             .value_or(False))

    assert isinstance(delete_subscriber(1), Failure)

def test_update_subscriber(setup_database):
    subscriber = update_subscriber(1, 88.987)
    assert subscriber.unwrap().id == 1
    assert subscriber.unwrap().user_id == 1
    assert subscriber.unwrap().store_id == 1
    assert isinstance(update_subscriber(2, 2), Failure)

def test_find_rentals_of_subscriber_by_id(setup_database):
    rentals = find_rentals_of_subscriber_by_id(1)
    assert len(rentals) == 0
