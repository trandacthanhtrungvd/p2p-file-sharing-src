import socket
import threading
from config import *
from shutdown import shutdown

# Start peer server to listen for download requests from others
def start_server():
    # Create a socket and listen for connection from other peers
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PEER_PORT))
    s.listen(CLIENT_LIMIT)

    try:
        while True:
            peer, addr = s.accept()
            t = threading.Thread(target=peer_handler, args=(peer, addr, s))
            t.start()
    except:
        print("Shutting down")
    finally:
        peer.close

# Handle connection from other peers
def peer_handler(peer, address, server):
    response = peer.recv(BUFFER_SIZE).decode()
    args = response.split()
    # Handle shutdown exception
    try:
        opcode = args[0]
    except:
        return
    
    # Handle server shutdown
    if opcode == 'shutdown':
        peer.close()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('localhost', PEER_PORT))
        server.close()
        return
    
    if opcode == 'ping':
        peer.send("Alive!".encode())
        peer.close()
        return

    # Handle fetch command from other peers
    with open(response, 'rb') as f:
        data = f.read()
        peer.sendall(data)
    peer.close()
    
if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    while True:
        if (str(input()) == 'shutdown'):
            shutdown()
            break