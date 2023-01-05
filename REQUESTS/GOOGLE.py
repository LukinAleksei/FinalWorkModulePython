from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests
import time
import io
import json
from tqdm import tqdm


class GoogleUploader:

    def __init__(self):
        """
        Для корректной работы экземпляра класса необходимо в дирректории проекта
        разместить файл client_secrets.json
        """
        self.goauth = GoogleAuth()
        self.goauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.goauth)

    def create_new_folder(self, name: str):
        """
        Метод создает папку на Google Диске пользователя
        :param name_dir: название папки
        :return: id новой папки
        """
        folder = self.drive.CreateFile({
            'title': name,
            'mimeType': 'application/vnd.google-apps.folder'
        })
        folder.Upload()
        return folder['id']

    def upload_file(self, id_dir: str, photo_vk: dict):
        """
        Метод загружает на Google Диск пользователя фото
        :param files: Список со словарями, которые содержат ссылки на фото
        :param id_dir: ID папки, в которую необходимо совешить загрузку
        (можно получить с помощью метода create_new_folder)
        """
        access_token = self.goauth.attr['credentials'].access_token
        for name, url in tqdm(photo_vk.items()):
            metadata = {
                "name": name + '.jpg',
                "parents": [id_dir]
            }
            files_gdrive = {
                'data': ('metadata', json.dumps(metadata), 'application/json'),
                'file': io.BytesIO(requests.get(url).content)
            }
            r = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers={"Authorization": "Bearer " + access_token},
                files=files_gdrive
            )
            time.sleep(1)


if __name__ == '__main__':
    path_to_file = 'text.txt'
    new_folder = 'papka'
    uploader = GoogleUploader()
    uploader.create_new_folder(new_folder)