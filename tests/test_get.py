from datetime import datetime

import pytest

from app import PetFriends
from settings import user_email, user_passwd


pf = PetFriends()


@pytest.fixture(scope='class')
def get_key(email=user_email, passwd=user_passwd):

    status, result = pf.get_api_key(email, passwd)
    assert status == 200
    assert 'key' in result
    print('\nreturn auth_key')

    return result


@pytest.fixture(autouse=True)
def request_fixture(request):
    if "Pets" in request.cls.__name__:
        print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")


class TestsPetsAPI:
    @pytest.mark.pos
    @pytest.mark.auth
    @pytest.mark.parametrize('email',
                             [user_email],
                             ids=['Valid_email'])
    @pytest.mark.parametrize('passwd',
                             [user_passwd],
                             ids=['Valid_password'])
    def test_get_api_key_valid_user(self, email, passwd):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        status, result = pf.get_api_key(email, passwd)
        assert status == 200
        assert 'key' in result

    @pytest.mark.act
    @pytest.mark.pos
    @pytest.mark.parametrize("filter",
                             ['', 'my_pets'],
                             ids=['empty string', 'only my pets'])
    def test_get_list_of_pets_with_valid_key(self, get_key, filter):
        """ Проверяем что запрос всех питомцев возвращает не пустой список. """

        status, result = pf.get_list_of_pets(get_key, filter)
        assert status == 200
        assert len(result['pets']) > 0


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    stop_time = datetime.now()
    print(f'\nТест шел: {stop_time-start_time}')
