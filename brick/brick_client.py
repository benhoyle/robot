#!/usr/bin/env python3

import socket
from ev3dev2.motor import (
    MoveTank, OUTPUT_A, OUTPUT_B, MoveSteering, SpeedPercent
)
from ev3dev2.power import PowerSupply
from ev3dev2.sensor import list_sensors
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


def argmax(vector):
    return vector.index(max(vector))


class Robot:
    """ Object to encapsulate the robot. """

    # Have these as part of a robot class with actions as class methods
    # left_m = LargeMotor(OUTPUT_A)
    # right_m = LargeMotor(OUTPUT_B)
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
    steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
    p = PowerSupply()
    # cs = ev3.ColorSensor()
    # cs.mode = 'COL-AMBIENT'

    # We want to use MoveTank and MoveSteering for the control

    def __init__(self):
        """ Initialise Robot and connection. """
        TCP_IP = os.environ.get('HOST')
        TCP_PORT = int(os.environ.get('PORT'))
        self.buffer_size = 1024
        if TCP_IP and TCP_PORT:
            self.build_socket(TCP_IP, TCP_PORT)
        else:
            print("Please set the HOST and PORT environment variables")

    def build_socket(self, ip, port):
        """Build socket on ip address with port."""
        self.pipe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pipe.connect((ip, port))

    @property
    def state(self):
        """ Get state and return as encoded JSON string. """
        return json.dumps( {
            'volts':self.p.measured_volts,
            'amps':self.p.measured_amps,
            'sensor_state':[s.value() for s in list_sensors()]
        } )

    def take_action(self, action):
        """ Take an action when passed an array instructing the action.

        Actions
        left - forward 1 unit - L
        right - backward 1 unit - R
        forward - forward 1 unit - F
        back - backward 1 unit - B
        encode as a vector [L, R, F, B] where 1 indicates chosen action
        """

        speed = SpeedPercent(75)
        time = 1
        if action[0]:
            self.steering_drive.on_for_seconds(-100, SpeedPercent(50), time/2)
        elif action[1]:
            self.steering_drive.on_for_seconds(100, SpeedPercent(50), time/2)
        elif action[2]:
            self.tank_drive.on_for_seconds(speed, speed, time)
        elif action[3]:
            self.tank_drive.on_for_seconds(-1*speed, -1*speed, time)


    def communicate(self):
        """ Send state vector and receive action vector. """
        self.pipe.send(self.state.encode('UTF-8'))
        try:
            data = json.loads(self.pipe.recv(self.buffer_size).decode('UTF-8'))
        except json.decoder.JSONDecodeError:
            # JSON gives us an error if there are multiple JSON objects
            # in the buffer
            data = [0,0,0,0]
        return data

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





