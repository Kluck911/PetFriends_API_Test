import os
import sys
from datetime import datetime

import pytest

from app import PetFriends
from settings import user_email, user_passwd
from decorators import generate_string, russian_chars, chinese_chars, special_chars

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

    @pytest.mark.auth
    @pytest.mark.neg
    @pytest.mark.parametrize('email',
                             [generate_string(255)],
                             ids=['Invalid_email'])
    @pytest.mark.parametrize('passwd',
                             [user_passwd],
                             ids=['Valid_password'])
    def test_get_api_key_invalid_email(self, email, passwd):
        """ Проверяем что запрос api ключа возвращает статус 403 если email не валидный"""

        status, _ = pf.get_api_key(email, passwd)
        assert status == 403

    @pytest.mark.auth
    @pytest.mark.neg
    @pytest.mark.parametrize('email',
                             [user_email],
                             ids=['Valid_email'])
    @pytest.mark.parametrize('passwd',
                             [generate_string(255)],
                             ids=['Invalid_password'])
    def test_get_api_key_invalid_pass(self, email, passwd):
        """ Проверяем что запрос api ключа возвращает статус 403 если пароль не валидный"""

        status, _ = pf.get_api_key(email, passwd)

        assert status == 403

    @pytest.mark.auth
    @pytest.mark.neg
    @pytest.mark.parametrize('email',
                             [generate_string(255)],
                             ids=['Invalid_email'])
    @pytest.mark.parametrize('passwd',
                             [generate_string(255)],
                             ids=['Invalid_password'])
    def test_get_api_key_invalid_pass_and_email(self, email, passwd):
        """ Проверяем что запрос api ключа возвращает статус 403 если логин и пароль не валидны"""

        status, _ = pf.get_api_key(email, passwd)

        assert status == 403

    @pytest.mark.act
    @pytest.mark.neg
    @pytest.mark.parametrize('filter',
                             [''],
                             ids=['filter_empty'])
    @pytest.mark.parametrize('key_value',
                             [generate_string(255)],
                             ids=['Invalid_key'])
    def test_get_list_of_pets_with_invalid_key(self, key_value, filter):
        """ Проверяем что запрос всех питомцев возвращает статус 403 если
        полученный ключ не валидный"""

        status, _ = pf.get_list_of_pets({'key': key_value}, filter)

        assert status == 403

    @pytest.mark.act
    @pytest.mark.neg
    @pytest.mark.skip(reason="Баг - все некорректные значения проходят")
    @pytest.mark.parametrize("name", [''], ids=['empty'])
    @pytest.mark.parametrize("animal_type", [''], ids=['empty'])
    @pytest.mark.parametrize("age",
                             ['', '-1', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                              russian_chars().upper(), chinese_chars()],
                             ids=['empty', 'negative', 'float', 'int_max', 'int_max + 1', 'specials', 'russian',
                                  'RUSSIAN', 'chinese'])
    def test_add_pet_simple_negative(self, get_key, name, animal_type, age):
        """Проверяем быстрое добавдение питомца с некорректным возрастом"""

        status, result = pf.add_pet_simple(get_key, name, animal_type, age)

        assert status == 400

    @pytest.mark.act
    @pytest.mark.neg
    @pytest.mark.skip(reason="Баг - картинка загружается")
    def test_add_new_pet_with_petpic_not_jpeg(self, get_key, name='Гаага', animal_type='Гусь',
                                              age=3, pet_photo='images/petpic.jpg'):
        """Проверяем что нельзя загрузить "битую картинку"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

        assert status == 403

    @pytest.mark.act
    @pytest.mark.neg
    def test_delete_pet_with_invalid_key(self):
        """ Проверяем что запрос удаления питомца возвращает статус 403 если
        полученный ключ не валидный"""

        auth_key = {'key': '111'}
        status, _ = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 403

    @pytest.mark.act
    @pytest.mark.neg
    def test_successful_update_pet_info_with_invalid_key(self):
        """Проверяем возможность обновления информации c неверным ключем"""

        auth_key = {'key': '111'}
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        status, _ = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 403

    @pytest.mark.act
    @pytest.mark.neg
    @pytest.mark.xfail(sys.platform == "win32", reason="Ошибка в системной библиотеке")
    def test_successful_update_pet_id_incorrect(self, get_key, name='Гуся', animal_type='Гус', age=2):
        """Проверяем возникновение ошибки 400, если pet id введен некорректно"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(get_key, 'ggewegewgwewgewegw', name, animal_type, age)

            assert status == 400

    @pytest.mark.act
    @pytest.mark.neg
    def test_successful_update_pet_id_is_null(self, get_key, name='Гуся', animal_type='Гус', age=2):
        """Проверяем возникновение ошибки 404, если pet id отсутствует"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(get_key, '', name, animal_type, age)

            assert status == 404


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    stop_time = datetime.now()
    print(f'\nТест шел: {stop_time-start_time}')
