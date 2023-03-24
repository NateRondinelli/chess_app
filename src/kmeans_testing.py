import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import chess.engine
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
#from sklearn.decomposition import PCA
from representational.closure import build_closure_tensor
from utils.puzzle_db_reader import get_random_puzzle
from stockfish import Stockfish

def init():
    np.random.seed(5)
    engine = Stockfish("stockfish\stockfish.exe")
    engine.set_depth(15)
    #pca = PCA(2)
    #df = pd.read_csv('lichess_db_puzzle_no_themes.csv')
    #X = df[["FEN","Moves"]]
    #print(X)

    X = []
    #Y = []
    for pz in get_random_puzzle(200):
        #position = chess.Board(pz.FEN)
        #state = engine.analyse(position, chess.engine.Limit(depth=15))
        #print(state["score"])
        engine.set_fen_position(pz.FEN)
        value = (engine.get_evaluation())["value"]
        #print(engine.get_evaluation())["value"])
        if(value < 0):
            X.append([value,0])

        else:
            X.append([value,1])

    X = np.array(X)
    #print(X)
    
    #df = pca.fit_transform(X)
    #print(df)

    return X

def elbow(X):
    # Using the elbow method to find the optimal number of clusters
    wcss = []
    for i in range (1,11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter =300, n_init = 10, random_state = 0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    # Use elbow method graph to find best cluster number
    plt.plot(range(1,11),wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

def base_kmeans(X):
    # Applying KMeans to the dataset using 3 clusters as determined by elbow method
    kmeans=KMeans(n_clusters= 3, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    Y = kmeans.fit_predict(X)
    #print(Y)

    # Results graph 
    labels = np.unique(Y)
    for i in labels:
        plt.scatter(X[Y == i , 1], X[Y == i , 0] )
    plt.title('Clusters of positions after normilization')
    plt.xlabel('Player Color')
    plt.ylabel('Advantage')
    plt.legend()
    plt.show()

def preprocessed_kmeans(X):
    kmeans=KMeans(n_clusters= 3, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    X = preprocessing.MinMaxScaler().fit_transform(X)
    #print(X)
    Y = kmeans.fit_predict(X)
    #print(Y)

    # Results graph 
    labels = np.unique(Y)
    for i in labels:
        plt.scatter(X[Y == i , 1], X[Y == i , 0] )
    plt.title('Clusters of positions after normilization')
    plt.xlabel('Player Color')
    plt.ylabel('Advantage')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    X = init()
    # elbow(X)
    base_kmeans(X)
    preprocessed_kmeans(X)