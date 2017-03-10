from sklearn.mixture import GaussianMixture

def train_gmm_set(data):
    """
    takes 
    returns
    """
	return {label: train_gmm(feature_vectors) for label, feature_vectors in data.iteritems()}

def train_gmm(data, num_components = 5):
	"""Train and return a KNN model"""
	gmm = GaussianMixture(n_components = num_components)
	gmm.fit(data)
	return gmm

def test_gmms(gmm_dict, data):
	return [test_sample_gmms(gmm_dict, signal) for signal in data]
	
def test_sample_gmms(gmm_dict, signal):
	probabilities = {label: gmm.score(signal) for label, gmm in gmm_dict.iteritems()}
	return max(probabilities.iterkeys(), key = lambda k: probabilities[k])
