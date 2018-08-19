#!/usr/bin/env python3

import socket
import ev3dev.ev3 as ev3
import os
import json
import termios
import sys
import tty

def getch():
    """Get character input."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


TCP_IP = os.environ['HOST']
TCP_PORT = int(os.environ['PORT'])
BUFFER_SIZE = 1024

def argmax(vector):
    return vector.index(max(vector))

class Robot:
    """ Object to encapsulate the robot. """

    # Have these as part of a robot class with actions as class methods
    left_m = ev3.LargeMotor('outA')
    right_m = ev3.LargeMotor('outB')
    p = ev3.PowerSupply()
    cs = ev3.ColorSensor()
    cs.mode = 'COL-AMBIENT'

    def __init__(self):
        """ Initialise Robot and connection. """
        self.pipe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pipe.connect((TCP_IP, TCP_PORT))

    @property
    def state(self):
        """ Get state and return as encoded JSON string. """
        return json.dumps( {
            'volts':self.p.measured_volts,
            'amps':self.p.measured_amps,
            'sensor_state':[s.value() for s in ev3.list_sensors()]
        } )

    def a_to_m(self, action):
        """ From an action vector return motor and direction parameters."""
        index = argmax(action)
        # You can probably do this more concisely
        if index > 1:
            motor = self.right_m
        else:
            motor = self.left_m
        # If index is even - go forward, else reverse
        if index % 2 == 0:
            direction = 1
        else:
            direction = -1
        return motor, direction

    def take_action(self, action):
        """ Take an action when passed an array instructing the action."""
        # Actions
        # left - forward 1 unit - LF
        # left - backward 1 unit - LR
        # right - forward 1 unit - RF
        # right - backward 1 unit - RR
        # encode as a vector [LF, LR, RF, RR] where 1 indicates chosen action
        unit_time = 3000 # Set number of ms to run as a unit time period
        unit_speed = 500 # Set tachos for a unit speed

        # Forward and reverse are not powering both motors at the same time

        # Convert from one hot action vector to motor and direction selection
        motor, direction = self.a_to_m(action)
        motor.run_timed(
            time_sp=unit_time,
            speed_sp=direction*unit_speed
            )

    def communicate(self):
        """ Send state vector and receive action vector. """
        self.pipe.send(self.state.encode('UTF-8'))
        return json.loads(self.pipe.recv(BUFFER_SIZE).decode('UTF-8'))

    def remote_control(self):
        """Receive remote commands."""
        print("Running remote control - press e to exit")
        # One issue is that sometimes there are multiple commands in
        # the buffer and json gives a value error
        while True:
            # ch = getch()

            # if ch == "e":
                # # Exit
                # print("Exiting Remote Control")
                # break
            action = self.communicate()
            print("Received action: {0}".format(action))
            if action:
                self.take_action(action)


    def stop(self):
        """ Tidy up the connection. """
        self.pipe.close()

    def __del__(self):
        """Run on exit/delete."""
        self.stop()





