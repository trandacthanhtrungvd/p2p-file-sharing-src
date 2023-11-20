import sys
import socket
from config import *

def main():
    # Syntax check
    if len(sys.argv) != 2:
        print("Usage: python ping.py hostname")
        exit(1)

    addr = sys.argv[1]
    ping(addr)

def ping(address):
    ping_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ping_sock.connect((address, PEER_PORT))
        ping_sock.settimeout(3)
        ping_sock.send('ping'.encode())
        print(ping_sock.recv(BUFFER_SIZE).decode())
        ping_sock.close()
        # Return 0 for 'Alive!'
        return 0
    except:
        print("Not alive!")
        # Return 1 for 'Not alive!'
        return 1

if __name__ == '__main__':
    main()