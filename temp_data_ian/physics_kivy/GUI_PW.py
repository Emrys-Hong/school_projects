# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 17:10:37 2018

@author: Ian
"""
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock
import time 
import numpy as np
from firebase import firebase

token="H40NkIAgxVkBN6UvKMEGoIrUm6TjgipqPMB0XIdj"
url="https://dwweek4project.firebaseio.com/"
firebase=firebase.FirebaseApplication(url,token)

Builder.load_string('''
<TemperaturePredictor>:
    rows:2
    BoxLayout:
        cols:4
        Label:
            text:'Current Time:'
            font_size:24
        Label: 
            id:current_time
            text:root.count_time
            font_size:24
        Label:
            text:'Prediction Time:'
            font_size:24
        Label:
            id:prediction_time
            text:root.pred_time
            font_size:24
    BoxLayout:
        cols:4
        Label:
            text:'Temperature Reading:'
            font_size:24
        Label:
            id:temp_read
            text:'--'
            font_size:24
        Label:
            text:'Predicted Temperature:'
            font_size:24
        Label:
            id:temp_pred
            text:'--'
            font_size:24             
                
''')

class TemperaturePredictor(GridLayout):
    
    count_time= StringProperty('0.00')
    pred_time= StringProperty('Predicting...')
    
    def __init__(self):
        super(TemperaturePredictor,self).__init__()
        Clock.schedule_interval(self.tick,0)
        self.start_time= time.time()
        
        self.time_in = 0
        self.inside= False #changes to True if sensor is in water
        self.predicted= False #changes to True if prediction is made 
        
    def tick(self,dt):
        #get time and temperature from firebase
        temp = firebase.get('/mydict/temp')
        current_time = firebase.get('/mydict/current_time')
        
        #update time and temp on display 
        try:    
            self.count_time='{:.2f} secs'.format(float(current_time))
            self.ids.temp_read.text= '{:.3f} deg'.format(float(temp))
        except Exception as e:
            pass
        
        self.temp_list= firebase.get('/mydict/temp_list')
        self.time_list= firebase.get('/mydict/time_list')
       
        #once sensor is inside the water, set .inside as True
        try:
            if np.abs(temp- np.mean(self.temp_list))>0.2 and not self.inside:
                self.time_in= current_time
                self.inside= True
        
        #once it has collected enough info, make prediction and display
            if current_time>self.time_in + 26 and not self.predicted:
                print('yay')
                temp_pred= self.PredictFunction(self.temp_list,time_list)
                self.ids.temp_pred.text='{:.3f} deg'.format(temp_pred)
                pred_time= time.time() -self.start_time -self.time_in
                self.pred_time= '{:.2f} secs'.format(pred_time)
                self.predicted= True
        
        #while sensor is collecting information update prediction time
            if self.inside and not self.predicted:    
                self.pred_time = '{:.2f} secs'.format(current_time- self.time_in)
        except Exception as e:
            pass      
        
    def PredictFunction(self, temp_list, time_list):
        #insert linear regression model here
        #insert linear regression model here
        temp = temp_list
        time = np.array(time_list).reshape(-1,1)
        if temp[-1] > temp[0]:
            delta = 0.01
            tw = temp[-1]+0.1
        elif temp[-1] < temp[0]:
            delta = -0.01
            tw = temp[-1]-0.1

        R_2 = 0
        while True:
            y = np.log( (tw-temp) / (tw-temp) )
            #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=seed)

            regr = linear_model.LinearRegression()

            regr.fit(time, y)

            y_pred = regr.predict(time)
            New_R_2 = r2_score(y, y_pred)
            if New_R_2 > R_2:
                R_2 = New_R_2
                tw = tw + delta

            else:
                break
        print(1.054*tw - 1.65)
        return 1.054*tw - 1.65

class TemperaturePredictorApp(App): 
    def build(self):
        return TemperaturePredictor()
    
TemperaturePredictorApp().run()
    