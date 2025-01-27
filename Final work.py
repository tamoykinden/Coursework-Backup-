import configparser
import requests
import pprint

# Считывание токенов
config = configparser.ConfigParser()
config.read("settings.ini")
vk_token = config["Tokens"]["vk_token"]
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
        return response.json()

class YD:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Authorization": f"OAth {self.token}"
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
    def download_photos(self, folder_name, file_name):
        url = self.base_url
        params = {
            "path": f"{folder_name}/{file_name}"}
        response = requests.post(url, headers=self.headers, params=params)
        return response.status_code
    







# Пример использования
if __name__ == "__main__":
    vk = VK(vk_token)
    result = vk.get_photos(user_id="151650235", album_id="profile", count=3)
    pprint.pp(result)