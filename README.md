# robot
Playing around with ev3

ev3 provides a tutorial that uses MQTT:
http://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
MQTT is not great for real-time communication.

It is mainly designed for asynchronous communication.

Maybe back to socket - here's a tutorial 
- https://pythonspot.com/python-network-sockets-programming-tutorial/.


To do:

brick:
run MQTT client.
send sensory state data to computer.
receive commands from computer. (commands may need to be defined)

computer:
run MQTT broker.
receive sensory state data.
predict action.
send action to brick.

(One option is to move the broker onto one of the Pis.)
