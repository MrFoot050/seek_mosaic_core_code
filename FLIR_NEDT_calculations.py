'''
The following code will calculate the NEDT of a microbolometer using the methods adpoted from equation 6 of Rashman et al 2018.
You will need 3 directories, the first and last containing at least 64 frames from your runs, then the middle needing at least 
128 frames. On top of finding the NEDT, it will also find the following paramters;
- Average Temp of center pixel in 20, 25, and 30
- The center pixel Temporal Noise
- the responsivity of the center pixel
- mean NEDT in mK and C
'''
import numpy as np
from astropy.io import fits
import glob

# SETTINGS
# Input Require File Paths
folder_20 = 'E:/CYCLE_1_DATA_fits_gz/2026-04-03_14-15-49/E05257AC071D/converted_fits'   # 64 frames
folder_25 = 'E:/CYCLE_1_DATA_fits_gz/2026-04-03_14-21-10/E05257AC071D/converted_fits'   # 128 frames
folder_30 = 'E:/CYCLE_1_DATA_fits_gz/2026-04-03_14-24-30/E05257AC071D/converted_fits'   # 64 frames

# Optional: counts → temperature conversion (set to 1 if unknown)
calibration_factor = 1.0  # counts per °C

# LOAD FUNCTION
def load_frames(folder):
    files = sorted(glob.glob(folder + '/*.fits'))
    frames = []
    for f in files:
        with fits.open(f) as hdul:
            frames.append(hdul[0].data.astype(float))
    return np.array(frames)

frames_20 = load_frames(folder_20)
frames_25 = load_frames(folder_25)
frames_30 = load_frames(folder_30)

# BASIC INFO
height, width = frames_25.shape[1:]
center_row, center_col = height // 2, width // 2

# MEAN TEMPERATURE
mean_20 = np.mean(frames_20, axis = 0)
mean_25 = np.mean(frames_25, axis = 0)
mean_30 = np.mean(frames_30, axis = 0)

# Convert to temperature if calibration known
mean_temp_20 = mean_20 / calibration_factor
mean_temp_25 = mean_25 / calibration_factor
mean_temp_30 = mean_30 / calibration_factor

mean_temp_center_20 = mean_temp_20[center_row, center_col]
mean_temp_center_25 = mean_temp_25[center_row, center_col]
mean_temp_center_30 = mean_temp_30[center_row, center_col]

print('Center pixel mean temp (20C dataset):', mean_temp_center_20)
print('Center pixel mean temp (25C dataset):', mean_temp_center_25)
print('Center pixel mean temp (30C dataset):', mean_temp_center_30)

# TEMPORAL NOISE (Rashman et al.)
# FLIR uses std dev at the middle temperature (25C)
sigma_counts = np.std(frames_25, axis = 0)

sigma_center = sigma_counts[center_row, center_col]

print('Center pixel temporal noise σ (counts):', sigma_center)
print('Mean σ across image:', np.mean(sigma_counts))

# RESPONSIVITY
# R = (response_30 - response_20) / delta_T
delta_T = 10.0  # 30C - 20C
responsivity = (mean_30 - mean_20) / delta_T

responsivity_center = responsivity[center_row, center_col]

print('Center pixel responsivity (counts/°C):', responsivity_center)

# NEDT
nedt_image = sigma_counts / responsivity   # in °C (or K)

nedt_center = nedt_image[center_row, center_col]

print('Center pixel NEDT (°C):', nedt_center)
print('Mean NEDT over image (°C):', np.mean(nedt_image))

# Convert to mK if desired
print('Mean NEDT (mK):', np.mean(nedt_image) * 1000)
