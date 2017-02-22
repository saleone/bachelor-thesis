#!/usr/bin/env python3
import socket
import time
import math
import random

HOST, PORT = 'localhost', 7777

LIMIT = 0.5

posx, posy, posz = 0.0, 0.0, 0.0

def change_pos(*values):
    range_delta = 0.1

    output = []
    for pos in values:
        pos_min = pos - range_delta
        pos_min = -0.5 if pos_min < -0.5 else pos_min

        pos_max = pos + range_delta
        pos_max = 0.5 if pos_max > 0.5 else pos_max

        output.append(round(random.uniform(pos_min, pos_max), 2))

    return output

num = 1
while True:
    with socket.socket() as sock:
        sock.connect((HOST, PORT))
        data = ';'.join([str(posx), str(posy), str(posz)])
        sock.sendall(bytes(data, 'utf-8'))
        time.sleep(0.5)
        posx, posy, posz = change_pos(posx, posy, posz)
    num += 1


