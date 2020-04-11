from keras.models import load_model
import numpy as np

class Model:
    def __init__(self):
        self.model = load_model('data/model.h5')
        self.xtest = np.load('data/xtest.npy')
        self.ytest = np.load('data/ytest.npy')

    def get_model(self):
        return self.model

    def forecast(self, idx):
        return self.model.predict(self.xtest[idx].reshape((33,1,117)))

    def get_predict(self, idx = None):
        alldata = []
        if idx == None:
            for i in range(0,45,1):
                alldata.append(self.model.predict(self.xtest[i].reshape((33,1,117))))
            alldata = np.array(alldata)
            return np.sum(alldata, axis = 0)
        else:
            return self.model.predict(self.xtest[idx - 1].reshape((33,1,117)))

    def get_actual(self, idx = None):
        if idx == None:
            return np.sum(self.ytest, axis=0)
        else:
            return self.ytest[idx - 1]