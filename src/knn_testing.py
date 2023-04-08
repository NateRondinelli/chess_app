from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from utils.puzzle_db_reader import gen_yield, get_db_dataframe
from stockfish import Stockfish


def init():
    np.random.seed(5)
    engine = Stockfish("stockfish\stockfish.exe")
    #engine.set_depth(15)
    engine.set_depth(20)
    sf = []
    evals = []

    totalData = get_db_dataframe()
    data = totalData.iloc[:200,:-3]
    data = data.drop(["PuzzleId"],axis=1)
    sf = data.FEN.values
    string_col = data.select_dtypes(include="object").columns
    df = pd.get_dummies(data, columns=string_col, drop_first=False)

    for fen in sf:
        engine.set_fen_position(fen)
        eval = (engine.get_evaluation())["value"]
        #print(eval)
        evals.append(eval)
        
    df['Eval'] = evals

    #print(df)
    return df


def split(df):
    y = df.Eval.values
    x = df.drop(["Eval"],axis=1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=25)
    y_train = y_train.reshape(-1,1)
    y_test = y_test.reshape(-1,1)
    #print(y_train)
    return x_train,x_test,y_train,y_test


def base_knn(x_train,y_train,x_test,y_test,n):
    knn = KNeighborsClassifier(n_neighbors=n)
    knn.fit(x_train,y_train.ravel())

    print("Accuracy of knn model: {}\n".format(knn.score(x_test, y_test.ravel())))


def get_neighbors_knn(x_train,y_train,x_test,y_test):
    #x_train = preprocessing.MinMaxScaler().fit_transform(x_train)
    #x_test = preprocessing.MinMaxScaler().fit_transform(x_test)
    #y_train = preprocessing.MinMaxScaler().fit_transform(y_train)
    #y_test = preprocessing.MinMaxScaler().fit_transform(y_test)

    #print(x_train)
    #print(y_train)

    #knn = KNeighborsClassifier(n_neighbors=3)
    #knn.fit(x_train,y_train)

    i=1
    x=0
    while( x < .125 ):
        knn = KNeighborsClassifier(n_neighbors=i)
        #labE = preprocessing.LabelEncoder()
        knn.fit(x_train,y_train.ravel())
        x = knn.score(x_test, y_test.ravel())
        #print(x)
        i += 1
    #print("Accuracy of preprocessed knn model: {}\n".format(knn.score(x_test, y_test)))
    return i


if __name__ == '__main__':
    df = init()
    x_train,x_test,y_train,y_test = split(df)
    n = get_neighbors_knn(x_train,y_train,x_test,y_test)
    base_knn(x_train,y_train,x_test,y_test,n)
    