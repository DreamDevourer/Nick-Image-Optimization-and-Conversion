r"""Logger module made for quick logging and troubleshooting Python programs by Nicolas Mendes
Based on https://github.com/DreamDevourer/Python-Fundamentals-Study
"""

import pathlib, os, time, json
from pathlib import Path

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
LOGS_PATH = OUTPUT_PATH / Path("./logs")

# load "version.json", get the "current_version" and store inside a variable called "current_version".
with open(f"{OUTPUT_PATH}/version.json", "r") as version_file:
    version_data = json.load(version_file)
    current_version = version_data["currentVersion"]


def relative_to_logs(path: str) -> Path:
    """Return a path relative to the logs folder."""
    return LOGS_PATH / Path(path)


# check if logs folder exists, if not, create it.
if not LOGS_PATH.exists():
    LOGS_PATH.mkdir()

log_routine_switch = True
debug_mode = True


class nick_logger:
    """Logger class to be imported as a simple object"""

    def log_routine_controller(debug_Mode_C: bool = True, log_routine_C: bool = True):
        """Enable/Disable the log_routine function. Defaults: debug_Mode_C = True, log_routine_C = True"""
        global log_routine_switch
        global debug_mode
        log_routine_switch = log_routine_C
        debug_mode = debug_Mode_C

    def log_routine(log: str, time_needed: bool = True):
        """Write strings to the log file and if debug is enabled, print it to console. ARGS: log, time_needed = True"""

        if time_needed is None:
            time_needed = True

        current_time = time.strftime("%m-%d-%Y -> %H:%M:%S")
        log_header = f"""{current_version}
===================================================
            LOG FILE MADE FOR DEBUG PURPOSES
        made by Nicolas Mendes - September 2021
===================================================\n
"""

        # Check if "ioc.log" exists, if not create this file.
        if not os.path.exists(relative_to_logs("ioc.log")):
            open(f"{relative_to_logs('ioc.log')}", "w+")
            # append log_header to the file.
            with open(f"{relative_to_logs('ioc.log')}", "a") as log_file:
                log_file.write(log_header)

        # if the first line of ioc.log is different from current_version
        with open(f"{relative_to_logs('ioc.log')}") as check_ver:
            first_line_ver = check_ver.readline().rstrip()
            if first_line_ver != current_version:
                if first_line_ver == "" or first_line_ver == " ":
                    with open(f"{relative_to_logs('ioc.log')}", "w+") as log_file:
                        log_file.write(log_header)
                        log_file.write(
                            "\n\n[NOTICE] Log file has been deleted or cleaned.\n"
                        )
                else:
                    # Delete everything inside the file and append log_header.
                    with open(f"{relative_to_logs('ioc.log')}", "w+") as log_file:
                        log_file.write(log_header)
                        log_file.write(
                            f"\n\n[NOTICE] IOC HAS BEEN UPDATED TO {current_version}!\n"
                        )

        # if the file exceeds 1000 lines, delete everything and append log_header to the file.
        with open(f"{relative_to_logs('ioc.log')}", "r") as log_file:
            if len(log_file.readlines()) > 1000:
                with open(f"{relative_to_logs('ioc.log')}", "w") as log_file:
                    log_file.write(log_header)

        if log_routine_switch == True:
            # Append the log to the file.
            if time_needed == True:
                with open(f"{relative_to_logs('ioc.log')}", "a") as log_file:
                    log_file.write(f"{current_time} - {log}\n")
            else:
                with open(f"{relative_to_logs('ioc.log')}", "a") as log_file:
                    log_file.write(f"{log}\n")

        if debug_mode == True:
            return print(f"DEBUG LOG: {log}")
