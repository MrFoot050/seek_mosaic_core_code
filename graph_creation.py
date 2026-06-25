'''
The following code will make graphs based on the given information. As is, it will make graphs for 
Average Temp vs BB Temp, Average Temporal Noise of Center Pixel vs BB Temp, and Averagr Temporal Noise 
of Whole Image vs BB Temp. 
'''

import numpy as np
import matplotlib.pyplot as plt

# Data Points
blackbody_temp = []
avg_temp_all_images = []
temporal_noise_center_pixel = []
temporal_noise_whole_image = []
average_standard_deviation = []

# Create polynomial for average temp
coefficients_avg_temp = np.polyfit(avg_temp_all_images, blackbody_temp, 1)
polynomial = np.poly1d(coefficients_avg_temp)
print('1D polynomial for Avg Temp vs BB Temp:', polynomial)

temp_grid = np.arange(15, 32.5, .1)
temp_fit = np.polyval(coefficients_avg_temp, temp_grid)

# Plot dataset and polynomial for average temp
plt.figure('plot')
plt.errorbar(
    blackbody_temp,
    avg_temp_all_images,
    yerr = average_standard_deviation,
    fmt = 'o',          # marker style
    capsize = 5,        # little caps on bars
    label = 'Data'
)
plt.title('Average Temperature of Full Series vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temperature Recorded(°C)')
plt.plot(temp_fit, temp_grid)
plt.show()


#------------------------------------------------------------------------------------------------------------------------
# Create polynomial for temporal noise of center pixel
coefficients_temeporal_noise_center_pixel = np.polyfit(blackbody_temp, temporal_noise_center_pixel, 1)
polynomial_temporal_noise_center_pixel = np.poly1d(coefficients_temeporal_noise_center_pixel)
print('1D polynomial for Avg Temporal Noise of Center Pixel vs BB Temp:', polynomial_temporal_noise_center_pixel)

# Plot dataset and polynomial for temporal noise of center pixel
plt.figure()
plt.scatter(blackbody_temp, temporal_noise_center_pixel)
plt.plot(blackbody_temp, polynomial_temporal_noise_center_pixel(blackbody_temp))
plt.title('Average Temporal Noise of Center Pixel vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temporal Noise Recorded')
plt.show()


#------------------------------------------------------------------------------------------------------------------------
# Create polynomial for temporal noise of center pixel
coefficients_temporal_noise_whole_image = np.polyfit(blackbody_temp, temporal_noise_whole_image, 1)
polynomial_temporal_noise_whole_image = np.poly1d(coefficients_temporal_noise_whole_image)
print('1D polynomial for Avg Temporal Noise of Whole Image vs BB Temp:', polynomial_temporal_noise_whole_image)

# Plot dataset and polynomial for temporal noise of center pixel
plt.figure()
plt.scatter(blackbody_temp, temporal_noise_whole_image)
plt.plot(blackbody_temp, polynomial_temporal_noise_whole_image(blackbody_temp))
plt.title('Average Temporal Noise of Full Images vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temporal Noise Recorded')
plt.show()
