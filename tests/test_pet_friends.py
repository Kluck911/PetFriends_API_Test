from app import PetFriends
from settings import user_email, user_passwd


pf = PetFriends()


def test_get_api_key_valid_user(user_email, passwd=user_passwd):
    status, result = pf.get_api_key(email, passwd)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(user_email, user_passwd)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
