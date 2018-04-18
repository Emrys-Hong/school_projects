from firebase import firebase
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

token="H40NkIAgxVkBN6UvKMEGoIrUm6TjgipqPMB0XIdj"
url="https://dwweek4project.firebaseio.com/"
firebase=firebase.FirebaseApplication(url,token)
while True:
    temp_list = firebase.get('/mydict/temp_list')[5:]
    a = len(temp_list)
    time_list = np.arange(0,100,0.88)[:a].reshape(-1,1)
    def PredictFunction(temp_list, time):
        #insert linear regression model here
        temp = np.array(temp_list)			
        
        if temp[-1] > temp[0]:
            delta = 0.1
            tw = temp[-1]+0.1
        elif temp[-1] < temp[0]:
            delta = -0.1
            tw = temp[-1]-0.1

        R_2 = 0
        while True:
            y = np.log( (tw-temp) / (tw-temp[0]) )
            #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=seed)

            regr = linear_model.LinearRegression()
            
            regr.fit(time, y)

            y_pred = regr.predict(time)
            New_R_2 = r2_score(y, y_pred)
            if New_R_2 > R_2:
                R_2 = New_R_2
                tw = tw + delta
                print(tw)
            else:
                break
        mydict = {}
        mydict['temp_pred']=1.054*tw - 1.65
        mydict['temp_list']=temp_list
        
        firebase.put('/','mydict',mydict)
    PredictFunction(temp_list,time_list)