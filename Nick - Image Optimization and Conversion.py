import re
import os
import sys
import PIL
import pathlib
import random
import shutil
import subprocess
from pathlib import Path
from PIL import Image
from pathlib import Path
from shutil import copyfile
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter import (
    Tk,
    Canvas,
    Button,
    messagebox,
    IntVar,
    StringVar,
    END,
    Listbox,
    PhotoImage,
    Entry,
    Checkbutton,
)

""" Made by Nicolas Mendes - September 2021
SUMMARY:

✍️ Initial Setup to load assets
🧝🏻‍♀️ Tk Window Settings
💬 Variables
🌈 UI
🔖 Load GUI files defs
⚙️ Logic and Defs
=========== 📜 Check Function
=========== 🧬 Optimization Functions
=========== 🎭 Convertion Functions

"""

# ✍️ Initial Setup to load assets

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    """Return a path relative to the assets folder."""
    return ASSETS_PATH / Path(path)


IMAGES_PATH = OUTPUT_PATH / Path("images")


def relative_to_images(path: str) -> Path:
    """Return a path relative to the images folder."""
    return IMAGES_PATH / Path(path)


# 🧝🏻‍♀️ Tk Window Settings
rootWindow = Tk()
rootWindow.resizable(False, False)
rootWindow.geometry("980x580")
rootWindow.configure(bg="#FFFFFF")
rootWindow.title("Nick - Image Optimization and Conversion")
rootWindow.iconbitmap(relative_to_assets("icon.ico"))

# 💬 Variables

files = os.listdir(IMAGES_PATH)
phoneticAlphabet = ["Alpha","Bravo","Charlie","Delta","Echo","Foxtrot","Golf","Hotel","India","Juliet","Kilo","Lima","Mike","November","Oscar","Papa","Quebec","Romeo","Sierra","Tango","Uniform","Victor","Whiskey","X-Ray","Yankee","Zulu"]

# 🌈 UI
canvas = Canvas(
    rootWindow,
    bg="#FFFFFF",
    height=580,
    width=980,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

# Buttons and Labels
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(95.0, 290.0, image=image_image_1)

# Make magic button ( Aka optimizing and conversion functions )
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: optimizationFunction(),
    relief="flat",
)
button_1.place(x=28.0, y=502.0, width=135.0, height=46.0)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(577.0, 348.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(577.0, 64.0, image=image_image_3)

# Browse Button ( Aka selecting files )
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: loadFolderForImg(),
    relief="flat",
)
button_2.place(x=812.0, y=41.0, width=135.0, height=46.0)

# 🔖 Load GUI files defs


def loadFolderForImg():
    """Load the folder with images"""

    global files
    # open dialog box to select folder
    printableFiles = askdirectory(initialdir=IMAGES_PATH)
    files = os.listdir(printableFiles)
    entry_DefPath.set(str(printableFiles))
    updateListbox()


# Entry to load files
entry_DefPath = StringVar()
entry_DefPath.set(str(IMAGES_PATH))
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(567.5, 74.0, image=entry_image_1)
entry_1 = Entry(
    bd=0, bg="#FFFFFF", fg="#000000", textvariable=entry_DefPath, highlightthickness=0
)
entry_1.place(x=364.0, y=41.0, width=407.0, height=44.0)

