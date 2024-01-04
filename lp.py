#!/usr/bin/env python3

import platform
import requests
import subprocess
import sys


# Define command execution function
def exec_cmd(command):
    try:
        return subprocess.run(command.split()).returncode
    except Exception as e:
        print(e)
        return -1


# Define check if cmd exists function
# def command_exists(command):
#     try:
#         subprocess.check_output(["which", command])
#         return True
#     except subprocess.CalledProcessError:
#         return False


# Define fetch json file function
def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[WARN] Error fetching JSON data: {e}, Now exiting.")
        exit(1)


def main():  # Define main function
    if platform.system() != "Linux":  # Check if running on Linux, if not, exit.
        print("[WARN] lp can only be run on linux-based systems. Now exiting.")
        exit(1)

    # Check if the correct number of arguments has been defined by the user
    if len(sys.argv) != 2:
        print("[WARN] lp usage: {} [PRESET_URL]".format(sys.argv[0]))
        exit(1)

    # Check value of arg1 and adjust argument parsing
    if any(sys.argv[1] == help_opt for help_opt in ["-h", "--help"]):
        print("Help coming soon idk")
        exit(0)

    # Extract the arguments
    url = sys.argv[1]

    # Extract values list
    values_list = list(fetch_json_data(url).values())

    print(
        f"[INFO] Selected Preset: {values_list}\n"
        "[INFO] Some presets require root. Errors may occur if lp is not run as root"
    )
    continueBoolean = input("Would you like to continue? [y/n]")
    if not any(continueBoolean == y for y in ["y", "Y"]):
        print(f"[WARN] {continueBoolean} was selected. Aborting preset and exiting.")
        exit(0)

    print("[INFO] This may take some time depending on the preset. Please wait")
    for cmd in values_list:
        print(f"{cmd!r} running...")
        status = exec_cmd(cmd)
        if status != 0:
            print(f"[WARN] cmd {cmd!r} failed. Exit status {status}")
    print("[INFO] lp has finished running the preset. Now exiting.")


if __name__ == "__main__":
    main()
