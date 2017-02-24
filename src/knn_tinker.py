from sklearn.neighbors import KNeighborsClassifier
import numpy as np

train_samples = np.array([
    [0, 0, 0],
    [1, 1, 1],
    [2, 2, 2]
])

train_labels = np.array([0, 1, 2])

clf = KNeighborsClassifier(n_neighbors=1)
clf.fit(train_samples, train_labels)

print clf.predict([[0.1, 0.3, 0.4], [0.5, 0.5, 0.5]])
