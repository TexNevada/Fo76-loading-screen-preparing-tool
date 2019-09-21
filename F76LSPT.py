
"""
==============
Import list
==============
"""

from distutils.dir_util import copy_tree
from colorama import init, Fore, Style
import os
import glob
import shutil
from PIL import Image
import PySimpleGUI as sg

"""
================
Prep variables
================
"""
init()
version = "1.2 - GUI Alpha"

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
    if not os.path.exists("Prep"):
        print("-Creating prep folder")
        os.makedirs("Prep")

    def button2():
        print('Button 2 callback')
        sg.PopupOK("Sorry bud. No updates.")

    # Lookup dictionary that maps button to function to call
    func_dict = {'Check for updates': button2}

    # Layout the design of the GUI
    layout = [[sg.Text("===================================\n"
                       f"F76LSPT - Version: {version}\n"
                       "Fo76 Loading Screen Preparing Tool\n"
                       "==================================="
                       , auto_size_text=True)],
              [sg.Image(r"Panda.png")],
              [sg.Text("Please put the images you want as a loading screen for 76 in the \"Prep\" folder before you continue.\n"
                       "INFO: This can be slow depending on the amount of files you have loaded in.\n\n"
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


def file_conversion():
    MaxNum = len(next(os.walk("Prep"))[2])
    TotalNumber = (MaxNum * 6) + 1
    i = 1



    FromDirectory = "Prep"
    ToDirectory = "Temp"
    if not os.path.exists("temp"):
        print(f"{yellow}-Creating temp folder{reset}")
        os.makedirs("Temp")

    sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
    print(f"Copying files.")
    copy_tree(FromDirectory, ToDirectory)

    print("Renaming files.")
    files = glob.glob('temp\\*.*')
    for file in files:
        i = i+1
        sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
        print(f"{cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}-thumbnail.png".format(parts[0])
        os.rename(file, new_name)

    print("Resizing images & fixing color depth")
    path = "Temp\\"
    dirs = os.listdir("Temp")
    for item in dirs:
        i = i + 1
        sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
        if os.path.isfile(path + item):
            print(f"{cyan}Fixing color depth & resizing {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            imResize = im.resize((480, 270), Image.ANTIALIAS)
            imResize.save(path+item, "PNG")

    print("Fixing color depth")
    path = "Prep\\"
    dirs = os.listdir("Prep")
    for item in dirs:
        i = i + 1
        sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
        if os.path.isfile(path + item):
            print(f"{cyan}Fixing color depth for {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            im.save(path+item, "PNG")

    if not os.path.exists("Finished"):
        print(f"{yellow}-Creating Finished folder{reset}")
        os.makedirs("Finished")

    files = glob.glob('Prep\\*.*')
    for file in files:
        i = i + 1
        sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
        print(f"{cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}.png".format(parts[0])
        os.rename(file, new_name)

    Move1 = glob.glob("Prep\\*.*")
    Move2 = glob.glob("Temp\\*.*")

    print("Moving files from Prep to Finished folder")
    for file in Move1:
        i = i + 1
        sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
        print(f"{cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from Prep to Finished")

    print("Moving files from Temp to Finished folder")
    for file in Move2:
        i = i + 1
        sg.OneLineProgressMeter('F76LSPT loading meter', i, TotalNumber, 'key')
        print(f"{cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from Temp to Finished")

    print(green)
    print("Done!\nYou can now close the program")


GUI()
