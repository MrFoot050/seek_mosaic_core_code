'''
The following code will show an image of any given fits file. Also shows a color bar.
'''

import matplotlib.pyplot as plt
from astropy.io import fits

# Insert the directory to your image here, specify what image you want to show. 
image_directory = ''
image_data = fits.getdata(image_directory)

plt.figure()
plt.imshow(image_data, origin='lower')
plt.colorbar()

plt.title('Average Fits Image')
plt.xlabel('X Axis Pixels')
plt.ylabel('Y Axis Pixels')
plt.show()
