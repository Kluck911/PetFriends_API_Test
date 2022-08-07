import pytest

from app import PetFriends

from settings import my_user
from datetime import datetime


pf = PetFriends()


@pytest.fixture(scope='class')
def get_key(email=my_user.login, passwd=my_user.passwd):

    status, result = pf.get_api_key(email, passwd)
    assert status == 200
    assert 'key' in result

    return result


@pytest.fixture(autouse=True)
def request_fixture(request):
    if "Pets" in request.cls.__name__:
        print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    stop_time = datetime.now()
    print(f'\nТест шел: {stop_time-start_time}')
