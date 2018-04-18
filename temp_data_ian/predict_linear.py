from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def linear_regression():
    bunch_object = pd.read_excel('temp_ver3_30.xls')
    bunch_object = bunch_object.dropna(axis=0,how='all')
    time = np.array(bunch_object.ix[:, 'time'])
    tw_list = []
    for col in bunch_object.columns[1:]:


        temp = np.array(bunch_object.ix[:, col])

        if temp[-1] > temp[0]:
            delta = 0.01
            tw = temp[-1]+0.01
        elif temp[-1] < temp[0]:
            delta = -0.01
            tw = temp[-1]-0.01

        R_2 = 0
        while True:
            bunch_object = pd.read_excel('temp_ver3_30.xls')
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
            if tw >60:
                break
        print(tw,float)
        tw_list.append(tw)
    actual = np.array([float(i)/10 for i in bunch_object.columns[1:]])
    error = actual-tw_list
    plt.scatter(tw_list,error)
    plt.show()

    regr_error = linear_model.LinearRegression()
    regr_error.fit(np.array(tw_list).reshape(-1,1),error)
    print( regr_error.coef_, regr_error.intercept_)





print(linear_regression())