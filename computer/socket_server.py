#!/usr/bin/env python
 
import socket
import os
 
TCP_IP = os.environ['HOST']
TCP_PORT = int(os.environ['PORT'])

BUFFER_SIZE = 1024 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
 
conn, addr = s.accept()
print('Connection address:', addr)
while 1:
     data = conn.recv(BUFFER_SIZE)
     if not data: break
     print("received data:", data)
     conn.send(data)  # echo
conn.close()
