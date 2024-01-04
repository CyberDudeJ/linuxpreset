#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import platform
import requests
import subprocess


# Define command execution function
def exec_cmd(command: str) -> int:
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


# read preset from local json file
def read_json_data(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        exit(1)


# json validation func
def validate_json_data(data):
    return isinstance(data, list) and all(isinstance(v, str) for v in data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", metavar="PRESET_URL")
    return parser.parse_args()


def main():  # Define main function
    if platform.system() != "Linux":  # Check if running on Linux, if not, exit.
        print("[WARN] lp can only be run on linux-based systems. Now exiting.")
        exit(1)

    args = parse_args()

    # Extract values list
    if Path(args.url).exists():
        values_list = read_json_data(args.url)
    else:
        values_list = fetch_json_data(args.url)

    # Validate data
    if not validate_json_data(values_list):
        print("[WARN] Invalid json format, should be list[str]")
        exit(1)

    print(
        "[INFO] Selected Preset:\n"
        + "\n".join(f"  {v!r}" for v in values_list)
        + "\n[INFO] Some presets require root. Errors may occur if lp is not run as root"
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
