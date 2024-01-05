#!/usr/bin/env python3

import argparse
import json
import logging
from pathlib import Path
import platform
import requests
import subprocess as sp
from typing import Any, List


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)-.4s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def exec_cmd(command: str) -> int:
    try:
        return sp.run(command.split()).returncode
    except Exception as e:
        log.error(e)
        return -1


def fetch_preset(url: str) -> Any:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error("Error fetching JSON data: %s, Now exiting.", e)
        exit(1)


def read_preset(path: str) -> Any:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        log.error("Error reading JSON data: %s", e)
        exit(1)


def validate_json_data(data: Any) -> bool:
    return isinstance(data, list) and all(isinstance(v, str) for v in data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", metavar="PRESET_URL")
    return parser.parse_args()


def run_preset(preset: List[str]):
    for i, cmd in enumerate(preset):
        log.info(f"[{i+1}/{len(preset)}] {cmd!r} running...")
        status = exec_cmd(cmd)
        if status != 0:
            log.warning(f"cmd {cmd!r} failed. Exit status {status}")


def main():
    if platform.system() != "Linux":
        log.error("lp can only be run on linux-based systems. Now exiting.")
        exit(1)

    args = parse_args()
    if Path(args.url).exists():
        preset = read_preset(args.url)
    else:
        preset = fetch_preset(args.url)

    if not validate_json_data(preset):
        log.error("Invalid json format, should be list[str]")
        exit(1)

    log.info(
        "Selected Preset:\n"
        + "\n".join(f"  {v!r}" for v in preset)
        + "\nSome presets require root. Errors may occur if lp is not run as root"
    )

    resp = input("Would you like to continue? [y/n]")
    if not any(resp == y for y in ["y", "Y"]):
        log.info(f"{resp!r} was selected. Aborting preset and exiting.")
        exit(0)

    log.info("This may take some time depending on the preset. Please wait")
    run_preset(preset)
    log.info("lp has finished running the preset. Now exiting.")


if __name__ == "__main__":
    main()
