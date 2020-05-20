# write your code here
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('host', help="server hostname")
parser.add_argument('port', help="server port number", type=int)
parser.add_argument('password', help="server password")
args = parser.parse_args()

with socket.socket() as sock:
    address = (args.host, args.port)
    sock.connect(address)
    data = args.password.encode()
    sock.send(data)
    response = sock.recv(1024)
    print(response.decode())
