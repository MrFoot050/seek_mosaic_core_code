'''
The following code will make graphs based on the given information. As is, it will make graphs for 
Average Temp vs BB Temp, Average Temporal Noise of Center Pixel vs BB Temp, and Averagr Temporal Noise 
of Whole Image vs BB Temp. 
'''

import numpy as np
import matplotlib.pyplot as plt

# Data Points for cycle 1
BB_Temp_Cycle_1 = [20, 22.5, 25, 27.5, 30]
Avg_temp_all_images = [21.5582, 24.228, 26.6307, 29.1463, 31.4535]
Temporal_Noise_Center_Pixel = [0.00159, 0.0009, 0.0001, 0.001, 0.0008]
Temporal_Noise_Whole_Image = [0.00115, 0.0009, 0.00007, 0.001, 0.0012]

average_standard_deviation = [0.1975 ,0.1682 ,0.131 ,0.2074 ,0.1552]

#Create polynomial for cycle 1 avergae temp
cycle_1_coefficients_avg_temp = np.polyfit(BB_Temp_Cycle_1, Avg_temp_all_images, 1)
cycle_1_polynomial = np.poly1d(cycle_1_coefficients_avg_temp)
print('1D polynomial for Avg Temp vs BB Temp:', cycle_1_polynomial)

# Plot dataset and polynomial for cycle 1 average temp
plt.figure()
plt.errorbar(
    BB_Temp_Cycle_1,
    Avg_temp_all_images,
    yerr = average_standard_deviation,
    fmt = 'o',          # marker style
    capsize = 5,        # little caps on bars
    label = 'Data'
)
plt.plot(BB_Temp_Cycle_1, cycle_1_polynomial(BB_Temp_Cycle_1))
plt.title('Average Temperature of Full Series vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temperature Recorded(°C)')
plt.show()


#------------------------------------------------------------------------------------------------------------------------
#Create polynomial for cycle 1 temporal noise of center pixel
cycle_1_coefficients_temeporal_noise_center_pixel = np.polyfit(BB_Temp_Cycle_1, Temporal_Noise_Center_Pixel, 1)
cycle_1_polynomial_temporal_noise_center_pixel = np.poly1d(cycle_1_coefficients_temeporal_noise_center_pixel)
print('1D polynomial for Avg Temporal Noise of Center Pixel vs BB Temp:', cycle_1_polynomial_temporal_noise_center_pixel)

# Plot dataset and polynomial for cycle 1 temporal noise of center pixel
plt.figure()
plt.scatter(BB_Temp_Cycle_1, Temporal_Noise_Center_Pixel)
plt.plot(BB_Temp_Cycle_1, cycle_1_polynomial_temporal_noise_center_pixel(BB_Temp_Cycle_1))
plt.title('Average Temporal Noise of Center Pixel vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temporal Noise Recorded')
plt.show()


#------------------------------------------------------------------------------------------------------------------------
#Create polynomial for cycle 1 temporal noise of center pixel
cycle_1_coefficients_temeporal_noise_whole_image = np.polyfit(BB_Temp_Cycle_1, Temporal_Noise_Whole_Image, 1)
cycle_1_polynomial_temporal_noise_whole_image = np.poly1d(cycle_1_coefficients_temeporal_noise_whole_image)
print('1D polynomial for Avg Temporal Noise of Whole Image vs BB Temp:', cycle_1_polynomial_temporal_noise_whole_image)

# Plot dataset and polynomial for cycle 1 temporal noise of center pixel
plt.figure()
plt.scatter(BB_Temp_Cycle_1, Temporal_Noise_Center_Pixel)
plt.plot(BB_Temp_Cycle_1, cycle_1_polynomial_temporal_noise_whole_image(BB_Temp_Cycle_1))
plt.title('Average Temporal Noise of Full Images vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temporal Noise Recorded')
plt.show()
