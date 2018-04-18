# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 13:59:16 2018

@author: jon_c
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from firebase import firebase
from functools import partial
import time

token = "PdWOHUtcScXODzmm8b3pSoFY78dxZQXVSpynXx1n"
url = "https://dw-1d-8f3a9.firebaseio.com/"
firebase = firebase.FirebaseApplication(url, token)


Builder.load_string("""
<RoadC>

    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Refresh'
            size_hint: 1, 0.1
            font_size: 30
            on_press: root.on_update()                  #a function that updates user on road conditions
        Button:
            text: 'Quit'
            size_hint: 1, 0.1
            font_size: 30
            on_press: root.on_stop()
            size_hint: 1, 0.1
        GridLayout:
            cols: 3
            Button:
                text: 'Road 1'
                font_size: 30
                id: r1
            Label:
                text: 'Number of cars on Road 1:'
                font_size: 20
            Label:
                text: '-'
                font_size: 20
                id: label1
            Button:
                text: 'Road 2'
                font_size: 30
                id: r2
            Label:
                text: 'Number of cars on Road 2:'
                font_size: 20
            Label:
                text: '-'
                font_size: 20
                id: label2
""")

class RoadC(BoxLayout):

    def on_update(self):
        ##### ROAD1
        f = firebase.get('inp1') # condition of Road 1
        # if the car is present on the road 1, the Road 1 button turn red.
        if f == True: # car present
            self.ids.r1.background_color = (1, 0, 0, 1) # button turns red

        # if there is no car present on road1 the button turn green
        if f == False: # no car present
            self.ids.r1.background_color = (0, 1, 0, 1) # button turns green



        
        ##### ROAD2, same as road 1
        g = firebase.get('inp2') # condition of Road 2
        if g == True:
            self.ids.r2.background_color = (1, 0, 0, 1)
        if g == False:
            self.ids.r2.background_color = (0, 1, 0, 1)

        self.ids.label1.text = str(firebase.get('car_num')) # reads the number of cars on Road 1, and shows how many car have passed in a certain range. this can help us get more information about the road condition at each period and make decisions

    def on_stop(self):
        App.get_running_app().stop() # quits application

class RoadConditions(App):
    def build(self):
        return RoadC()

RoadConditions().run()
