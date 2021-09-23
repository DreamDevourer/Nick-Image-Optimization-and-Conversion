import PIL
import os
import sys
import pathlib
from pathlib import Path
from tkinter import *
from PIL import Image
from pathlib import Path

""" Made by Nicolas Mendes - September 2021
SUMMARY:
💬 Variables
🌈 UI
⚙️ Logic and Defs
=========== 🧬 Optimization Functions
=========== 🎭 Convertion Functions
"""

""" 🎯 TO DO:
- [] Make a Listbox
- [x] Fix icons not loading properly
- [x] Make the optimization script
- [x] Make the conversion script
- [] Connect everything to the tk UI
"""

# Initial Setup to load assets
OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Initial Setup to load images
IMAGES_PATH = OUTPUT_PATH / Path("images")


def relative_to_images(path: str) -> Path:
    return IMAGES_PATH / Path(path)


# Tk Window Settings
rootWindow = Tk()
rootWindow.resizable(False, False)
rootWindow.geometry("980x580")
rootWindow.configure(bg="#FFFFFF")
rootWindow.title("Nick - Image Optimization and Conversion")

# 💬 Variables

files = os.listdir(ASSETS_PATH)

# 🌈 UI
canvas = Canvas(
    rootWindow,
    bg="#FFFFFF",
    height=580,
    width=980,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

# Buttons and Labels
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    95.0,
    290.0,
    image=image_image_1
)

# Make magic button ( Aka optimizing and conversion functions )
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=28.0,
    y=502.0,
    width=135.0,
    height=46.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    577.0,
    348.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    577.0,
    64.0,
    image=image_image_3
)

# Browse Button ( Aka selecting files )
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=812.0,
    y=41.0,
    width=135.0,
    height=46.0
)

# Entry to load files
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    567.5,
    74.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000000",
    highlightthickness=0
)
entry_1.place(
    x=364.0,
    y=41.0,
    width=407.0,
    height=44.0
)

# Dummy label ( Don't touch )
canvas.create_text(
    210.0,
    53.0,
    anchor="nw",
    text="Select Folder",
    fill="#000000",
    font=("Mulish Regular", 18 * -1)
)

# Listbox to show files loaded
canvas.create_rectangle(
    210.0,
    155.0,
    947.0,
    548.0,
    fill="#ECEBFB",
    outline="")

canvas.create_text(
    253.0,
    155.0,
    anchor="nw",
    text="Images found inside the folder",
    fill="#000000",
    font=("Mulish Regular", 16 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    226.0,
    165.0,
    image=image_image_4
)

# Logo text ( Don't touch )
canvas.create_text(
    58.0,
    114.0,
    anchor="nw",
    text="I.O.C",
    fill="#FFFFFF",
    font=("Mulish Bold", 36 * -1)
)

# Progress Icon
image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    95.0,
    260.0,
    image=image_image_5
)

canvas.create_text(
    37.0,
    282.0,
    anchor="nw",
    text="Progress Status",
    fill="#FFFFFF",
    font=("Mulish Regular", 16 * -1)
)

# Dynamic label to show the progress
canvas.create_text(
    51.0,
    328.0,
    anchor="nw",
    text="Placeholder",
    fill="#FFFFFF",
    font=("Mulish SemiBold", 16 * -1)
)

# Logo Icon
image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    95.0,
    64.0,
    image=image_image_6
)

# ⚙️ Logic and Defs

""" 
Optimization and Convertion Scripts forked from my Python Fundamentals Study GitHub repository. 
Forked on September 23, 2021.
https://github.com/DreamDevourer/Python-Fundamentals-Study
"""

# =========== 🧬 Optimization Functions ===========


# def optimizationFunction():
#     print(
#         f"These are all of the files in our current working directory: {files}")
#     confirmFiles = input("Confirm files? (Y/n) ")
#     confirmDownRes = input(
#         "Do you want to reduce the resolution by 50%? (Y/n) ")

#     if confirmDownRes == "y" or confirmDownRes == "Y" or confirmDownRes == "":
#         confirmReduction = True

#     if confirmFiles == "y" or confirmFiles == "Y" or confirmFiles == "":
#         for file in files:
#             if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
#                 print(f"Optimizing {file}")
#                 imgOptimize = Image.open(relative_to_assets(str(file)))
#                 imgWidth, imgHeight = imgOptimize.size
#                 if confirmReduction == True:
#                     imgOptimize = imgOptimize.resize(
#                         (int(imgWidth / 2), int(imgHeight / 2)), PIL.Image.ANTIALIAS)

#                     if file.endswith(".png"):
#                         imgOptimize.save(str(relative_to_assets(
#                             str(file))), optimize=True, quality=70)
#                     if file.endswith(".jpg") or file.endswith(".jpeg"):
#                         imgOptimize.save(str(relative_to_assets(
#                             str(file))), optimize=True, quality=80)
#                 else:
#                     if file.endswith(".png"):
#                         imgOptimize.save(str(relative_to_assets(
#                             str(file))), optimize=True, quality=70)
#                     if file.endswith(".jpg") or file.endswith(".jpeg"):
#                         imgOptimize.save(str(relative_to_assets(
#                             str(file))), optimize=True, quality=80)
#                 print(f"{file} optimized!")
#             else:
#                 print(f"{file} is not a PNG or JPG, skipping")
#     else:
#         print("Exiting...")
#         sys.exit()

# =========== 🎭 Convertion Functions ===========


# def convertionFunction():
#     print(
#         f"These are all of the files in our current working directory: {files}")
#     confirmFiles = input("Confirm files? (Y/n) ")

#     if confirmFiles == "y" or confirmFiles == "Y" or confirmFiles == "":
#         for file in files:
#             if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
#                 print(f"Converting {file} to WebP")
#                 loadImg = Image.open(relative_to_assets(str(file)))
#                 loadImg.save(str(relative_to_assets(str(file))) +
#                              ".webp", "WEBP", quality=80)
#                 print(f"{file} converted to WebP")
#             else:
#                 print(f"{file} is not a PNG or JPG, skipping...")
#     else:
#         print("Exiting...")
#         sys.exit()


rootWindow.mainloop()
