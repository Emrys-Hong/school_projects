from pythymiodw import *
from pythymiodw import io
from pythymiodw.sm import *
from libdw import sm
from firebase import firebase

token = "PdWOHUtcScXODzmm8b3pSoFY78dxZQXVSpynXx1n"
url = "https://dw-1d-8f3a9.firebaseio.com/"
firebase = firebase.FirebaseApplication(url,token)

class MySMClass(sm.SM):
    start_state = None
    def get_next_values(self, state, inp):      #used to stop the robot by pressing the back button
        if inp.button_backward:
            return 'halt', io.Action(0,0)

        ground = inp.prox_ground.delta          #IR readings from the sensors on the Thymio
        left = ground[0]                        #assign left to be the reading from the left IR sensor
        right = ground[1]                       #assign right to be the reading from the right IR sensor
        
        # coordination with the traffic light
        check = firebase.get("/light1_state")   #determine the state of the upcoming traffic light on the road the Thymio is on
        
        print(left,right)                       #to see the IR readings as the program runs
        print(check)                            #to see the state of the firebase variable as the program runs
        
        # to stop the car we need to make sure two thing:
        # 1. the thymio have reached the black line at the crossing road
        # 2. the light is red
        if left < 200 and right < 200 and check == "red":       #IR readings imply black line
            return ("Stop", io.Action(fv=0.0, rv=0.0))          #check if the traffic light is red, then stop
        
        # to stop the car we need to make sure two thing:
        # 1. the thymio have reached the black line at the crossing road
        # 2. the light is red
        elif left < 200 and right < 200 and check == "green":   #IR readings imply black line
            return ("Go", io.Action(fv=0.03, rv=0.0))           #check if the traffic light is green, then go

        return (None, io.Action(fv=0.03, rv=0)) # at normal state, we assume the thymio is continuesly moving forward until it encounter the traffic light


    #########################################
    # Don't modify the code below.
    # this is to stop the state machine using
    # inputs from the robot
    #########################################
    def done(self,state):
        if state=='halt':
            return True
        else:
            return False

MySM=MySMClass()

############################

m=ThymioSMReal(MySM)
try:
    m.start()
except KeyboardInterrupt:
    m.stop()
