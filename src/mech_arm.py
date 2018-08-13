# mech_arm.py
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
from vectormath import Vector2
from pyfabrik import Fabrik

from actuator import Actuator

from typing import List


class MechanicalArm:
    def __init__(self, actuators: List[Actuator], ik_2d: Fabrik):
        if not len(ik_2d.joints) == len(actuators):
            raise ValueError('number of joints must mach number of actuators')

        self.actuators = actuators
        self.ik = ik_2d

    def _set_angles(
            self,
            angles: List[float],
            dry_run: bool = False) -> List[bool]:
        return [a.set_angle(int(angles[i]), dry_run) 
                for i, a in enumerate(self.actuators)]

    def move(self, x: float, y: float, z: float):
        y *= -1 # reversed value due to contruction
        old_joints_pos = [*self.ik.joints]
        self.ik.move(Vector2(math.sqrt(x**2 + y**2), z))
        angles = [math.degrees(math.atan2(y, x)), *self.ik.angles_deg]
        angles[1] = 180 - angles[1] # reversed rotation due to contruction

        if all(self._set_angles(angles, dry_run=True)):
            self._set_angles(angles, dry_run=False)
        else:
            self.ik.joints = old_joints_pos

        print('base: {} \t arm: {} \t elbow: {}'.format(*angles))
