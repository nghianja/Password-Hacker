# write your code here
import argparse
import itertools
import socket


def test_password(sock, password):
    sock.send(password.encode())
    response = sock.recv(1024)
    reply = response.decode()

    if reply == "Connection success!":
        print(password)
        return 1
    elif reply == "Too many attempts to connect!":
        return -1
    else:
        return 0


def main(args):
    with socket.socket() as testsock:
        address = (args.host, args.port)
        testsock.connect(address)

        with open(args.dict, 'r') as dictionary:
            for line in dictionary:
                testword = line.rstrip('\n')
                if testword == testword.upper():
                    if test_password(testsock, testword) != 0:
                        break
                else:
                    testwords = map(''.join, itertools.product(*zip(testword, testword.upper())))
                    for testword in testwords:
                        if test_password(testsock, testword) != 0:
                            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="server hostname")
    parser.add_argument('port', help="server port number", type=int)
    parser.add_argument('--dict', help="dictionary of typical passwords", default="passwords.txt")
    main(parser.parse_args())
