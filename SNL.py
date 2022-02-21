r"""Standard Nick Logger module made for quick logging and troubleshooting Python programs by Nicolas Mendes
Based on https://github.com/DreamDevourer/Python-Fundamentals-Study
"""

# 🧶 Modules Imports
import pathlib, os, time, json, platform, base64, re, random
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
__SNL_version__ = "v1.0.5"

program_ver = ""

# ✍️ Initial Setup to load assets

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
LOGS_PATH = OUTPUT_PATH / Path("./Resources/logs")
VERSION_PATH = OUTPUT_PATH / Path("./Resources/tmp/verinfo.bin")
VERSION_PATH_RAW = OUTPUT_PATH / Path("./Resources")

def relative_to_ver(path: str) -> Path:
    """Return a path relative to the logs folder."""
    return VERSION_PATH_RAW / Path(path)


def version_handler():
    SOFTWARE_VER = f"""{{ 'currentVersion': '{program_ver}' }}"""
    OBFUSCATED_VER = base64.b64encode(SOFTWARE_VER.encode("utf-8"))

    # Create a file called verinfo.bin inside the ./Resources folder
    if not os.path.exists(relative_to_ver("tmp")):
        os.makedirs(relative_to_ver("tmp"))
        # Write SOFTWARE_VER to verinfo.bin
        with open(relative_to_ver("verinfo.bin"), "w") as f:
            f.write(OBFUSCATED_VER)


def encryptSecurity():
    """Encrypt the version file"""
    KEY = "MjI0"  # up 255
    KEY = base64.b64decode(KEY)
    cleanKey = re.sub(r"[^A-Za-z0-9-]", "", KEY.decode("utf-8"))
    finalKey = int(cleanKey)

    loadEnc00 = open(relative_to_ver("./tmp/verinfo.bin"), "rb")
    byteReaderData = loadEnc00.read()
    loadEnc00.close()

    byteReaderData = bytearray(byteReaderData)
    for index, value in enumerate(byteReaderData):
        byteReaderData[index] = value ^ finalKey

    Enc = open(relative_to_ver("verinfo.bin"), "wb")
    Enc.write(byteReaderData)
    Enc.close()

    os.remove(relative_to_ver("./tmp/verinfo.bin"))


def decryptSecurity():
    """Decrypt the version file"""
    KEY = "MjI0"  # up 255
    KEY = base64.b64decode(KEY)
    cleanKey = re.sub(r"[^A-Za-z0-9-]", "", KEY.decode("utf-8"))
    finalKey = int(cleanKey)

    loadEnc00 = open(relative_to_ver("verinfo.bin"), "rb").read()

    byteReader = bytearray(loadEnc00)
    for index, value in enumerate(byteReader):
        byteReader[index] = value ^ finalKey

    decEnc = open(relative_to_ver("./tmp/verinfo.bin"), "wb")
    decEnc.write(byteReader)


decryptSecurity()

with open(f"{VERSION_PATH}", "r+") as version_file:
    version_data = json.load(version_file)

    if (
        (version_data is None)
        or (version_data == "")
        or ("currentVersion" not in version_data)
    ):
        version_file.write(json.dumps({"currentVersion": "v1.0.0 - Release"}))

    current_version = version_data["currentVersion"]
    version_file.close()
    encryptSecurity()


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
get_timestamp = None
OS_Detector = None
current_time = time.strftime("%m-%d-%Y -> %H:%M:%S")

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
        program_version: str = "v1.0.0 - Release",
    ):
        """Control Log Routine main function. Defaults: debug_Mode_C = True, log_routine_C = True, file_name = 'logs', max_lines = 1000, show_pid = True, show_timestamp = True, track_platform = True, program_version = 'v1.0.0 - Release' """
        global log_routine_switch
        global debug_mode
        global file_log_name
        global max_lines_allowed
        global Pid
        global get_timestamp
        global OS_Detector
        global program_ver

        log_routine_switch = log_routine_C
        debug_mode = debug_Mode_C
        file_log_name = file_name
        max_lines_allowed = max_lines
        program_ver = program_version

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

        version_handler()

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
                   Standard Nick Logger
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
                log_file.close()

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
                        log_file.close()
                else:
                    # Delete everything inside the file and append log_header.
                    with open(
                        f"{relative_to_logs(f'{file_log_name}.log')}", "w+"
                    ) as log_file:
                        log_file.write(log_header)
                        log_file.write(
                            f"\n\n[NOTICE] PROGRAM HAS BEEN UPDATED TO {current_version}!\n"
                        )
                        log_file.close()

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
    exit()
