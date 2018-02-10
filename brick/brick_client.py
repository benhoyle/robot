#!/usr/bin/env python3
 
import socket
import ev3dev.ev3 as ev3
import os
import json

 
TCP_IP = os.environ['HOST']
TCP_PORT = int(os.environ['PORT'])
BUFFER_SIZE = 1024
MESSAGE = (
	"My battery is running at {0} volts."
	"with a current draw of {1} amps."
	)

# Have these as part of a robot class with actions as class methods
left_m = ev3.LargeMotor('outA')
right_m = ev3.LargeMotor('outB')

#m.run_timed(time_sp=3000, speed_sp=500)
	
p = ev3.PowerSupply()
#sensors = ev3.list_sensors()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
	volts = p.measured_volts
	amps = p.measured_amps
	sensor_state = list()
	for sensor in ev3.list_sensors():
		sensor_state.append(sensor.value())
	robot_state = {
		'volts':volts, 
		'amps':amps, 
		'sensor_state':sensor_state
		}
	message = json.dumps(robot_state)
	s.send(message.encode('UTF-8'))
	data = s.recv(BUFFER_SIZE)
	print("received data:", data)
s.close()
 



