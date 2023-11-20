# Import modules
import os
import sys
import socket
from config import *

# Main function
def main():
    # Syntax check
    if len(sys.argv) != 2:
        print("Usage: python fetch.py fname")
        exit(1)

    # Filename
    fname = sys.argv[1]
    start_fetch(SERVER, fname)

# Start fetch process
def start_fetch(server, fname):
    # Get addres and lname from server
    addr, lname = fetch(server, fname)
    # File was not found
    if addr == '':
        print("fname was not found!")
        return 1
    # Send download request to hostname received from server
    download(addr, lname, fname)
    return 0


# Get address and lname from server using fetch command
def fetch(server, fname):
    # Create a socket and connect to centralized server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, SERVER_PORT))

    # Send fetch command
    s.send(f"fetch {fname}".encode())

    # Get return values
    address = s.recv(BUFFER_SIZE).decode()
    lname = s.recv(BUFFER_SIZE).decode()

    # Close socket
    s.close()

    # Return address of peer's address which have the needed file and its location
    return address, lname

def download(address, lname, fname):
    # Create a socket and connect to peer containing needed file
    download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    download_socket.connect((address, PEER_PORT))
    download_socket.send("fetch".encode())
    download_socket.send(lname.encode())

    # Create download folder
    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    # Receive data and write to file
    f = open("downloads/" + fname, "wb")
    while True:
        data = download_socket.recv(BUFFER_SIZE)
        if not data:
            break
        f.write(data)

    f.close()
    # Close socket
    download_socket.close()

if __name__ == '__main__':
    main()