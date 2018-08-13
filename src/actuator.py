#!/usr/bin/env python3
# actuator.py
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


import sys

from pymata_aio.constants import Constants
from pymata_aio.pymata3 import PyMata3

from typing import Dict, Any


class Actuator:
    def __init__(
            self, 
            board: PyMata3, 
            pin: int, 
            min_angle: int = 0, 
            max_angle: int = 180, 
            offset: int = 0) -> None:
        self.min_angle: int = min_angle
        self.max_angle: int = max_angle
        self.offset: int = offset
        self.pin: int = pin
        self.board: PyMata3 = board
        self.board.servo_config(self.pin)

    def set_angle(self, angle: int, dry_run: bool = False) -> bool:
        if not self.min_angle <= angle <= self.max_angle:
            print('unreachable angle {} for {}'.format(angle, self.pin))
            return False
        if not dry_run: 
            self.board.analog_write(self.pin, int(angle) - self.offset)
        return True
