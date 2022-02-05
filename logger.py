"""Logger module made for quick logging and troubleshooting Python programs."""
import pathlib
import os
import time
import json
from pathlib import Path

OUTPUT_PATH = pathlib.Path(__file__).parent.absolute()
LOGS_PATH = OUTPUT_PATH / Path("./logs")

# load "version.json", get the "currentVersion" and store inside a variable called "currentVersion".
with open(f"{OUTPUT_PATH}/version.json", "r") as version_file:
    version_data = json.load(version_file)
    currentVersion = version_data["currentVersion"]


def relative_to_logs(path: str) -> Path:
    """Return a path relative to the logs folder."""
    return LOGS_PATH / Path(path)

# check if logs folder exists, if not, create it.
if not LOGS_PATH.exists():
    LOGS_PATH.mkdir()

logRoutineSwitch = True
debugMode = True

class nickLogger:
    """Logger class to be imported as a simple object"""

    def logRoutineController(debugModeC: bool = True, logRoutineC: bool = True):
        """Enable/Disable the logRoutine function."""
        global logRoutineSwitch
        global debugMode
        logRoutineSwitch = logRoutineC
        debugMode = debugModeC

    def logRoutine(log: str, timeNeeded: bool = True):
        """Write strings to the log file and if debug is enabled, print it to console."""

        if timeNeeded is None:
            timeNeeded = True

        currentTime = time.strftime("%m-%d-%Y -> %H:%M:%S")
        logHeader = f"""{currentVersion}
===================================================
            LOG FILE MADE FOR DEBUG PURPOSES
        made by Nicolas Mendes - September 2021
===================================================\n
"""

        # Check if "ioc.log" exists, if not create this file.
        if not os.path.exists(relative_to_logs("ioc.log")):
            open(f"{relative_to_logs('ioc.log')}", "w+")
            # append logHeader to the file.
            with open(f"{relative_to_logs('ioc.log')}", "a") as logFile:
                logFile.write(logHeader)

        # if the first line of ioc.log is different from currentVersion
        with open(f"{relative_to_logs('ioc.log')}") as checkVer:
            firstlineVer = checkVer.readline().rstrip()
            if firstlineVer != currentVersion:
                if firstlineVer == "" or firstlineVer == " ":
                    with open(f"{relative_to_logs('ioc.log')}", "w+") as logFile:
                        logFile.write(logHeader)
                        logFile.write(
                            "\n\n[NOTICE] Log file has been deleted or cleaned.\n"
                        )
                else:
                    # Delete everything inside the file and append logHeader.
                    with open(f"{relative_to_logs('ioc.log')}", "w+") as logFile:
                        logFile.write(logHeader)
                        logFile.write(
                            f"\n\n[NOTICE] IOC HAS BEEN UPDATED TO {currentVersion}!\n"
                        )

        # if the file exceeds 1000 lines, delete everything and append logHeader to the file.
        with open(f"{relative_to_logs('ioc.log')}", "r") as logFile:
            if len(logFile.readlines()) > 1000:
                with open(f"{relative_to_logs('ioc.log')}", "w") as logFile:
                    logFile.write(logHeader)

        if logRoutineSwitch == True:
            # Append the log to the file.
            if timeNeeded == True:
                with open(f"{relative_to_logs('ioc.log')}", "a") as logFile:
                    logFile.write(f"{currentTime} - {log}\n")
            else:
                with open(f"{relative_to_logs('ioc.log')}", "a") as logFile:
                    logFile.write(f"{log}\n")

        if debugMode == True:
            return print(f"DEBUG LOG: {log}")
