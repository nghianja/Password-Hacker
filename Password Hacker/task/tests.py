from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from threading import Thread
from time import sleep
import socket
import random

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

abc = 'abcdefghijklmnopqrstuvwxyz1234567890'


passwords = [
    'chance', 'frankie', 'killer', 'forest', 'penguin'
    'jackson', 'rangers', 'monica', 'qweasdzxc', 'explorer'
    'gabriel', 'bollocks', 'simpsons', 'duncan', 'valentin',
    'classic', 'titanic', 'logitech', 'fantasy', 'scotland',
    'pamela', 'christin', 'birdie', 'benjamin', 'jonathan',
    'knight', 'morgan', 'melissa', 'darkness', 'cassie'
]


def generate_password():
    '''function - generator of all passwords from dictionary'''
    for password in passwords:
        yield password.rstrip().lower()


def random_password():
    '''function - generating random password from dictionary'''
    pas = random.choice(list(generate_password()))
    uppers = []
    for i in range(len(pas)):
        uppers.append(random.randint(0, 1))

    return ''.join(
        pas[j].upper() if uppers[j] == 1
        else pas[j]
        for j in range(len(pas)))


class Hacking(StageTest):

    def __init__(self, module):
        super().__init__(module)
        self.ready = False
        self.sock = None
        self.serv = None
        self.connected = False
        self.message = []
        self.password = None

    def start_server(self):
        self.serv = Thread(target=lambda: self.server())
        self.serv.start()
        self.ready = False
        while not self.ready:
            sleep(0.1)  # socket needs to be set up before test

    def stop_server(self):
        self.sock.close()
        self.serv.join()

    def server(self):
        '''function - creating a server and answering clients'''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 9090))
        self.ready = True
        try:
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            self.connected = True
            while True:
                data = conn.recv(1024)
                self.message.append(data.decode('utf8'))
                if len(self.message) > 1_000_000:
                    conn.send('Too many attempts to connect!'.encode('utf8'))
                    break
                if not data:
                    break
                if data.decode('utf8') == self.password:
                    conn.send('Connection success!'.encode('utf8'))
                    break
                else:
                    conn.send('Wrong password!'.encode('utf8'))
            conn.close()
        except:
            pass

    def generate(self):
        self.message = []
        self.password = random_password()
        self.start_server()
        return [TestCase(args=['localhost', '9090'],
                         attach=[self.password])]

    def check(self, reply, attach):
        self.stop_server()

        if not self.connected:
            return CheckResult.wrong("You didn't connect to the server")

        real_password = attach[0]
        printed_password = reply.split('\n')[0]
        if reply.split('\n')[0] != real_password:
            return CheckResult.wrong(
                'The password you printed is not correct\n'
                'You printed: \"' + printed_password + '\"\n'
                'Correct password: \"' + real_password + '\"'
            )

        return CheckResult.correct()


if __name__ == '__main__':
    test = Hacking('hacking.hack')
    test.run_tests()
    test.stop_server()
