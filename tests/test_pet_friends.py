from app import PetFriends
from settings import user_email, user_passwd


pf = PetFriends()

def test_get_API_key_valid_user(user_email, user_paswd):
    status, result = pf.get_API_key(user_email, user_paswd)
    print(status, result)