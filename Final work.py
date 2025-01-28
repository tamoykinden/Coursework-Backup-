import configparser
import requests
import pprint
import tqdm 
import json
import datetime

# Считывание токенов
config = configparser.ConfigParser()
config.read("settings.ini")
vk_token = config["Tokens"]["vk_token"]
yd_token = config["Tokens"]["yand_token"]
# Определение класса методов взаимодействия с VK
class VK:
    def __init__(self, token, version="5.199"):
        self.params = {
            'access_token': token,
            'v': version
        }
        self.base_url = 'https://api.vk.com/method/'
    
    def get_photos(self, user_id, album_id="profile", count=5):
        """Получает фотографии с профиля пользователя VK."""
        url = f"{self.base_url}photos.get"
        params = {
            "owner_id": user_id,
            "album_id": album_id,
            "count": count,
            "extended": 1  
        }
        params.update(self.params)
    
        response = requests.get(url, params=params)
        data = response.json()
        
        # Проверка на ошибки в ответе
        if "error" in data:
            error_msg = data["error"]["error_msg"]
            raise Exception(f"Ошибка VK API: {error_msg}")
        
        if "response" not in data:
            raise Exception("Некорректный ответ от VK API: отсутствует ключ 'response'")
        
        return data

class YD:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Authorization": f"OAuth {self.token}"
        }
    # Функция создания папки
    def create_folder (self, folder_name):
        url = self.base_url
        params = {
            "path": folder_name
            }
        response = requests.put(url, headers=self.headers, params=params)
        return response.status_code
    
    # Функция для загрузки фотографий
    def upload_photo(self, folder_name, file_name, photo_url):
        upload_url = f"{self.base_url}/upload"
        params = {
            "path": f"{folder_name}/{file_name}",
            "url": photo_url
            }
        response = requests.post(upload_url, headers=self.headers, params=params)
        return response.status_code
    
# Функция для определения максимального размера фотографии
def get_max_ph_size(sizes):
    return max(sizes, key = lambda x: x["height"] * x["width"])

def main_func(vk_token, yd_token, vk_user_id):

    vk = VK(vk_token)
    yd = YD(yd_token)
    
    # Получение фото с профиля
    photos = vk.get_photos(vk_user_id)["response"]["items"]

    # Папка на ЯД
    folder_name = f"Загруженные фото из ВК {vk_user_id}"
    yd.create_folder(folder_name)

    photos_info = []

    # Загрузка фото
    for photo in tqdm.tqdm(photos, desc = "Загрузка фото"):
        max_size_ph = get_max_ph_size(photo["sizes"])
        ph_url = max_size_ph["url"]
        likes = photo["likes"]["count"]
        date = datetime.fromtimestamp(photo["date"]).strftime("%Y-%m-%d")
        file_name = f"{likes}_{date}.jpg"
        yd.upload_photo(folder_name, file_name, ph_url)
        
        photos_info.append({
            "file_name": file_name,
            "size": max_size_ph["type"]
            })
    # Сохранение информации в json
    with open("photos_info.json", "w") as f:
        json.dump(photos_info, f)
    print("Загрузка завершена")

if __name__ == "__main__":
    main_func(vk_token, yd_token, vk_user_id = "609868366")