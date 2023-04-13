import requests

from config import API_KEY_OMDB, MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS, MONGO_DB

from lib.mongo.collection import OMDB_CACHE
from lib.mongo.connection import MongoConnection

db = MongoConnection(f"mongodb://{MONGO_HOST}:{MONGO_PORT}", MONGO_DB)

class OMDbApiWrapper:
    
    def __init__(self) -> None:
        self.api_key = API_KEY_OMDB
        self.url = "http://www.omdbapi.com/?"
        self.cacheCollection = db.getCollection(OMDB_CACHE)
        pass

    # builds the URL with all the params requested, including the API key
    def __buildUrl(self, params: list, withOriginalUrl: bool = True) -> str:
        # params.append(("i", "tt3896198"))
        API_KEY_ENTRY = ("apikey", self.api_key)
        if not params.__contains__(API_KEY_ENTRY):
            params.append(API_KEY_ENTRY)
        url = self.url if withOriginalUrl else ""
        params.sort()
        for param in params:
            url += f"{param[0]}={param[1]}&"
        return url

    # search by title the movie
    def searchTitle(self, title: str) -> object:
        params = []
        params.append(("t", title))
        url = self.__buildUrl(params=params)
        cache = self.getCache(url)
        # if not cache is None:
        if cache:
            # print("cache")
            return cache["data"]
        res = requests.get(url)
        data = res.json()
        if data["Response"] == "True":
            self.setCache(url, data)
        return data
    
    def setCache(self, url: str, cacheData: object) -> bool:
        db.insert(OMDB_CACHE, {
            "_id": url,
            "data": cacheData
        })
        return True
    
    def getCache(self, url: str) -> object | None:
        return db.find(OMDB_CACHE, {"_id": url})

        
if __name__ == "__main__":
    api = OMDbApiWrapper()
    data = api.searchTitle("super mario bros the movie")
    print(data)