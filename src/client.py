#!/usr/bin/env python3
import socket
import time
import math
import random
import sys

HOST, PORT = 'localhost', 7777

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

posx = random.randint(-100, 100)
posy = random.randint(-100, 100)
posz = random.randint(-100, 100)

def change_pos(*values):
    range_delta = 10

    output = []
    for pos in values:
        pos_min = pos - range_delta
        pos_min = -100 if pos_min < -100 else pos_min

        pos_max = pos + range_delta
        pos_max = 100 if pos_max > 100 else pos_max

        output.append(random.randint(pos_min, pos_max))

    return output

num = 1
while True:
    with socket.socket() as sock:
        sock.connect((HOST, PORT))
        data = ';'.join([str(posx), str(posy), str(posz)])
        sock.sendall(bytes(data, 'utf-8'))
        time.sleep(1)
        posx, posy, posz = change_pos(posx, posy, posz)
    num += 1


