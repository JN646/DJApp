# import the library
import socket
import sys
import time
import webbrowser
from appJar import gui

#Define Connection
host = '127.0.0.1'
port = 5555

# create a GUI variable called app
app = gui("DJ Request Client v0.3")
app.setFont(12)
app.setBg("lightBlue")
app.setResizable(canResize=False)
#app.setGeometry(400,800)

#Open and bind ports
s = socket.socket()

print("      DJ Request Client v0.3")
print("")
print("*********************************")
print("*    DJ Request Client - CLI    *")
print("*      Written by J AW Ginn     *")
print("*            (C) 2017           *")
print("*********************************")
print("Client started at: " + str(time.strftime('%H:%M:%S', time.gmtime(time.time()))))
print("")

try:
    s.connect((host, port))
    print("Connection Made!")
except socket.error as e:
    app.warningBox("Connection Error", "Cannot find the host.", parent=None)
    print("Connection Failed! - Can not find the host on: "+str(host)+":"+str(port))
    print(str(e))
    app.stop()
    sys.exit()

# handle button events
def press(button):
    if button == "Cancel":
        s.close()
        app.stop()
    else:
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
                #app.removeListItem("list", items[0])
                print(app.selectListItem("list", items[0], callFunction=True))
            
def pressGenre(button):
    if button == "Pop":
        genre = "POP"
        try:
            s.send(genre.encode())
            print("Sent:", genre)
        except socket.error as e:
            app.warningBox("Error", "Request Not Sent", parent=None)
            print(str(e))
    elif button == "Dance":
        genre = "DANCE"
        try:
            s.send(genre.encode())
            print("Sent:", genre)
        except socket.error as e:
            app.warningBox("Error", "Request Not Sent", parent=None)
            print(str(e))
    elif button == "Rock":
        genre = "ROCK"
        try:
            s.send(genre.encode())
            print("Sent:", genre)
        except socket.error as e:
            app.warningBox("Error", "Request Not Sent", parent=None)
            print(str(e))
    elif button == "Jazz":
        genre = "JAZZ"
        try:
            s.send(genre.encode())
            print("Sent:", genre)
        except socket.error as e:
            app.warningBox("Error", "Request Not Sent", parent=None)
            print(str(e))
    elif button == "RnB":
        genre = "RNB"
        try:
            s.send(genre.encode())
            print("Sent:", genre)
        except socket.error as e:
            app.warningBox("Error", "Request Not Sent", parent=None)
            print(str(e))
    elif button == "Other":
        genre = "OTHER"
        try:
            s.send(genre.encode())
            print("Sent:", genre)
        except socket.error as e:
            app.warningBox("Error", "Request Not Sent", parent=None)
            print(str(e))

def mnuPress(button):
    if button == "Close":
        s.close()
        app.stop()
    elif button == "Refresh":
        print("Refreshing connection")

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
app.addButtons(["Pop", "Dance", "Rock", "Jazz", "RnB", "Other"], pressGenre)
app.stopLabelFrame()

# song list
app.startLabelFrame("Song List")
app.addListBox("list", ["apple", "orange", "pear", "kiwi"])
app.addButtons(["Request"], Requestpress)
app.stopLabelFrame()

# add text field
app.startLabelFrame("Send Request")
app.addLabelEntry("Request")
app.stopLabelFrame()

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)

# set the initial field of entry
app.setFocus("Request")

# start the GUI
app.go()
