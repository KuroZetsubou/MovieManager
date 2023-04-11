from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult

class MongoConnection:
    def __init__(self, uri: str, database: str) -> None:
        self.client = MongoClient(uri)
        self.db = self.client[database]
        pass

    def getCollection(self, collectionName: str) -> Collection:
        return self.db[collectionName]

    def find(self, collectionName: str, filter: object) -> object | None:
        colle = self.getCollection(collectionName=collectionName)
        data = colle.find_one(filter)
        return data
    
    def findMany(self, collectionName: str, filter: object) -> list:
        colle = self.getCollection(collectionName=collectionName)
        data = colle.find(filter)
        out = []
        for entry in data:
            out.append(entry)
        return out

    def insert(self, collectionName: str, data: object) -> InsertOneResult:
        colle = self.getCollection(collectionName=collectionName)
        result = colle.insert_one(data)
        return result

    def updateOne(self, collectionName: str, filter: object, data: object) -> UpdateResult:
        colle = self.getCollection(collectionName=collectionName)
        result = colle.update_one(filter=filter, update=data)
        return result
    
    def deleteOne(self, collectionName: str, filter: object) -> DeleteResult:
        colle = self.getCollection(collectionName=collectionName)
        return colle.delete_one(filter=filter)
    
    def random(self, collectionName: str) -> object:
        colle = self.getCollection(collectionName=collectionName)
        result = colle.aggregate([{ "$sample": { "size": 1 } }])
        b = None
        for a in result:
            b = a
        return b
    
    def drop(self, collectionName: str):
        self.getCollection(collectionName=collectionName).drop()
        pass