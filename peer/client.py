import socket
import threading
from config import *

# Start peer server to listen for download requests from others
def start_server():
    # Create a socket and listen for connection from other peers
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PEER_PORT))
    s.listen(CLIENT_LIMIT)

    while True:
        peer, addr = s.accept()
        t = threading.Thread(target=peer_handler, args=(peer, addr,))
        t.start()

# Handle connection from other peers
def peer_handler(peer, address):
    lname = peer.recv(BUFFER_SIZE).decode()
    sendFile(lname, peer)
    peer.close()
    
# Send file through socket
def sendFile(filename, peer):
    with open(filename, 'rb') as f:
        data = f.read()
        peer.sendall(data)

if __name__ == '__main__':
    threading.Thread(target=start_server).start()