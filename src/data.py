from mfcc import mfcc, filtered_mfcc
from features import files_to_features, unfold_matrix_list_with_labels, knn_train_features
from gmm import train_gmm_set
import utilities

import soundfile as sf
import os, shutil
import numpy as np

def chunk_audio(signal, chunk_size):
    chunks = []
    start = 0
    while start < len(signal):
        chunks.append(signal[start : start + chunk_size])
        start += chunk_size

    return chunks

def split_and_save(src, destdir, chunk_length=3):
    """Load the file given in srcpath, split it up into a big and little chunk,
    and save the pieces to destpath."""
    signal, sr = sf.read(src)

    if not os.path.exists(destdir):
        os.makedirs(destdir)

    basename = os.path.basename(src)

    n_chunks = sr * chunk_length

    # little_chunk = signal[:n_chunks]
    # big_chunk = signal[n_chunks:]
    little_chunk = signal[-n_chunks:]
    big_chunk = signal[:-n_chunks]

    sf.write(os.path.join(destdir, "big_%s" % basename), big_chunk, sr)
    sf.write(os.path.join(destdir, "little_%s" % basename), little_chunk, sr)

def split_and_save_into_num(src, destdir, num=5):
	signal, sr = sf.read(src)

	if not os.path.exists(destdir):
		os.makedirs(destdir)

	basename = os.path.basename(src)
	chunks = np.array_split(signal, num)

	for index, chunk in enumerate(chunks):
		sf.write(os.path.join(destdir, ('%s_chunk_%s' + '.wav') % (basename[:-4], index)), chunk, sr)

def normalize(signal):
    return signal / np.ptp(signal)

def normalize_and_save(src, dest):
	"""Normalize the signal at src by its range, and save it to dest."""
	signal, sr = sf.read(src)
	norm_sig = normalize(signal)
	sf.write(dest, norm_sig, sr)

def save_professor_gmms(srcdir, dest):
    """Save the professor voices as a pickled GMM."""
    train_data, train_labels = files_to_features(srcdir, features=[mfcc])
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    utilities.save(gmm_dict, dest)

def normalize_professors():
    for name in ["aravindan", "cossairt", "dinda", "fabian", "fatemah",
                "goce", "ian", "ilya","jason", "jennie", "larry", 
                "nathan","nell", "pardo", "robby", "russ", "sara", "sasha", "tov"]:
        normalize_and_save('data/professors/%s/%s.wav' % (name, name), 'data/professors_normalized/%s.wav' % name)

def split_professors():
    for name in ["aravindan", "cossairt", "dinda", "downey", "fabian", "fatemah",
                "goce", "ian", "ilya","jason", "jennie", "larry",
                "nathan","nell", "pardo", "robby", "russ", "sara", "sasha", "tov"]:
        split_and_save('data/professors/%s/%s.wav' % (name, name), 'data/professors_split/%s' % name)

def create_train_and_test_dirs(src_dir):
	new_dirs = [os.path.join(src_dir, 'train'), os.path.join(src_dir, 'test')]
	for dir_name in new_dirs:
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
	for name in [name for name in os.listdir(src_dir) if name not in ('test', 'train')]:
		name_path = os.path.join(src_dir, name)
		train_path = os.path.join(src_dir, 'train', name)
		test_path = os.path.join(src_dir, 'test', name)
		for dir_name in (train_path, test_path):
			if not os.path.exists(dir_name):
				os.mkdir(dir_name)

		shutil.copy2(os.path.join(name_path, 'big_' + name + '.wav'), train_path)
		shutil.copy2(os.path.join(name_path, 'little_' + name + '.wav'), test_path)

def save_professor_knn_features(srcdir, dest):
    train_data, train_labels = knn_train_features(srcdir)

    utilities.save((train_data, train_labels), dest)

if __name__ == "__main__":
    # save_professor_gmms('data/professors_split/train', 'professor_gmms_train.p')
    # save_professor_knn_features('data/professors_split/train', 'professor_knn_features_train.p')
    # split_professors()
	# create_train_and_test_dirs('data/professors_split')
	split_and_save_into_num('data/us_split/nathan/big_nathan.wav', 'data/us_split/nathan/chunks', num=5)
