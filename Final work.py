import configparser
config = configparser.ConfigParser()
config.read("settings.ini")
vk_token = config["Tokens"]["vk_token"]

class VK:
    def __init__(self, token, version = "5.199"):
        self.params = {
            'access_token': token,
            "v": version
        }
        self.base_url = 'https://api.vk.com/method/'
    
    def get_photos(self, user_id)
        