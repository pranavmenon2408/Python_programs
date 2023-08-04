import socket
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("127.0.0.1",12345))


while True:
 try:
    data,addr=sock.recvfrom(4096)
    print(str(data))
    message="I am UDP Server"
    sock.sendto(bytes(message,'utf-8'),addr)
 except KeyboardInterrupt:
    print("Exited by user")
    sock.close()
    break
    
