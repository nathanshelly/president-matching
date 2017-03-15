from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def train_knn(data, labels, n_neighbors=5):
    """
    Train and return a KNN model
    Takes 
    """
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(data, labels)
    return clf

def test_knn(knn_classifier, data, labels):
    sorted_labels = sorted(labels)
    summed_classes = [np.sum(knn_classifier.predict_proba(matrix), axis = 0) for matrix in data]

    temp = [sorted_labels[np.argmax(class_probs)] for class_probs in summed_classes]
    return temp
