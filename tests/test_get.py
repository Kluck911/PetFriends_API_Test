import pytest

from app import PetFriends
from settings import my_user


pf = PetFriends()


class TestsGetAPI:
    @pytest.mark.get
    @pytest.mark.pos
    @pytest.mark.auth
    @pytest.mark.parametrize('email',
                             [my_user.login],
                             ids=['Valid_email'])
    @pytest.mark.parametrize('passwd',
                             [my_user.passwd],
                             ids=['Valid_password'])
    def test_get_api_key_valid_user(self, email, passwd):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        status, result = pf.get_api_key(email, passwd)
        assert status == 200
        assert 'key' in result

    @pytest.mark.get
    @pytest.mark.act
    @pytest.mark.pos
    @pytest.mark.parametrize("filter",
                             ['', 'my_pets'],
                             ids=['empty string', 'only my pets'])
    def test_get_list_of_pets_with_valid_key(self, get_key, filter):
        """ Проверяем что запрос всех питомцев возвращает не пустой список. """

        status, result = pf.get_list_of_pets(get_key, filter)
        if len(result['pets']) > 0:
            assert status == 200
            assert len(result['pets']) > 0
        else:
            raise Exception('У Вас нет питомцев, плак, плак :(')
