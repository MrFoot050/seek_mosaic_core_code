"""
The following code will convert any saved fits.gz files to .fits files.To run it, you will type 
the following (Replace asterisks with whatever you save the file as in  on your system):
python3 *************** 
you will then be prompted to enter the path of the fits.gz files where the script will look for any 
files ending with the fits.gz tag. It will list them in order and ask which frames you would like to 
convert with a starting and ending frame. It will create a copy of the frames as a .fits file and will
create a new folder within the previously input directory containing the new saved fits files.
"""

import glob
from astropy.io import fits
import os
import re

# Ask for folder
folder = input('Enter folder path containing .fits.gz files: ').strip()

# Find all .fits.gz files in that folder
gz_files = glob.glob(os.path.join(folder, '*.fits.gz'))

if not gz_files:
    print('No .fits.gz files found in that folder.')
    exit()

# Sort numerically based on digits in filename
def extract_number(path):
    # Find last integer in filename
    m = re.findall(r'\d+', os.path.basename(path))
    return int(m[-1]) if m else -1

gz_files = sorted(gz_files, key = extract_number)

print(f'Found {len(gz_files)} .fits.gz files in {folder}')

# Ask user for frame range
start = int(input(f'Enter start frame (0 to {len(gz_files) - 1}): '))
end = int(input(f'Enter end frame (0 to {len(gz_files) - 1}): '))

# Clip range to valid values
start = max(0, start)
end = min(len(gz_files) - 1, end)

# Create output subfolder
out_folder = os.path.join(folder, 'converted_fits')
os.makedirs(out_folder, exist_ok = True)

# Convert files in range
for i in range(start, end + 1):
    gz_file = gz_files[i]
    with fits.open(gz_file) as hdul:
        base_name = os.path.basename(os.path.splitext(gz_file)[0])
        out_file = os.path.join(out_folder, base_name)
        hdul.writeto(out_file, overwrite = True)
        print(f'Converted frame {i}: {gz_file} -> {out_file}')

print(f'Conversion finished. New files saved to {out_folder}')
