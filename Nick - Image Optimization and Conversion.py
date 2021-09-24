import PIL
import os
import sys
import pathlib
import shutil
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import *
from tkinter.filedialog import *
from PIL import Image
from pathlib import Path
from shutil import copyfile
from tkinter import messagebox

""" Made by Nicolas Mendes - September 2021
SUMMARY:
💬 Variables
🌈 UI
🔖 Load GUI files defs
⚙️ Logic and Defs
=========== 🧬 Optimization Functions
=========== 🎭 Convertion Functions
"""

""" 🎯 TO DO:
- [x] Make a Listbox
- [x] Make a Scrollbar in the Listbox
- [x] Make a checkbox to reduce image resolution by half.
- [x] Make a way to detect image resolution and if it is larger than 1366x760, reduce it by half.
- [x] Add message when the process is finished.
- [x] Add app Icon
- [x] Fix icons not loading properly
- [x] Make the optimization script
- [x] Make the conversion script
- [x] Connect everything to the tk UI
--- [x] Make the app load all possible images inside the Listbox
--- [x] When the user clicks the Make Magic button, run defs
--- [x] Create two defs - one for optimizing and other for converting
--- [x] After the optimizing def runs, initiate the convert def.
--- [x] Open the folder with the optimized images
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
rootWindow.iconbitmap(relative_to_assets("icon.ico"))

# check if icon.ico exists inside assets folder [Debug]
# if os.path.isfile(relative_to_assets("icon.ico")):
#     print("Icon found!")
# else:
#     print("Icon not found!")

# 💬 Variables

files = os.listdir(IMAGES_PATH)

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
    command=lambda: optimizationFunction(),
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
    command=lambda: loadFolderForImg(),
    relief="flat"
)
button_2.place(
    x=812.0,
    y=41.0,
    width=135.0,
    height=46.0
)

# 🔖 Load GUI files defs


def loadFolderForImg():
    global files
    # open dialog box to select folder
    printableFiles = askdirectory(initialdir=IMAGES_PATH)
    files = os.listdir(printableFiles)
    entry_DefPath.set(str(printableFiles))


# Entry to load files
entry_DefPath = StringVar()
entry_DefPath.set(str(IMAGES_PATH))
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
    textvariable=entry_DefPath,
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

# Listbox to show files loaded rootWindow
list_items = Listbox(
    x=210.0,
    y=115.0,
    height=5,
    width=50,
    bg="#ECEBFB",
    fg="#000000",
    font=("Mulish Regular", 18 * -1),
    highlightcolor="#ECC0FB",
    border=0,
)
list_items.place(relx=0.5, rely=0.5, anchor="center")

for file in files:
    if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):
        list_items.insert(END, file)

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

"""
Removing status area for now, I need to study more about updating label values dinamically.
"""
# Progress Icon
# image_image_5 = PhotoImage(
#     file=relative_to_assets("image_5.png"))
# image_5 = canvas.create_image(
#     95.0,
#     260.0,
#     image=image_image_5
# )

# canvas.create_text(
#     37.0,
#     282.0,
#     anchor="nw",
#     text="Progress Status",
#     fill="#FFFFFF",
#     font=("Mulish Regular", 16 * -1)
# )

# # Dynamic label to show the progress
# canvas.create_text(
#     51.0,
#     328.0,
#     anchor="nw",
#     text="Placeholder",
#     fill="#FFFFFF",
#     font=("Mulish SemiBold", 16 * -1)
# )

# Checkbox (To reduce resolution by half)
reduceByHalf = IntVar()
reduceByHalfChck = Checkbutton(
    text="Reduce Resolution?",
    variable=reduceByHalf,
    bg="#AC59F3",
    fg="#FFFFFF",
    font=("Mulish Regular", 13 * -1),
)
reduceByHalfChck.deselect()
reduceByHalfChck.place(relx=0.03, rely=0.7, anchor="nw")

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

folderImgs = entry_1.get()
print(folderImgs)


def updateListbox():
    global files

    updateFilesFound = os.listdir(IMAGES_PATH)
    files = updateFilesFound

    for file in files:
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):
            list_items.delete(0, END)
            list_items.insert(END, file)
            print(f"Found valid images in {folderImgs} with {file}.")


def optimizationFunction():
    global reduceByHalf
    global files

    updateListbox()

    print(
        f"These are all of the files in our current working directory: {files}")
    confirmFiles = "y"
    confirmDownRes = IntVar()
    confirmDownRes = reduceByHalf.get()

    if confirmFiles == "y":
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):

                # Backup operation
                shutil.copy(
                    f"{folderImgs}/{file}",
                    f"{folderImgs}/backup/_backup_{file}"
                )
                print(f"Copying {file} to backup folder")

                print(f"Optimizing {file}")

                imgOptimize = Image.open(relative_to_images(str(file)))
                imgWidth, imgHeight = imgOptimize.size
                print(f"Image size: {imgWidth} x {imgHeight}")
                print(f"The state of resolution option is: {confirmDownRes}")

                list_items.delete(0, END)
                list_items.insert(END, file)

                # If confirmDownRes = 1, imgWidth and imgHeight are larger than 1366x768 reduce the resolution by half.
                if imgWidth > 1366 and imgHeight > 768 and confirmDownRes == 1:
                    imgOptimize = imgOptimize.resize(
                        (int(imgWidth / 2), int(imgHeight / 2)), PIL.Image.ANTIALIAS)
                    print(f"Reducing image resolution by half of {file}")
                    print(f"Optimized {file}")

                    if file.endswith(".png"):
                        imgOptimize.save(str(relative_to_images(
                            str(file))), optimize=True, quality=70)
                        convertionFunction()
                    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):
                        imgOptimize.save(str(relative_to_images(
                            str(file))), optimize=True, quality=80)
                        convertionFunction()

                # If user don't want to reduce image resolution by half.
                else:
                    print(
                        f"Image: {file}, is not larger enough to reduce resolution.")

                    print(f"Performing standard optimization on {file}")
                    if file.endswith(".png"):
                        imgOptimize.save(str(relative_to_images(
                            str(file))), optimize=True, quality=70)
                        convertionFunction()
                    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):
                        imgOptimize.save(str(relative_to_images(
                            str(file))), optimize=True, quality=80)
                        convertionFunction()

                print(f"{file} optimized!")

            else:
                print(
                    f"No valid files found in {folderImgs} with {file}... Checking again.")
                updateListbox()
    else:
        print("Exiting...")
        sys.exit()

# =========== 🎭 Convertion Functions ===========


def convertionFunction():
    print(
        f"These are all of the files in our current working directory: {files}")

    confirmFiles = "y"

    if confirmFiles == "y":
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".gif"):
                print(f"Converting {file} to WebP")
                loadImg = Image.open(relative_to_images(str(file)))
                loadImg.save(str(relative_to_images(str(file))) +
                             ".webp", "WEBP", quality=80)
                print(f"{file} converted to WebP")
                # Open images folder in default OS file manager.
                subprocess.Popen(
                    ["open", "-R", folderImgs])
                print(f"Opening {file} in Finder")
                # Show a message window with "Optimization and conversion completed!"
                messagebox.showinfo(
                    "Optimization and conversion completed! \n", "All files have been optimized and converted to WebP!")
                print("All files have been optimized and converted to WebP!")
            else:
                print(f"{file} is not a PNG or JPG, skipping...")
    else:
        print("Exiting...")
        sys.exit()


rootWindow.mainloop()
