import socket


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1235))
    message = input(
        "Please type your message here, and we'll mirror it back to you:\n\n"
    )
    # length_header = str(len(message))
    s.send(bytes(message, "utf-8"))
    mirror_message = s.recv(10240).decode("utf-8")
    if mirror_message != "exit()":
        print(mirror_message)
        continue
    s.close()
    break
