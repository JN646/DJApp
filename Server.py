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

# declare
host = '127.0.0.1'
port = 5555
ApplicationName = 'DJ Request System'

# create a GUI variable called app
app = gui("DJ Request Server v0.4")
app.setFont(12)
app.setBg("lightBlue")
app.setResizable(canResize=False) # no fullscreen

# preferences sub window
app.startSubWindow("Preferences", modal=True)
app.addLabel("l1", "Preferences")
app.setLabelBg("l1", "blue")
app.setLabelFg("l1", "White")
app.addLabelEntry("Host: ")
app.addLabelEntry("IP: ")
app.stopSubWindow()

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
        if not data:
            break
        conn.sendall(str.encode(reply))
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
    app.setLabelBg("title", "blue")
    app.setLabelFg("title", "White")

    # request textbox
    app.startLabelFrame("Requests")
    app.addListBox("list", ["apple", "orange", "pear", "kiwi"])
    app.stopLabelFrame()

    # status bar
    app.addStatusbar(fields=1)
    app.setStatusbar("ONLINE", 0) # Due to window handeling server "cannot" be offline.
    app.setStatusbarBg("green", 0)
    app.setStatusbarFg("white", 0)

    # link the buttons to the function called press
    app.addButtons(["Accept"], press)

    # start GUI
    app.go() # start GUI
