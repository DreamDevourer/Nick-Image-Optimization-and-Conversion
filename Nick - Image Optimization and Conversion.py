#!/usr/bin/env python3
# 🧶 Modules Imports
# Try following pep8 (https://pep8.org/) and try using "black" as the default formatter.
# In this case, use Snake case with the first letter of each word capitalized.
import re
import os
import time
import pathlib
import subprocess
import shutil
import PIL
import tkinter as tkCore
from PIL import Image
from pathlib import Path
from logger import nick_logger as nick_log
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

🧶 Modules Imports
✍️ Initial Setup to load assets
🧝🏻‍♀️ Tk Window Settings
💬 Variables
🌈 UI
🔖 Load GUI files defs
⚙️ Logic and Defs
=========== 📜 Check Function
=========== 🧬 Optimization Functions
=========== 🎭 Convertion Functions
🙌 __Main__

"""

# ✍️ Initial Setup to load assets

Pid = os.getpid()
Log_Routine_Controller = nick_log.log_routine_controller(False)

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
Images_PATH = OUTPUT_PATH / Path("./images")


def Get_Timestamp():
    """Return a unix timestamp."""
    return time.time()


def Relative_To_Assets(path: str) -> Path:
    """Return a path relative to the assets folder."""
    nick_log.log_routine(
        f"[WARNING] Assets folder have been accessed.\n|--------------------------------> [OK] {path} has been loaded."
    )
    return ASSETS_PATH / Path(path)


def Relative_To_Images(path: str) -> Path:
    """Return a path relative to the images folder."""
    nick_log.log_routine(
        f"[WARNING] Images folder path have been accessed.\n|--------------------------------> [OK] {path} has been loaded."
    )
    return Images_PATH / Path(path)


nick_log.log_routine(
    f"\n\n[OK] ===> Python loaded. Starting new instance at PID: {Pid} | UTS: {Get_Timestamp()}\n",
    False,
)

try:

    # 🧝🏻‍♀️ Tk Window Settings
    Root_Window = Tk()
    Root_Window.resizable(False, False)
    Root_Window.geometry("980x580")
    Root_Window.configure(bg="#FFFFFF")
    Root_Window.title("Nick - Image Optimization and Conversion")
    Root_Window.iconbitmap(Relative_To_Assets("icon.ico"))

    # 💬 Variables

    files = os.listdir(Images_PATH)
    Printable_Files = Images_PATH

    # 🌈 UI
    canvas = Canvas(
        Root_Window,
        bg="#FFFFFF",
        height=580,
        width=980,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )

    # Buttons and Labels
    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(file=Relative_To_Assets("image_1.png"))
    image_1 = canvas.create_image(95.0, 290.0, image=image_image_1)

    # Make magic button ( Aka optimizing and conversion functions )
    button_image_1 = PhotoImage(file=Relative_To_Assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: optimizationFunction(),
        relief="flat",
    )
    button_1.place(x=28.0, y=502.0, width=135.0, height=46.0)

    image_image_2 = PhotoImage(file=Relative_To_Assets("image_2.png"))
    image_2 = canvas.create_image(577.0, 348.0, image=image_image_2)

    image_image_3 = PhotoImage(file=Relative_To_Assets("image_3.png"))
    image_3 = canvas.create_image(577.0, 64.0, image=image_image_3)

    # Browse Button ( Aka selecting files )
    button_image_2 = PhotoImage(file=Relative_To_Assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: Load_Folder_For_Img(),
        relief="flat",
    )
    button_2.place(x=812.0, y=41.0, width=135.0, height=46.0)

    # 🔖 Load GUI files defs

    def Load_Folder_For_Img():
        """Load the folder with images"""

        global Images_PATH
        global entry_DefPath
        global files
        global Printable_Files

        # open dialog box to select folder
        Printable_Files = askdirectory(initialdir=Images_PATH)

        # If the user cancel it will fallback to the default folder.
        if Printable_Files == "" or Printable_Files == " ":
            Printable_Files = Images_PATH
            entry_DefPath.set(str(Images_PATH))
        else:
            entry_DefPath.set(str(Printable_Files))

        # Regular expression to pick all words after the last "/".
        # Folder_Imgs = re.findall(r"[^\\\/]+$", Printable_Files)
        nick_log.log_routine(
            f"inside loadFolderForImg: {Printable_Files}, {entry_DefPath.get()} and {entry_1.get()}"
        )
        Images_PATH = Path(f"{Printable_Files}")
        files = os.listdir(Images_PATH)
        Quick_Update_List()

    # Entry to load files
    entry_DefPath = StringVar()
    entry_DefPath.set(str(Images_PATH))
    entry_image_1 = PhotoImage(file=Relative_To_Assets("entry_1.png"))
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

    # Listbox to show files loaded Root_Window
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

    image_image_4 = PhotoImage(file=Relative_To_Assets("image_4.png"))
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
    Reduce_By_Half = IntVar()
    Reduce_By_HalfChck = Checkbutton(
        text="Smart Scale Mode",
        variable=Reduce_By_Half,
        bg="#AC59F3",
        fg="#FFFFFF",
        font=("Mulish Regular", 13 * -1),
    )
    Reduce_By_HalfChck.deselect()
    Reduce_By_HalfChck.place(relx=0.03, rely=0.7, anchor="nw")

    # Logo Icon
    image_image_6 = PhotoImage(file=Relative_To_Assets("image_6.png"))
    image_6 = canvas.create_image(95.0, 64.0, image=image_image_6)

    # ⚙️ Logic and Defs

    """
    Optimization and Convertion Scripts forked from my Python Fundamentals Study GitHub repository.
    Forked on September 23, 2021.
    https://github.com/DreamDevourer/Python-Fundamentals-Study
    """

    def Cleaning_Routine():
        """Removes any legacy image"""

        nick_log.log_routine("Beginning cleaning routine")

        for file in files:
            File_Name = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                File_Name.endswith(".png")
                or File_Name.endswith(".jpg")
                or File_Name.endswith(".jpeg")
                or File_Name.endswith(".gif")
            ):
                # Delete original file
                nick_log.log_routine(f"Deleting {File_Name}")
                os.remove(f"{Folder_Imgs}/{File_Name}")

    # =========== 📜 Check Function ===========

    Folder_Imgs = entry_1.get()

    def Quick_Update_List():
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

    def Scheduler_Controller():
        """Function to execute tasks in X ms."""
        Quick_Update_List()
        Root_Window.after(2000, Scheduler_Controller)

    def Update_Listbox():
        """Update the list box with all files found in the folder"""

        global files
        global Folder_Imgs

        Folder_Imgs = entry_1.get()

        # check if backup folder exists inside images folder
        if not os.path.exists(f"{Folder_Imgs}/backup"):
            os.mkdir(f"{Folder_Imgs}/backup")
            nick_log.log_routine("[OK] Backup folder created.")

        Update_Files_Found = os.listdir(Images_PATH)
        files = Update_Files_Found

        list_items.delete(0, END)
        for file in files:

            # regular expression to replace spaces to underlines and remove any digits.
            File_Name = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".gif")
            ):
                # rename all files to replace spaces to underlines.
                os.rename(
                    os.path.join(Folder_Imgs, file),
                    os.path.join(Folder_Imgs, File_Name),
                )
                list_items.insert(END, File_Name)
                nick_log.log_routine(
                    f"[OK] Found valid images in {Folder_Imgs} with {file}."
                )

            if file.endswith(".webp") and "Optimized" not in file:
                November_File_Name = file.replace(".webp", "")

                Oscar_File_Name = re.sub(r"\_[_][_]|\_|\_[_]", " ", November_File_Name)
                Oscar_File_Name = re.sub(r"^\s+|\s+$", "", Oscar_File_Name)

                nick_log.log_routine(f"Renaming {file} to {Oscar_File_Name}")

                if Oscar_File_Name == " " or Oscar_File_Name == "":
                    os.rename(
                        f"{Folder_Imgs}/{file}",
                        f"{Folder_Imgs}/Optimized {len(Oscar_File_Name)}.webp",
                    )
                else:
                    os.rename(
                        f"{Folder_Imgs}/{file}",
                        f"{Folder_Imgs}/Optimized {Oscar_File_Name}.webp",
                    )

                Quick_Update_List()

    # =========== 🧬 Optimization Functions ===========

    def optimizationFunction():
        """Optimization function to reduce the resolution of the images and remove images bloatware."""

        global Reduce_By_Half
        global files

        nick_log.log_routine(
            f"These are all of the files in our current working directory: {files}"
        )
        Confirm_Down_Res = IntVar()
        Confirm_Down_Res = Reduce_By_Half.get()

        # check if backup folder exists inside images folder
        if not os.path.exists(f"{Folder_Imgs}/backup"):
            os.mkdir(f"{Folder_Imgs}/backup")
            nick_log.log_routine("[OK] Backup folder created.")

        Update_Listbox()

        for file in files:

            File_Name = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".gif")
            ):

                nick_log.log_routine(f"[OK] Renamed {file} to {File_Name}")
                # Backup operation
                shutil.copy(
                    f"{Folder_Imgs}/{File_Name}",
                    f"{Folder_Imgs}/backup/_backup_{File_Name}",
                )
                nick_log.log_routine(f"Copying {File_Name} to backup folder")

                nick_log.log_routine(f"Optimizing {File_Name}")

                Img_Optimize = Image.open(Relative_To_Images(str(File_Name)))
                imgWidth, imgHeight = Img_Optimize.size
                nick_log.log_routine(f"Image size: {imgWidth} x {imgHeight}")
                nick_log.log_routine(
                    f"The state of resolution option is: {Confirm_Down_Res}"
                )

                list_items.delete(0, END)
                list_items.insert(END, File_Name)

                # If Confirm_Down_Res = 1, imgWidth and imgHeight are larger than 1366x768 reduce the resolution by half.
                if (
                    (imgWidth > 1366 and imgHeight > 768)
                    or (imgWidth > 1400 and imgHeight > 1400)
                    and Confirm_Down_Res == 1
                ):
                    Img_Optimize = Img_Optimize.resize(
                        (int(imgWidth / 2), int(imgHeight / 2)), PIL.Image.ANTIALIAS
                    )
                    nick_log.log_routine(f"Reducing image resolution by half of {File_Name}")
                    nick_log.log_routine(f"[OK] Optimized {File_Name}")

                    if file.endswith(".png"):
                        Img_Optimize.save(
                            str(Relative_To_Images(str(File_Name))),
                            optimize=True,
                            quality=70,
                        )
                    if (
                        file.endswith(".jpg")
                        or file.endswith(".jpeg")
                        or file.endswith(".gif")
                    ):
                        Img_Optimize.save(
                            str(Relative_To_Images(str(File_Name))),
                            optimize=True,
                            quality=80,
                        )

                # If user don't want to reduce image resolution by half.
                else:
                    nick_log.log_routine(
                        f"Image: {File_Name}, is not larger enough to reduce resolution."
                    )

                    nick_log.log_routine(f"Performing standard optimization on {File_Name}")
                    if File_Name.endswith(".png"):
                        Img_Optimize.save(
                            str(Relative_To_Images(str(File_Name))),
                            optimize=True,
                            quality=70,
                        )

                    if (
                        File_Name.endswith(".jpg")
                        or File_Name.endswith(".jpeg")
                        or File_Name.endswith(".gif")
                    ):
                        Img_Optimize.save(
                            str(Relative_To_Images(str(File_Name))),
                            optimize=True,
                            quality=80,
                        )

                nick_log.log_routine(f"[OK] {File_Name} optimized!")

            else:
                nick_log.log_routine(
                    f"No valid files found in {Folder_Imgs} with {File_Name}... Checking again."
                )

        Convertion_Function()
        Update_Listbox()

    # =========== 🎭 Convertion Functions ===========

    def Convertion_Function():
        """Convert all images to webp format."""

        nick_log.log_routine(
            f"These are all of the files in our current working directory: {files}"
        )

        for file in files:

            File_Name = re.sub(r"\s+|\d|\(|\)", "_", file)

            if (
                File_Name.endswith(".png")
                or File_Name.endswith(".jpg")
                or File_Name.endswith(".jpeg")
                or File_Name.endswith(".gif")
            ):
                nick_log.log_routine(f"Converting {File_Name} to WebP")
                Load_Img = Image.open(Relative_To_Images(str(File_Name)))

                # remove ".png", ".jpg", ".jpeg", ".gif" from File_Name
                if File_Name.endswith(".png"):
                    Delta_File_Name = File_Name.replace(".png", "")
                elif File_Name.endswith(".jpg"):
                    Delta_File_Name = File_Name.replace(".jpg", "")
                elif File_Name.endswith(".jpeg"):
                    Delta_File_Name = File_Name.replace(".jpeg", "")
                elif File_Name.endswith(".gif"):
                    Delta_File_Name = File_Name.replace(".gif", "")

                Load_Img.save(
                    str(Relative_To_Images(str(Delta_File_Name))) + ".webp",
                    "WEBP",
                    quality=80,
                )
                nick_log.log_routine(f"[OK] {File_Name} converted to WebP")

            else:
                nick_log.log_routine(f"{File_Name} is not a eligible, skipping...")

        # Show a message window with "Optimization and conversion completed!"
        Cleaning_Routine()
        subprocess.Popen(["open", "-R", Folder_Imgs])
        messagebox.showinfo(
            title="Optimization and conversion completed! \n",
            message="All files have been optimized and converted to WebP!",
            icon="info",
        )
        nick_log.log_routine("[OK] Images optimized! Starting to update list.")
        Quick_Update_List()

except (
    RuntimeError,
    TypeError,
    NameError,
    FileNotFoundError,
    OSError,
    tkCore.TclError,
    AttributeError,
) as eM:
    nick_log.log_routine(f"[X] ERROR: {eM}", False)
    messagebox.showerror(
        title="Error",
        message="Check the log for details.",
        icon="error",
    )

except Exception as eFatal:
    nick_log.log_routine(f"[X] FATAL ERROR: {eFatal}")

except:
    nick_log.log_routine("[X] FATAL ERROR: Unknown error!")

# 🙌 __Main__
if __name__ == "__main__":
    nick_log.log_routine("[OK] IOC has started!\n===========PROGRAM INITIATED===========\n")
    Root_Window.after(500, Scheduler_Controller)
    Root_Window.mainloop()
