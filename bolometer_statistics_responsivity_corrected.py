'''
The following code will find the standard deviation, temperature and temporal noise
using equation 6 from Rashman et al. 2018 for any given pixel. It will also get an average 
standard deviation, temperature and temporal noise for ther whole series of images. 
'''

import numpy as np
from astropy.io import fits
import glob

# SETTINGS
folder = 'E:/CYCLE_3_DATA_fits_gz/2026-04-03_16-33-12/E05257AC071D/converted_fits'

# Pixel selection
use_center_pixel = True
row, col = 99, 74

# LOAD FRAMES
files = sorted(glob.glob(folder + '/*.fits'))

frames = []
for f in files:
    with fits.open(f) as hdul:
        frames.append(hdul[0].data.astype(float))

frames = np.array(frames)  # shape: (N,H,W)

# Apply calibration equation to pixel measurements 
frames = 0.9684 * frames + 2.252

N, H, W = frames.shape

# Choose pixel
if use_center_pixel:
    row, col = H // 2, W // 2

print(f"Using pixel: ({col - 1}, {row - 1})")

# STANDARD DEVIATION

# Per-pixel standard deviation over time
std_image = np.std(frames, axis=0)

# Center pixel std
std_center = std_image[row, col]

# Whole-image average std
std_whole = np.mean(std_image)

print('\nSTANDARD DEVIATION (°C)')
print(f'Center pixel std: {std_center:.6f}')
print(f'Whole image std: {std_whole:.6f}')

# AVERAGE TEMPERATURE

mean_image = np.mean(frames, axis=0)

mean_center = mean_image[row, col]
mean_whole = np.mean(mean_image)

print('\nAVERAGE TEMPERATURE (°C)')
print(f'Center pixel mean: {mean_center:.6f}')
print(f'Whole image mean: {mean_whole:.6f}')

# TEMPORAL NOISE (Rashman et al.)

# Frame-to-frame differences
diff = (frames[1:] - frames[:-1]) / np.sqrt(2)

# Temporal noise per pixel
temporal_noise_image = np.std(diff, axis=0)

# Center pixel temporal noise
temporal_noise_center = temporal_noise_image[row, col]

# Whole image temporal noise
temporal_noise_whole = np.mean(temporal_noise_image)

print('\nTEMPORAL NOISE (Rashman method) (°C)')
print(f'Center pixel temporal noise: {temporal_noise_center:.6f}')
print(f'Whole image temporal noise: {temporal_noise_whole:.6f}')
