import pytest
import os
from app import PetFriends
from settings import user_email, user_passwd
from datetime import datetime

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
    def test_get_api_key_valid_user(self, email=user_email, passwd=user_passwd):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        status, result = pf.get_api_key(email, passwd)
        assert status == 200
        assert 'key' in result

    @pytest.mark.act
    @pytest.mark.pos
    def test_get_list_of_pets_with_valid_key(self, get_key, filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список. """

        status, result = pf.get_list_of_pets(get_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

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
    def test_delete_pet(self, get_key):
        """Проверяем возможность удаления питомца"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        if len(my_pets) == 0:
            pf.add_new_pet(get_key, 'Гаага111', 'Гусь111', 999, 'images/goose.jpg')
            _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(get_key, pet_id)

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        assert status == 200
        assert pet_id not in my_pets.values()

    @pytest.mark.act
    @pytest.mark.pos
    def test_successful_update_pet_info(self, get_key, name='Гуся', animal_type='Гус', age=5):
        """Проверяем возможность обновления информации о питомце"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

            assert status == 200
            assert result['name'] == name
        else:
            raise Exception('У Вас нет питомцев, плак, плак :(')

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
