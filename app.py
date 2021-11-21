import json
import requests


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email, passwd):

        headers = {
            'email': email,
            'password': passwd,
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result.get('key')

    def get_list_of_pets(self, auth_key, filter):

        headers = {'auth_key': auth_key}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
