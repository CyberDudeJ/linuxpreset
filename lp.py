#!/usr/bin/env python3

import argparse
import json
import logging
from pathlib import Path
import sys, requests, subprocess, platform
from typing import Any


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)-.4s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# Define command execution function
def exec_cmd(command: str) -> int:
    try:
        return subprocess.run(command.split()).returncode
    except Exception as e:
        log.error(e)
        return -1


# Define check if cmd exists function
# def command_exists(command):
#     try:
#         subprocess.check_output(["which", command])
#         return True
#     except subprocess.CalledProcessError:
#         return False


# Define fetch json file function
def fetch_json_data(url) -> Any:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error("Error fetching JSON data: %s, Now exiting.", e)
        sys.exit(1)


# read preset from local json file
def read_json_data(path: Path) -> Any:
    try:
        with open(path) as f:
            return json.load(f)
    except:
        exit(1)


# json validation func
def validate_json_data(data) -> bool:
    return isinstance(data, list) and all(isinstance(v, str) for v in data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", metavar="PRESET_URL")
    return parser.parse_args()


def main():  # Define main function
    if platform.system() != "Linux":  # Check if running on Linux, if not, exit.
        log.error("lp can only be run on linux-based systems. Now exiting.")
        exit(1)

    args = parse_args()

    # Extract values list
    if Path(args.url).exists():
        values_list = read_json_data(args.url)
    else:
        values_list = fetch_json_data(args.url)

    # Validate data
    if not validate_json_data(values_list):
        log.error("Invalid json format, should be list[str]")
        exit(1)

    log.info(
        "Selected Preset:\n"
        + "\n".join(f"  {v!r}" for v in values_list)
        + "\nSome presets require root. Errors may occur if lp is not run as root"
    )
    continueBoolean = input("Would you like to continue? [y/n]")
    if not any(continueBoolean == y for y in ["y", "Y"]):
        log.info(f"{continueBoolean!r} was selected. Aborting preset and exiting.")
        exit(0)

    log.info("This may take some time depending on the preset. Please wait")
    for cmd in values_list:
        log.info(f"{cmd!r} running...")
        status = exec_cmd(cmd)
        if status != 0:
            log.warning(f"cmd {cmd!r} failed. Exit status {status}")
    log.info("lp has finished running the preset. Now exiting.")


if __name__ == "__main__":
    main()
