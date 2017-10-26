##  DJ Request System (Client)
##  Written by J AW Ginn (C) 2017

# imports
import socket
import sys
import time
import webbrowser
import logging
import csv
from appJar import gui

# logging config
logging.basicConfig(filename="LOGS/CLIENT-logging.log", level=logging.WARNING,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# define Colours
colour = [
    "Black",
    "White",
    "GreenYellow",
    "blue",
    "LightSteelBlue",
    "RoyalBlue",
    "CrimsonRed"]

# define Connection
host = '127.0.0.1'
port = 5555

# create a GUI variable called app
app = gui("DJ Request Client v0.4c")
app.setFont(12)
app.setBg(colour[4])
app.setResizable(canResize=False) # no fullscreen

# oSpen and bind ports
s = socket.socket()

# add intro text
print("      DJ Request Client v0.4c")
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
            logging.info("Sent:", usr)

            # TODO
            # add code to check to see if the field is empty.
            # Do not allow message to be sent if field is empty.

            app.clearEntry("Request", callFunction=True) # clears the text box
        except socket.error as e:
            app.warningBox("Error", "Error", parent=None)
            logging.warning(str(e))

# request song from list
def Requestpress(button):
    if button == "Request":
        items = app.getListBox("list")
        if len(items)> 0:
            # send the selected item to the server.
            s.send(str(items[0]).encode())
            app.setListItemBg("list", app.getListBox("list"), colour[3])
            logging.info("Sent:", app.getListBox("list")) # get name of selected item
            app.removeListItem("list", items[0])
        else:
            logging.info("No selected item.")

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
        logging.info("Sent:", genre) # send a copy of the message to local console.
    except socket.error as e:
        app.warningBox("Error", "Request for " + genre + " has not been sent", parent=None)
        logging.warning(str(e))

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
        s.connect((host, port)) # connect to host and port.
        logging.info("Connection Made!")
    except socket.error as e:
        app.warningBox("Connection Error", "Cannot find the host.", parent=None)
        logging.warning("Connection Failed! - Cannot find the host on: "+str(host)+":"+str(port))
        logging.warning(str(e))
        app.stop() # stop the app
        sys.exit() # close all windows and kill the process

# close the connection and the application.
def closeConn():
    try:
        s.close()   # close the connection
        app.stop()  # stop the app
    except socket.error as e:
        logging.warning(str(e))

# refresh connection
def refreshConn():
    try:
        logging.info("Refreshing connection")
        closeConn() # close existing connection (if present)
        startConn() # start new connection
    except socket.error as e:
        # catch error and failure scenario
        app.warningBox("Connection Error", "Cannot refresh the connection", parent=None)
        logging.warning(str(e))

# about box
def aboutbox():
    app.infoBox("About", "DJ Request App - Client", parent=None)

# file import
def fileImport():
    # open list of songs.
    with open('WordList.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            # add each line as a new list item.
            app.addListItem("list", line[1] + " - " + line[0])

# start connection
startConn()

# app menu bar
fileMenus = ["Refresh","-","Close"]
helpMenus = ["About"]
app.addMenuList("File", fileMenus, mnuPress)
app.addMenuList("Help", helpMenus, mnuPress)

# set widget padding
app.setPadding([10,5])      # 20 pixels padding outside the widget [X, Y]
app.setInPadding([5,5])     # 5 pixels padding inside the widget [X, Y]

# add Title label
app.addLabel("title", "DJ Request Client")
app.setLabelBg("title", colour[5])
app.setLabelFg("title", colour[1])

# add genre buttons
app.addButtons(["Pop", "Dance", "Rock", "Jazz", "RnB", "Other", "Test"], pressGenre)

# song list
app.addListBox("list", ["Remove.Me"])
fileImport()
app.addButtons(["Request"], Requestpress)

# add text field
app.addLabelEntry("Request")
app.addButtons(["Submit"], press)
app.setEntryMaxLength("Request", 30)

# set the initial field of entry
app.setFocus("Request")

# start GUI
try:
    app.go()
except GUIError: # GUI error catch
    logging.warning("GUI Error")
