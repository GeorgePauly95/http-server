from urllib.parse import unquote, unquote_plus
from .utils import splitter

class Request:
    def __init__(self, message={}):
        self.method = message["method"]
        self.uri = message["uri"]
        self.protocol = message["protocol"]
        self.headers = message["headers"]
        self.body = None
        self.path_params = []
        self.query_params = {}

    def query_params_checker(self):
        uri = unquote(self.uri)
        uri_pair = splitter(self.uri, "?")
        if len(uri_pair) == 1:
            return uri
        query_params = unquote_plus(uri_pair[1]).split("&")
        for query_param in query_params:
            key, value = query_param.split("=")
            self.query_params[key] = value
        return uri_pair[0]

    def close_connection(self):
        if self.protocol == "HTTP/1.0":
            return "Connection" not in self.headers \
                    or self.headers["Connection"] == "close"
        return "Connection" in self.headers \
                and self.headers["Connection"] == "close"
