# Seek Thermal FITS Capture and Conversions
This repository contains 3 different scripts, with the main script running the Seek Thermal Mosaic Core and capturing thermography images and the other two scripts converting both from fit.gz to fits and vice-versa.

### Features
-Single frame and multi-frame captures
-Linear and Histogram AGC(auto-gain control)
-Automatic and Manual camera shutter control
-Fits.gz output with metadata headers

### Seek_Camera_Code Example Usage
python3 seek_capture_fits.py --mode multi --duration 5 --agc linear --shutter auto
mode takes multi or single
duration is time in seconds, can be changed to any time the user would like
agc is the gain, takes either linear or histogram
shutter is the shutter of the camera, takes either auto or manual. When in manual, control shutter with 's' key on keyboard.

### gz_to_fits Example Usage
python3 gz_to_fits.py
Enter folder path containing .fits.gz files: ***COPY AND PASTE FOLDER PATH HERE***
Found 128 .fits.gz files in ***EXAMPLE_FOLDERPATH***
Enter start frame (0 to 127): ***ENTER WHAT FRAME YOU WOULD LIKE TO START CONVERSION AT***
Enter end frame (0 to 127): ***ENTER WHAT FRAME YOU WOULD LIKE TO END CONVERSION AT***
***AFTER PREVIOUS COMAND YOU WILL SEE MULTIPLE LINES SAYING EACH FILE WAS INDIVIDUALLY COPIED AND CONVERTED***
Conversion finished. New files saved to ***EXAMPLE_FOLDERPATH_CONVERTED***

