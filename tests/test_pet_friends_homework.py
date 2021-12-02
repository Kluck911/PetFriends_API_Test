from app import PetFriends
from settings import invalid_user, invalid_passwd, user_email, user_passwd
import os


pf = PetFriends()


def test_get_api_key_invalid_email(email=invalid_passwd, passwd=user_passwd):
    """ Проверяем что запрос api ключа возвращает статус 403 если email не валидный"""

    status, _ = pf.get_api_key(email, passwd)
    assert status == 403


def test_get_api_key_invalid_pass(email=user_email, passwd=invalid_passwd):
    """ Проверяем что запрос api ключа возвращает статус 403 если пароль не валидный"""

    status, _ = pf.get_api_key(email, passwd)
    assert status == 403


def test_get_list_of_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает статус 403 если
    полученный ключ не валидный"""

    status, _ = pf.get_list_of_pets({'key': '111'}, filter)

    assert status == 403


