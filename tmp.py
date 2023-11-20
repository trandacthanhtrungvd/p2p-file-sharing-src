import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 1234))
server.listen(5)

while True:
    client, address = server.accept()