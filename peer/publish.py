import os
import sys
import socket
from config import *

def main():
    # Syntax check
    if len(sys.argv) != 3:
        print("Usage: python publish.py lname fname")
        exit(1)

    # Get lname, fname from arguments
    lname = sys.argv[1]
    fname = sys.argv[2]

    publish(SERVER, lname, fname)

# Publish a file to centralized server
def publish(server, lname, fname):
    # Create a socket and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, SERVER_PORT))

    # Change lname path to absolute path for some reasons :v
    lname = os.path.abspath(lname)

    # Send publish command to the server
    s.send(f'publish {lname} {fname}'.encode())

    # Close socket
    s.close()
    return

if __name__ == '__main__':
    main()