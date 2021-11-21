from app import PetFriends
from settings import user_email, user_passwd


pf = PetFriends()

def test_get_API_key_valid_user(email=user_email, passwd=user_passwd):
    status, result = pf.get_API_key(email, passwd)
    assert status == 200
    assert 'key' in result
