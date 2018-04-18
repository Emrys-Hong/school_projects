from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def linear_regression():
    bunch_object = pd.read_excel('/Users/MH/Dropbox/temp_data_ian/temp_51.xlsx')
    bunch_object = bunch_object.dropna(how='all')
    
    time = bunch_object.ix[:, 0]
    print(bunch_object.columns)


    
    
    temp = np.array(bunch_object.ix[:, 1])
    print(temp)
    if temp[-1] > temp[0]:
        delta = 0.1
        tw = temp[-1]+0.1
    elif temp[-1] < temp[0]:
        delta = -0.1
        tw = temp[-1]-0.1

    R_2 = 0
    while True:
        
        x = time
        x = x.reshape(-1,1)
 
        y = np.log( (tw-np.array(bunch_object.ix[:,1])) / (tw-bunch_object.ix[0,1]) )
        
        #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=seed)
        
        regr = linear_model.LinearRegression()

        regr.fit(x, y)

        y_pred = regr.predict(x)
        New_R_2 = r2_score(y, y_pred)
        if New_R_2 > R_2:
            R_2 = New_R_2
            tw = tw + delta

        else:
            break

    print( 1.054*tw - 1.65 )




print(linear_regression())