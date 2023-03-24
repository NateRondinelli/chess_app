from representational.closure import build_closure_tensor
from matplotlib import pyplot as plt
from utils.puzzle_db_reader import get_random_puzzle
from sklearn.manifold import TSNE
from tensorflow.python.keras import backend as K
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import keras
from keras import backend as K
#print(f'Available gpus: {K._get_available_gpus()}')

def get_tsne(closure_tensors):
    """
    It takes a closure tensor and returns a tsne representation of it.
    """
    closure_tensors = np.array(closure_tensors).reshape(len(closure_tensors), -1)
    tsne = TSNE(n_components=2, n_iter=300, init='pca', learning_rate='auto')
    tsne_results = tsne.fit_transform(closure_tensors)
    return tsne_results

def plot_tsne(tsne_results):
    """
    It takes a tsne representation and plots it.
    """
    plt.figure(figsize=(16,10))
    plt.scatter(tsne_results[:,0], tsne_results[:,1])
    plt.show()

def get_autoencoder_features(data):
    shape = [data.shape[1], 2048, 512, 128]
    encoder = keras.models.Sequential([
        keras.layers.Dense(shape[i+1], input_shape=[size], activation='relu') for i, size in enumerate(shape[:-1])
    ])

    decoder = keras.models.Sequential([
        keras.layers.Dense(size, input_shape=[shape[::-1][i]], activation='relu') for i, size in enumerate(shape[:-1][::-1])
    ])

    def custom_loss_function(y_true, y_pred):
        codings = encoder(data)
        squared_difference = tf.square(y_true - y_pred)
        return tf.reduce_mean(squared_difference)+tf.reduce_mean(tf.square(codings) )
    autoencoder = keras.models.Sequential([encoder, decoder])
    # autoencoder.compile(loss='mse', optimizer = keras.optimizers.SGD(lr=0.01))
    autoencoder.compile(loss=custom_loss_function, optimizer = keras.optimizers.SGD(lr=0.01))

    X_tr, X_valid = train_test_split(data, test_size=0.2)
    history = autoencoder.fit(X_tr,X_tr, epochs=50,validation_data=(X_valid,X_valid),
                            callbacks=[keras.callbacks.EarlyStopping(patience=10)])
                            
    codings = encoder.predict(data)
    return codings

if __name__ == '__main__':
    np.random.seed(5)
    closure_tensors = []
    for pz in get_random_puzzle(200):
        closure_tensors.append(build_closure_tensor(pz.FEN))
    tsne_results = get_tsne(get_autoencoder_features(np.array(closure_tensors).reshape(len(closure_tensors), -1)))
    plot_tsne(tsne_results)