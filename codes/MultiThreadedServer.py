import socket
from _thread import *
server_socket=socket.socket()

host="127.0.0.1"
port=1233
thread_count=0


server_socket.bind((host,port))



print("Waiting for connection")
server_socket.listen(5)

def client_thread(connection):
    connection.send(str.encode("Hey welcome to the server"))
    while True:
        data=connection.recv(2048)
        reply="Hello I am server {} ".format(data.decode('utf-8'))
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client,addr=server_socket.accept()
    print("Connected to {} and {} ".format(addr[0],addr[1]))
    start_new_thread(client_thread,(client,))
    thread_count+=1
    print(str(thread_count))
    if not client:
        break

server_socket.close()

