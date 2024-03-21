import socket
import RPi.GPIO as GPIO
import serial
import math
from time import sleep
import time

HOST = "192.168.165.102"
PORT = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
comm_socket, client_add = server.accept()
print(f"Connected to: {client_add}")

out_dir1 = 19 #left
out_pwm1 = 21

out_dir2 = 23 #right
out_pwm2 = 40

dirs = [32, 35, 31]
pwms = [26, 37, 33]

conveyer_dir = 24
conveyer_pwm = 22

shoot_right_wheel_dir = 18
shoot_right_wheel_pwm = 16

shoot_left_wheel_dir = 13
shoot_left_wheel_pwm = 15

servo = 29

myPWM = []

"""def mpu_velocities(imu_ang, desired_ang):
	global pw
	vel = []
	
	if(float(imu_ang)==float(9999)):
		imu_ang = float(0.0)
	
	if(desired_ang == imu_ang):
		pw = 0
		vel = [0, 0, 0]
		
	elif(desired_ang > imu_ang and (desired_ang-imu_ang)>1):
		vel = []
		pw = ((desired_ang - imu_ang)*50)/180
		vel.append(-1*pw)
		vel.append(pw)
		vel.append(pw)
		
	elif(imu_ang > desired_ang and (imu_ang-desired_ang)>1):
		vel=[]
		pw = ((imu_ang - desired_ang)*50)/180
		vel.append(pw)
		vel.append(-1*pw)
		vel.append(-1*pw)
	
	else:
		vel = []
		pw = 0
		vel = [0, 0, 0]
		
	return vel"""
	
def movement_of_base(vels):
	
	vel1 = int(vels[0])
	vel2 = int(vels[1])
	vel3 = int(vels[2])
	
	if((vel1 == int(15) and vel2 == int(-15) and vel3 == int(30)) or (vel1 == int(-15) and vel2 == int(15) and vel3 == int(-30))):
		if(vel3<0):
			vel3 = int(-85)
			vel1 = int(-15)
			vel2 = int(15)
			
			
		elif(vel3>0):
			vel3 = int(85)
	
	"""velocities = mpu_velocities(imu_ang, desired_ang)
	velocities = [0, 0, 0]
	
	vel1 = vel1 + int(velocities[0])
	vel2 = vel2 + int(velocities[1])
	vel3 = vel3 + int(velocities[2])
	
	#print(velocities)"""
	
	if(vel1>0):
		GPIO.output(dirs[0], GPIO.LOW)
		
	elif(vel1<0):
		GPIO.output(dirs[0], GPIO.HIGH)
		
	if(vel2>0):
		GPIO.output(dirs[1], GPIO.LOW)
		
	elif(vel2<0):
		GPIO.output(dirs[1], GPIO.HIGH)
		
	if(vel3>0):
		GPIO.output(dirs[2], GPIO.LOW)
		
	elif(vel3<0):
		GPIO.output(dirs[2], GPIO.HIGH)
		
	if(vel1<-100):
		vel1 = -100
	elif(vel1>100):
		vel1 = 100
		
	if(vel2<-100):
		vel2 = -100
	elif(vel2>100):
		vel2 = 100
		
	if(vel3<-100):
		vel3 = -100
	elif(vel3>100):
		vel3 = 100
	
	try:	
		myPWM[0].ChangeDutyCycle(abs(vel1))
		myPWM[1].ChangeDutyCycle(abs(vel2))
		myPWM[2].ChangeDutyCycle(abs(vel3))
	except:
		print("in except")
			
def on_point(rot_string):
	
	print(rot_string)
	
	if(rot_string.find("LR")>=0):
		GPIO.output(dirs[0], GPIO.LOW)
		GPIO.output(dirs[1], GPIO.HIGH)
		GPIO.output(dirs[2], GPIO.HIGH)
		
		myPWM[0].ChangeDutyCycle(5)
		myPWM[1].ChangeDutyCycle(5)
		myPWM[2].ChangeDutyCycle(5)
		
	elif(rot_string.find("RR")>=0):
		GPIO.output(dirs[0], GPIO.HIGH)
		GPIO.output(dirs[1], GPIO.LOW)
		GPIO.output(dirs[2], GPIO.LOW)
		
		myPWM[0].ChangeDutyCycle(2)
		myPWM[1].ChangeDutyCycle(2)
		myPWM[2].ChangeDutyCycle(2)
		
def only_one_leadscrew(ls_side):
	
	if((ls_side.find("RIGHT")>=0) or (ls_side.find("LEFT")>=0)):
		
		if(ls_side.find("RIGHT")>=0):
			print("right leadscrew enabled")
			GPIO.output(out_dir2, GPIO.LOW)
			out_pwm2.ChangeDutyCycle(10)
			
		elif(ls_side.find("LEFT")>=0):
			print("left leadscrew enabled")
			GPIO.output(out_dir1, GPIO.LOW)
			out_pwm1.ChangeDutyCycle(15)
	
	else:
		GPIO.output(out_dir1, GPIO.HIGH)
		GPIO.output(out_dir2, GPIO.HIGH)
		out_pwm1.ChangeDutyCycle(0)
		out_pwm2.ChangeDutyCycle(0)
		
