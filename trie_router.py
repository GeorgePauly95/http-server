class initialnode:
    def __init__(self):
        self.children = {}
        self.value = None


class node:
    def __init__(self):
        self.root = initialnode()
        self.children = {}
        self.value = None

    def add(self, uri_keys, controller):
        cur = self.root
        for uri_key in uri_keys:
            if uri_key not in cur.children:
                cur.children[uri_key] = node()
            cur = cur.children[uri_key]
        cur.value = controller

    def search(self, uri_keys):
        cur = self.root
        for uri_key in uri_keys:
            if uri_key not in cur.children:
                return None
            print(f"children are: {cur.children}")
            cur = cur.children[uri_key]
        return cur.value
