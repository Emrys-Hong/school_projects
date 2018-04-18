from firebase import firebase
from RPi import GPIO
from firebase import firebase
import time
from threading import Thread

url = "https://dw-1d-8f3a9.firebaseio.com/"  #URL to Firebase database
token = "PdWOHUtcScXODzmm8b3pSoFY78dxZQXVSpynXx1n"  #unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

#GPIO lights control
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ledcolor ={'road1_red' :19, 'road1_green' :18 ,         #GPIO 19,18,13,12 are the only PWM outputs that can 
           'road2_red' :13 ,'road2_green' :12}          #change the voltage of LEDs thus the intensity
                          

for a in ledcolor.values():
    GPIO.setup(a, GPIO.OUT)

#PWM output, with 100Hz frequency highest
road1_red = GPIO.PWM(19 ,255)  
road1_green = GPIO.PWM(18 ,255)
road2_red = GPIO.PWM(13 ,255)
road2_green = GPIO.PWM(12 ,255)


road1_red.start(0)
road1_green.start(0)
road2_red.start(0)
road2_green.start(0)

state = 'red'       #state refers to the state of light1, which is traffic light 1, being either red or green
                    #the state of light2, which is traffic light 2, is the opposite of light1 and thus is not defined
                    
intensity1 = 50     #intensity of light1   #starts at low intensity, only increases to 255 when a car is detected
intensity2 = 50     #intensity of light2

def flashLed():
    global state
    global intensity1
    global intensity2
    while True:
        if state == 'red':                #the traffic light expression of red and green
            GPIO.output(19 ,intensity1)   #red light on for light1
            GPIO.output(18 ,0)            #green light off for light1
            GPIO.output(13 ,0)            #red light off for light2
            GPIO.output(12 ,intensity2)   #green light on for light2
        elif state == 'green':            
            GPIO.output(19 ,0)
            GPIO.output(18 ,intensity1)
            GPIO.output(13 ,intensity2)
            GPIO.output(12 ,0)


def function():
    global state
    while True:
        #gets input from firebase
        input1 = firebase.get('/inp1')      #True if a car is detected on road 1, False otherwise
        input2 = firebase.get('/inp2')      #True if a car is detected on road 2, False otherwise

        #varies the intensity of the traffic lights
        if input1 == True:              #if a car is detected on road 1
            intensity1 = 255            #intensity increases 
        else: intensity1 = 50           #otherwise intensity is low
        
        if input2 == True:              #if a car is detected on road 2
            intensity2 = 255            #intensity increases
        else: intensity2 = 50           #otherwise intensity is low

        #pseudo state machine that defines which lights are on according to the situation
        if state == 'red' and input1 == True and input2 == False:
            state = 'green'
        elif state == 'green' and input2 == True and input1 == False:
            state = 'red'
        elif state == 'green' and input2 == True and input1 == True:
            state = 'green'
        elif state == 'red' and input2 == True and input1 == True:
            state = 'red'

        opposite_state = 'green' if state == 'red' else 'red'       #the state of light2 on road 2 is opposite to light1 on road 1

        #update the states onto firebase
        firebase.put('/', 'light1_state', state)                     
        firebase.put('/', 'light1_intensity' ,intensity1)
        firebase.put('/', 'light2_state' ,opposite_state)
        firebase.put('/', 'light2_intensity' ,intensity2)

t1 = Thread(target=flashLed, args=[]) # t1 thread should updating the traffic light from teh firebase
t2 = Thread(target=function, args=[]) # t2 thread should updating the flash light base on the output from the camera detection.
t1.start()
t2.start()
