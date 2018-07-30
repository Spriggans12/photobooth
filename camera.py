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
    CAMERA_BUTTON_PIN = CONFIG['CAMERA_BUTTON_PIN']
    EXIT_BUTTON_PIN = CONFIG['EXIT_BUTTON_PIN']
    TOTAL_PICS = CONFIG['TOTAL_PICS']
    PREP_DELAY = CONFIG['PREP_DELAY']
    COUNTDOWN = CONFIG['COUNTDOWN']
    PHOTO_W = CONFIG['PHOTO_W']
    PHOTO_H = CONFIG['PHOTO_H']
    SCREEN_W = CONFIG['SCREEN_W']
    SCREEN_H = CONFIG['SCREEN_H']
    CAMERA_ROTATION = CONFIG['CAMERA_ROTATION']
    CAMERA_HFLIP = CONFIG['CAMERA_HFLIP']
    SAVE_RAW_IMAGES_FOLDER = CONFIG['SAVE_RAW_IMAGES_FOLDER']

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

def health_test_required_folders():
    folders_list=[SAVE_RAW_IMAGES_FOLDER]
    folders_checked=[]

    for folder in folders_list:
        if folder not in folders_checked:
            folders_checked.append(folder)
        else:
            print('ERROR: Cannot use same folder path ('+folder+') twice. Refer config file.')

        #Create folder if doesn't exist
        if not os.path.exists(folder):
            print('Creating folder: ' + folder)
            os.makedirs(folder)

def print_overlay(string_to_print):
    print(string_to_print)
    CAMERA.annotate_text = string_to_print

def get_base_filename_for_images():
    base_filename = str(datetime.datetime.now()).split('.')[0]
    base_filename = base_filename.replace(' ', '_')
    base_filename = base_filename.replace(':', '-')
    base_filepath = REAL_PATH + '/' + SAVE_RAW_IMAGES_FOLDER + '/' + base_filename
    return base_filepath

def remove_overlay(overlay_id):
    if overlay_id != -1:
        CAMERA.remove_overlay(overlay_id)

# overlay one image on screen
def overlay_image(image_path, duration=0, layer=3, mode='RGB', window=None):
    # Load the (arbitrarily sized) image
    img = Image.open(image_path)

    if( img.size[0] > SCREEN_W):
        # To avoid memory issues associated with large images, we are going to resize image to match our screen's size:
        basewidth = SCREEN_W
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)

    # Create an image padded to the required size with mode 'RGB' / 'RGBA'
    pad = Image.new(mode, (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
    ))
    pad.paste(img, (0, 0))
    try:
        padded_img_data = pad.tobytes()
    except AttributeError:
        padded_img_data = pad.tostring()

    if window != None:
        o_id = CAMERA.add_overlay(padded_img_data, size=img.size, fullscreen=False)
        o_id.window = (window[0], window[1], window[2], window[3])
    else:
        o_id = CAMERA.add_overlay(padded_img_data, size=img.size)
    o_id.layer = layer

    if duration > 0:
        sleep(duration)
        CAMERA.remove_overlay(o_id)
        o_id = -1

    return o_id

def prep_for_photo_screen(photo_number):
    #Get ready for the next photo
    get_ready_image = REAL_PATH + '/assets/01_get_ready_' + str(photo_number) + '.png'
    overlay_image(get_ready_image, PREP_DELAY, 3, 'RGBA')

def taking_photo(photo_number, filename_prefix):
    filename = filename_prefix + '_' + str(photo_number) + 'of'+ str(TOTAL_PICS)+'.jpg'

    #countdown from 3, and display countdown on screen
    for counter in range(COUNTDOWN, 0, -1):
        print_overlay("             ..." + str(counter))
        sleep(1)

    CAMERA.annotate_text = ''
    CAMERA.capture(filename)
    print('Photo (' + str(photo_number) + ') saved: ' + filename)
    return filename

def playback_screen(filename_prefix):
    print('Processing...')
    processing_image = REAL_PATH + '/assets/02_done.png'
    overlay_image(processing_image, 2)

    # Grille
    grid_image = REAL_PATH + '/assets/03_grid.png'
    back_image = REAL_PATH + '/assets/03_background.png'
    back_overlay = overlay_image(back_image, 0, 4, mode='RGBA')
    grid_overlay = overlay_image(grid_image, 0, 10, mode='RGBA')
    
    # Affiche les 4 images
    # 1 2
    # 3 4
    img1 = filename_prefix + '_1of4.jpg'
    img2 = filename_prefix + '_2of4.jpg'
    img3 = filename_prefix + '_3of4.jpg'
    img4 = filename_prefix + '_4of4.jpg'
    
    o1 = overlay_image(img1, 0, 6, window=[0,0,512,384])
    o2 = overlay_image(img2, 0, 6, window=[513,0,512,384])
    o3 = overlay_image(img3, 0, 6, window=[0,385,512,384])
    o4 = overlay_image(img4, 0, 6, window=[513,385,512,384])
    
    # Waits
    sleep(5)
    
    # Removes all overlays
    remove_overlay(grid_overlay)
    remove_overlay(back_overlay)
    remove_overlay(o1)
    remove_overlay(o2)
    remove_overlay(o3)
    remove_overlay(o4)
    print('All done!')
    finished_image = REAL_PATH + '/assets/04_thank_you.png'
    overlay_image(finished_image, 5)

def main():
    """
    Main program loop
    """

    #Start Program
    print('Welcome to the photo booth!')
    print('')
    print('Press the \'Take photo\' button to take a photo')
    print('Use [Ctrl] + [c] to exit')
    print('')

    #Setup any required folders (if missing)
    health_test_required_folders()

    #Start camera preview
    CAMERA.start_preview(resolution=(SCREEN_W, SCREEN_H))

    #Display intro screen
    intro_image_1 = REAL_PATH + '/assets/00_intro_1.png'
    intro_image_2 = REAL_PATH + '/assets/00_intro_2.png'
    overlay_1 = overlay_image(intro_image_1, 0, 3)
    overlay_2 = overlay_image(intro_image_2, 0, 4)
    
    i = 0
    blink_speed = 10
   
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
                    #After every 10 cycles, alternate the overlay
                    i = i+1
                    if i == blink_speed:
                        overlay_2.alpha = 255
                    elif i == (2 * blink_speed):
                        overlay_2.alpha = 0
                        i = 0
                    #Regardless, restart loop
                    sleep(0.1)
                    continue

                #Button has been pressed!
                print('Button pressed!')

                #Get filenames for images
                filename_prefix = get_base_filename_for_images()
                remove_overlay(overlay_2)
                remove_overlay(overlay_1)

                photo_filenames = []
                # Takes 4 photos
                for photo_number in range(1, TOTAL_PICS + 1):
                    prep_for_photo_screen(photo_number)
                    fname = taking_photo(photo_number, filename_prefix)
                    photo_filenames.append(fname)

                #thanks for playing
                playback_screen(filename_prefix)

                # Display intro screen again
                overlay_1 = overlay_image(intro_image_1, 0, 3)
                overlay_2 = overlay_image(intro_image_2, 0, 4)
                
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
