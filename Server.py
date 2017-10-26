##  DJ Request System (Server)
##  Written by J AW Ginn (C) 2017

# imports
import socket
import sys
import time
import csv
import webbrowser
import logging
from datetime import datetime
from _thread import *
from appJar import gui

# logging config
logging.basicConfig(filename="LOGS/SERVER-logging.log", level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# define Colours
colour = [
    "Black",
    "White",
    "GreenYellow",
    "blue",
    "LightSteelBlue",
    "RoyalBlue",
    "Red"]

# declare
host = '127.0.0.1'
port = 5555
ApplicationName = 'DJ Request System'

# create a GUI variable called app
app = gui("DJ Request Server v0.4")
app.setBg(colour[4])
app.setResizable(canResize=False) # no fullscreen
app.setFont(12)
app.setPadding([10,5])      # 20 pixels padding outside the widget [X, Y]
app.setInPadding([5,5])     # 5 pixels padding inside the widget [X, Y]

# declare Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try to bind host
try:
    s.bind((host, port))
    # add intro text
    print("      DJ Request Client v0.4b")
    print("") # new line
    print("*********************************")
    print("*    DJ Request Server - CLI    *")
    print("*      Written by J AW Ginn     *")
    print("*            (C) 2017           *")
    print("*********************************")
    print("") # new line

    # server start time
    print("Server started at: " + str(time.strftime('%H:%M:%S', time.gmtime(time.time()))))
    print("") # new line

    # GUI notice
    print("NOTE: GUI will only open when a client connection has been made...")
    print("Waiting for client connection...")
    print("") # new line

    # host details
    print("Host: " + str(host) + " Port: " + str(port))
    print("") # new line

    # error catch
except socket.error as e:
    print(str(e))

#Start listening
s.listen(5)

#Start threaded client

# TELNET Connection
def threaded_client(conn):

    # beware of Windows TELNET bug (line breaks)
    conn.send(str.encode('Welcome to DJ Request System, type your request\n'))

    #Receive data
    while True:
        try:
            data = conn.recv(2048)
            reply = 'Server Output: '+data.decode('utf-8')
            app.addListItem("list", data.decode('utf-8'))

            # recieved message console identifier
            print(str(datetime.now().strftime("%H:%M:%S"))+" ->"+" R "+"-> "+data.decode('utf-8'))
        except socket.error as e:
            logging.warning(str(e))
        try:
            # causes application failure on closing connection.
            if not data:
                logging.warning("Client has disconnected.")
                break
            conn.sendall(str.encode(reply))
        except socket.error as e:
            logging.warning(str(e))
    #Close connection
    conn.close()

while True:
    #Accept connection
    try:
       conn, addr = s.accept()
       logging.info('connected to: '+addr[0]+':'+str(addr[1]))
       connStat = 1
    except socket.error as e:
       logging.warning(str(e))

    #Start client
    start_new_thread(threaded_client,(conn,))

    # handle button events
    def press(button):
        if button == "Cancel":
            connClose()
        else:
            items = app.getListBox("list")
            if len(items)> 0:
                app.removeListItem("list", items[0])
                logging.info(str(datetime.now().strftime("%H:%M:%S"))+" ->"+" I "+"-> "+"Request Deleted")

    # handle menu button events
    def mnuPress(button):
       if button == "Close":
           connClose()
       elif button == "About":
           aboutbox()

    # handle button events
    def tbFunc(button):
        if button == "ABOUT":
            aboutbox()
        elif button == "REFRESH":
            refreshbutton()
        elif button == "CLOSE":
            connClose()
        elif button == "PRINT":
            printbutton()
        elif button == "PREFERENCES":
            preferencesbutton()
        elif button == "HELP":
            webbrowser.open("README.html")  # Go to readme html.

    # close connection
    def connClose():
        try:
           logging.info("Application has closed...")
           connStat = 0
           s.close()
           app.stop()
        except socket.error as e:
           logging.warning(str(e))

    # preferences sub window
    def launch():
       app.showSubWindow("Preferences")

    # about box
    def aboutbox():
        app.infoBox("About", "DJ Request App - Server", parent=None)

    # print button
    def printbutton():
        print(app.getAllListItems("list")) # print items to the console
        
    # preferences button
    def preferencesbutton():
        logging.info("Preferences Button Pressed") # not implemented
        #app.infoBox("Coming Soon...", "Preferences not implemented.", parent=None)
        launch()

    # refresh button
    def refreshbutton():
        logging.info("Refreshing connection") # not implemented
        app.infoBox("Coming Soon...", "Refresh Connection not implemented.", parent=None)

    # update host details
    def updateHost(button):
        if button == "Update":
            logging.info("Updating host...") # not implemented
        elif button == "Cancel":
            app.hideSubWindow("Preferences")

    # font sizes
    def fontSize(i):
        logging.info("Font Size control")
        app.setFont(12)
        if i == 0:
            app.setFont(10)
        if i == 1:
            app.setFont(11)
        if i == 2:
            app.setFont(12)
        if i == 3:
            app.setFont(13)
        if i == 4:
            app.setFont(14)
            
    ## MAIN APPLICATION
    # app menu bar
    fileMenus = ["Close"]
    helpMenus = ["About"]
    app.addMenuList("File", fileMenus, mnuPress)
    app.addMenuList("Help", helpMenus, mnuPress)

    app.createMenu("Config")
    app.addSubMenu("Config", "Font Size")
    for i in range(5):
        app.addMenuRadioButton("Font Size", "font", "1" + str(i), fontSize)
    
    # toolbar
    tools = ["ABOUT", "REFRESH", "CLOSE", "PRINT", "IMPORT", "PREFERENCES", "HELP"]

    # add toolbar with icons
    app.addToolbar(tools, tbFunc, findIcon=True)
    app.setToolbarPinned(pinned=True)

    # add & configure widgets - widgets get a name, to help referencing them later
    app.addLabel("title", "DJ Request Server")
    app.setLabelBg("title", colour[5])
    app.setLabelFg("title", colour[1])

    # request textbox
    app.addListBox("list", ["apple", "orange", "pear", "kiwi"])

    # status bar
    app.addStatusbar(fields=1)

    if connStat == 0:
        app.setStatusbar("OFFLINE", 0) # Due to window handeling server "cannot" be offline.
        app.setStatusbarBg(colour[6], 0)
        app.setStatusbarFg(colour[0], 0)
    else:
        app.setStatusbar("ONLINE", 0) # Due to window handeling server "cannot" be offline.
        app.setStatusbarBg(colour[2], 0)
        app.setStatusbarFg(colour[0], 0)

    # link the buttons to the function called press
    app.addButtons(["CHECK"], press)

    ## PREFERENCES WINDOW
    # preferences sub window
    app.startSubWindow("Preferences", modal=True)
    app.setPadding([10,5]) # 20 pixels padding outside the widget [X, Y]
    app.setInPadding([5,5]) # 5 pixels padding inside the widget [X, Y]
    app.setResizable(canResize=False) # no fullscreen
    app.setFont(12)
    app.setBg(colour[4])
    app.addLabel("l1", "Preferences")
    app.setLabelBg("l1", colour[5])
    app.setLabelFg("l1", colour[1])

    # host update controls
    # app.startLabelFrame("Update Host")
    app.addLabelEntry("IP:   ")
    app.addLabelEntry("Port: ")
    app.setEntryDefault("IP:   ", str(host))
    app.setEntryDefault("Port: ", str(port))
    app.addButtons(["Update", "Cancel"], updateHost)
    # app.stopLabelFrame()

    # stop sub window
    app.stopSubWindow()

    # start GUI
    try:
        app.go()
    except GUIError: # GUI error catch
        logging.warning("GUI Error")
