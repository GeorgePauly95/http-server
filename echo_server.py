import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1236))
s.listen(5)
while True:
    clientsocket, address = s.accept()
    message = clientsocket.recv(1024)
    mirror_message = f"\n\nThis is your mirror message:\n\n {message.decode('utf-8')}"
    clientsocket.send(bytes(mirror_message, "utf-8"))
