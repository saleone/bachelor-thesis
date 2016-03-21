#!/usr/bin/env python3

import time
import sys
import os

import serial.tools.list_ports as list_ports
from pyfirmata import Arduino, util


def find_uno():
    """
    Searches through all the computer com ports for Arduino Uno.
    Returns port string if it finds it else returns False.
    """
    port_list = list(list_ports.comports())
    for port in port_list:
        if  "VID:PID=2341:0043" in port[0]\
            or "VID:PID=2341:0043" in port[1]\
            or "VID:PID=2341:0043" in port[2]:
                print("Arduino Uno found on port {}".format(port[0]))
                return port[0]
    return False


# TODO: Convert to class from which you make instance with board and pins,
# and later you just call step function
def step(board, pins, steps=1, active_coil=0, speed=50):
    """
    Uses firmata  protocol to move a stepper motor konected on pins.
    Pins are passed as a tuple where lowest tuple index is the first
    input pin etc. Speed is set as steps per second. Currently expects
    just 4 coils on stepper motor.  Returns the coil on which the function
    stopped.
    """
    if len(pins) < 4:
        print("You need to define four input pins.")
        return False

    for pin in pins:
        if not isinstance(pin, int):
            print("Pins need to be defined as integers.")
            return False

    if not isinstance(steps, int) or not isinstance(speed, int) \
            or not isinstance(active_coil, int):
        print("All parameters need to be defined as integers.")
        return False

    # Rotates clockwise if 1, if -1 rotates counter clockwise.
    cw = 1
    if steps <  0:
        cw = -1
    elif steps == 0:
        # If there is not steps to do then no function won't do anything.
        return True

    # Make sure just the starting coil is on.
    for coil, _ in enumerate(pins):
        if coil == active_coil:
            board.digital[pins[coil]].write(1)
        else:
            board.digital[pins[coil]].write(0)

    for _ in range(steps):
    # We offset range by 4 to escape the first 4 steps and make calculations easier.
        active_coil = active_coil + cw

        if cw == 1 and active_coil > 3:
        # There is only 4 coils that are indexed from 0 to 3.
            active_coil = active_coil - 4
        elif cw == -1 and active_coil < 0:
            active_coil = active_coild + 4

        # If we have a set speed in steps per second, then we need to wait
        # 1/speed second per step.
        time.sleep(1/speed)
        board.digital[pins[active_coil]].write(1)
        print("Sending 1 on pinNo {}.".format(pins[active_coil]))

        # Keep the previous coil on for a bit.
        time.sleep(0.001)
        board.digital[pins[active_coil-1]].write(0)
        print("Sending 0 on pinNo {}.".format(pins[active_coil-1]))

    # We return active coil so we can continue moving from the same place.
    return active_coil


def save_position(dbfile, coil):
    try:
        if not isinstance(coil, int):
            print("Coil number must be an integer. Exiting...")
            return False
        with open(dbfile, "w") as db:
            db.write(str(coil))
    except Exception as e:
        print("Error occured while saving position: \n {}\nExiting...".format(e))
        sys.exit()
        return False
    return True


def read_position(dbfile):
    try:
        if not os.path.exists(dbfile):
            print("Position file does not exist. Exiting...")
            sys.exit()
        with open(dbfile, "r") as db:
            position = int(db.readline())
            print("Loaded last active coil: {}".format(position))
            return position
    except Exception as e:
        print("Error occured while reading position: \n {}\nExiting...".format(e))
        sys.exit()
        return False


def main():
    uno_port = find_uno()
    if not uno_port:
        print("Arduino Uno was not found. Exiting...")
        return False

    #TODO: Currently we do not have rights to connect to /dev/ttyAMC0 when
    #      Arduino is connected even when it's found by the find_uno().
    #      Using chown on the port gives you the rights to communicate.
    #      Find something that is possible without SU.
    try:
        print("Connecting to port {}".format(uno_port))
        uno = Arduino(uno_port)
    except Exception as e:
        print(e)
        print("Could not connect to port. Exiting...")
        return False
    dbfile = "./position.txt"
    last_coil = read_position(dbfile)
    while True:
        last_coil = step(uno, (8,9,10,11),active_coil=last_coil, speed=10)
        save_position(dbfile, last_coil)

# TODO: Make tests to check if everything is ok instead of trying to run the code manually and adjusting it.
#       It's a lot of work but still ...
if __name__ == "__main__":
    main()
