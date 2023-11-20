import os
import socket
import threading
from config import *
from shutdown import shutdown

# Main function
def start_server(): 
    # Create a socket and listen for commands from clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', SERVER_PORT))
    server.listen(CLIENT_LIMIT)

    # Make a directory for savefiles
    if not os.path.exists("peers"):
        os.mkdir("peers")

    try:
        while True:
            client, address = server.accept()
            t = threading.Thread(target=client_handler, args=(client, address, server, ))
            t.start()
    except:
        print("Shutting down")
    finally:
        client.close()

# Handle client: publish / fetch
def client_handler(client, address, server):
    response = client.recv(BUFFER_SIZE).decode()
    args = response.split()

    # Handle shutdown exception
    try:
        opcode = args[0]
    except:
        return

    # Handle publish lname fname
    if opcode == 'publish':
        # Get client's address
        # Published filenames are saved in a savefile named {address}.txt
        file_name = address[0]
        lname = " ".join(args[1:-1])
        fname = args[-1]
        # Write the name of published file to savefile
        # Data format of each line: lname|fname
        with open("peers/" + file_name, "a") as f:
            content = lname + "|" + fname + "\n"
            f.write(content)

    # Handle fetch fname
    if opcode == 'fetch':
        # Get fname to fetch
        fname = args[1]
        found = bool(False)
        files = os.scandir("peers")

        # Loop through every savefile to find fname's location
        for file in files:
            with open("peers/" + file.name, 'r') as f:
                for item in f.read().split('\n'):
                    if fname in item:
                        client.send(file.name.encode())
                        client.send(item.split('|')[0].encode())
                        found = True
                        break
            if found:
                break

        # Close scandir iterator
        files.close()
    
    # Handle server shutdown
    if opcode == 'shutdown':
        client.close()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('localhost', SERVER_PORT))
        server.close()
        return
        
    client.close()

if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    while True:
        if (str(input()) == 'shutdown'):
            shutdown()
            break