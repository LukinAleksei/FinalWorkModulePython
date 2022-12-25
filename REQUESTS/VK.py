import requests
from pprint import pprint


def get_vk_token():
    with open('tokenVK.txt', 'r') as token_file:
        return token_file.readline()


class VkApiClient:
    def __init__(self, token: str, api_version: str, base_url='https://api.vk.com/method'):
        self.token = token
        self.api_version = api_version
        self.base_url = base_url

    def general_parameters(self):
        return {
            'access_token': self.token,
            'v': self.api_version
        }

    def get_users_info(self, user_ids: str, fields: str):
        params = {
            'user_ids': user_ids,
            'fields': fields
        }
        return requests.get(f'{self.base_url}/users.get',
                            params={**params, **self.general_parameters()}).json()

    def search_group(self, query: str, sorting: int = 0, count: int = 10):
        '''
        0 - сортировка по умолчанию
        1 - сортировка по скорости роста
        2 - отношение дневной посещаемости
        3 - отношение колличества лайков к колличеству пользователей
        4 - отношение комментариев к колличеству пользователей
        5 - отношение записей в обсуждениях к колличеству пользователей
        '''
        params = {
            'q': query,
            'sort': sorting,
            'count': count
        }
        return requests.get(f'{self.base_url}/groups.search',
                            params={**params, **self.general_parameters()}).json()['response']['items']

    def additional_group_info(self, target_group_ids: str, fields: str):
        params = {
            'group_ids': target_group_ids,
            'fields': fields,
        }
        return requests.get(f'{self.base_url}/groups.getById',
                            params={**params, **self.general_parameters()}).json()['response']

    def get_profiles_photo(self, owner_id: str, count: int = 1):
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'rev': '0',
            'extended': 'likes',
            'count': count
        }
        return requests.get(f'{self.base_url}/photos.get',
                            params={**params, **self.general_parameters()}).json()['response']['items']


# vk_client = VkApiClient(token=get_vk_token(), api_version='5.131')
# pprint(vk_client.get_users_info(user_ids='1335817', fields='counters'))
# pprint(vk_client.get_profiles_photo(owner_id='1335817'))




