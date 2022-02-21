r"""Logger module made for quick logging and troubleshooting Python programs by Nicolas Mendes
Based on https://github.com/DreamDevourer/Python-Fundamentals-Study
"""

# 🧶 Modules Imports
import pathlib, os, time, json, platform, base64, re
from pathlib import Path

""" Made by Nicolas Mendes - Feb 2022
SUMMARY:

🧶 Modules Imports
✍️ Initial Setup to load assets
🔖 Main class
⚙️ Logic and Defs
=========== ✍️ Module controller
=========== 📖 Main log function

"""

__copyright__ = """

    Standard Nick Logger (SNL) - Copyright (c) 2021-2022, Nicolas Mendes; mailto:nicolasmendes_developer@outlook.com

    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose and without fee or royalty is hereby granted,
    provided that the above copyright notice appear in all copies and that
    both that copyright notice and this permission notice appear in
    supporting documentation or portions thereof, including modifications,
    that you make.

"""

# ✍️ Initial Setup to load assets

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
LOGS_PATH = OUTPUT_PATH / Path("./logs")
VERSION_PATH = OUTPUT_PATH / Path("version.json")

# load "version.json", get the "current_version" and store inside a variable called "current_version".
# if the file does not exist, create it and append: '{ "currentVersion": "v1.0.0 - Release" }'
if not VERSION_PATH.exists():
    with open(f"{VERSION_PATH}", "w") as version_file:
        version_file.write(json.dumps({"currentVersion": "v1.0.0 - Release"}))

with open(f"{VERSION_PATH}", "r+") as version_file:
    version_data = json.load(version_file)
    
    if (
        (version_data is None)
        or (version_data == "")
        or ("currentVersion" not in version_data)
    ):
        version_file.write(json.dumps({"currentVersion": "v1.0.0 - Release"}))

    current_version = version_data["currentVersion"]


def relative_to_logs(path: str) -> Path:
    """Return a path relative to the logs folder."""
    return LOGS_PATH / Path(path)


# check if logs folder exists, if not, create it.
if not LOGS_PATH.exists():
    LOGS_PATH.mkdir()

log_routine_switch = None
debug_mode = None
file_log_name = None
max_lines_allowed = None
Pid = None
current_time = time.strftime("%m-%d-%Y -> %H:%M:%S")
get_timestamp = None
OS_Detector = None

# 🔖 Main class
class nick_logger:
    """Logger class to be imported as a simple object"""

    # ⚙️ Logic and Defs

    # ✍️ Module controller

    def log_routine_controller(
        debug_Mode_C: bool = True,
        log_routine_C: bool = True,
        file_name: str = "logs",
        max_lines: int = 1000,
        show_pid: bool = True,
        show_timestamp: bool = True,
        track_platform: bool = True,
    ):
        """Control Log Routine main function. Defaults: debug_Mode_C = True, log_routine_C = True, file_name = "logs", max_lines = 1000, show_pid = True, show_timestamp = True, track_platform = True"""
        global log_routine_switch
        global debug_mode
        global file_log_name
        global max_lines_allowed
        global Pid
        global get_timestamp
        global OS_Detector

        log_routine_switch = log_routine_C
        debug_mode = debug_Mode_C
        file_log_name = file_name
        max_lines_allowed = max_lines

        if show_pid:
            Pid = os.getpid()
        else:
            Pid = ""

        if show_timestamp:
            get_timestamp = time.time()
        else:
            get_timestamp = ""

        if track_platform:
            OS_Detector = platform.system()
        else:
            OS_Detector = ""

    def log_os_details(
        log_message: str = f"\n\n[OK] ===> Python loaded on {OS_Detector}. Starting new instance at PID: {Pid} | UTS: {get_timestamp}\n",
    ):
        """Logs OS details"""

        if Pid != "" and get_timestamp != "" and OS_Detector != "":
            os_log_det = f"\n\n[OK] ===> Python loaded on {OS_Detector}. Starting new instance at PID: {Pid} | UTS: {get_timestamp}\n"
            return os_log_det

    # 📖 Main log function
    def log_routine(log: str, time_needed: bool = True, hide_pid: bool = True):
        """Write strings to the log file and if debug is enabled, print it to console. ARGS: log, time_needed = True"""

        global current_time

        if time_needed is None:
            time_needed = True

        log_header = f"""{current_version}
===================================================
                            SNL
            LOG FILE MADE FOR DEBUG PURPOSES
        made by Nicolas Mendes - September 2021
===================================================\n
"""

        # Check if "{file_log_name}.log" exists, if not create this file.
        if not os.path.exists(relative_to_logs(f"{file_log_name}.log")):
            open(f"{relative_to_logs(f'{file_log_name}.log')}", "w+")
            # append log_header to the file.
            with open(f"{relative_to_logs(f'{file_log_name}.log')}", "a") as log_file:
                log_file.write(log_header)

        # if the first line of {file_log_name}.log is different from current_version
        with open(f"{relative_to_logs(f'{file_log_name}.log')}") as check_ver:
            first_line_ver = check_ver.readline().rstrip()
            if first_line_ver != current_version:
                if first_line_ver == "" or first_line_ver == " ":
                    with open(
                        f"{relative_to_logs(f'{file_log_name}.log')}", "w+"
                    ) as log_file:
                        log_file.write(log_header)
                        log_file.write(
                            "\n\n[NOTICE] Log file has been deleted or cleaned.\n"
                        )
                else:
                    # Delete everything inside the file and append log_header.
                    with open(
                        f"{relative_to_logs(f'{file_log_name}.log')}", "w+"
                    ) as log_file:
                        log_file.write(log_header)
                        log_file.write(
                            f"\n\n[NOTICE] PROGRAM HAS BEEN UPDATED TO {current_version}!\n"
                        )

        # if the file exceeds 1000 lines, delete everything and append log_header to the file.
        with open(f"{relative_to_logs(f'{file_log_name}.log')}", "r") as log_file:
            if len(log_file.readlines()) > max_lines_allowed:
                with open(
                    f"{relative_to_logs(f'{file_log_name}.log')}", "w"
                ) as log_file:
                    log_file.write(log_header)

        if log_routine_switch == True:
            # Append the log to the file.
            if time_needed == True and (Pid != "") and (hide_pid == False):
                with open(
                    f"{relative_to_logs(f'{file_log_name}.log')}", "a"
                ) as log_file:
                    log_file.write(f"{current_time} | PID {Pid} - {log}\n")
            elif (time_needed == True) and (Pid == "") and (hide_pid == True):
                with open(
                    f"{relative_to_logs(f'{file_log_name}.log')}", "a"
                ) as log_file:
                    log_file.write(f"{current_time} - {log}\n")
            else:
                with open(
                    f"{relative_to_logs(f'{file_log_name}.log')}", "a"
                ) as log_file:
                    log_file.write(f"{log}\n")

        if debug_mode == True:
            return print(f"DEBUG LOG: {log}")


if __name__ == "__main__":
    print(__copyright__)
