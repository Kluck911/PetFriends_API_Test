import pytest

from app import PetFriends
from settings import user_email, user_passwd


pf = PetFriends()


def get_key(email=user_email, passwd=user_passwd):

    status, result = pf.get_api_key(email, passwd)
    assert status == 200
    assert 'key' in result
    print('\nreturn auth_key')

    return result


class TestsPetsAPI:
    @pytest.mark.del_all
    def test_delete_all_pet(self, get_key):
        """Удаляем всех созданных питомцев"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        while len(my_pets['pets']) > 0:
            for i in range(len(my_pets['pets'])):
                pet_id = my_pets['pets'][i]['id']
                status, _ = pf.delete_pet(get_key, pet_id)

                assert status == 200
            _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        assert len(my_pets['pets']) == 0
