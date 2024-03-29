import copy
from flask import request
import json
import logging
from datetime import datetime

logger = logging.getLogger()


class RESTContext:

    _default_limit = 10

    def __init__(self, request_context, path_parameters=None):

        log_message = ""

        self.limit = RESTContext._default_limit

        self.path = request_context.path
        args = dict(request_context.args)

        args = self._de_array_args(args)
        self.path = request.path

        self.data = None
        self.headers = dict(request.headers)
        self.method = request.method
        self.host_url = request.host_url
        self.full_path = request.full_path
        self.base_url = request.base_url
        self.url = request.url

        self.path_parameters = path_parameters

        try:
            self.data = request_context.get_json()
        except Exception as e:
            pass

        args, limit = self._get_and_remove_arg(args, "limit")
        self.limit = limit

        args, offset = self._get_and_remove_arg(args, "offset")
        self.offset = offset

        args, order_by = self._get_and_remove_arg(args, "order_by")
        self.order_by = order_by

        args, fields = self._get_and_remove_arg(args, "fields")

        if fields is not None:
            fields = fields.split(",")

        self.fields = fields

        self.args = args

        try:
            if request.data is not None:
                data = request.json
            else:
                data = None
        except Exception as e:
            # This would fail the request in a more real solution.
            data = "You sent something but I could not get JSON out of it."

            log_message = str(datetime.now()) + ": Method " + self.method

        # TODO Convert string numbers to numbers.
        # This should be a separate functions
        # TODO Need to think about to actually handle this properly.
        #
        for k,v in self.args.items():
            new_v = None
            try:
                new_v = int(v)
            # TODO This exception is too broad
            except Exception as e:
                pass

            if new_v is None:
                try:
                    new_v = float(v)
                except Exception as e:
                    pass

            if new_v:
                self.args[k] = new_v

        log_message += " received: \n" + json.dumps(str(self), indent=2)
        logger.debug(log_message)

    @staticmethod
    def _de_array_args(args):
        result = {}

        if args is not None:
            for k, v in args.items():
                if type(v) == list:
                    result[k] = ",".join(v)
                else:
                    result[k] = v

        return result

    def to_json(self):

        result = {
            'path': self.path,
            "path_parameters": self.path_parameters,
            'args': self.args,
            'headers': self.headers,
            'limit': self.limit,
            'offset': self.offset,
            'method': self.method,
            'host_url': self.host_url,
            'order_by': self.order_by,
            'fields': self.fields,
            'data': self.data}

        return result

    def __str__(self):
        result = self.to_json()
        result = json.dumps(result, indent=2)
        return result

    @staticmethod
    def _get_and_remove_arg(args, arg_name):
        val = copy.copy(args.get(arg_name, None))
        if val is not None:
            del args[arg_name]

        return args, val

    # 1. Extract the input information from the requests object.
    # 2. Log the information
    # 3. Return extracted information.
    #
    @staticmethod
    def log_response(method, status, data, txt):
        msg = {
            "method": method,
            "status": status,
            "txt": txt,
            "data": data
        }

        logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))

    @staticmethod
    def log_request(method_name, request_context):

        info = {
            "method_name": method_name,
            "request": request_context
        }
        msg = json.dumps(info, indent=2, default=str)

        logger.debug(str(datetime.now()) + ": \n" + msg)

    def construct_base_url_without_limit_offset(self):

        result = self.base_url

        if self.args:
            qs = []

            for k,v in self.args.items():
                qs.append(k + "=" + v)

            qs = "?" + "&".join(qs)
            result += qs

        return result

    def add_pagination(self, response_data):

        page_info = []

        self_link = {
            "rel": "self",
            "href": self.url
        }

        page_info.append(self_link)

        if self.limit is not None:
            current_limit = int(self.limit)

            if self.offset is not None:
                current_offset = int(self.offset)
            else:
                current_offset = 0

            data_len = len(response_data)

            base_url = self.construct_base_url_without_limit_offset()

            # Do we need to add a next link?
            if data_len >= current_limit:

                next_offset = current_offset + current_limit
                next_link =  base_url + "&offset=" + str(next_offset) + "&limit=" + str(current_limit)

                page_info.append(
                    {
                        "rel": "next",
                        "href": next_link
                    }
                )

            # Do we need to add a previous link?
            if current_offset > 0:

                previous_offset = max(current_offset-current_offset, 0)
                previous_link = base_url + "&offset=" + str(previous_offset) + "&limit=" + str(current_limit)
                page_info.append(
                    {
                        "rel": "prev",
                        "href": previous_link
                    }
                )

        result = {
            "data": response_data,
            "links": page_info
        }

        return result


def split_key_string(s):

    result = s.split("_")
    return result

def version():
    return "0.0.1"
