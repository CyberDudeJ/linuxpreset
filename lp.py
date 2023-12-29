#!/usr/bin/env python3

import sys, os, requests, subprocess, platform

# Define global variables
arg1 = None
arg2 = None

def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestExceptions as e:
        print(f"[WARN] Error fetching JSON data {e}, Now exiting.")
        sys.exit(1)

def extract_values(json_data):
    values_list= []

    for item in json_data:
        for key, value in item.items():
            values_list.append(value)

    return values_list

def main(): # Define main function
    global arg1, arg2 # Declare arg1 + arg2 as global variables

    # Check if the correct number of arguments has been defined by the user
    if len(sys.argv) < 2:
        print("[WARN] lp usage: {} [arg1] [arg2]".format(sys.argv[0]))
    
    # Extract the arguments
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 1 else None

    # Check value of arg1 and adjust argument parsing
    if arg1 in ["h", "help", "?"]:
        print("Help coming soon idk")
    elif arg1 in ["r", "run"]:
        if len(sys.argv) > 2: # Check if arg2 exists
            arg2 = sys.argv[2] # begin script after getting arg2 again
            json_data = fetch_json_data(arg2)

            if json_data is not None:
                values_list = extract_values(json_data)
                print("Values list:", values_list)

        else:
            print(f"[WARN] arg2 is required for {arg1} to properly function. Now exiting.")
    else:
        print(f"[WARN] Invalid option: {arg1}, Now Exiting")

if platform.system() == "Linux": # Check if running on Linux, if not, exit.
    if __name__ == "__main__":
        main()
else:
    print("[WARN] lp can only be run on linux-based systems. Now exiting.")
