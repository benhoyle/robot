#!/usr/bin/env python3
 
import socket
import ev3dev.ev3 as ev3
import os
import json

 
TCP_IP = os.environ['HOST']
TCP_PORT = int(os.environ['PORT'])
BUFFER_SIZE = 1024

class Robot:
	""" Object to encapsulate the robot. """
	
	# Have these as part of a robot class with actions as class methods
	left_m = ev3.LargeMotor('outA')
	right_m = ev3.LargeMotor('outB')
	p = ev3.PowerSupply()
	
	@property
	def state(self):
		""" Get state and return as encoded JSON string. """
		return json.dumps( {
			'volts':self.p.measured_volts, 
			'amps':self.p.measured_amps, 
			'sensor_state':[s.value() for s in ev3.list_sensors()]
		} )
	
	# Actions
	# left - forward 1 unit
	# left - backward 1 unit
	# right - forward 1 unit
	# right - backward 1 unit



#m.run_timed(time_sp=3000, speed_sp=500)
	

#sensors = ev3.list_sensors()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
robot = Robot()
while 1:
	s.send(robot.state.encode('UTF-8'))
	data = s.recv(BUFFER_SIZE)
	print("received data:", data)
s.close()
 



