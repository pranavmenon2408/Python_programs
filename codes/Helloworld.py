import pygame
import time
#import bluetooth as bt
import socket
from Mapping_speed import joystickToDiff

class Gamepad(object):
    def __init__(self):
        pygame.init()
        self.control=pygame.joystick.Joystick(0)
        self.control.init()
        self.address="84:CC:A8:7A:38:C2"
        self.channel=1
        self.s=socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.s.connect((self.address,self.channel))
        self.axis_data=None
        self.button_data=None
        if not self.axis_data:
            self.axis_data={}
        if not self.button_data:
            self.button_data={}
            for i in range(self.control.get_numbuttons()):
                self.button_data[i]=False

    def infosend(self,dir2):
        self.s.send(bytes(dir2,'UTF-8'))
    




    def dir(self):
       dir1=""
       if(0 in self.axis_data.keys() and 1 in self.axis_data.keys()):
            x=round(self.axis_data[0],1)
            y=round(self.axis_data[1],1)
            if(x==0.0 and y==0.0):
               dir1="S"
               return dir1
       else:
            dir1="S"
            return dir1
    
    
       if ((y<=-0.8 and y>=-1.0) and (x<0.3 and x>-0.3)):
            dir1="F"
       elif (y<=1.0 and y>0.75) and (x<0.3 and x>-0.3):
            dir1="B"
       elif (x>0.85 and x<=1.0) and (y<0.3 and y>-0.3):
            dir1="R"
       elif (x<-0.85 and x>=-1.0) and (y<0.3 and y>-0.3):
            dir1="L"
       elif (x>=0.3 and x<=1.0):
            if(y>=0.3 and y<=1.0):
                dir1="J"
            elif(y>=-1.0 and y<=-0.3):
                dir1="I"
       elif (x<=-0.3 and x>=-1.0):
            if(y>=0.3 and y<=1.0):
                dir1="H"
            elif(y>=-1.0 and y<=-0.3):
                dir1="G"
       return dir1
     



    def movement(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                if event.type == pygame.JOYBUTTONDOWN:
                   self.button_data[event.button] = True
                if event.type == pygame.JOYBUTTONUP:
                   self.button_data[event.button] = False
                
                #print(self.axis_data)
                dir1=dir(self)
                print(dir1,end=' ')
                self.infosend(dir1)

if __name__=='__main__':
    try:
        x=Gamepad()
        x.movement()
    except KeyboardInterrupt:
        print("Interrupted")
