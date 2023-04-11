import requests

from config import API_KEY_OMDB

class OMDbApiWrapper:
    
    def __init__(self) -> None:
        self.api_key = API_KEY_OMDB
        self.url = "http://www.omdbapi.com/?"
        pass

    # builds the URL with all the params requested, including the API key
    def __buildUrl(self, params: list) -> str:
        # params.append(("i", "tt3896198"))
        params.append(("apikey", self.api_key))
        url = self.url
        for param in params:
            url += f"{param[0]}={param[1]}&"
        return url

    # search by title the movie
    def searchTitle(self, title) -> object:
        params = []
        params.append(("t", title))
        url = self.__buildUrl(params=params)
        res = requests.get(url)
        return res.json()
        
if __name__ == "__main__":
    api = OMDbApiWrapper()
    data = api.searchTitle("super mario")
    print(data)