"""
The following code will convert any saved .fits files to .fits.gz files. To run it, you will type 
the following (Replace asterisks with whatever you save the file as in  on your system):
python3 *************** 
you will then be prompted to enter the path of the .fits files where the script will look for any 
files ending with the fits.gz tag. It will list them in order and ask which frames you would like to 
convert with a starting and ending frame. It will create a copy of the frames as a .fits.gz file and will
create a new folder within the previously input directory containing the new saved fits.gz files.
"""

import glob
from astropy.io import fits
import os
import re

# Ask for folder
folder = input('Enter folder path containing .fits files: ').strip()

# Find all .fits files in that folder
fits_files = glob.glob(os.path.join(folder, '*.fits'))

if not fits_files:
    print('No .fits files found in that folder.')
    exit()

# Sort numerically based on digits in filename
def extract_number(path):
    m = re.findall(r'\d+', os.path.basename(path))
    return int(m[-1]) if m else -1

fits_files = sorted(fits_files, key = extract_number)

print(f'Found {len(fits_files)} .fits files in {folder}')

# Ask user for frame range
start = int(input(f'Enter start frame (0 to {len(fits_files)-1}): '))
end = int(input(f'Enter end frame (0 to {len(fits_files)-1}): '))

# Clip range to valid values
start = max(0, start)
end = min(len(fits_files) - 1, end)

# Create output subfolder
out_folder = os.path.join(folder, 'converted_fits_gz')
os.makedirs(out_folder, exist_ok = True)

# Convert files in range
for i in range(start, end + 1):
    fits_file = fits_files[i]
    with fits.open(fits_file) as hdul:
        base_name = os.path.basename(fits_file) + '.gz'
        out_file = os.path.join(out_folder, base_name)
        hdul.writeto(out_file, overwrite = True)
        print(f'Converted frame {i}: {fits_file} -> {out_file}')

print(f'Conversion finished. New files saved to {out_folder}')
