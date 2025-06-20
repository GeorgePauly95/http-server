import socket


def mirror_message(clientsocket):
    message = clientsocket.recv(1)
    while True:
        try:
            mirror_message = f"{message.decode('utf-8')}"
            clientsocket.send(bytes(mirror_message, "utf-8"))
            break
        except UnicodeDecodeError:
            message = b"".join([message, clientsocket.recv(1024)])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((socket.gethostname(), 1235))
    s.listen(10)
    try:
        while True:
            clientsocket = s.accept()[0]
            mirror_message(clientsocket)
    except KeyboardInterrupt:
        print("Server has been closed!")
