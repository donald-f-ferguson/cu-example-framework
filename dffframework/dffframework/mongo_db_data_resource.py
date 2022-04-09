from .base_data_service import BaseDataResource
from pymongo import MongoClient


class MongoDBResource(BaseDataResource):

    """
    A class for wrapping access to MongoDB via pymongo
    """
    def __init__(self, config_info):
        super().__init__(config_info)
        self._mongo_client = None

    def get_client(self):
        """
        Get a client to the configured MongoDB instance.
        :return: An instance of MongoClient
        """

        # TODO Need to figure out how to use MongoDB sessions.
        if self._mongo_client is None:
            if self.config_info is None:
                self._mongo_client = MongoClient()
            else:
                self._mongo_client = MongoClient(
                    self.config_info.get("url", None)
                )

        return self._mongo_client

    def get_db(self):
        """

        :return: Get's the DB object.
        """
        m_client = self.get_client()
        db = m_client[self.config_info.get("database")]
        return db

    def get_resource_names(self):
        """
        Return a list of the collection names and types in the database.
        :return:
        """
        db = self.get_db()
        result = db.list_collections()

        # Result is a cursor. Covert to a list.
        result = list(result)

        # Simplify the list to return the essential information.
        result = [{"name": l["name"], "type": l["type"]} for l in result]

        return result

    def get_by_template(self, resource_name, template=None, field_list=None):

        db = self.get_db()

        # Have to convert the list of fields to the MongoDB projection format.
        if field_list:
            projection = {f:1 for f in field_list}
        else:
            projection = None

        result = db[resource_name].find(
            filter=template,
            projection=projection
        )

        # TODO Need to add pagination mapped to limit and offset.
        result = list(result)

        return result



