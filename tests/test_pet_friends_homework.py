from app import PetFriends
from settings import user_email, user_passwd
import os


pf = PetFriends()

def test_get_api_key_invalid_user(email=, passwd=user_passwd):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, passwd)
    assert status == 200
    assert 'key' in result