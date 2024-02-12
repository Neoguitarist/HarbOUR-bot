import json

def loadFromFile(filePath):
    config = Config()
    config.reloadFromFile(filePath)
    return config

class Config:

    def __init__(self):
        self.__appId = None
        self.__botToken = None

    @property
    def appId(self): return self.__appId
    @property
    def botToken(self): return self.__botToken

    def reloadFromFile(self, filePath: str):
        data = None
        try:
            with open(filePath) as file:
                data = json.load(file)
            self.__appId = data["APP_ID"]
            self.__botToken = data["TOKEN"]
        except Exception as e:
            print(f"Could not load configuration: {e}")
