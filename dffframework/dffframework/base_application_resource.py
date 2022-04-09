from abc import ABC, abstractmethod
import copy


class BaseApplicationResource(ABC):
    """
    This is the base class for the data layer in the application framework.
    """

    def __init__(self, data_service, data_resource_name, resource_path, config_info):
        """
        :param data_service: The data service (subclass of BaseDataService) that the resources uses to access the DBs
        :param data_resource_name: The name of the table, collection, etc in the data services
        :param resource_path: The relative path to this resource
        :param config_info: A JSON dictionary with properties subclasses need for initialization.
        """
        self.config_info = copy.deepcopy(config_info)
        self.data_service = data_service
        self.resource_path = resource_path
        self.data_resource_name = data_resource_name

    def get_by_template(self, query_args, field_list):

        result = self.data_service.get_by_template(
                                      resource_name=self.data_resource_name,
                                      template=query_args,
                                      field_list=field_list)
        return result


