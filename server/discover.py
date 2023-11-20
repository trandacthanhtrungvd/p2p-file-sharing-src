import sys

# Syntax check
if len(sys.argv) != 2:
    print("Usage: python discover.py hostname")

# Get hostname (address) from argument
hostname = sys.argv[1]

# List published filenames from host named hostname
def discover(hostname):
    with open("peers/" + hostname, "r") as f:
        while True:
            data = f.readline()
            if len(data) == 0:
                break
            print(data.split('|')[1].strip('\n'))

# Call discover function
discover(hostname)