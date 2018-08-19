# Robot

A python-controlled playground for Lego Mindstorms ev3 robotics.
This can form a base for AI projects.

## Prequisites

* A Lego Mindstorms ev3 kit.
* An install on the ev3 brick of the brilliant [ev3dev](https://www.ev3dev.org/docs/getting-started/)
** Use the "stretch" install to support the ev3dev2 python library.
* Some form of robot with a left motor on InputA and a right motor on InputB.

## Background

The project works on a client-server basis. There is a folder called
```brick``` that stores the code for the ev3 brick and a folder called
```computer``` that stores the code for a server to communicate with
the brick.

The ev3dev site provides a [tutorial that uses MQTT](http://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/).
It turns out that MQTT is not great for real-time communication as it is designed for asynchronous communication.
The present project chooses to use a [TCP/IP connection](https://pythonspot.com/python-network-sockets-programming-tutorial/) instead.

The general pattern is we send data between the client and the server as
an encoded JSON string.

## Install on Computer

Create a new virtual environment using Python or Conda.

```conda create --name robot python```

Setup environment variables for the server IP address and port to use
for the TCP connection. For conda we can use the instructions [here](https://conda.io/docs/user-guide/tasks/manage-environments.html#macos-and-linux).
Then edit the files as instructed and set the following variables:
HOST=\[IP Address of server\]
PORT=\[Port to use on server\]
and unset these in the deactivate file.

## Install on Brick

Copy the files from the ```brick``` folder into the home directory of
the ```robot``` user. I use SFTP to access the file system and just
copy the files across.

## Running Remote Control

### Run the Brain on the Server

Navigate to the top of the directories (e.g. the robot folder).

Run python - ```python```.
Import the RobotBrain then run wait_for_connect:
```from computer.socket_server import RobotBrain
brian = RobotBrain()
brian.wait_for_connect()```

## Run the Brick

SSH into the robot:
```ssh robot@ev3dev.local```
Then when logged in check the HOST and PORT env variables match.
Then run:
```python3
from brick_client import Robot
r = Robot()```

On the server you should see a connection register:
```Connection address: ('[Robot IP Address', X)```

Now run - ```r.remote_control()``` on the robot and ```brian.remote_control()```
on the server. You should be able to use the a-w-s-d keys to move L-F-B-R!



