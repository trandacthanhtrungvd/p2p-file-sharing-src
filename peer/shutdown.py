import socket

def shutdown():
    shutdown_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    shutdown_sock.connect(('localhost', 4321))
    shutdown_sock.send('shutdown'.encode())

if __name__ == '__main__':
    shutdown()