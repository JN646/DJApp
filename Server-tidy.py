import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("DJ Request Server - v0.5 CLI")
print("")
print("Host: " + str(TCP_IP) + " Port: " + str(TCP_PORT))
print("")

conn, addr = s.accept()
print("Connection address:", addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:", data.decode('utf-8'))
    conn.send(data)  # echo
conn.close()
