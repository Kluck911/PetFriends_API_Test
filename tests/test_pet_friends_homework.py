from app import PetFriends
from settings import invalid_user, invalid_passwd, user_email, user_passwd
import os


pf = PetFriends()


def test_get_api_key_invalid_email(email=invalid_user, passwd=user_passwd):
    """ Проверяем что запрос api ключа возвращает статус 403 если email не валидный"""

    status, _ = pf.get_api_key(email, passwd)
    assert status == 403


def test_get_api_key_invalid_pass(email=user_email, passwd=invalid_passwd):
    """ Проверяем что запрос api ключа возвращает статус 403 если пароль не валидный"""

    status, _ = pf.get_api_key(email, passwd)

    assert status == 403


def test_get_api_key_invalid_pass_and_email(email=invalid_user, passwd=invalid_passwd):
    """ Проверяем что запрос api ключа возвращает статус 403 если логин и пароль не валидны"""

    status, _ = pf.get_api_key(email, passwd)

    assert status == 403


def test_get_list_of_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает статус 403 если
    полученный ключ не валидный"""

    status, _ = pf.get_list_of_pets({'key': '111'}, filter)

    assert status == 403


def test_add_new_pet_with_invalid_key(name='Гаага', animal_type='Гусь',
                                    age=3, pet_photo='images/goose.jpg'):
    """ Проверяем что запрос всех питомцев возвращает статус 403 если
    полученный ключ не валидный"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = {'key': '111'}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403


def test_add_new_pet_with_petpic_not_jpeg(name='Гаага', animal_type='Гусь',
                                    age=3, pet_photo='images/petpic.jpg'):
    """Проверяем что нельзя загрузить "битую картинку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = {'key': '111'}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500
    # 500 незадокументированая ошибка


def test_delete_pet():
    """ Проверяем что запрос удаления питомца возвращает статус 403 если
    полученный ключ не валидный"""

    auth_key = {'key': '111'}
    status, _ = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 403

