'''
The following code will make graphs based on the given information. As is, it will make graphs for 
Average Temp vs BB Temp, Average Temporal Noise of Center Pixel vs BB Temp, and Averagr Temporal Noise 
of Whole Image vs BB Temp. 
'''

# Data Points
blackbody_temp = [20, 22.5, 25, 27.5, 30]
avg_temp_all_images = [20.3407, 23.3113, 25.7162, 28.2587, 30.618]
temporal_noise_center_pixel = [0.0051, 0.0046, 0.0053, 0.0046, 0.0057]
temporal_noise_whole_image = [0.0053, 0.0053, 0.0056, 0.0049, 0.0063]
average_standard_deviation = [0.5682, 0.5921, 0.5987, 0.5557, 0.456]

#Create polynomial for avergae temp
coefficients_avg_temp = np.polyfit(BB_Temp_Cycle_1, Avg_temp_all_images, 1)
polynomial = np.poly1d(cycle_1_coefficients_avg_temp)
print('1D polynomial for Avg Temp vs BB Temp:', cycle_1_polynomial)

# Plot dataset and polynomial for average temp
plt.figure()
plt.errorbar(
    blackbody_temp,
    avg_temp_all_images,
    yerr = average_standard_deviation,
    fmt = 'o',          # marker style
    capsize = 5,        # little caps on bars
    label = 'Data'
)
plt.plot(blackbody_temp, polynomial(blackbody_temp))
plt.title('Average Temperature of Full Series vs BB Temperature')
plt.xlabel('Black Body Temperature (°C)')
plt.ylabel('Average Temperature Recorded(°C)')
plt.show()


#------------------------------------------------------------------------------------------------------------------------
#Create polynomial for temporal noise of center pixel
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
#Create polynomial for temporal noise of center pixel
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
