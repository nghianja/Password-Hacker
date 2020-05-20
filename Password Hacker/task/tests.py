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


def random_password():
    '''function - generating random password of length from 2 to 3'''
    return ''.join(random.choice(abc) for i in range(random.randint(2, 3)))


class Hacking(StageTest):

    def __init__(self, module):
        super().__init__(module)
        self.ready = False
        self.sock = None
        self.serv = None
        self.connected = False
        self.message = []

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
        ''' creating a server and answering clients '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 9090))
        self.ready = True
        try:
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            self.connected = True
            # print ('connected:', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                self.message.append(data.decode('utf8'))
                conn.send('Wrong password!'.encode('utf8'))
            conn.close()
        except:
            pass

    def generate(self):
        self.start_server()
        test_word = random_password()
        return [
            TestCase(
                args=['localhost', '9090', test_word], attach=[test_word])
        ]

    def check(self, reply, attach):
        self.stop_server()

        if not self.connected:
            return CheckResult.wrong("You didn't connect to the server")

        if len(reply) == 0:
            return CheckResult.wrong(
                'You did not print anything')
        if reply.split('\n')[0] != 'Wrong password!':
            return CheckResult.wrong(
                'The line you printed is not the one sent by server')
        if len(self.message) == 0:
            return CheckResult.wrong('You sent nothing to the server')
        if self.message != attach:
            return CheckResult.wrong(
                'You sent the wrong information to the server')
        return CheckResult.correct()


if __name__ == '__main__':
    test = Hacking('hacking.hack')
    test.run_tests()
    test.stop_server()
