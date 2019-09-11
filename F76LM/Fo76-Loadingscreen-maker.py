
"""
==============
Import list
==============
"""

from distutils.dir_util import copy_tree
from colorama import init, Fore, Style
import os
import glob

"""
=============
Code begins
=============
"""
init()

red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
green = Fore.GREEN
reset = Style.RESET_ALL


def file_conversion():
    FromDirectory = "Prep"
    ToDirectory = "Temp"

    print(yellow)
    print(f"Copying files.\n{reset}{red}This can be fast or slow depending on the amount of files you have loaded in.{reset}")

    copy_tree(FromDirectory, ToDirectory)

    print(yellow)
    print("Renaming files.")
    print(reset, cyan)

    files = glob.glob('temp\*.*')
    for file in files:
        print(f"Renaming {file}")
        parts = file.split(".png" or ".jpg")
        new_name = "{}-thumbnail.png".format(parts[0])
        os.rename(file, new_name)

    print(reset, yellow)

    TempDirectory = "Temp"
    FinishedDirectory = "Finished"

    print("Copying original files")
    copy_tree(FromDirectory, FinishedDirectory)

    print("Copying renamed files")
    copy_tree(TempDirectory, FinishedDirectory)

    cleanup1 = glob.glob("Prep\\*.*")
    cleanup2 = glob.glob("Temp\\*.*")

    print("Cleaning up prep folder")
    for file in cleanup1:
        os.remove(file)

    print("Cleaning up temp folder")
    for file in cleanup2:
        os.remove(file)

    print(reset, green)
    print("Done!")


file_conversion()
