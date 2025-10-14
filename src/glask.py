from src.server import Server


class Glask:
    def __init__(self):
        self.server = Server()

    def register_route(self, route, methods):
        return self.server.router.register_route(route, methods)

    def start(self):
        return self.server.start()
