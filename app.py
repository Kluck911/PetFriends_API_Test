from settings import email, passwd
import json
import requests


class PetFriends:
    def __init__(self):
        self.base_url = 'http://petfriends1.herokuapp.com/'

    def get_API_key(self, email_, passwd_):

        headers = {
            'email': email_,
            'password': passwd_,
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


a = PetFriends()
print(a.get_API_key(email, passwd)[1].get('key'))
print(a.base_url)