# Dummy label ( Don't touch )
canvas.create_text(
    210.0,
    53.0,
    anchor="nw",
    text="Select Folder",
    fill="#000000",
    font=("Mulish Regular", 18 * -1),
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
    if (
        file.endswith(".png")
        or file.endswith(".jpg")
        or file.endswith(".jpeg")
        or file.endswith(".gif")
    ):
        list_items.insert(END, file)

    if file.endswith(".webp") and "Optimized" not in file:
        list_items.insert(END, file)

canvas.create_text(
    253.0,
    155.0,
    anchor="nw",
    text="Images found inside the folder",
    fill="#000000",
    font=("Mulish Regular", 16 * -1),
)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(226.0, 165.0, image=image_image_4)

# Logo text ( Don't touch )
canvas.create_text(
    58.0,
    114.0,
    anchor="nw",
    text="I.O.C",
    fill="#FFFFFF",
    font=("Mulish Bold", 36 * -1),
)

# Checkbox (To reduce resolution by half)
reduceByHalf = IntVar()
reduceByHalfChck = Checkbutton(
    text="Smart Scale Mode",
    variable=reduceByHalf,
    bg="#AC59F3",
    fg="#FFFFFF",
    font=("Mulish Regular", 13 * -1),
)
reduceByHalfChck.deselect()
reduceByHalfChck.place(relx=0.03, rely=0.7, anchor="nw")

# Logo Icon
image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(95.0, 64.0, image=image_image_6)

# ⚙️ Logic and Defs

""" 
Optimization and Convertion Scripts forked from my Python Fundamentals Study GitHub repository. 
Forked on September 23, 2021.
https://github.com/DreamDevourer/Python-Fundamentals-Study
"""


def cleaningRoutine():
    """Removes any legacy image"""

    for file in files:
        fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

        if (
            fileName.endswith(".png")
            or fileName.endswith(".jpg")
            or fileName.endswith(".jpeg")
            or fileName.endswith(".gif")
        ):
            # Delete original file
            print(f"Deleting {fileName}")
            os.remove(f"{folderImgs}/{fileName}")


# =========== 📜 Check Function ===========

folderImgs = entry_1.get()
print(folderImgs)


def updateListbox():
    """Update the list box with all files found in the folder"""

    global files

    updateFilesFound = os.listdir(IMAGES_PATH)
    files = updateFilesFound

    for file in files:

        # regular expression to replace spaces to underlines and remove any digits.
        fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

        if (
            file.endswith(".png")
            or file.endswith(".jpg")
            or file.endswith(".jpeg")
            or file.endswith(".gif")
        ):
            # rename all files to replace spaces to underlines.
            os.rename(
                os.path.join(folderImgs, file),
                # os.path.join(folderImgs, f"{random.choice(phoneticAlphabet)}"+fileName),
                os.path.join(folderImgs, fileName),
            )
            list_items.delete(0, END)
            list_items.insert(END, fileName)
            print(f"Found valid images in {folderImgs} with {file}.")

        if file.endswith(".webp") and "Optimized" not in file:
            NovemberfileName = file.replace(".webp", "")

            OscarfileName = re.sub(r"\_[_][_]|\_|\_[_]", " ", NovemberfileName)
            OscarfileName = re.sub(r"^\s+|\s+$", "", OscarfileName)

            print(f"Renaming {file} to {OscarfileName}")

            if OscarfileName == " " or OscarfileName == "":
                os.rename(
                    f"{folderImgs}/{file}",
                    f"{folderImgs}/Optimized {len(OscarfileName)}.webp",
                )
            else:
                os.rename(
                    f"{folderImgs}/{file}",
                    f"{folderImgs}/Optimized {OscarfileName}.webp",
                )
            
            list_items.delete(0, END)
            list_items.insert(END, OscarfileName)


# =========== 🧬 Optimization Functions ===========


def optimizationFunction():
    """Optimization function to reduce the resolution of the images and remove images bloatware."""

    global reduceByHalf
    global files

    print(f"These are all of the files in our current working directory: {files}")
    confirmDownRes = IntVar()
    confirmDownRes = reduceByHalf.get()

    updateListbox()

    for file in files:

        fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

        if (
            file.endswith(".png")
            or file.endswith(".jpg")
            or file.endswith(".jpeg")
            or file.endswith(".gif")
        ):

            print(f"Renamed {file} to {fileName}")
            # Backup operation
            shutil.copy(
                f"{folderImgs}/{fileName}",
                f"{folderImgs}/backup/_backup_{fileName}"
            )
            print(f"Copying {fileName} to backup folder")

            print(f"Optimizing {fileName}")

            imgOptimize = Image.open(relative_to_images(str(fileName)))
            imgWidth, imgHeight = imgOptimize.size
            print(f"Image size: {imgWidth} x {imgHeight}")
            print(f"The state of resolution option is: {confirmDownRes}")

            list_items.delete(0, END)
            list_items.insert(END, fileName)

            # If confirmDownRes = 1, imgWidth and imgHeight are larger than 1366x768 reduce the resolution by half.
            if (
                (imgWidth > 1366 and imgHeight > 768)
                or (imgWidth > 1400 and imgHeight > 1400)
                and confirmDownRes == 1
            ):
                imgOptimize = imgOptimize.resize(
                    (int(imgWidth / 2), int(imgHeight / 2)), PIL.Image.ANTIALIAS
                )
                print(f"Reducing image resolution by half of {fileName}")
                print(f"Optimized {fileName}")

                if file.endswith(".png"):
                    imgOptimize.save(
                        str(relative_to_images(str(fileName))),
                        optimize=True,
                        quality=70,
                    )
                if (
                    file.endswith(".jpg")
                    or file.endswith(".jpeg")
                    or file.endswith(".gif")
                ):
                    imgOptimize.save(
                        str(relative_to_images(str(fileName))),
                        optimize=True,
                        quality=80,
                    )

            # If user don't want to reduce image resolution by half.
            else:
                print(
                    f"Image: {fileName}, is not larger enough to reduce resolution."
                )

                print(f"Performing standard optimization on {fileName}")
                if fileName.endswith(".png"):
                    imgOptimize.save(
                        str(relative_to_images(str(fileName))),
                        optimize=True,
                        quality=70,
                    )

                if (
                    fileName.endswith(".jpg")
                    or fileName.endswith(".jpeg")
                    or fileName.endswith(".gif")
                ):
                    imgOptimize.save(
                        str(relative_to_images(str(fileName))),
                        optimize=True,
                        quality=80,
                    )

            print(f"{fileName} optimized!")

        else:
            print(
                f"No valid files found in {folderImgs} with {fileName}... Checking again."
            )

    convertionFunction()
    updateListbox()


# =========== 🎭 Convertion Functions ===========


def convertionFunction():
    """Convert all images to webp format."""

    print(f"These are all of the files in our current working directory: {files}")

    for file in files:

        fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

        if (
            fileName.endswith(".png")
            or fileName.endswith(".jpg")
            or fileName.endswith(".jpeg")
            or fileName.endswith(".gif")
        ):
            print(f"Converting {fileName} to WebP")
            loadImg = Image.open(relative_to_images(str(fileName)))

            # remove ".png", ".jpg", ".jpeg", ".gif" from fileName
            if fileName.endswith(".png"):
                DeltafileName = fileName.replace(".png", "")
            elif fileName.endswith(".jpg"):
                DeltafileName = fileName.replace(".jpg", "")
            elif fileName.endswith(".jpeg"):
                DeltafileName = fileName.replace(".jpeg", "")
            elif fileName.endswith(".gif"):
                DeltafileName = fileName.replace(".gif", "")

            loadImg.save(
                str(relative_to_images(str(DeltafileName))) + ".webp",
                "WEBP",
                quality=80,
            )
            print(f"{fileName} converted to WebP")

        else:
            print(f"{fileName} is not a eligible, skipping...")

    # Show a message window with "Optimization and conversion completed!"
    cleaningRoutine()
    subprocess.Popen(["open", "-R", folderImgs])
    messagebox.showinfo(
        title="Optimization and conversion completed! \n",
        message="All files have been optimized and converted to WebP!",
        icon="info",
    )


if __name__ == "__main__":
    rootWindow.mainloop()
