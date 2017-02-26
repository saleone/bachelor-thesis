#!/usr/bin/env python3
import socketserver
from socketserver import BaseRequestHandler
from socketserver import TCPServer

from inv_kinematics import get_angles

class ConnectionHandler(BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(128).strip().decode()
        print('Data from {}:\n\t {}'.format(self.client_address[0], self.data))
        x, y, z = [int(value) for value in self.data.split(';')]
        theta0, theta1, theta2 = get_angles(x, y, z)
        print('\n')
        print('Setting angles to: \n\t{};{};{}'.format(theta0, theta1, theta2))
        print('\n{}\n'.format('='*40))

def main():
    host = ''
    port = 7777
    server = None
    while server is None:
        try:
            server = TCPServer((host, port), ConnectionHandler)
        except OSError:
            port += 1
            continue
    print("Serving on: {}".format(port))
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()
