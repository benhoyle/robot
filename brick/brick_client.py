#!/usr/bin/env python3
 
import socket
import ev3dev.ev3 as ev3
import os

 
TCP_IP = os.environ['HOST']
TCP_PORT = int(os.environ['PORT'])
BUFFER_SIZE = 1024
MESSAGE = (
	"My battery is running at {0} volts."
	"with a current draw of {1} amps."
	)
	
p = ev3.PowerSupply()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
	volts = p.measured_volts
	amps = p.measured_amps
	s.send(MESSAGE.format(volts, amps).encode('utf-8'))
	data = s.recv(BUFFER_SIZE)
	print("received data:", data)
s.close()
 



