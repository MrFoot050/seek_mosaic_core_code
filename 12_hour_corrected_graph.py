'''
The following code will read .FITS from a given directory. It will then read the header of each one and extract the temperature of the 
center pixel and average temperature of the whole frame. It will order them chronolgically and will apply a correction based on the data
from a blackbody calibration test. These corrected values will then be plotted as a function of time. 
'''

import numpy as np
from astropy.io import fits
from datetime import datetime
import matplotlib.pyplot as plt
import glob
import pandas as pd
from dateutil import parser
from astropy.timeseries import LombScargle

# Put the directory of your images here
filenames = glob.glob('/home/miles-group/seekcamera-python/examples/DATA/12_hour_shutter_off_calibration/2026-04-09_20-14-39_12_hour/E05257AC071D/converted_fits/*.fits')
imagedata = [None] * len(filenames)

# Start_header will get the header of the fits images, starting with the first image.
# Start_time will take the DATE_OBS part of whichever fits file the previous variable is on.
start_header = fits.getheader(filenames[0])
start_time = datetime.strptime(start_header['DATE-OBS'], "%Y-%m-%dT%H:%M:%S.%f")
files_with_times = []

for i in filenames:
    hdr = fits.getheader(i)
    t = parser.parse(hdr['DATE-OBS'])
    files_with_times.append((i, t))

files_with_times.sort(key=lambda x: x[1])

filenames = [ft[0] for ft in files_with_times]
times = [ft[1] for ft in files_with_times]

start_time = times[0]

#This loop will order each file in terms of time. 
for j, current_time in zip(filenames, times):
    with fits.open(j, mode='update') as hdul:
        header = hdul[0].header
        delta_time = (current_time - start_time).total_seconds()
        header['DELTAT'] = (delta_time, 'Time since first frame (chronological)')
        hdul.flush()

#image_header will get the header of whichever image you would like
image_header = fits.getheader(filenames[10000])
print(image_header) 

# All 3 variables will make an array of all 0s the length of filenames, which is the amount of images
fluxes = np.zeros(len(filenames))
fluxes_mean = np.zeros(len(filenames))
times = np.zeros(len(filenames))

for i, filename in enumerate(filenames):
    image = fits.getdata(filename) 
    header = fits.getheader(filename)
    
    flux = image[0,0]
    fluxes[i] = flux
    
    flux_mean = np.mean(image)
    fluxes_mean[i] = flux_mean

    try:
        obs_time = datetime.strptime(header['DATE-OBS'], "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        obs_time = datetime.strptime(header['DATE-OBS'], "%Y-%m-%dT%H:%M:%S")
        
    times[i] = (obs_time - start_time).total_seconds()

# Apply calibration correction using y = 1.058x - .5532
fluxes = 1.058 * fluxes - 0.5532
fluxes_mean = 1.058 * fluxes_mean - 0.5532

# Plot the corrected temperatures as a function of time
plt.figure()
plt.title('Average Temp and Center Pixel Temp vs Elapsed Time', fontsize = '20')
plt.plot(times, fluxes, 'b', label = 'Single Pixel')
plt.plot(times, fluxes_mean, 'r', label = 'Mean of Pixels')
plt.xlabel('Time (Seconds)', fontsize = '20')
plt.ylabel('Corrected Temperature in °C', fontsize = '20')
plt.legend()
plt.show()