def movement_of_leadscrew(val):
	
	if(val.find("DOWN")>=0):
		vel=int(20)
		
	elif(val.find("UP")>=0):
		vel=int(-20)
		
	else:
		vel=int(0)
		
	if(vel>0):
		print("Going Down")
		GPIO.output(out_dir2, GPIO.HIGH)
		out_pwm2.ChangeDutyCycle(17)
		GPIO.output(out_dir1, GPIO.HIGH)
		out_pwm1.ChangeDutyCycle(32)
		
	elif(vel<0):
		print("Going Up")
		GPIO.output(out_dir2, GPIO.LOW)
		out_pwm2.ChangeDutyCycle(17)
		GPIO.output(out_dir1, GPIO.LOW)
		out_pwm1.ChangeDutyCycle(33)
		
	else:
		print("in else")
		out_pwm1.ChangeDutyCycle(0)
		out_pwm2.ChangeDutyCycle(0)
		
def move_belt(duty):
	
	if(duty==int(0)):
		GPIO.output(shoot_right_wheel_dir, GPIO.LOW)
		GPIO.output(shoot_left_wheel_dir, GPIO.HIGH)
		
		shoot_left_wheel_pwm.ChangeDutyCycle(0)
		shoot_right_wheel_pwm.ChangeDutyCycle(0)
		
	elif(duty==int(1)):
		GPIO.output(shoot_right_wheel_dir, GPIO.LOW)
		GPIO.output(shoot_left_wheel_dir, GPIO.HIGH)
		
		shoot_left_wheel_pwm.ChangeDutyCycle(23) #initially 33
		shoot_right_wheel_pwm.ChangeDutyCycle(23)
		
	elif(duty==int(2)):
		GPIO.output(shoot_right_wheel_dir, GPIO.LOW)
		GPIO.output(shoot_left_wheel_dir, GPIO.HIGH)
		
		shoot_left_wheel_pwm.ChangeDutyCycle(56) #initially 49
		shoot_right_wheel_pwm.ChangeDutyCycle(56)
		
	elif(duty==int(3)):
		GPIO.output(shoot_right_wheel_dir, GPIO.LOW)
		GPIO.output(shoot_left_wheel_dir, GPIO.HIGH)
		
		shoot_left_wheel_pwm.ChangeDutyCycle(75) #initially 68
		shoot_right_wheel_pwm.ChangeDutyCycle(75)
		
def move_servo_once(act):
	
	if(act=="SHOOT"):
		
		servo_pwm.ChangeDutyCycle(2)
		sleep(0.9)
		"""movement_of_leadscrew("UP")
		sleep(0.2)
		movement_of_leadscrew("NO")
		sleep(0.05)"""
		servo_pwm.ChangeDutyCycle(8)
		sleep(0.3)
		return
		
	elif(act=="OUT"):
		servo_pwm.ChangeDutyCycle(2)
		sleep(1)
		return
		
def shoot_n_times():
	
	print("shooting multiple times")
	print("\n")
	move_belt(3)
	for i in range(3):
		servo_pwm.ChangeDutyCycle(2)
		sleep(0.7)
		movement_of_leadscrew("UP")
		sleep(0.2)
		movement_of_leadscrew("NO")
		sleep(0.1)
		servo_pwm.ChangeDutyCycle(9)
		sleep(0.9)
			
	move_belt(2)
	for i in range(3):
		servo_pwm.ChangeDutyCycle(2)
		sleep(0.7)
		movement_of_leadscrew("UP")
		sleep(0.2)
		movement_of_leadscrew("NO")
		sleep(0.1)
		servo_pwm.ChangeDutyCycle(9)
		sleep(0.9)
			
	move_belt(1)
	for i in range(3):
		servo_pwm.ChangeDutyCycle(2)
		sleep(0.7)
		movement_of_leadscrew("UP")
		sleep(0.1)
		movement_of_leadscrew("NO")
		sleep(0.1)
		servo_pwm.ChangeDutyCycle(9)
		sleep(0.9)		
		move_belt(1)
			
def shooting_thread():
	global shooting
	shooting = True
	shoot_n_times()
	shooting = False
	
