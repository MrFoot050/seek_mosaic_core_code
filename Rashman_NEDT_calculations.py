'''
The following code will calculate the NEdT of a given set of .FITS files. It will do this by adapting equation 6 
from Rashman et al. 2018. 
'''

import numpy as np
from astropy.io import fits
import glob

# SETTINGS
folder = 'E:/CYCLE_4_DATA_fits_gz/2026-04-03_16-46-41/E05257AC071D/converted_fits'

# Pixel selection
use_center_pixel = True
row, col = 75, 100   # used if not center

# LOAD FRAMES
files = sorted(glob.glob(folder + '/*.fits'))

frames = []
for f in files:
    with fits.open(f) as hdul:
        frames.append(hdul[0].data.astype(float))

frames = np.array(frames)  # shape: (N, H, W)
N, H, W = frames.shape

# Choose pixel
if use_center_pixel:
    row, col = H // 2, W // 2

print(f"Using pixel: ({row}, {col})")

# STANDARD DEVIATION
# Per pixel over time
std_image = np.std(frames, axis=0)

# Center pixel std
std_center = std_image[row, col]

# Whole image std (average over all pixels)
std_whole = np.mean(std_image)

print('\nSTANDARD DEVIATION')
print(f'Center pixel std: {std_center}')
print(f'Whole image std (mean over pixels): {std_whole}')

# AVERAGE TEMPERATURE
# Mean per pixel over time
mean_image = np.mean(frames, axis = 0)

# Center pixel mean
mean_center = mean_image[row, col]

# Whole image mean
mean_whole = np.mean(mean_image)

print('\nAVERAGE TEMPERATURE (or counts)')
print(f'Center pixel mean: {mean_center}')
print(f'Whole image mean: {mean_whole}')

# TEMPORAL NOISE (Rashman et al.)
# σ = (frame[i+1] - frame[i]) / sqrt(2)
diff = frames[1:] - frames[:-1]
temporal_noise = diff / np.sqrt(2)

# Average temporal noise per pixel
temporal_noise_image = np.mean(temporal_noise, axis = 0)

# Center pixel temporal noise
temporal_noise_center = temporal_noise_image[row, col]

# Whole image temporal noise (mean over pixels)
temporal_noise_whole = np.mean(temporal_noise_image)

print('\nTEMPORAL NOISE (Rashman method)')
print(f'Center pixel temporal noise: {temporal_noise_center}')
print(f'Whole image temporal noise: {temporal_noise_whole}')
