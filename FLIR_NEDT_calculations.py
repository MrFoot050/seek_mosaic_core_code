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
folder_20 = 'E:/CYCLE_4_DATA_fits_gz/2026-04-03_16-35-58/E05257AC071D/converted_fits'
folder_25 = 'E:/CYCLE_4_DATA_fits_gz/2026-04-03_16-41-56/E05257AC071D/converted_fits'
folder_30 = 'E:/CYCLE_4_DATA_fits_gz/2026-04-03_16-46-41/E05257AC071D/converted_fits'

# LOAD FUNCTION
def load_frames(folder):
    files = sorted(glob.glob(folder + '/*.fits'))
    frames = []

    for f in files:
        with fits.open(f) as hdul:
            frames.append(hdul[0].data.astype(float))

    return np.array(frames)

# LOAD DATASETS
frames_20 = load_frames(folder_20)
frames_25 = load_frames(folder_25)
frames_30 = load_frames(folder_30)

# APPLY BLACKBODY CALIBRATION
# T_corrected = 0.9684*T_measured + 2.252

frames_20 = 0.9684 * frames_20 + 2.252
frames_25 = 0.9684 * frames_25 + 2.252
frames_30 = 0.9684 * frames_30 + 2.252

# IMAGE INFO
height, width = frames_25.shape[1:]
center_row, center_col = height // 2, width // 2

print(f'Center pixel: ({center_col},{center_row})')

# MEAN TEMPERATURE

mean_20 = np.mean(frames_20, axis = 0)
mean_25 = np.mean(frames_25, axis = 0)
mean_30 = np.mean(frames_30, axis = 0)

mean_temp_center_20 = mean_20[center_row, center_col]
mean_temp_center_25 = mean_25[center_row, center_col]
mean_temp_center_30 = mean_30[center_row, center_col]

print('\nCENTER PIXEL MEAN TEMPERATURES (°C)')
print(f'20°C dataset: {mean_temp_center_20:.6f}')
print(f'25°C dataset: {mean_temp_center_25:.6f}')
print(f'30°C dataset: {mean_temp_center_30:.6f}')

# STANDARD DEVIATION

std_image = np.std(frames_25, axis=0)

std_center = std_image[center_row, center_col]

print('\nSTANDARD DEVIATION (°C)')
print(f'Center pixel std: {std_center:.6f}')
print(f'Mean image std: {np.mean(std_image):.6f}')

# TEMPORAL NOISE (RASHMAN ET AL. 2018)
# σ = std[(frame(i+1)-frame(i))/sqrt(2)]

diff = (frames_25[1:] - frames_25[:-1]) / np.sqrt(2)

temporal_noise_image = np.std(diff, axis = 0)

temporal_noise_center = temporal_noise_image[center_row, center_col]
temporal_noise_whole = np.mean(temporal_noise_image)

print('\nTEMPORAL NOISE (RASHMAN METHOD) (°C)')
print(f'Center pixel temporal noise: {temporal_noise_center:.6f}')
print(f'Mean temporal noise image: {temporal_noise_whole:.6f}')

# RESPONSIVITY
# R = (response30 - response20)/ΔT

delta_T = 10.0

responsivity = (mean_30 - mean_20) / delta_T

responsivity_center = responsivity[center_row, center_col]
responsivity_whole = np.mean(responsivity)

print('\nRESPONSIVITY')
print(f'Center pixel responsivity: {responsivity_center:.6f}')
print(f'Mean image responsivity: {responsivity_whole:.6f}')

# NEDT
# NEDT = temporal noise / responsivity

nedt_image = temporal_noise_image / responsivity

nedt_center = nedt_image[center_row, center_col]
nedt_whole = np.mean(nedt_image)

print('\nNEDT')
print(f'Center pixel NEDT: {nedt_center:.6f} °C')
print(f'Mean image NEDT: {nedt_whole:.6f} °C')
print(f'Mean image NEDT: {nedt_whole * 1000:.2f} mK')