if __name__=='__main__':
	global shooting
	zoo = ""
	vel = [0, 0, 0]
	GPIO.setmode(GPIO.BOARD)
	
	#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	
	GPIO.setup(out_dir1, GPIO.OUT)
	GPIO.setup(out_pwm1, GPIO.OUT)
	out_pwm1 = GPIO.PWM(out_pwm1, 10000)
	
	GPIO.setup(out_dir2, GPIO.OUT)
	GPIO.setup(out_pwm2, GPIO.OUT)
	out_pwm2 = GPIO.PWM(out_pwm2, 10000)
	
	for i in range(3):
		GPIO.setup(dirs[i], GPIO.OUT)
		GPIO.setup(pwms[i], GPIO.OUT)
		myPWM.append(GPIO.PWM(pwms[i], 10000))
		
	for i in range(3):
		myPWM[i].start(0)
		
	GPIO.setup(servo, GPIO.OUT)
	servo_pwm = GPIO.PWM(servo, 50)
	
	GPIO.setup(shoot_right_wheel_dir, GPIO.OUT)
	GPIO.setup(shoot_right_wheel_pwm, GPIO.OUT)
	shoot_right_wheel_pwm = GPIO.PWM(shoot_right_wheel_pwm, 10000)
	
	GPIO.setup(shoot_left_wheel_dir, GPIO.OUT)
	GPIO.setup(shoot_left_wheel_pwm, GPIO.OUT)
	shoot_left_wheel_pwm = GPIO.PWM(shoot_left_wheel_pwm, 10000)
	
	GPIO.setup(conveyer_dir, GPIO.OUT)
	GPIO.setup(conveyer_pwm, GPIO.OUT)
	conveyer_pwm = GPIO.PWM(conveyer_pwm, 10000)
	
	servo_pwm.start(2)
	shoot_right_wheel_pwm.start(0)
	shoot_left_wheel_pwm.start(0)
	conveyer_pwm.start(45)
	out_pwm1.start(0)
	out_pwm2.start(0)
	
	for i in range(5):
		zoo = comm_socket.recv(8192).decode('utf-8', 'ignore')
	
	imu_ang = 0
	desired_ang = 0
	shooting = False
	
	values = ""
	value = ""
	c = 0
	array = []
	prev_buttons = "1111111111111"
	c_negative=0
	c_positive=0
	flybelt_duty=0
	GPIO.output(conveyer_dir, GPIO.HIGH)
	conveyer_pwm.ChangeDutyCycle(60)
	while True:
		
		c = c+1
		vels = []
		index1 = float(-1)
		index2 = float(-1)
		
		message = comm_socket.recv(8192).decode('utf-8', 'ignore')
		
		for i in range(len(message)):
			if(index1==-1):
				if(message[i]=='['):
					index1=int(i)
			if(index1!=float(-1) and index2==float(-1) and i!=index1):
				if(message[i]==']'):
					index2=int(i)
					break
		
		if(index1==-1 or index2==-1):
			continue
		
		"""ser.flush()	
		if(ser.in_waiting > 0):
			value = ser.readline().decode('utf-8', 'ignore')
		print(value)"""
		
		values = message[index1+1 : index2]
		array = values.split(",")
		sums = 0
		
		for i in range(3):
			sums=sums+int(array[i])
			vels.append(int(array[i]))
		
		buttons = array[3]
		index1 = -1
		index2  -1
		index1 = buttons.find("\'")
		index2 = buttons.rfind("\'")
		buttons=buttons[index1+1:index2]
		
		print(vels)
		print(buttons)
		
		if(buttons=="1111111111111" and sums==0):
			out_pwm1.ChangeDutyCycle(0)
			out_pwm2.ChangeDutyCycle(0)
			for i in range(3):
				myPWM[i].ChangeDutyCycle(0)
			servo_pwm.ChangeDutyCycle(0)
			
		
		elif(sums!=0 and buttons=="1111111111111"):
			movement_of_base(vels)
			
		if(buttons.find("0")==0):
			on_point("LR")
			
		elif(buttons.find("01")==1):
			on_point("RR")
		
		else:
			out_pwm1.ChangeDutyCycle(0)
			out_pwm2.ChangeDutyCycle(0)
			
		if(buttons.find("01")==2):
			only_one_leadscrew("LEFT")
			
		elif(buttons.find("01")==3):
			only_one_leadscrew("RIGHT")
			
		else:
			out_pwm1.ChangeDutyCycle(0)
			out_pwm2.ChangeDutyCycle(0)
		
		if(buttons.find("01")==4):
			movement_of_leadscrew("UP")
		
		elif(buttons.rfind("0")==5):
			movement_of_leadscrew("DOWN")
			
				
		elif(buttons.find("01")==6 and prev_buttons != buttons):
			print("servo out")
			move_servo_once("OUT")
		
		elif(buttons.find("01")==7 and prev_buttons != buttons):
			print("shoot once")
			move_servo_once("SHOOT")
			
		elif(buttons.find("01")==8 and prev_buttons != buttons):
			print("shooting multiple times")
			shooting_thread()
		
		elif(buttons.find("01")==9 and prev_buttons != buttons):
			print("moving flybelt")
			flybelt_duty = flybelt_duty + 1
			move_belt(flybelt_duty%4)
		
		elif(buttons.find("01")==10):
			print("STOP LEADSCREW")
			out_pwm1.ChangeDutyCycle(0)
			out_pwm2.ChangeDutyCycle(0)
			
		prev_buttons = buttons
