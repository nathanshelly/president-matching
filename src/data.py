from mfcc import files_to_mfcc_features, unfold_matrix_list_with_labels
from gmm import train_gmm_set
import utilities

import soundfile as sf
import os
import numpy as np

def chunk_audio(signal, chunk_size):
    chunks = []
    start = 0
    while start < len(signal):
        chunks.append(signal[start : start + chunk_size])
        start += chunk_size

    return chunks

def split_and_save(src, destdir, chunk_length=3):
    """Load the file given in srcpath, split it up, into sections of duration chunk_length,
    and save the pieces to destpath."""
    signal, sr = sf.read(src)

    if not os.path.exists(destdir):
        os.makedirs(destdir)

    chunks = chunk_audio(signal, sr * chunk_length)

    for i in range(len(chunks)):
        sf.write(os.path.join(destdir, "chunk_%d.wav" % i), chunks[i], sr)

def normalize(signal):
    return signal / np.ptp(signal)

def normalize_and_save(src, dest):
    """Normalize the signal at src by its range, and save it to dest."""
    signal, sr = sf.read(src)

    norm_sig = normalize(signal)

    sf.write(dest, norm_sig, sr)

def save_professors(srcdir, dest):
    """Save the professor voices as a pickled GMM."""
    train_data, train_labels = files_to_mfcc_features(srcdir)
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    utilities.save(gmm_dict, dest)

def normalize_professors():
    for name in ["aravindan", "cossairt", "dinda", "fabian", "fatemah",
                "goce", "ian", "ilya","jason", "jennie", "larry", "lincoln",
                "nathan","nell", "pardo", "robby", "russ", "sara", "sasha", "tov"]:
        normalize_and_save('data/professors/%s/%s.wav' % (name, name), 'data/professors_normalized/%s.wav' % name)

if __name__ == "__main__":
    # save_professors('data/professors', 'professor_gmms.p')
    # normalize_professors()
    save_professors('data/professors_normalized', 'normalized_professor_gmms.p')
