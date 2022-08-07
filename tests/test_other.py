import pytest

from app import PetFriends
from decorators import generate_string, chinese_chars, russian_chars, special_chars


pf = PetFriends()


class TestsPetsAPI:
    @pytest.mark.act
    @pytest.mark.pos
    def test_delete_pet(self, get_key):
        """Проверяем возможность удаления питомца"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(get_key, 'Гаага111', 'Гусь111', 999, 'images/goose.jpg')
            _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(get_key, pet_id)

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        assert status == 200
        assert pet_id not in my_pets.values()

    @pytest.mark.act
    @pytest.mark.pos
    @pytest.mark.parametrize("name",
                             [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                              chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                                  'digit'])
    @pytest.mark.parametrize("animal_type",
                             [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                              chinese_chars(), special_chars(), '123'],
                             ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                                  'digit'])
    @pytest.mark.parametrize("age", [1, 1000], ids=['min_age', 'max_age'])
    def test_successful_update_pet_info(self, get_key, name, animal_type, age):
        """Проверяем возможность обновления информации о питомце"""

        _, my_pets = pf.get_list_of_pets(get_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

            assert status == 200
            assert result['name'] == name
        else:
            raise Exception('У Вас нет питомцев, плак, плак :(')

    @pytest.mark.act
    @pytest.mark.pos
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
