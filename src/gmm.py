from sklearn.mixture import GaussianMixture

def train_gmm_set(data):
    return {label: train_gmm(feature_vectors) for label, feature_vectors in data.iteritems()}

def train_gmm(data, num_components = 32):
    """Train and return a KNN model"""
    gmm = GaussianMixture(n_components = num_components)
    gmm.fit(data)
    return gmm

def test_gmms(gmm_dict, data):
    # returns result of testing each signal in data
    # against each gmm in gmm_dict
    pred_and_probs = [test_sample_gmms(gmm_dict, signal) for signal in data]
    return [pred for pred, _ in pred_and_probs], [probs for _, probs in pred_and_probs]
    
def test_sample_gmms(gmm_dict, signal):
    # generates probabilities for each 
    probabilities = {label: gmm.score(signal) for label, gmm in gmm_dict.iteritems()}
    return max(probabilities.iterkeys(), key = lambda k: probabilities[k]), sorted(probabilities.iteritems(), key=lambda (k, v): v)
