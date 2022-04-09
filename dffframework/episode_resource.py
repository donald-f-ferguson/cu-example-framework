from dffframework.base_application_resource import BaseApplicationResource
from dffframework.mongo_db_data_resource import MongoDBResource

class EpisodesResource(BaseApplicationResource):

    def __init__(self, data_service, data_resource_name, resource_path, config_info):
        super().__init__(data_service, data_resource_name, resource_path, config_info)
