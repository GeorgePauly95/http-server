import re

class Request:
    def __init__(self, message={}):
        self.message = message
        self.method = message["Method"]
        self.uri = message["URI"]
        self.protocol = message["Protocol"]
        self.headers = message["headers"]
        self.body = ''
        self.path_params = []
        self.routes = {}
        self.route_regexes = {}
        self.match = ''

    def route_matcher(self):
        for route_regex in self.route_regexes:
            if re.match(route_regex, self.uri) is not None:
                self.match = True
                self.path_params = re.findall(route_regex, self.uri)
                if self.path_params[0] != re.match(route_regex, self.uri).group():
                    return self.routes[self.route_regexes[route_regex]], self.path_params
                return self.routes[self.route_regexes[route_regex]]
            self.match = False
        return None



