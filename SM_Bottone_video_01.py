
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
from subprocess import Popen
from subprocess import call
from subprocess import PIPE

#LedPin = 27    # pin11 --- led
BtnPin = 17    # pin17 --- button P0

state=0
movie1 = ("videoA.mp4")
movie2 = ("videoB.mp4")
video_on=0

#-------------------------------------------------------------------------------

def setup():
	GPIO.setmode(GPIO.BCM)
	#GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(BtnPin, GPIO.IN)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	#GPIO.output(LedPin, GPIO.LOW) # Set LedPin high(+3.3V) to off led
	un_var = os.system("clear") 
#-------------------------------------------------------------------------------

def CB_bottone(ev=None):
	global state
	state=2
	print("bottone premuto - next state 2")
#-------------------------------------------------------------------------------	
def check_video():
	global omxc
	global video_on
	global state
	omxc.poll()
	rcode=omxc.returncode
	print(rcode)
	if rcode is None: 
		video_on=1 #video is running
	elif rcode==0:
		video_on=0 #video is off
		state=0
		print("next state 0")

#-------------------------------------------------------------------------------

def loop():
	global omxc
	global state
	GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=CB_bottone, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
	while True:
		if state == 0:
			print("now state 0")
			'''
			GPIO.output(LedPin, GPIO.HIGH) #led on
			print("led on")
			'''
			omxc = Popen(['omxplayer', '-b', movie1] ,stdin=PIPE, stdout=PIPE)
			#omxc = Popen(['omxplayer','--win','200 200 600 600', movie1] ,stdin=PIPE, stdout=PIPE)
			state=1
			print("next state 1 - premi il bottone...")
		elif state ==2:
			print("now state 2")
			'''
			GPIO.output(LedPin, GPIO.LOW) #led off
			print("led off per 10 secondi")
			time.sleep(10)   # Don't do anything
			'''
			outs, errs = omxc.communicate(input='q')
			omxc = Popen(['omxplayer', '-b', movie2] ,stdin=PIPE, stdout=PIPE)
			#omxc = Popen(['omxplayer','--win','200 200 600 600', movie2] ,stdin=PIPE, stdout=PIPE)
			state=1
			print("next state 1")
		elif state ==1:
			print("now state 1")
			check_video()
			time.sleep(1)   # Don't do anything
		else:
			time.sleep(1)   # Don't do anything

#-------------------------------------------------------------------------------
def destroy():
	#GPIO.output(LedPin, GPIO.LOW)     # led off
	GPIO.cleanup() 
	print("GPIO resettati")                  # Release resource

#-------------------------------------------------------------------------------
if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

