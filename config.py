import json

def loadFromFile(filePath):
    config = Config()
    config.reloadFromFile(filePath)
    return config

class Config:

    def __init__(self):
        self.__appId = None
        self.__ownerId = None
        self.__botToken = None

    @property
    def appId(self): return self.__appId
    @property
    def ownerId(self): return self.__ownerId
    @property
    def botToken(self): return self.__botToken

    def reloadFromFile(self, filePath: str):
        data = None
        with open(filePath) as file:
            data = json.load(file)
        self.__appId = int(data["APP_ID"])
        self.__ownerId = int(data["OWNER_ID"])
        self.__botToken = data["TOKEN"]
        
