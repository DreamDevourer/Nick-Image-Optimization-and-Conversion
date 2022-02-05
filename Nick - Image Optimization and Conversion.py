#!/usr/bin/env python3
import re
import os
import PIL
import pathlib
import shutil
import subprocess
import time
import tkinter as tkCore
from PIL import Image
from pathlib import Path
from logger import nickLogger as nLog
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

pid = os.getpid()
logRoutineController = nLog.logRoutineController(False, False)

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
Images_PATH = OUTPUT_PATH / Path("./images")


def get_timestamp():
    """Return a unix timestamp."""
    return time.time()


def relative_to_assets(path: str) -> Path:
    """Return a path relative to the assets folder."""
    nLog.logRoutine(
        f"[WARNING] Assets folder have been accessed.\n|--------------------------------> [OK] {path} has been loaded."
    )
    return ASSETS_PATH / Path(path)


def relative_to_images(path: str) -> Path:
    """Return a path relative to the images folder."""
    nLog.logRoutine(
        f"[WARNING] Images folder path have been accessed.\n|--------------------------------> [OK] {path} has been loaded."
    )
    return Images_PATH / Path(path)


nLog.logRoutine(
    f"\n\n[OK] ===> Python loaded. Starting new instance at PID: {pid} | UTS: {get_timestamp()}\n",
    False,
)

