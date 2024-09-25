from operator import attrgetter
import pytest
from returns.maybe import Nothing
from returns.result import Failure
from repository.database import create_tables, drop_tables
from repository.store_repository import insert_store, find_store_by_id, find_stores_by_store_name, \
    find_store_by_store_state, delete_store, update_store, find_subscriptions_of_store_by_id, get_all_stores
from models import Store
import toolz as t
from operator import eq

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    insert_store(Store(store_name='Shai store', store_state='NY', store_city='NY',
                       store_address='Kadachat 6', rental_fee=70.4, late_fee=7.04))
    yield
    drop_tables()

def test_insert_store(setup_database):
    store = insert_store(Store(store_name='Shalom store', store_state='NG', store_city='BRO',
                               store_address='Kadachat 99', rental_fee=45.4, late_fee=4.54))
    assert store.unwrap().id is not None

def test_get_all_stores(setup_database):
    stores = get_all_stores()
    assert len(stores) > 0

def test_find_store_by_id(setup_database):
    store = find_store_by_id(1)
    assert store.unwrap().store_name == 'Shai store'
    store = find_store_by_id(-1)
    assert store is Nothing

def test_find_stores_by_user_name(setup_database):
    stores = find_stores_by_store_name('Shai store')
    assert len(stores) > 0
    stores = find_stores_by_store_name('')
    assert len(stores) == 0

def test_find_store_by_store_store(setup_database):
    store = find_store_by_store_state('NY')
    assert len(store) > 0
    store = find_store_by_store_state('')
    assert len(store) == 0

def test_delete_store(setup_database):
    deleted_store =  delete_store(1)
    assert (deleted_store
             .map(attrgetter("id"))
             .map(t.partial(eq, 1))
             .value_or(False))

    assert isinstance(delete_store(1), Failure)

def test_update_store(setup_database):
    store = update_store(1, Store(store_name='Shalom store'))
    assert store.unwrap().id == 1
    assert store.unwrap().store_name == 'Shalom store'
    assert store.unwrap().store_state == 'NY'
    assert isinstance(update_store(2, Store()), Failure)

def test_find_subscriptions_of_store_by_id(setup_database):
    subscription = find_subscriptions_of_store_by_id(1)
    assert len(subscription) == 0
