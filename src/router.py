from .utils import splitter, not_found
from .trie import Trie


class Router:
    def __init__(self):
        self.router = {
            "GET": Trie(),
            "POST": Trie(),
            "PUT": Trie(),
            "PATCH": Trie(),
            "DELETE": Trie(),
            "HEAD": Trie(),
            "OPTIONS": Trie(),
        }

    def register_route(self, route, methods):
        def wrapper_register_route(controller):
            for method in methods:
                route_keys = route.split("/")
                self.router[method].add(route_keys, controller)
            return controller

        return wrapper_register_route

    def match_route(self, request):
        uri = request.query_params_checker()
        uri_keys = splitter(uri, "/")
        router_trie = self.router[request.method]
        result = router_trie.search(uri_keys)
        if result is None:
            request.path_params = []
            return not_found
        controller, path_params = result
        request.path_params = path_params
        return controller
