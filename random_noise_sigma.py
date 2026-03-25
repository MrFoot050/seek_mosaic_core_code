"""
This code will use equation 6 from the paper 'Adapting thermal-infrared technology and astronomical
techniques for use in conservation biology' to get a random noise measurement sigma from the frames
gathered from the blackbody at various temperatures at the center pixel (Or any pixel requested)
"""

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

frames = []

for i in range(101):
    with fits.open(f'shutter_off_21.0C/frame_{i:03d}.fits') as hdul:
        frame = hdul[0].data
    frames.append(frame)

frames = np.array(frames)

#Get mean of frames at center pixel
center = frames[:, 75, 100]
sigmas = ((center[1:] - center[:-1]) / np.sqrt(2))

print(sigmas)
average = np.average(sigmas)
print('Average σ across all frames at center pixel', average)

plt.plot(sigmas)
plt.xlabel("Frame Index")
plt.ylabel('sigma')
plt.show
