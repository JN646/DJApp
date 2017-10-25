##  DJ Request System (Server)
##  Written by J AW Ginn (C) 2017

# imports
import socket
import sys
import time
import webbrowser
from datetime import datetime
from _thread import *
from appJar import gui

# define Colours
colour = [ "Black", "White", "GreenYellow", "blue", "LightSteelBlue", "RoyalBlue", "CrimsonRed"]

# declare
host = '127.0.0.1'
port = 5555
ApplicationName = 'DJ Request System'

# create a GUI variable called app
app = gui("DJ Request Server v0.4")
app.setFont(12)
app.setBg(colour[4])
app.setResizable(canResize=False) # no fullscreen
app.setPadding([10,5]) # 20 pixels padding outside the widget [X, Y]
app.setInPadding([5,5]) # 5 pixels padding inside the widget [X, Y]

# declare Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try to bind host
try:
    s.bind((host, port))
    # add intro text
    print("      DJ Request Client v0.4")
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
            print(str(e))
        try:
            if not data:
                break
            conn.sendall(str.encode(reply))
        except socket.error as e:
            print(str(e))
    #Close connection
    conn.close()

while True:
    #Accept connection
    try:
       conn, addr = s.accept()
       print('connected to: '+addr[0]+':'+str(addr[1]))
    except socket.error as e:
       print(str(e))

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
                print(str(datetime.now().strftime("%H:%M:%S"))+" ->"+" I "+"-> "+"Request Deleted")

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
           print("Application has closed...")
           s.close()
           app.stop()
        except socket.error as e:
           print(str(e))

    # preferences sub window
    def launch():
       app.showSubWindow("Preferences")

    # about box
    def aboutbox():
        app.infoBox("About", "DJ Request App - Server", parent=None)

    # print button
    def printbutton():
        print("Print Button Pressed") # not implemented
        app.infoBox("Coming Soon...", "Print not implemented.", parent=None)

    # preferences button
    def preferencesbutton():
        print("Preferences Button Pressed") # not implemented
        #app.infoBox("Coming Soon...", "Preferences not implemented.", parent=None)
        launch()

    # refresh button
    def refreshbutton():
        print("Refreshing connection") # not implemented
        app.infoBox("Coming Soon...", "Refresh Connection not implemented.", parent=None)

    # Update host details
    def updateHost(button):
        if button == "Update":
            print("Updating host...") # not implemented
        elif button == "Cancel":
            app.hideSubWindow("Preferences")
    ## MAIN APPLICATION
    # app menu bar
    fileMenus = ["Close"]
    helpMenus = ["About"]
    app.addMenuList("File", fileMenus, mnuPress)
    app.addMenuList("Help", helpMenus, mnuPress)

    # toolbar
    tools = ["ABOUT", "REFRESH", "CLOSE", "PRINT", "PREFERENCES", "HELP"]

    # add toolbar with icons
    app.addToolbar(tools, tbFunc, findIcon=True)

    # add & configure widgets - widgets get a name, to help referencing them later
    app.addLabel("title", "DJ Request Server")
    app.setLabelBg("title", colour[5])
    app.setLabelFg("title", colour[1])

    # request textbox
    #app.startLabelFrame("Requests")
    app.addListBox("list", ["apple", "orange", "pear", "kiwi"])
    #app.stopLabelFrame()

    # status bar
    app.addStatusbar(fields=1)
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
        print("GUI Error")
