import os

fname = 'test.txt'
files = os.scandir("files")
for file in files:
    with open("files/" + file.name, 'r') as f:
        if fname in f.read():
            peer = file.name
            break

