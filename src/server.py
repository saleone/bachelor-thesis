#!/usr/bin/env python3

import sys

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants


class Actuator:
    """
    This class represent the motor used on my robot, it tries to create the same
    interface for different kind of motors

    :param board instance of pymata_aio.pymata3.PyMata3 class
    :param pin int or tuple cointaing pin or pins used by actuators to receive signal
    :param steps_per_rev characteristic of a stepper motor used for angle conversion
    """
    def __init__(self, board, pin, steps_per_rev = 4096):
        self.position = 0 # tracks the current position of the actuator (angle)
        self.max_angle = None
        self.min_angle = None
        self.servo = None
        self.pins = []
        self.active_coil = 0

        self.pin = pin

        # Reference to the board on which motors are connected.
        self.board = board

        # Constant for the stepper motor
        self.steps_per_rev = 4096
        self.angle_to_step_ratio = self.steps_per_rev // 360


        # Check are we using servo or stepper motor (we will just use 4 coil per motor).
        self.servo = True
        if isinstance(pin, tuple):
            self.servo = False
            self.pins = pin

        # Check if the values are right and configure the pins.
        self.__check_values()
        self.__configure_actuator()


    def __check_values(self):
        """
        Checks if the values in pin variable are valid. For servos, class
        expects one pin defined as integer. For steppers, class expects tuple containing
        four integers
        """
        if self.servo:
            if not isinstance(self.pin, int):
                print("Pin number must be an integer.")
                sys.exit()
        else:
            if not len(self.pins) == 4:
                print("There must be 4 pins defined to be used for stepper motor.")
                sys.exit()

            for pin in self.pins:
                if not isinstance(pin, int):
                    print("Pin numbers must be integers.")
                    sys.exit()


    def __configure_actuator(self):
        """
        Configures the board to use the pins correctly. Defines pin for servo as servo pin
        or defines stepper pins.
        """
        if self.servo:
            self.board.servo_config(self.pin)
        elif not self.servo:
            # We need to set all output signal pins for stepper motor.
            for pin in self.pins:
                self.board.set_pin_mode(pin, Constants.OUTPUT)


    def set_angle(self, angle):
        """
        Moves the actuator to the specified angle:

        :param angle integer
        """
        angle = int(angle)
        #if isinstance(angle, int):
        #    return False
        if self.servo:
            self.__set_angle_servo(angle)
        else:
            self.__set_angle_stepper(angle)
        self.position = angle
        return True


    def __set_angle_servo(self, angle):
        """
        Should not be used publicly. Moves the servo to given angle.

        :param angle integer
        """
        self.board.analog_write(self.pin, int(angle))
        return True


    def __set_angle_stepper(self, angle):
        """
        Should not be used publicly. Moves the stepper to the given angle.

        :param angle integer
        """
        d_angle = self.position - angle

        # For the given change in angle calculate how many steps stepper has to move
        steps = d_angle * self.angle_to_step_ratio
        #print("Needs to move {} steps or {} degrees".format(steps, d_angle))
        direction = 1
        if steps < 0:
            direction = -1

        for step in range(direction * steps):
            # Pins are just sending signal to activate coil. Coils here
            # represent index in the array (tuple) of pins.
            coil = (step + direction) % 4
            self.board.digital_write(self.pins[coil], 1)
            #print("Setting coil {} to 1".format(coil))
            self.board.digital_write(self.pins[coil-1], 0)
            self.position = self.position +\
                (direction * step // self.angle_to_step_ratio)
        return True


def main_servo():
    board = PyMata3(2)
    servo = Actuator(board, 5)
    from tkinter import Tk, Scale, HORIZONTAL, CENTER
    main_window = Tk()
    slider=Scale(
            command=servo.set_angle,
            length=500,
            orient=HORIZONTAL,
            to=180,
            background="#fff",
            troughcolor="#f00",
            label="SERVO")
    slider.pack(anchor=CENTER)
    main_window.mainloop()


def main_step():
    board = PyMata3(2)
    stepper = Actuator(board, (8,9,10,11))
    from tkinter import Tk, Scale, HORIZONTAL, CENTER
    main_window = Tk()
    slider=Scale(
            command=stepper.set_angle,
            length=500,
            orient=HORIZONTAL,
            to=180,
            background="#fff",
            troughcolor="#f00",
            label="STEPPER")
    slider.pack(anchor=CENTER)
    main_window.mainloop()

def main_servo_step():
    board = PyMata3(2)
    servo = Actuator(board, 5)
    stepper = Actuator(board, (8,9,10,11))
    from tkinter import Tk, Scale, HORIZONTAL, CENTER
    main_window = Tk()
    servo_slider=Scale(
            command=servo.set_angle,
            length=500,
            orient=HORIZONTAL,
            to=180,
            background="#fff",
            troughcolor="#f00",
            label="SERVO")
    servo_slider.pack(anchor=CENTER)
    step_slider=Scale(
            command=stepper.set_angle,
            length=500,
            orient=HORIZONTAL,
            to=180,
            background="#fff",
            troughcolor="#f00",
            label="STEPPER")
    step_slider.pack(anchor=CENTER)
    main_window.mainloop()


# TODO: Make tests to check if everything is ok instead of trying to run the code manually and adjusting it.
#       It's a lot of work but still ...
if __name__ == "__main__":
    main_servo_step()
