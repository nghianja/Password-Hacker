# write your code here
import argparse
import itertools
import socket
import string

parser = argparse.ArgumentParser()
parser.add_argument('host', help="server hostname")
parser.add_argument('port', help="server port number", type=int)
args = parser.parse_args()

with socket.socket() as sock:
    address = (args.host, args.port)
    sock.connect(address)

    characters = [c for c in string.ascii_lowercase] + [str(n) for n in range(10)]
    i = 1

    flag = True
    while flag:
        for t in itertools.product(characters, repeat=i):
            p = ''.join(t)

            sock.send(p.encode())
            response = sock.recv(1024)
            r = response.decode()

            if r == "Connection success!":
                print(p)
                flag = False
                break
            elif r == "Too many attempts":
                flag = False
                break
        i += 1
