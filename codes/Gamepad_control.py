import pygame
import time
#import bluetooth as bt
#import socket
import sys
from Mapping_speed import joystickToDiff,mechanum,omni
'''def send(dir2):
    s.send(bytes(dir2,'UTF-8'))'''


'''def digital_drive(button_val):
    flag=False
    if(button_val[11]==1):
        print(127,127,sep=' ')
        flag=True
    elif(button_val[12]==1):
        print(-127,-127,sep=' ')
        flag=True
    elif(button_val[13]==1):
        print(127,0,sep=' ')
        flag=True
    elif(button_val[14]==1):
        print(0,127,sep=' ')
        flag=True
    else:
         pass
    return flag'''
         

def dir(axis_val):
    dir1=""
    if(0 in axis_val.keys() and 1 in axis_val.keys()):
        x=round(axis_val[0],1)
        y=round(axis_val[1],1)
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
    
speed=[10]
flag1=[0]
flag2=[0]

def speedsend(button_val,speed):
    l1=button_val[9]
    r1=button_val[10]
    flag1.append(l1)
    flag2.append(r1)
    if r1==1:
        if speed[0]==100 or (flag2[-2]==r1):
            pass
        else:
            speed[0]=speed[0]+10
    
    if l1==1:
        if (speed[0]==10 or (flag1[-2]==l1)):
            pass
        else:
            speed[0]=speed[0]-10
        
           
      
    




pygame.init()
axis_data = None
button_data = None
hat_data = None
j = pygame.joystick
j.init()
if(j.get_count()==0):
    print("No Controller")
else:
    print("Controller present")
control=j.Joystick(0)
control.init()


'''addres="9C:9C:1F:C5:0E:DE"
channel = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 
socket.BTPROTO_RFCOMM)
s.connect((addres,channel))'''



#print(control.get_name())
#print(control.get_numaxes())    
#print(control.get_numbuttons())
if not axis_data:
            axis_data = {}

if not button_data:
            button_data = {}
            for i in range(control.get_numbuttons()):
                button_data[i] = False
if not hat_data:
            hat_data = {}
            for i in range(control.get_numhats()):
                  hat_data[i] = (0, 0)


try:
 while True:
        for event in pygame.event.get():
            #start=time.time()
             if event.type == pygame.JOYAXISMOTION:
                axis_data[event.axis] = round(event.value,2)
             if event.type == pygame.JOYBUTTONDOWN:
                button_data[event.button] = True
             if event.type == pygame.JOYBUTTONUP:
                button_data[event.button] = False
             if event.type == pygame.JOYHATMOTION:
                hat_data[event.hat] = event.value
             
             #print(axis_data)
             #if(digital_drive(button_data)):
                  #continue
            
             dir1=dir(axis_data)
             if dir1:
                
                 print(dir1,end=' ')
                 speedsend(button_data,speed)
                 inch=speed[0]//10
                 #print(speed[0])
                 if(inch==10):
                    inch='q'
                 else:
                    inch=str(inch)
                 print(inch)
                 if(0 in axis_data.keys() and 1 in axis_data.keys()):
                    #speed_right,speed_left=joystickToDiff(axis_data[0],axis_data[1],-1,1,-255,255)
                    omni_vel=omni(axis_data[0],axis_data[1],-255,255)
                    print(omni_vel)
                    #s.send(bytes(f"{','.join(map(str, omni_vel))}\n", "UTF-8"))
                    
                    #send(speed_s)
             #send(dir1)
             #print(axis_data.keys())   
             #time.sleep(0.1)
             if(button_data[0]==1):
                 sys.exit(0)
            #print(time.time()-start)
except KeyboardInterrupt:
    print("Interrupted")
    #s.close()
