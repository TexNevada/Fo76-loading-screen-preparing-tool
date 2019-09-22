
"""
==============
Import list
==============
"""

from distutils.dir_util import copy_tree
from colorama import init, Fore, Style
import os
import sys
import glob
import shutil
from PIL import Image
import PySimpleGUI as sg
import requests
import webbrowser

"""
================
Prep variables
================
"""
init()
version = "1.2"

red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
green = Fore.GREEN
reset = Style.RESET_ALL
"""
=============
Code begins
=============
"""


def GUI():
    image_path = resource_path("vault-tec.png")
    if not os.path.exists("Prep"):
        print(f"NOTE: {yellow}-Creating Prep folder{reset}")
        os.makedirs("Prep")

    def button2():
        r = requests.get("https://raw.githubusercontent.com/texnevada/Fo76-loading-screen-preparing-tool/master/version.txt")
        if r.text <= version:
            sg.PopupOK("No new updates.")
        else:
            sg.Popup("There is a new update out!")
            website = "https://github.com/texnevada/Fo76-loading-screen-preparing-tool/releases/latest"
            webbrowser.open_new_tab(website)

    # Lookup dictionary that maps button to function to call
    func_dict = {'Check for updates': button2}

    # Layout the design of the GUI
    layout = [[sg.Text("===================================\n"
                       f"F76LSPT - Version: {version}\n"
                       "Fo76 Loading Screen Preparing Tool\n"
                       "==================================="
                       , auto_size_text=True)],
              [sg.Image(image_path)],
              [sg.Text("Put the images you want as loading screens for 76 in the \"Prep\" folder before you continue.\n"
                       "NOTE: This can be slow depending on the amount of files you have loaded in.\n\n"
                       "Press RUN to continue"
                       , auto_size_text=True)],
              [sg.Button('Run'), sg.Button('Check for updates'), sg.Quit()]]

    # Show the Window to the user
    window = sg.Window('F76LSPT', layout)

    # Event loop. Read buttons, make callbacks
    while True:
        # Read the Window
        event, value = window.Read()
        if event in ('Quit', None):
            break
        elif event in ('Run', None):
            MaxNum = len(next(os.walk("Prep"))[2])
            if MaxNum == 0:
                sg.Popup("There is no images in the prep folder.\nYou will need to put some images in the prep "
                         "folder.\nThe folder will open automatically for you once you hit \"OK\"\n"
                         "Press \"Run\" once you have added some images into the Prep folder.")
                path = "Prep"
                path = os.path.realpath(path)
                os.startfile(path)
            elif MaxNum != 0:
                window.Close()
                file_conversion()
                break
        # Lookup event in function dictionary
        try:
            func_to_call = func_dict[event]  # look for a match in the function dictionary
            func_to_call()  # if successfully found a match, call the function found
        except:
            pass

    window.Close()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def file_conversion():
    MaxNum = len(next(os.walk("Prep"))[2])
    TotalNumber = (MaxNum * 6)
    i = 1

    FromDirectory = "Prep"
    ToDirectory = "LSPTTemp"
    if not os.path.exists("LSPTTemp"):
        print(f"NOTE: {yellow}-Creating temp folder{reset}")
        os.makedirs("LSPTTemp")
    else:
        try:
            shutil.rmtree("LSPTTemp")
        except:
            sg.Popup("Error: Unable to remove temp folder. Please empty its contents and delete the folder.")
            sys.exit()

    print(f"Copying files.")
    if sg.OneLineProgressMeter('.\\F76LSPT loading meter', i, TotalNumber, 'key', "Copying files to LSPT Temp directory. "
                                                                                  "This step might take a bit.") == False:
        sys.exit()
    copy_tree(FromDirectory, ToDirectory)

    print("Renaming files.")
    files = glob.glob('LSPTTemp\\*.*')
    for file in files:
        i = i + 1
        if sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key', "Renaming files in LSPT Temp directory") == False:
            sys.exit()
        print(f"INFO: {cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}-thumbnail.png".format(parts[0])
        try:
            os.rename(file, new_name)
        except:
            os.replace(file, new_name)

    print("Resizing images & fixing color depth")
    path = "LSPTTemp\\"
    dirs = os.listdir("LSPTTemp")
    for item in dirs:
        i = i + 1
        if sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key', "Resizing images & fixing color depth") == False:
            sys.exit()
        if os.path.isfile(path + item):
            print(f"INFO: {cyan}Fixing color depth & resizing {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            imResize = im.resize((480, 270), Image.ANTIALIAS)
            imResize.save(path+item, "PNG")

    files = glob.glob('Prep\\*.*')
    for file in files:
        i = i + 1
        if sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key', "Prep all images to PNG") == False:
            sys.exit()
        print(f"INFO: {cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}.png".format(parts[0])
        try:
            os.rename(file, new_name)
        except:
            os.replace(file, new_name)

    print("Fixing color depth")
    path = "Prep\\"
    dirs = os.listdir("Prep")
    for item in dirs:
        i = i + 1
        if sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key', "Fixing color depth for Prep images") == False:
            sys.exit()
        if os.path.isfile(path + item):
            print(f"INFO: {cyan}Fixing color depth for {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            im.save(path + item, "PNG")

    Move1 = glob.glob("Prep\\*.*")
    Move2 = glob.glob("LSPTTemp\\*.*")

    if not os.path.exists("Finished"):
        print(f"NOTE: {yellow}-Creating Finished folder{reset}")
        os.makedirs("Finished")

    print("Moving files from Prep to Finished folder")
    for file in Move1:
        i = i + 1
        if sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key', "Don't worry if the program doesn't respond.\nIts moving files") == False:
            sys.exit()
        print(f"INFO: {cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from Prep to Finished")

    print(f"NOTE: {yellow}Deleting Prep folder{reset}")
    os.rmdir("Prep")

    print("Moving files from LSPTTemp to Finished folder")
    for file in Move2:
        i = i + 1
        if sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key', "Don't worry if the program doesn't respond.\nIts moving files") == False:
            sys.exit()
        print(f"INFO: {cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from LSPTTemp to Finished")

    print(f"NOTE: {yellow}Deleting LSPTTemp folder{reset}")
    os.rmdir("LSPTTemp")

    sg.Popup("Done!\nYou can now move the photos to 76")
    path = "Finished"
    path = os.path.realpath(path)
    os.startfile(path)


GUI()
