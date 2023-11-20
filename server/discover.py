import sys

def main():
    # Syntax check
    if len(sys.argv) != 2:
        print("Usage: python discover.py hostname")
        
    # Get hostname (address) from argument
    hostname = sys.argv[1]

    # Call discover function
    discover(hostname)

# List published filenames from host named hostname
def discover(hostname):
    files = []
    with open("peers/" + hostname, "r") as f:
        while True:
            data = f.readline()
            if len(data) == 0:
                break
            files.append(data.split('|')[1])
    data = "".join(files)
    print(data)
    return data

if __name__ == '__main__':
    main()