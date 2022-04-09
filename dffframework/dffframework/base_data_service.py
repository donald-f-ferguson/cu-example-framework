from abc import ABC, abstractmethod
import copy


class BaseDataResource(ABC):
    """
    This is the base class for the data layer in the application framework.
    """

    def __init__(self, config_info):
        """

        :param config_info: A JSON dictionary with properties subclasses need for initialization.
        """
        self.config_info = copy.deepcopy(config_info)

    @abstractmethod
    def get_resource_names(self):
        """
        Returns a list of the names of the resource collections in this data resource
        :return:
        """
        pass

    @abstractmethod
    def get_by_template(self, resource_name, template=None, field_list=None):
        """
        Gets
        :param resource_name: The name of the (collection) resource inside the data resource.
        :param template: A dictionary of (field_name, value) pairs used to filter the
        :param field_list: An array containing the names of the fields to return.
        :return: An array of dicts, with each element mapping to a row/document/etc.
        """
        pass