import socket
import sys

try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err:
    print("Failed to create a socket")
    print("Reason %s"&str(err))
    sys.exit()
print("Socket created")
target_host=input("Enter target host name to connect :")
target_port=input("Enter target port :")
try:
    s.connect((target_host,int(target_port)))
    print("Socket connected to host {} and port {}".format(target_host,target_port))
    s.shutdown(2)
except socket.error as err:
    print("Failed to connect to host {} and port {}".format(target_host,target_port))
    print("Reason {} ".format(err))
    sys.exit()

