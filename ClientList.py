##  DJ Request System (Client)
##  Written by J AW Ginn (C) 2017

# imports
import socket
import sys
import time
import webbrowser
from appJar import gui

# define Connection
host = '127.0.0.1'
port = 5555

# create a GUI variable called app
app = gui("DJ Request Client v0.4")
app.setFont(12)
app.setBg("lightBlue")
app.setResizable(canResize=False) # no fullscreen

# oSpen and bind ports
s = socket.socket()

# add intro text
print("      DJ Request Client v0.4")
print("") # new line
print("*********************************")
print("*    DJ Request Client - CLI    *")
print("*      Written by J AW Ginn     *")
print("*            (C) 2017           *")
print("*********************************")

# server start time
print("Client started at: " + str(time.strftime('%H:%M:%S', time.gmtime(time.time()))))
print("") # new line

# handle button events
def press(button):
    if button == "Submit":
        usr = app.getEntry("Request")
        try:
            s.send(usr.encode())
            print("Sent:", usr)
        except socket.error as e:
            app.warningBox("Error", "Error", parent=None)
            print(str(e))

# request song from list
def Requestpress(button):
    if button == "Request":
            items = app.getListBox("list")
            if len(items)> 0:
                app.selectListItem("list", items[0], callFunction=True)
                #Add code to send the name of the selected item to the server.
                print(app.selectListItem("list", items[0], callFunction=True))

# genre buttons
def pressGenre(button):
    if button == "Pop":
        genre = "POP"
        sendGenre(genre)
    elif button == "Dance":
        genre = "DANCE"
        sendGenre(genre)
    elif button == "Rock":
        genre = "ROCK"
        sendGenre(genre)
    elif button == "Jazz":
        genre = "JAZZ"
        sendGenre(genre)
    elif button == "RnB":
        genre = "RNB"
        sendGenre(genre)
    elif button == "Other":
        genre = "OTHER"
        sendGenre(genre)
    elif button == "Test":
        genre = "TEST"
        sendGenre(genre)

# handles genre buttons
def sendGenre(genre):
    try:
        s.send(genre.encode())
        print("Sent:", genre)
    except socket.error as e:
        app.warningBox("Error", "Request for " + genre + " has not been sent", parent=None)
        print(str(e))

# handles menu buttons
def mnuPress(button):
    if button == "Close":
        closeConn()
    elif button == "Refresh":
        refreshConn()
    elif button == "About":
        aboutbox()

# start the connection
def startConn():
    try:
        s.connect((host, port))
        print("Connection Made!")
    except socket.error as e:
        app.warningBox("Connection Error", "Cannot find the host.", parent=None)
        print("Connection Failed! - Cannot find the host on: "+str(host)+":"+str(port))
        print(str(e))
        app.stop()
        sys.exit()

# close the connection and the application.
def closeConn():
    try:
        s.close()
        app.stop()
    except socket.error as e:
        print(str(e))

# refresh connection
def refreshConn():
    try:
        print("Refreshing connection")
        closeConn() # close existing connection (if present)
        startConn() # start new connection
    except socket.error as e:
        # catch error and failure scenario
        app.warningBox("Connection Error", "Cannot refresh the connection", parent=None)
        print(str(e))

# about box
def aboutbox():
    app.infoBox("About", "DJ Request App - Client", parent=None)

# start connection
startConn()

# app menu bar
fileMenus = ["Refresh","-","Close"]
helpMenus = ["About"]
app.addMenuList("File", fileMenus, mnuPress)
app.addMenuList("Help", helpMenus, mnuPress)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "DJ Request Client")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "White")

# add genre buttons
app.startLabelFrame("Genres")
app.addButtons(["Pop", "Dance", "Rock", "Jazz", "RnB", "Other", "Test"], pressGenre)
app.stopLabelFrame()

# song list
app.startLabelFrame("Song List")
app.addListBox("list", ["apple", "orange", "pear", "kiwi"])
app.addButtons(["Request"], Requestpress)
app.stopLabelFrame()

# add text field
app.startLabelFrame("Send Request")
app.addLabelEntry("Request")
app.addButtons(["Submit"], press)
app.stopLabelFrame()

# set the initial field of entry
app.setFocus("Request")

# start GUI
app.go() # start GUI
