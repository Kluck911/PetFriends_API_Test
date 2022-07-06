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


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    stop_time = datetime.now()
    print(f'\nТест шел: {stop_time-start_time}')