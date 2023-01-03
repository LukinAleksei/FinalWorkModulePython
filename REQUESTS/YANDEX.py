from requests import get, put, post
from pprint import pprint
import time
from tqdm import tqdm


def get_ya_token():
    with open('tokenYANDEX.txt', 'r') as token_file:
        return token_file.readline()


class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.token = token

    @property
    def headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, path):
        put(f'{self.url}?path={path}', headers=self.headers)
        return path

    def get_upload_link(self, file_path: str, folder: str) -> dict:
        params = {'path': f'{folder}/{file_path}', 'overwrite': 'true'}
        response = get(f'{self.url}/upload', params=params, headers=self.headers)
        return response.json()

    def upload(self, file_path: str, folder: str):
        href = self.get_upload_link(file_path, folder)['href']
        with open(file_path, 'rb') as file:
            try:
                response = put(href, data=file)
                print('Success!')
            except (KeyError, ConnectionError):
                print(response.status_code)

    def upload_url(self, folder: str, photo_vk: dict):
        for name, url in tqdm(photo_vk.items()):
            params = {'path': f'{folder}/{name}', 'url': url}
            post(f'{self.url}/upload', params=params, headers=self.headers)
            time.sleep(1)


if __name__ == '__main__':
    path_to_file = 'text.txt'
    new_folder = input()
    uploader = YaUploader(get_ya_token())
    uploader.create_folder(new_folder)
    uploader.upload_url(new_folder, path_to_file)

