# DJ Song Request Application
This is a DJ song request server/client application.
## Application Status
This is a work in progress application that is in it's infancy. This is a proof of concept of a DJ music request application that is both web based and cross platform.

**NOTE: This application is in it's very early stages of development and should not be used in a production environment and is provided _'As Is'_ for educational purposes.**

### Server
The server application runs in python with both a console and GUI. This accepts song requests from the client applications. The DJ can then mark off the requests as they arrive at the system.

### Client
The client application runs in python with both a console and a GUI. This application sends song requests to a server on running on the same network. The user can choose from a genre, individual song or manually type a request before it is sent.

### Web
The web application is a work in progress that will allow WebSocket connection to the Python server, providing similar capabilities as the python client application. This will be using Bootstrap v4.0-beta3 and will be responsive to all device screens and sizes.

## Required dependencies
This applications require the following Python dependencies to run as expected. These should be downloaded and placed in the root folder.
- AppJar - GUI and interface.