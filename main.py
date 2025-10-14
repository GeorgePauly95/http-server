from src.glask import Glask

App = Glask()


@App.register_route("/books", methods=["POST", "GET", "PUT"])
def home(request):
    return "George's FLASK", 200, {"Server": "Glask"}

@App.register_route("/journals", methods=["GET"])
def home(request):
    return "FLASK", 200, {"Server": "Jlask"}

@App.register_route("/books/sherlock", methods=["GET"])
def home(request):
    f = open("big.txt")
    return f"{f.read()}", 200, {"Server": "Glask"}

@App.register_route("/books/moby", methods=["GET"])
def home(request):
    f = open("pg2701.txt")
    return f"{f.read()}", 200, {"Server": "Glask"}

@App.register_route("/chat", methods=["GET"])
def home(request):
    for i in chat():
        return i

def chat():   
    while True:
        yield input("What do you want to say?:\n"), 200, {"Server":"Glask"}

App.start()
