from pymongo import MongoClient
from bson.objectid import ObjectId
import config as conf


class Database():

    def __init__(self):
        ip = hasattr(conf, 'dbhost') and conf.dbhost or '127.0.0.1'
        port = hasattr(conf, 'dbport') and conf.dbport or '27017'
        db = hasattr(conf, 'db') and conf.db or 'test'
        self.host = ip
        self.port = port
        self.database = db
        db = set()
        self.__client = set()

    def find(self, collection, filter={}):

        self.__runClient()

        info = self.db[collection].find(filter)
        count = self.db[collection].count_documents(filter)

        listData = []
        if count:
            for item in info:
                item['_id'] = str(item['_id'])
                listData.append(item)

        data = {
            'data': listData,
            'count': count
        }

        self.__closeClient()

        return data

    def insert_one(self, collection, data={}):

        self.__runClient()

        self.db[collection].insert_one(data)

        data['_id'] = str(data['_id'])

        self.__closeClient()

        return data

    def insert_many(self, collection, data={}):

        self.__runClient()

        self.db[collection].insert_many(data)

        data['_id'] = str(data['_id'])

        self.__closeClient()

        return data

    def update_one(self, collection, replace, data={}):

        self.__runClient()

        if '_id' in replace:
            replace['_id'] = ObjectId(replace['_id'])

        self.db[collection].update_one(replace, {'$set': data})

        data['_id'] = str(replace['_id'])

        self.__closeClient()

        return data

    def update_many(self, collection, replace, data={}):

        self.__runClient()

        if '_id' in replace:
            replace['_id'] = ObjectId(replace['_id'])

        self.db[collection].update_many(replace, data)

        data['_id'] = str(data['_id'])

        self.__closeClient()

        return data

    def delete_one(self, collection, data={}):

        self.__runClient()

        if '_id' in data:
            data['_id'] = ObjectId(data['_id'])

        self.db[collection].delete_one(data)

        data['_id'] = str(data['_id'])

        self.__closeClient()

        return data

    def delete_many(self, collection, data={}):

        self.__runClient()

        if '_id' in data:
            data['_id'] = ObjectId(data['_id'])
        

        self.db[collection].delete_many(data)

        data['_id'] = str(data['_id'])

        self.__closeClient()

        return data

    def __runClient(self):
        self.__client = MongoClient(self.host, int(self.port))
        self.db = self.__client[self.database]

    def __closeClient(self):
        return self.__client.close()
