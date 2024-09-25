from datetime import datetime, date
from operator import attrgetter
import pytest
from returns.maybe import Nothing
from returns.result import Failure
from repository.database import create_tables, drop_tables
from repository.movie_repository import insert_movie
from repository.store_repository import insert_store
from repository.rental_repository import insert_rental, find_rental_by_id, find_all_rentals_by_rental_date, \
    find_all_rentals_by_return_date, delete_rental, update_rental, get_all_rentals
from models import Subscriber, Rental, Store, User, Movie
import toolz as t
from operator import eq
from repository.subscriber_repository import insert_subscriber
from repository.user_repository import insert_user


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    insert_user(User(user_name='Shai', user_email='shai@gmail.com', user_phone='0551234567'))
    insert_store(Store(store_name='Shai store', store_state='NY', store_city='NY',
                       store_address='Kadachat 6', rental_fee=70.4, late_fee=7.04))
    insert_movie(Movie(movie_title='Shais movie', movie_gener='shais comedy', movie_year=1998))
    insert_subscriber(Subscriber(user_id=1, store_id=1, total_payment=55.5))
    insert_rental(Rental(subscription_id=1, movie_id=1, rental_date=datetime(year=2000, month=12, day=21),
                         return_date=datetime.now().date()))
    yield
    drop_tables()

def test_insert_rental(setup_database):
    subscription = insert_rental(Rental(subscription_id=1, movie_id=1, rental_date=datetime.now().date()))
    assert subscription.unwrap().id is not None

def test_get_all_rentals(setup_database):
    rentals = get_all_rentals()
    assert len(rentals) > 0

def test_find_rental_by_id(setup_database):
    rental = find_rental_by_id(1)
    assert rental.unwrap().rental_date == date(year=2000, month=12, day=21)
    rental = find_rental_by_id(-1)
    assert rental is Nothing

def test_find_all_rentals_by_rental_date(setup_database):
    rentals = find_all_rentals_by_rental_date(date(year=2000, month=12, day=21))
    assert len(rentals) > 0
    rentals = find_all_rentals_by_rental_date(datetime.now().date())
    assert len(rentals) == 0

def test_find_all_rentals_by_return_date(setup_database):
    rentals = find_all_rentals_by_return_date(datetime.now().date())
    assert len(rentals) > 0
    rentals = find_all_rentals_by_return_date(date(year=2000, month=12, day=21))
    assert len(rentals) == 0

def test_delete_rental(setup_database):
    deleted_rental =  delete_rental(1)
    assert (deleted_rental
             .map(attrgetter("id"))
             .map(t.partial(eq, 1))
             .value_or(False))

    assert isinstance(delete_rental(1), Failure)

def test_update_rental(setup_database):
    subscriber = update_rental(1, rental=Rental(rental_date=date(year=2022, month=12, day=31)))
    assert subscriber.unwrap().id == 1
    assert subscriber.unwrap().rental_date == date(year=2022, month=12, day=31)
    assert subscriber.unwrap().return_date == datetime.now().date()
    assert isinstance(update_rental(2, Rental(rental_date=date(year=2022, month=12, day=31))), Failure)
