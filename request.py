class Request:
    def __init__(self, message={}):
        print("The request object is created!")
        self.method = message["method"]
        self.uri = message["uri"]
        self.protocol = message["protocol"]
        self.headers = message["headers"]
        self.body = None
        self.path_params = []
        self.query_params = {}
