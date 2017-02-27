import numpy as np
from scipy.io.wavfile import write

for i in range(950):
	data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
	scaled = np.int16(data/np.max(np.abs(data)) * 32767)
	write('white_noise/white_noise_' + str(i) + '.wav', 11025, scaled)