try:

    # 🧝🏻‍♀️ Tk Window Settings
    rootWindow = Tk()
    rootWindow.resizable(False, False)
    rootWindow.geometry("980x580")
    rootWindow.configure(bg="#FFFFFF")
    rootWindow.title("Nick - Image Optimization and Conversion")
    rootWindow.iconbitmap(relative_to_assets("icon.ico"))

    # 💬 Variables

    files = os.listdir(Images_PATH)
    printableFiles = Images_PATH

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

        global Images_PATH
        global entry_DefPath
        global files
        global printableFiles

        # open dialog box to select folder
        printableFiles = askdirectory(initialdir=Images_PATH)

        # If the user cancel it will fallback to the default folder.
        if printableFiles == "" or printableFiles == " ":
            printableFiles = Images_PATH
            entry_DefPath.set(str(Images_PATH))
        else:
            entry_DefPath.set(str(printableFiles))

        # Regular expression to pick all words after the last "/".
        # folderImgs = re.findall(r"[^\\\/]+$", printableFiles)
        nLog.logRoutine(
            f"inside loadFolderForImg: {printableFiles}, {entry_DefPath.get()} and {entry_1.get()}"
        )
        Images_PATH = Path(f"{printableFiles}")
        files = os.listdir(Images_PATH)
        quickUpdateList()

    def pickGenUp():
        """Load new folder after browser"""

        global printableFiles
        printableFiles = entry_DefPath.get()

        nLog.logRoutine(f"inside pickGenUp: {printableFiles}")
        return printableFiles

    # Entry to load files
    entry_DefPath = StringVar()
    entry_DefPath.set(str(Images_PATH))
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(567.5, 74.0, image=entry_image_1)
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000000",
        disabledbackground="#FFFFFF",
        disabledforeground="#000000",
        textvariable=entry_DefPath,
        highlightthickness=0,
        state="disabled",
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

        nLog.logRoutine("Beginning cleaning routine")

        for file in files:
            fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                fileName.endswith(".png")
                or fileName.endswith(".jpg")
                or fileName.endswith(".jpeg")
                or fileName.endswith(".gif")
            ):
                # Delete original file
                nLog.logRoutine(f"Deleting {fileName}")
                os.remove(f"{folderImgs}/{fileName}")

    # =========== 📜 Check Function ===========

    folderImgs = entry_1.get()

    def quickUpdateList():
        """Refresh the list quicker."""
        global files

        files = None
        files = os.listdir(Images_PATH)

        time.sleep(0.5)
        list_items.delete(0, END)

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

    def schedulerController():
        """Function to execute tasks in X ms."""
        quickUpdateList()
        rootWindow.after(2000, schedulerController)

    def updateListbox():
        """Update the list box with all files found in the folder"""

        global files
        global folderImgs

        folderImgs = entry_1.get()

        # check if backup folder exists inside images folder
        if not os.path.exists(f"{folderImgs}/backup"):
            os.mkdir(f"{folderImgs}/backup")
            nLog.logRoutine("[OK] Backup folder created.")

        updateFilesFound = os.listdir(Images_PATH)
        files = updateFilesFound

        list_items.delete(0, END)
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
                    os.path.join(folderImgs, fileName),
                )
                list_items.insert(END, fileName)
                nLog.logRoutine(f"[OK] Found valid images in {folderImgs} with {file}.")

            if file.endswith(".webp") and "Optimized" not in file:
                NovemberfileName = file.replace(".webp", "")

                OscarfileName = re.sub(r"\_[_][_]|\_|\_[_]", " ", NovemberfileName)
                OscarfileName = re.sub(r"^\s+|\s+$", "", OscarfileName)

                nLog.logRoutine(f"Renaming {file} to {OscarfileName}")

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

                quickUpdateList()

    # =========== 🧬 Optimization Functions ===========

    def optimizationFunction():
        """Optimization function to reduce the resolution of the images and remove images bloatware."""

        global reduceByHalf
        global files

        nLog.logRoutine(
            f"These are all of the files in our current working directory: {files}"
        )
        confirmDownRes = IntVar()
        confirmDownRes = reduceByHalf.get()

        # check if backup folder exists inside images folder
        if not os.path.exists(f"{folderImgs}/backup"):
            os.mkdir(f"{folderImgs}/backup")
            nLog.logRoutine("[OK] Backup folder created.")

        updateListbox()

        for file in files:

            fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".gif")
            ):

                nLog.logRoutine(f"[OK] Renamed {file} to {fileName}")
                # Backup operation
                shutil.copy(
                    f"{folderImgs}/{fileName}",
                    f"{folderImgs}/backup/_backup_{fileName}",
                )
                nLog.logRoutine(f"Copying {fileName} to backup folder")

                nLog.logRoutine(f"Optimizing {fileName}")

                imgOptimize = Image.open(relative_to_images(str(fileName)))
                imgWidth, imgHeight = imgOptimize.size
                nLog.logRoutine(f"Image size: {imgWidth} x {imgHeight}")
                nLog.logRoutine(f"The state of resolution option is: {confirmDownRes}")

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
                    nLog.logRoutine(f"Reducing image resolution by half of {fileName}")
                    nLog.logRoutine(f"[OK] Optimized {fileName}")

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
                    nLog.logRoutine(
                        f"Image: {fileName}, is not larger enough to reduce resolution."
                    )

                    nLog.logRoutine(f"Performing standard optimization on {fileName}")
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

                nLog.logRoutine(f"[OK] {fileName} optimized!")

            else:
                nLog.logRoutine(
                    f"No valid files found in {folderImgs} with {fileName}... Checking again."
                )

        convertionFunction()
        updateListbox()

    # =========== 🎭 Convertion Functions ===========

    def convertionFunction():
        """Convert all images to webp format."""

        nLog.logRoutine(
            f"These are all of the files in our current working directory: {files}"
        )

        for file in files:

            fileName = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                fileName.endswith(".png")
                or fileName.endswith(".jpg")
                or fileName.endswith(".jpeg")
                or fileName.endswith(".gif")
            ):
                nLog.logRoutine(f"Converting {fileName} to WebP")
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
                nLog.logRoutine(f"[OK] {fileName} converted to WebP")

            else:
                nLog.logRoutine(f"{fileName} is not a eligible, skipping...")

        # Show a message window with "Optimization and conversion completed!"
        cleaningRoutine()
        subprocess.Popen(["open", "-R", folderImgs])
        messagebox.showinfo(
            title="Optimization and conversion completed! \n",
            message="All files have been optimized and converted to WebP!",
            icon="info",
        )
        nLog.logRoutine("[OK] Images optimized! Starting to update list.")
        quickUpdateList()

except (
    RuntimeError,
    TypeError,
    NameError,
    FileNotFoundError,
    OSError,
    tkCore.TclError,
    AttributeError,
) as eM:
    nLog.logRoutine(f"[X] ERROR: {eM}", False)
    messagebox.showerror(
        title="Error",
        message="Check the log for details.",
        icon="error",
    )

except Exception as eFatal:
    nLog.logRoutine(f"[X] FATAL ERROR: {eFatal}")

except:
    nLog.logRoutine("[X] FATAL ERROR: Unknown error!")

if __name__ == "__main__":
    nLog.logRoutine("[OK] IOC has started!\n===========PROGRAM INITIATED===========\n")
    rootWindow.after(500, schedulerController)
    rootWindow.mainloop()
