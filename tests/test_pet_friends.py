from app import PetFriends
from settings import user_email, user_passwd
import os


pf = PetFriends()


def test_get_api_key_valid_user(email=user_email, passwd=user_passwd):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, passwd)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(user_email, user_passwd)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_key(name='Гаага', animal_type='Гусь',
                                    age='3', pet_photo='images/goose.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(user_email, user_passwd)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def tests_delete_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(user_email, user_passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets) == 0:
        pf.add_new_pet(auth_key, 'Гаага111', 'Гусь111', '999', 'images/goose.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()
