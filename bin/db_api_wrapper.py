import pymongo


# available fields: reddit_id, type, content, timestamp, subreddit

class DBWrapper:

    def __init__(self, configuration):
        self.mongo = pymongo.MongoClient(configuration["host"],
                                         configuration["port"])

        self.db = self.mongo["reddit_data"]

        self.items = self.db["items"]

        self._createIndexes()

    def insert(self, data):
        self.items.insert(data)

    def find(self, filter):
        return self.items.find(filter)

    def _createIndexes(self):
        indexName1 = "subredditIndex"
        indexName2 = "keywordIndex"

        if indexName1 not in self.items.index_information():
            self.items.create_index([("subreddit", pymongo.ASCENDING), ("timestamp", pymongo.DESCENDING)],
                                    name=indexName1)

        if indexName2 not in self.items.index_information():
            self.items.create_index([("content", pymongo.TEXT)],
                                    default_language="none", #u se simple tokenization and exact keyword match
                                    name=indexName2)