import YANDEX
import VK
import json
from pprint import pprint

vk_client = VK.VkApiClient(token=VK.get_vk_token(), api_version='5.131')
photo_list = vk_client.get_profiles_photo(owner_id='1335817', count=5)
upload_dict = {}
json_list = []
url_value = ''
for photo_data in photo_list:
    json_dict = {}
    for data, inform in photo_data.items():
        if data == 'sizes':
            for size_inform in inform:
                if size_inform['type'] == 'z':
                    url_value = size_inform['url']
        if data == 'likes':
            upload_dict[inform['count']] = url_value
            json_dict['file_name'] = f'{inform["count"]}.jpg'
            json_dict['size'] = 'z'
    json_list.append(json_dict)


with open('photo_file_info', 'w') as catalog_variable:
    write_dict = json.dumps(json_list)
    catalog_variable.write(write_dict)

ya_disk = YANDEX.YaUploader(token=YANDEX.get_ya_token())
ya_disk.upload_url(ya_disk.create_folder('PhotoVK'), upload_dict)