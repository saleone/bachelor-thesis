#!/usr/bin/env python3
import socketserver
from socketserver import BaseRequestHandler
from socketserver import TCPServer

HOST = ''
PORT = 7777

class ConnectionHandler(BaseRequestHandler):

    client = []


    def handle(self):
        self.data = self.request.recv(128).strip()
        print('{} wrote:\n{}'.format(self.client_address[0], self.data))

def main():
    server = TCPServer((HOST, PORT), ConnectionHandler)
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()
