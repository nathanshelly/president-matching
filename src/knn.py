from sklearn.neighbors import KNeighborsClassifier

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
	# print 'labels', labels.shape
	# print 'sorted_labels', sorted_labels.shape

	classes = [knn_classifier.predict_proba(matrix) for matrix in data]
	summed_classes = np.sum(np.log(classes), axis = 2)
	# print 'classes', classes.shape
	# print 'summed_classes', summed_classes.shape

	temp = [labels[(class_probs.index(max(class_probs)))] for class_probs in summed_classes]
	# print temp.shape
	return temp
    
