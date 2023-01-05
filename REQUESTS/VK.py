import requests
from pprint import pprint


def get_vk_token():
    with open('tokenVK.txt', 'r') as token_file:
        return token_file.readline().strip()


class VkApiClient:
    def __init__(self, token: str, api_version: str = '5.131', base_url='https://api.vk.com/method'):
        self.token = token
        self.api_version = api_version
        self.base_url = base_url

    @property
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
                            params={**params, **self.general_parameters}).json()

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
                            params={**params, **self.general_parameters}).json()['response']['items']

    def additional_group_info(self, target_group_ids: str, fields: str):
        params = {
            'group_ids': target_group_ids,
            'fields': fields,
        }
        return requests.get(f'{self.base_url}/groups.getById',
                            params={**params, **self.general_parameters}).json()['response']

    def get_photo(self, owner_id: str, count: int = 1, album_id: str = 'profile'):
        '''
        Выберите (из предложенного списка) из какого альбома начать скачку фотографий
        и введите в соответствии с названием:
        wall - фотографии со стены
        profile - фотографии профиля
        saved -  сохраненные фотографии. Возвращается только с ключом доступа пользователя.
        '''
        params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'rev': '0',
            'extended': 'likes',
            'count': count
        }
        return requests.get(f'{self.base_url}/photos.get',
                            params={**params, **self.general_parameters}).json()['response']['items']


if __name__ == '__main__':
    vk_client = VkApiClient(token=get_vk_token())
    pprint(vk_client.get_users_info(user_ids='1335817', fields='counters'))
    pprint(vk_client.get_photo(owner_id='1335817', count=5))




