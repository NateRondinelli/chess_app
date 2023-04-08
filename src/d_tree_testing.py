import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from utils.puzzle_db_reader import get_db_dataframe
from stockfish import Stockfish

def init():
    np.random.seed(5)
    engine = Stockfish("stockfish\stockfish.exe")
    engine.set_depth(15)
    #engine.set_depth(20)
    sf = []
    evals = []

    totalData = get_db_dataframe()
    #totalData = totalData.sample(200)
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

    #print("Length: ", len(df))
    #print("Shape: ", df.shape)
    #print("Dataset: ",df.head())
	
    return df


def split(df):

    y = df.Eval.values
    x = df.drop(["Eval"],axis=1)

    x_train, x_test, y_train, y_test = train_test_split(
	x, y, test_size = 0.2, random_state = 25)
	
    return x, y, x_train, x_test, y_train, y_test

def accuracy(y_test, prediction):
	
	#print("Matrix: ", confusion_matrix(y_test, y_pred))
	#print("Report : ", classification_report(y_test, y_pred))
    print ("Accuracy : ", accuracy_score(y_test,prediction))

def prediction(x_test, classifier):

	y_pred = classifier.predict(x_test)
	print("Predicted values:")
	print(y_pred)
	return y_pred
	

def gini_train(X_train, y_train):

	gini = DecisionTreeClassifier(
            criterion = "gini",
			random_state = 100,
            max_depth = 3, min_samples_leaf = 5)
            #max_depth = 6, min_samples_leaf = 15)

	gini.fit(X_train, y_train)
	return gini
	

def entropy_train(X_train, y_train):

	entropy = DecisionTreeClassifier(
			criterion = "entropy", random_state = 100,
			max_depth = 3, min_samples_leaf = 5)
            #max_depth = 6, min_samples_leaf = 15)

	entropy.fit(X_train, y_train)
	return entropy



if __name__=="__main__":
	data = init()
	X, Y, X_train, X_test, y_train, y_test = split(data)
	gini = gini_train(X_train, y_train)
	entropy = entropy_train(X_train, y_train)
	
	print("\nResults Using Gini Index:")
	gini_prediction = prediction(X_test, gini)
	accuracy(y_test, gini_prediction)
	
	print("\nResults Using Entropy:")
	entropy_prediction = prediction(X_test, entropy)
	accuracy(y_test, entropy_prediction)