class Request:
    def __init__(self, message={}):
        self.message = message
        self.method = message["Method"]
        self.uri = message["URI"]
        self.protocol = message["Protocol"]
        self.headers = message["headers"]
        self.body = ""
        self.path_params = ()
        self.controller = None
