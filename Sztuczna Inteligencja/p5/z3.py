import random
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

LEARNING_DATA_SIZE = "smaller"

def _parse_input(entry):
    result = int(entry.split()[0])
    board = [{'_': 1/2, '1': 1, '0': 0}[char] for char in entry.split()[1]]
    return (board, result)

with open("reversi_learning_data/{}.dat".format(LEARNING_DATA_SIZE), 'r') as f:
    data = [_parse_input(entry) for entry in f.read().split("\n") if entry]

random.shuffle(data)
N = len(data) // 10
test_data = data[:N]
dev_data = data[N:]

X = [b for (b, r) in dev_data]
y = [r for (b, r) in dev_data]

X_test = [b for (b, r) in test_data]
y_test = [r for (b, r) in test_data]

# creating model
nn = MLPClassifier(hidden_layer_sizes=(10,),activation='tanh')
# training modelz
nn.fit(X,y)

print("Dev Score", nn.score(X,y))
print("Test Score", nn.score(X_test, y_test))

joblib.dump(nn, "{}Z3NN.dat".format(LEARNING_DATA_SIZE))
