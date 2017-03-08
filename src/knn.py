from sklearn.neighbors import KNeighborsClassifier

def train_knn(data, labels, n_neighbors=5):
    """Train and return a KNN model"""
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(data, labels)
    return clf

def test_knn(knn_classifier, data):
    return knn_classifier.predict(data)
