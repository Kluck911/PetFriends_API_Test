import pytest
import requests
from app import PetFriends
from settings import invalid_user, invalid_passwd, user_email, user_passwd
from datetime import datetime
import os


pf = PetFriends()


@pytest.fixture(scope='class')
def get_key():
    response = requests.post(url='https://petfriends1.herokuapp.com/login',
                             data={"email": user_email, "pass": user_passwd})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    print('\nreturn auth_key')
    return response.request.headers.get('Cookie')



class TestsPetsAPI:

    def test_get_api_key_valid_user(self, email=user_email, passwd=user_passwd):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        status, result = pf.get_api_key(email, passwd)
        assert status == 200
        assert 'key' in result

    def test_get_list_of_pets_with_valid_key(self, filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список. """

        _, auth_key = pf.get_api_key(user_email, user_passwd)
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_key(self, name='Гаага', animal_type='Гусь',
                                        age=3, pet_photo='images/goose.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(user_email, user_passwd)

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        assert status == 200
        assert result['name'] == name

    def test_delete_pet(self):
        """Проверяем возможность удаления питомца"""

        _, auth_key = pf.get_api_key(user_email, user_passwd)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets) == 0:
            pf.add_new_pet(auth_key, 'Гаага111', 'Гусь111', 999, 'images/goose.jpg')
            _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert pet_id not in my_pets.values()

    def test_successful_update_pet_info(self, name='Гуся', animal_type='Гус', age=5):
        """Проверяем возможность обновления информации о питомце"""

        _, auth_key = pf.get_api_key(user_email, user_passwd)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            assert status == 200
            assert result['name'] == name
        else:
            raise Exception('У Вас нет питомцев, плак, плак :(')

    def test_add_pet_simple_with_valid_key(self, name='Гагага', animal_type='Гусь', age=3):
        """Проверяем что можно добавить питомца с корректными данными"""

        _, auth_key = pf.get_api_key(user_email, user_passwd)

        status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    def test_add_photo_of_pet_with_valid_key(self, name='Гусек', animal_type='Гусь', age=35, pet_photo='images/goose2.jpg'):
        """Проверяем что можно добавить фото для питомца созданного при помощи
        add_pet_simple с корректными данными"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, auth_key = pf.get_api_key(user_email, user_passwd)
        _, my_pet_without_photo = pf.add_pet_simple(auth_key, name, animal_type, age)
        pet_id = my_pet_without_photo['id']

        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['name'] == name

    def test_get_api_key_invalid_email(self, email=invalid_user, passwd=user_passwd):
        """ Проверяем что запрос api ключа возвращает статус 403 если email не валидный"""

        status, _ = pf.get_api_key(email, passwd)
        assert status == 403

    def test_get_api_key_invalid_pass(self, email=user_email, passwd=invalid_passwd):
        """ Проверяем что запрос api ключа возвращает статус 403 если пароль не валидный"""

        status, _ = pf.get_api_key(email, passwd)

        assert status == 403

    def test_get_api_key_invalid_pass_and_email(self, email=invalid_user, passwd=invalid_passwd):
        """ Проверяем что запрос api ключа возвращает статус 403 если логин и пароль не валидны"""

        status, _ = pf.get_api_key(email, passwd)

        assert status == 403

    def test_get_list_of_pets_with_invalid_key(self, filter=''):
        """ Проверяем что запрос всех питомцев возвращает статус 403 если
        полученный ключ не валидный"""

        status, _ = pf.get_list_of_pets({'key': '111'}, filter)

        assert status == 403

    def test_add_new_pet_with_invalid_key(self, name='Гаага', animal_type='Гусь',
                                          age=3, pet_photo='images/goose.jpg'):
        """ Проверяем что запрос всех питомцев возвращает статус 403 если
        полученный ключ не валидный"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = {'key': '111'}

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        assert status == 403

    def test_add_new_pet_with_petpic_not_jpeg(self, name='Гаага', animal_type='Гусь',
                                              age=3, pet_photo='images/petpic.jpg'):
        """Проверяем что нельзя загрузить "битую картинку"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        auth_key = {'key': '111'}

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        assert status == 500  # 500 незадокументированая ошибка

    def test_delete_pet_with_invalid_key(self):
        """ Проверяем что запрос удаления питомца возвращает статус 403 если
        полученный ключ не валидный"""

        auth_key = {'key': '111'}
        status, _ = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 403

    def test_successful_update_pet_info_with_invalid_key(self):
        """Проверяем возможность обновления информации c неверным ключем"""

        auth_key = {'key': '111'}
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        status, _ = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 403

    def test_successful_update_pet_id_incorrect(self, name='Гуся', animal_type='Гус', age=2):
        """Проверяем возникновение ошибки 400, если pet id введен некорректно"""

        _, auth_key = pf.get_api_key(user_email, user_passwd)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, 'ggewegewgwewgewegw', name, animal_type, age)

            assert status == 400

    def test_successful_update_pet_id_is_null(self, name='Гуся', animal_type='Гус', age=2):
        """Проверяем возникновение ошибки 404, если pet id отсутствует"""

        _, auth_key = pf.get_api_key(user_email, user_passwd)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, '', name, animal_type, age)

            assert status == 404  # 500 незадокументированая ошибка


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    stop_time = datetime.now()
    print(f'\nТест шел: {stop_time-start_time}')
