"""Trie class"""


class node:
    def __init__(self):
        self.children = {}
        self.value = None
        self.wildcard = {}

    def add(self, uri_keys, val):
        if uri_keys[0] in self.children:
            child = self.children[uri_keys[0]]
            if len(uri_keys) == 1:
                child.value = val
                return
            uri_keys = uri_keys[1:]
            child.add(uri_keys, val)
            return
        elif ":" in uri_keys[0]:
            if uri_keys[0] in self.wildcard:
                child = self.wildcard[uri_keys[0]]
                if len(uri_keys) == 1:
                    child.value = val
                    return
                uri_keys = uri_keys[1:]
                child.add(uri_keys, val)
                return
            else:
                self.wildcard[uri_keys[0]] = node()
                child = self.wildcard[uri_keys[0]]
                if len(uri_keys) == 1:
                    child.value = val
                    return
                uri_keys = uri_keys[1:]
                child.add(uri_keys, val)
                return
        self.children[uri_keys[0]] = node()
        child = self.children[uri_keys[0]]
        if len(uri_keys) == 1:
            child.value = val
            return
        uri_keys = uri_keys[1:]
        child.add(uri_keys, val)
        return

    def search(self, uri_keys, path_params=None):
        if path_params is None:
            path_params = {}
        if uri_keys[0] in self.children:
            child = self.children[uri_keys[0]]
            if len(uri_keys) == 1:
                return child.value, path_params
            uri_keys = uri_keys[1:]
            return child.search(uri_keys, path_params)
        elif len(self.wildcard) != 0:
            child = list(self.wildcard.values())[0]
            path_params[list(self.wildcard.keys())[0]] = uri_keys[0]
            if len(uri_keys) == 1:
                return child.value, path_params
            uri_keys = uri_keys[1:]
            return child.search(uri_keys, path_params)
        return "Not a Route!"
