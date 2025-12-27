""" 
The following code will connect to a Seek thermal camera and record the raw thermography frames over a fixed amount 
of time given by the user. It will record it in either histogram or linear mode and will save the data as a fits.gz file
with metadata headers. It is ran using the following command in a linux terminal:
python3 record_frames_gz.py --mode multi --duration 43200 --agc histogram --shutter auto
where mode is if you want to capture a single frame or multiple, duration is the amount of time in seconds,
agc is the gain mode (either histogram or linear) and shutter is automatic or manual by pressing the s key.
It will save the frames into a new folder every time it has started recording and the folder will be named after the 
date and time in YEAR/MONTH/DAY-HOUR/MINUTE/SECOND, then another folder named after the camera chip ID number.

Author: Ruben Huerta
"""

import argparse
from time import sleep, time
from datetime import datetime
import numpy as np
import os
import threading
import cv2
from astropy.io import fits

from seekcamera import (
    SeekCameraIOType,
    SeekCameraManager,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
    SeekCameraAGCMode,
    SeekCameraShutterMode,
)

# PARSE COMMAND LINE ARGUMENTS 
parser = argparse.ArgumentParser(description = 'Capture thermal images from Seek Camera')
parser.add_argument('--mode:', choices = ['single', 'multi'], default = 'multi', help='Capture one frame or multiple')
parser.add_argument('--duration:', type = int, default = 3, help = 'Recording duration in seconds (only for multi mode)')
parser.add_argument('--agc:', choices = ['linear', 'histogram', 'once'], default = 'linear', help = 'AGC mode for camera')
parser.add_argument('--shutter:', choices = ['auto', 'manual'], default = 'auto', help = 'Shutter mode for camera')
args = parser.parse_args()

# GLOBAL SETTINGS 
BASE_PATH = '/home/miles-group/seekcamera-python/examples/DATA' # Base path is where you would like your new folders to be saved to
camera_state = {}
recording = True  # For manual shutter quit control
current_camera = None  # Reference to active camera for manual shuttering

# CALLBACK: FRAME RECEIVED
def on_frame(camera, camera_frame, _user_data):
    chipid = camera.chipid
    frame = camera_frame.thermography_float
    now = time()

    # Initialize state for new camera
    if chipid not in camera_state:
        # Create unique session folder with timestamp
        session_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(BASE_PATH, session_time, chipid)
        os.makedirs(output_dir, exist_ok = True)
        camera_state[chipid] = {
            'frame_count': 0,
            'output_dir': output_dir,
            'start_time' now,
        }

    state = camera_state[chipid]

    # Handle stopping condition
    if args.mode == 'multi':
        if now - state['start_time'] > args.duration:
            camera.capture_session_stop()
            print(f'[{chipid}] Recording complete (time limit reached).')
            return
    elif args.mode == 'single' and state['frame_count'] > 0:
        camera.capture_session_stop()
        print(f'[{chipid}] Single frame saved. Stopping capture.')
        return

    # Save thermal data to compressed FITS
    filename = f'frame_{state['frame_count']:03}.fits.gz'  # Save as compressed FITS
    fits_path = os.path.join(state['output_dir'], filename)
    thermal_data = np.array(frame.data, dtype = np.float32)

    # Build FITS header
    hdr = fits.Header()
    hdr['DATE-OBS'] = datetime.now().isoformat()
    hdr['CHIP_ID'] = chipid
    try:
        hdr['ENV_TEMP'] = camera_frame.metadata.environment_temperature
    except AttributeError:
        hdr['ENV_TEMP'] = "N/A"
    hdr['AGC_MODE'] = args.agc.upper()
    hdr['SHUTTER'] = args.shutter.upper()

    hdu = fits.PrimaryHDU(thermal_data, header=hdr)
    hdu.writeto(fits_path, overwrite=True)  # Astropy auto-compresses due to .gz

    print(f'[{chipid}] Saved frame {state['frame_count']} to {fits_path}')
    state['frame_count'] += 1

# CALLBACK: CAMERA EVENT
def on_event(camera, event_type, event_status, _user_data):
    global current_camera
    print(f"{event_type}: {camera.chipid}")

    if event_type == SeekCameraManagerEvent.CONNECT:
        current_camera = camera  # Store reference for manual shutter use

        # Set AGC mode (only LINEAR and HISTEQ are supported in this SDK)
        agc_mode_map = {
            'linear': SeekCameraAGCMode.LINEAR,
            'histogram': SeekCameraAGCMode.HISTEQ
        }
        if args.agc not in agc_mode_map:
            print(f'WARNING: Unsupported AGC mode '{args.agc}'. Defaulting to LINEAR.')
            camera.agc_mode = SeekCameraAGCMode.LINEAR
        else:
            camera.agc_mode = agc_mode_map[args.agc]
            print(f'Set AGC mode to: {args.agc.upper()}')

        # Set shutter mode
        if args.shutter == 'manual':
            camera.shutter_mode = SeekCameraShutterMode.MANUAL
            print('Shutter mode set to MANUAL (press "s" to trigger, "q" to quit).')
        else:
            camera.shutter_mode = SeekCameraShutterMode.AUTO
            print('Shutter mode set to AUTO.')

        # Start capture session
        camera.register_frame_available_callback(on_frame, None)
        camera.capture_session_start(SeekCameraFrameFormat.THERMOGRAPHY_FLOAT)

    elif event_type == SeekCameraManagerEvent.DISCONNECT:
        camera.capture_session_stop()

    elif event_type == SeekCameraManagerEvent.ERROR:
        print(f'ERROR: {event_status} ({camera.chipid})')

# THREAD: KEY LISTENER FOR MANUAL SHUTTER
def key_listener():
    global recording
    while recording:
        key = cv2.waitKey(1) & 0xFF
        if args.shutter == 'manual' and key == ord('s') and current_camera:
            print('Triggering shutter manually')
            current_camera.shutter_trigger()
        elif key == ord('q'):
            print('Stopping recording')
            recording = False
            if current_camera:
                current_camera.capture_session_stop()
            break

# MAIN LOOP
def main():
    global recording
    with SeekCameraManager(SeekCameraIOType.USB) as manager:
        manager.register_event_callback(on_event)
        print("Waiting for camera...")

        # Start key listener in a separate thread if manual mode
        if args.shutter == "manual":
            listener_thread = threading.Thread(target=key_listener, daemon=True)
            listener_thread.start()

        try:
            # Run until capture is done or user interrupts
            start = time()
            timeout = args.duration + 5 if args.mode == 'multi' else 10
            while recording and (time() - start < timeout):
                sleep(1.0)
        except KeyboardInterrupt:
            print('Interrupted by user')
        finally:
            recording = False
            print('Exiting')

if __name__ == "__main__":
    main()
