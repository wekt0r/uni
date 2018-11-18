import random
from reversi_show import *
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

learn = 0
LEARNING_DATA_SIZE = 'bigger'
data = joblib.load("reversi_learning_data/parsed_{}.dat".format(LEARNING_DATA_SIZE))
random.shuffle(data)
data = data[:30000]
print("done loading")

if learn:
    print("started learning")
    N = len(data) // 10
    test_data = data[:N]
    dev_data = data[N:]

    X = [b for (b, r) in dev_data]
    y = [r for (b, r) in dev_data]

    X_test = [b for (b, r) in test_data]
    y_test = [r for (b, r) in test_data]

    # creating model
    nn = MLPClassifier(hidden_layer_sizes=(40,20,5), activation='tanh')
    # training model
    nn.fit(X,y)
    print("done learning")
    print("Dev Score", nn.score(X,y))
    print("Test Score", nn.score(X_test, y_test))

    joblib.dump(nn, "{}Z4NN.dat".format(LEARNING_DATA_SIZE))

else:
    X_test = [b for (b, r) in data]
    y_test = [r for (b, r) in data]
    nn = joblib.load("{}Z4NN.dat".format(LEARNING_DATA_SIZE))
    print("Test Score", nn.score(X_test, y_test))
