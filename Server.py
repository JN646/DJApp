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
app = gui("DJ Request Server v0.3")
app.setFont(12)
app.setBg("lightBlue")
app.setResizable(canResize=False)

# declare Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try to bing host
try:
    s.bind((host, port))
    print("      DJ Request Client v0.3")
    print("")
    print("*********************************")
    print("*    DJ Request Server - CLI    *")
    print("*      Written by J AW Ginn     *")
    print("*            (C) 2017           *")
    print("*********************************")
    print("")
    print("Server started at: " + str(time.strftime('%H:%M:%S', time.gmtime(time.time()))))
    print("")
    print("NOTE: GUI will only open when a client connection has been made...")
    print("Waiting for client connection...")
    print("")
    print("Host: " + str(host) + " Port: " + str(port))
    print("")
except socket.error as e:
    print(str(e))

#Start listening
s.listen(5)

#Start threaded client
def threaded_client(conn):
    conn.send(str.encode('Welcome to DJ Request System, type your request\n'))

    #Receive data
    while True:
        try:
            data = conn.recv(2048)
            reply = 'Server Output: '+data.decode('utf-8')
            app.addListItem("list", data.decode('utf-8'))
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
            try:
               print("Application has closed...")
               s.close()
               app.stop()
            except socket.error as e:
               app.warningBox("Error", "Error", parent=None)
               print(str(e))
        else:
            items = app.getListBox("list")
            if len(items)> 0:
                app.removeListItem("list", items[0])
                print(str(datetime.now().strftime("%H:%M:%S"))+" ->"+" I "+"-> "+"Request Deleted")

    def mnuPress(button):
       if button == "Close":
           connClose()

    # handle button events
    def tbFunc(button):
        if button == "ABOUT":
               app.warningBox("INFO", "About Box", parent=None)
        elif button == "REFRESH":
               print("Refreshing connection")
        elif button == "CLOSE":
               connClose()
        elif button == "PRINT":
               print("Print Button Pressed")
        elif button == "HELP":
               webbrowser.open("README.html")  # Go to readme html.

    def connClose():
        try:
           print("Application has closed...")
           s.close()
           app.stop()
        except socket.error as e:
           print(str(e))
           
    # app menu bar
    fileMenus = ["Close"]
    helpMenus = ["About"]
    app.addMenuList("File", fileMenus, mnuPress)
    app.addMenuList("Help", helpMenus, mnuPress)

    # toolbar
    tools = ["ABOUT", "REFRESH", "CLOSE", "PRINT", "PREFERENCES", "HELP"]

    app.addToolbar(tools, tbFunc, findIcon=True)
    
    # add & configure widgets - widgets get a name, to help referencing them later
    app.addLabel("title", "DJ Request Server")
    app.setLabelBg("title", "blue")
    app.setLabelFg("title", "White")

    # requests
    app.startLabelFrame("Requests")
    app.addListBox("list", ["apple", "orange", "pear", "kiwi"])
    app.stopLabelFrame()

    # status bar
    app.addStatusbar(fields=1)
    app.setStatusbar("ONLINE", 0)
    app.setStatusbarBg("green", 0)
    app.setStatusbarFg("white", 0)

    # link the buttons to the function called press
    app.addButtons(["Accept"], press)
    app.go()
