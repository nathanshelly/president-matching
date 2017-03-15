import soundfile as sf
import os

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

if __name__ == "__main__":
    for prof in ["cossairt", "dinda", "fabian", "fatemah", "goce", "ilya", "jennie", "lincoln", "nell", "robby", "russ", "sara", "tov"]:
        split_and_save("data/professors/train/%s/%s.wav" % (prof, prof), "data/professors/train/split/%s" % prof)
