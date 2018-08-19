#!/usr/bin/env python3
"""Server code for robot control."""

import sys
import tty
import socket
import os
from random import randint
import json
import termios
import logging

# Can we record control with the remote control and then
# try to recreate this?
# YES - if we log action-state pairs we can use this for training
# We can build backend control - use key control first then add
# a Web frontend for this

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


class RobotBrain:
    """Object to encapsulate the server."""

    def __init__(self):
        """Init Functions."""
        # Initialise Logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('robotdata.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        # Get Host / Port Variables
        ip = os.environ['HOST']
        port = int(os.environ['PORT'])
        # Initialise Socket
        self.buffer_size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(1)
        self.conn = None
        self.addr = None
        # Wait for a connection
        self.wait_for_connect()

    def wait_for_connect(self):
        """Wait for an incoming connection."""
        print("Waiting for a connection to client.")
        while not self.conn:
            self.conn, self.addr = self.socket.accept()
            print('Connection to IP:', self.addr)

    def stop(self):
        """Shut down the connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Delete object actions."""
        self.stop()

    def predict_action(self, robot_state):
        """Take the current robot state and predict the next action."""
        # Needs to return a string that is interpretable by the robot
        action = [0]*4 # Create a blank action vector - [LF, LR, RF, RR]
        action[randint(0, 3)] = 1 # Randomly select an action
        message = json.dumps(action).encode('UTF-8')
        return message.encode('UTF-8')

    def get_state(self):
        """Get the current state of the robot."""
        try:
            robot_state = json.loads(self.conn.recv(self.buffer_size).decode('UTF-8'))
        except json.decoder.JSONDecodeError:
            robot_state = {}
        return robot_state


    def send_action(self, action):
        """Send an action to the robot.

        action is an array [L, R, F, B] where 1 indicates action
        and 0 indicates no action.
        """
        message = json.dumps(action).encode('UTF-8')
        if self.conn:
            self.conn.send(message)
            robot_state = self.get_state()
            self.logger.info("state: {0}".format(robot_state))
            self.logger.info("action: {0}".format(action))
            # We want to log action and received state here


    def monitor_state(self):
        """Monitor the state of the robot."""
        while 1:
            robot_state = self.get_state()
            if not robot_state: break
            print("Robot State:", robot_state)

    def remote_control(self):
        """Control the robot with the arrow keys on the server.

        Based on code from here:
        https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_keyboard.py
        """
        while True:
            ch = getch()
            print(ch)
            if ch == "e":
                # Exit
                print("Exiting Remote Control")
                break
            elif ch == "a":
                # Go left
                print("Left")
                self.send_action([1, 0, 0, 0])
            elif ch == "d":
                # Go right
                print("Right")
                self.send_action([0, 1, 0, 0])
            elif ch == "w":
                # Go forward
                print("Forward")
                self.send_action([0, 0, 1, 0])
            elif ch == "s":
                # Go backwards
                print("Backward")
                self.send_action([0, 0, 0, 1])

# conn, addr = s.accept()
# print('Connection address:', addr)
# while 1:
    # robot_state = conn.recv(BUFFER_SIZE)
    # if not robot_state: break
    # print("Robot State:", robot_state)
    # action = predict_action(robot_state)
    # conn.send(action)  # echo
# conn.close()
