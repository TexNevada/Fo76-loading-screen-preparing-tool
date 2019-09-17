
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

"""
================
Prep variables
================
"""
init()
version = "1.1"

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
    print(f"{red}This can be slow depending on the amount of files you have loaded in.{reset}")
    input("Press ENTER to continue\n")
    file_conversion()


def file_conversion():
    FromDirectory = "Prep"
    ToDirectory = "Temp"
    if not os.path.exists("temp"):
        print(f"{yellow}-Creating temp folder{reset}")
        os.makedirs("Temp")

    print(f"Copying files.")

    copy_tree(FromDirectory, ToDirectory)

    print("Renaming files.")
    files = glob.glob('temp\\*.*')
    for file in files:
        print(f"{cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}-thumbnail.png".format(parts[0])
        os.rename(file, new_name)

    print("Resizing images & fixing color depth")
    path = "Temp\\"
    dirs = os.listdir("Temp")
    for item in dirs:
        if os.path.isfile(path + item):
            print(f"{cyan}Fixing color depth & resizing {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            imResize = im.resize((480, 270), Image.ANTIALIAS)
            imResize.save(path+item, "PNG")

    print("Fixing color depth")
    path = "Prep\\"
    dirs = os.listdir("Prep")
    for item in dirs:
        if os.path.isfile(path + item):
            print(f"{cyan}Fixing color depth for {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            im.save(path+item, "PNG")

    if not os.path.exists("Finished"):
        print(f"{yellow}-Creating Finished folder{reset}")
        os.makedirs("Finished")

    files = glob.glob('Prep\\*.*')
    for file in files:
        print(f"{cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}.png".format(parts[0])
        os.rename(file, new_name)

    Move1 = glob.glob("Prep\\*.*")
    Move2 = glob.glob("Temp\\*.*")

    print("Moving files from Prep to Finished folder")
    for file in Move1:
        print(f"{cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from Prep to Finished")

    print("Moving files from Temp to Finished folder")
    for file in Move2:
        print(f"{cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from Temp to Finished")

    print(green)
    input("Done!\nYou can now close the program")


menu()
