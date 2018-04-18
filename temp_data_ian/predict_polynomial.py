from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def exponential_regression():
    bunch_object = pd.read_excel('temp_ver3_25.xls')
    time = bunch_object.ix[:,'time']
    predict = []
    actual = []
    for col in bunch_object.columns[1:]:
        regr = linear_model.LinearRegression()
        y = bunch_object.ix[:,col]
        x = np.exp(-time/19.068).reshape(-1,1)
        regr.fit(x, y)
        predict.append(regr.intercept_)
        actual.append(float(col)/10)
    error = np.array(predict)-np.array(actual)
    plt.scatter(np.array(predict), actual-np.array(predict)*1.025+0.78)
    plt.show()
    regr1 = linear_model.LinearRegression()
    regr1.fit(np.array(predict).reshape(-1,1), error)
    return regr1.coef_, regr1.intercept_
        
        
print(exponential_regression())
    
def linear_regression():
    bunch_object = pd.read_excel('temp_ver3.xls')
    bunch_object = bunch_object.dropna(axis=0,how='all')
    time = bunch_object.ix[:, 'time']
    tw_list = []
    for col in bunch_object.columns[1:]:


        temp = bunch_object.ix[:, col]

        if temp[31] > temp[0]:
            delta = 0.1
            tw = temp[31]+0.1
        elif temp[31] < temp[0]:
            delta = -0.1
            tw = temp[31]-0.1

        R_2 = 0
        while True:
            bunch_object = pd.read_excel('temp_ver3.xls')
            x = time
            x = x.reshape(-1,1)

            y = np.log( (tw-np.array(bunch_object.ix[:,col])) / (tw-bunch_object.ix[0,col]) )
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
        tw_list.append(tw)
    actual = np.array([float(i)/10 for i in bunch_object.columns[1:]])
    error = actual-tw_list
    plt.scatter(tw_list,error)
    plt.show()




