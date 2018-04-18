import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def version1():
    path = os.getcwd()
    dirs = os.listdir(path)
    res = pd.DataFrame()
    for file in dirs:
        if file[-1] == 't':
            with open(file,'r') as f:
                lines = f.readlines()
                temp_data = [line.strip().split() for line in lines]
                temp_data = pd.DataFrame(temp_data)
                res = pd.concat([res, temp_data], axis=1, join='outer')
    res.to_excel('temp_ver1.xls')

def version2():
    path = os.getcwd()
    dirs = os.listdir(path)
    res = pd.DataFrame(np.arange(0.98,400,0.962),columns=['time'])
    for file in dirs:
        if file[-1] == 't':
            with open(file, 'r') as f:
                lines = f.readlines()
                temp_data = [round(float(line.strip().split()[1]),3) for line in lines]
                temp_data = pd.DataFrame(temp_data,columns=[file[9:12]])
                res = pd.concat([res, temp_data], axis=1, join='outer')
    res.to_excel('temp_ver2.xls')
version2()

def smooth(x, window_len=11, window='blackman'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise (ValueError, "smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise (ValueError, "Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise (ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y

def log_data():
    data = pd.read_excel('temp_ver3.xls')
    for col in data.columns[1:]:

        data.ix[:,col] =  np.log( (np.float(col)/10 - np.array(data.ix[:,col]))/((np.float(col)/10)-np.array(data.ix[0,col])) )
    data.to_excel('temp_log_ver3.xls')
##log_data()

def data_visualization():
    bunch_object = pd.read_excel('temp_ver3_30.xls')
    time = bunch_object.ix[:, 'time']
    for col in bunch_object.columns[1:]:

            temp = bunch_object.ix[:,col]
            plt.plot(time,temp,color='lightblue')

    plt.show()
# data_visualization()


def data_visualization_log():
    bunch_object = pd.read_excel('temp_log_ver3.xls')
    time = bunch_object.ix[:, 'time']
    for col in bunch_object.columns[1:]:
        temp = bunch_object.ix[:,col]
        plt.plot(time,temp,color='lightblue')

    plt.show()
##data_visualization_log()


def linear_regression1(bunchobject, x_index, y_index, size, seed):
    # extract the data
    x = bunchobject.data[:, np.newaxis, x_index]
    y = bunchobject.data[:, np.newaxis, y_index]
    # split the data into the training and test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=seed)
    # get an instance of the linear regression classifier
    regr = linear_model.LinearRegression()
    # fit the model to the training set to get the equation
    regr.fit(x_train, y_train)
    # use the model to predict the test set
    y_pred = regr.predict(x_test)
    # output parameters
    output_dict = {}
    output_dict['coefficients'] = regr.coef_
    output_dict['intercept'] = regr.intercept_
    # calculate the mean square error
    output_dict['mean squared error'] = mean_squared_error(y_test, y_pred)
    output_dict['r2 score'] = r2_score(y_test, y_pred)

    return x_train, y_train, x_test, y_pred, output_dict

def linear_regression(x,y):
    regr = linear_model.LinearRegression()
    regr.fit(x,y)
    return regr.coef_, regr.intercept_

def plot_linear_regression():
    bunch_object = pd.read_excel('temp_log_ver3_30.xls')
    x = bunch_object.ix[:,'time']
    coeff_list, intercept_list, temp_list = [], [], []
    for col in bunch_object.columns[1:]:

        y = bunch_object.ix[:,col]
        col = np.float(col) / 10

        coeff, intercept = linear_regression(x.reshape(-1,1),y)
        coeff_list.append(coeff)
        intercept_list.append(intercept)
        temp_list.append(col)
    temp_list = np.array(temp_list)
    coeff_list = np.array([-1/i for i in coeff_list])
    
    plt.scatter(temp_list, coeff_list)
    plt.show()
    return np.average(coeff_list)
# print(plot_linear_regression())
