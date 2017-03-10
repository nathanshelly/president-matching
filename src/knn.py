from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def train_knn(data, labels, n_neighbors=5):
    """Train and return a KNN model"""
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    
    # print data
    # print len(data)
    # print len(labels)

    clf.fit(data, labels)
    return clf

def test_knn(knn_classifier, data, labels):
    sorted_labels = sorted(labels)
    print 'labels', len(labels)
    print 'sorted_labels', len(sorted_labels)

    summed_classes = [np.sum(np.log(knn_classifier.predict_proba(matrix)), axis = 0) for matrix in data]

    # print type(classes)
    # print classes.shape
    # summed_classes = np.sum(classes, axis = 2)
    # print 'classes', classes.shape
    # print 'summed_classes', summed_classes.shape

    temp = [labels[np.argmax(class_probs)] for class_probs in summed_classes]
    print len(temp)
    return temp
    
