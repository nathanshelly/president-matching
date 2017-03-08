from sklearn.mixture import GaussianMixture

def train_gmm_set(data):
	return {label: train_gmm(features) for label, features in data.iteritems()}

def train_gmm(data, num_components = 5):
	"""Train and return a KNN model"""
	gmm = GaussianMixture(n_components = num_components)
	gmm.fit(data)
	return gmm

def test_gmm(gmm_classifier, data):
	return gmm_classifier.predict(data)
