"""Trie class"""

i = 0


class Trie:
    def __init__(self):
        global i
        i += 1
        print(f"The Trie object no: {i} is created!")
        self.children = {}
        self.value = None

    def add(self, uri_keys, val):
        if len(uri_keys) == 0:
            self.value = val
            return
        key = uri_keys.pop(0)
        if key in self.children:
            self.children[key].add(uri_keys, val)
            return
        child = Trie()
        if ":" in key:
            self.children["WILDCARD"] = child
            child.add(uri_keys, val)
            return
        self.children[key] = child
        child.add(uri_keys, val)

    def search(self, uri_keys, path_params=None):
        if path_params is None:
            path_params = []
        if len(uri_keys) == 0:
            return self.value, path_params
        key = uri_keys.pop(0)
        if key in self.children:
            child = self.children[key]
            return child.search(uri_keys, path_params)
        if "WILDCARD" in self.children:
            child = self.children["WILDCARD"]
            path_params.append(key)
            return child.search(uri_keys, path_params)
        return None
