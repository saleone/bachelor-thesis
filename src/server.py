#!/usr/bin/env python3
# server.py
#
# Copyright 2019 Saša Savić <sasa@sasa-savic.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT


import math
from socketserver import BaseRequestHandler
from socketserver import TCPServer
from time import sleep

from pymata_aio.pymata3 import PyMata3
from vectormath import Vector2  

from actuator import Actuator
from mech_arm import MechanicalArm
from fabrik import Fabrik


class ConnectionHandler(BaseRequestHandler):
    def handle(self) -> None:
        self.data: str = self.request.recv(128).strip().decode()
        x, y, z = [int(val) for val in self.data.split(';')]

        mech_arm.move(x, y, z)
        print('')

def main():
    host = ''
    port = 7777
    server = None
    board = PyMata3(5)
    shoulder = Actuator(board, 9)
    arm = Actuator(board, 10)
    elbow = Actuator(board, 11, min_angle=-90, max_angle=90, offset=-90)

    global mech_arm
    mech_arm = MechanicalArm(
        [shoulder, arm, elbow],
        Fabrik(
            joint_positions=[Vector2(0, 0), Vector2(53, 0), Vector2(100, 0)],
            link_lengths=[53, 47],
            tolerance=0.1
        )
    )

    sleep(2)

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
