#!/usr/bin/env python3
 
import socket
import os
 
TCP_IP = os.environ['HOST']
TCP_PORT = int(os.environ['PORT'])

BUFFER_SIZE = 1024 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# Do we want a robot class here? And a robot_brain class?

# Can we record control with the remote control and then
# try to recreate this?

def predict_action(robot_state):
	""" Take the current robot state and predict the next action. """
	# Needs to return a string that is interpretable by the robot
	return "Go!".encode('UTF-8')
	
def get_state():
	""" Get the current state of the robot. """
	pass
 
conn, addr = s.accept()
print('Connection address:', addr)
while 1:
     robot_state = conn.recv(BUFFER_SIZE)
     if not robot_state: break
     print("Robot State:", robot_state)
     action = predict_action(robot_state)
     conn.send(action)  # echo
conn.close()
