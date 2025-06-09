import socket

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))
    message = input(
        "Please type your message here, and we'll mirror it back to you:\n\n"
    )
    s.send(bytes(message, "utf-8"))
    mirror_message = s.recv(10240)
    output = mirror_message.decode("utf-8")
    if output != "exit()":
        print(output)
        continue
    s.close()
    break
