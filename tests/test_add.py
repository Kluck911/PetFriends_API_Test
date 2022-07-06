import os
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
    @pytest.mark.act
    @pytest.mark.pos
    def test_add_new_pet_with_valid_key(self, get_key, name='Гаага', animal_type='Гусь',
                                        age=3, pet_photo='images/goose.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

        assert status == 200
        assert result['name'] == name

    @pytest.mark.act
    @pytest.mark.pos
    def test_add_pet_simple_with_valid_key(self, get_key, name='Гагага', animal_type='Гусь', age=3):
        """Проверяем что можно добавить питомца с корректными данными"""

        status, result = pf.add_pet_simple(get_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    @pytest.mark.act
    @pytest.mark.pos
    def test_add_photo_of_pet_with_valid_key(self, get_key, name='Гусек', animal_type='Гусь', age=35,
                                             pet_photo='images/goose2.jpg'):
        """Проверяем что можно добавить фото для питомца созданного при помощи
        add_pet_simple с корректными данными"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, my_pet_without_photo = pf.add_pet_simple(get_key, name, animal_type, age)
        pet_id = my_pet_without_photo['id']

        status, result = pf.add_photo_of_pet(get_key, pet_id, pet_photo)

        assert status == 200
        assert result['name'] == name


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    stop_time = datetime.now()
    print(f'\nТест шел: {stop_time-start_time}')
