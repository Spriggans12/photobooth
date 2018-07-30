#!/usr/bin/env python

from time import sleep
from shutil import copy2
import sys
import datetime
import os
import evdev
import keyboard

REAL_PATH = os.path.dirname(os.path.realpath(__file__))

from PIL import Image
from ruamel import yaml
import picamera

PATH_TO_CONFIG = 'camera-config.yaml'

#Read config file using YAML interpreter
with open(PATH_TO_CONFIG, 'r') as stream:
    CONFIG = {}
    try:
        CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#Required config
try:
    PHOTO_W = CONFIG['PHOTO_W']
    PHOTO_H = CONFIG['PHOTO_H']
    SCREEN_W = CONFIG['SCREEN_W']
    SCREEN_H = CONFIG['SCREEN_H']
    CAMERA_ROTATION = CONFIG['CAMERA_ROTATION']
    CAMERA_HFLIP = CONFIG['CAMERA_HFLIP']

except KeyError as exc:
    print('')
    print('ERROR:')
    print(' - Problems exist within configuration file: [' + PATH_TO_CONFIG + '].')
    print(' - The expected configuration item ' + str(exc) + ' was not found.')
    print('')
    sys.exit()

CAMERA = picamera.PiCamera()
CAMERA.rotation = CAMERA_ROTATION
CAMERA.annotate_text_size = 80
CAMERA.resolution = (PHOTO_W, PHOTO_H)
CAMERA.hflip = CAMERA_HFLIP

def print_overlay(string_to_print):
    CAMERA.annotate_text = string_to_print

def main():
    """
    Main program loop
    """

    #Start Program
    print('Test program to check that everything works !')
    print('')
    print('Check that the angle for pictures is fine')
    print('Press the \'Take photo\' button to test inputs')
    print('Use [Ctrl] + [c] to exit')
    print('')

    #Start camera preview
    CAMERA.start_preview(resolution=(SCREEN_W, SCREEN_H))
    
    # Finds BT remote controller
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
   
    if len(devices) == 0:
        print "No devices found, try bluetoothctl ? Is the remote turned on ?"
        sys.exit(1)
   
    for device in devices:
        if device.name == 'AB Shutter3':
            print(device)
            print "Connection set !"
            device.grab()
            
            # Event listener loop
            while True:
                photo_button_is_pressed = None
                event = device.read_one()
                
                if event != None and event.type == evdev.ecodes.EV_KEY and event.code == 115 and event.value == 01:
                    photo_button_is_pressed = True

                #Stay inside loop, until button is pressed
                if photo_button_is_pressed is None:
                    sleep(0.1)
                    continue

                #Button has been pressed!
                print('Button pressed!')
                print_overlay("TEST !")
                
                #Remove pending button presses
                cleanPending = True
                while cleanPending == True:
                    pendingEvent = device.read_one()
                    if pendingEvent == None:
                        cleanPending = False
                    else:
                        print "Cleaned one event"
                
                print('Press the button to take a photo')

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('Goodbye')

    finally:
        CAMERA.stop_preview()
        CAMERA.close()
        sys.exit()
