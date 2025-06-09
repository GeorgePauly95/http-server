import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(1)
i = 0
while True:
    i += 1
    print(i)
    clientsocket, address = s.accept()
    message = clientsocket.recv(10)
    mirror_message = f"{message.decode('utf-8')}"
    clientsocket.send(bytes(mirror_message, "utf-8"))
