
"""
==============
Import list
==============
"""

from distutils.dir_util import copy_tree
from colorama import init, Fore, Style
import os, sys
import glob
import shutil
from PIL import Image

"""
================
Prep variables
================
"""
init()
version = "1.0"

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


def menu():
    print(yellow)
    print("===================================")
    print(f"F76LSPT - Version: {version}")
    print("Fo76 Loading Screen Preparing Tool ")
    print("===================================")
    print(reset)

    if not os.path.exists("Prep"):
        print("-Creating prep folder")
        os.makedirs("Prep")
    print("Please put the images you want as a loading screen for 76 in the \"Prep\" folder before you continue.")
    input("Press ENTER to continue\n")
    file_conversion()


def file_conversion():
    FromDirectory = "Prep"
    ToDirectory = "Temp"
    if not os.path.exists("temp"):
        print(f"{yellow}-Creating temp folder{reset}")

    print(f"Copying files.\n{red}This can be slow depending on the amount of files you have loaded in.{reset}")

    copy_tree(FromDirectory, ToDirectory)

    print("Renaming files.")
    files = glob.glob('temp\\*.*')
    for file in files:
        print(f"{cyan}Renaming {file}{reset}")
        parts = file.split(".png" or ".jpg")
        new_name = "{}-thumbnail.png".format(parts[0])
        os.rename(file, new_name)

    print("Resizing images")
    path = "Temp\\"
    dirs = os.listdir("Temp")
    for item in dirs:
        if os.path.isfile(path + item):
            print(f"Resizing {item}")
            im = Image.open(path + item)
            imResize = im.resize((480, 270), Image.ANTIALIAS)
            imResize.save(path+item, "PNG")

    if not os.path.exists("Finished"):
        print(f"{yellow}-Creating Finished folder{reset}")

    Move1 = glob.glob("Prep\\*.*")
    Move2 = glob.glob("Temp\\*.*")

    print("Moving files from Prep to Finished folder"+cyan)
    for file in Move1:
        print(f"{cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print(reset+"Moved files from Prep to Finished")

    print("Moving files from Temp to Finished folder"+cyan)
    for file in Move2:
        print(f"{cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print(reset + "Moved files from Temp to Finished")


    print(green)
    input("Done!\nYou can now close the program")

menu()
