#!/usr/bin/env python3

import sys, os, requests, subprocess, platform

# Define global variables
arg1 = None
arg2 = None

# Define command execution function
def exec_cmd(command):
    stream = os.popen(command)
    output = stream.read()
    output

    return output

# Define check if cmd exists function
def command_exists(command):
    try:
        subprocess.check_output(['which', command])
        return True
    except subprocess.CalledProcessError:
        return False

# Define fetch json file function
def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestExceptions as e:
        print(f"[WARN] Error fetching JSON data {e}, Now exiting.")
        sys.exit(1)

# Define extract values function
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
                print("[INFO] Selected Preset:", values_list)
                print("[INFO] Some presets require root. Errors may occur if lp is not run as root")
                index = 0
                continueBoolean = input("Would you like to continue? [y/n]")
                if continueBoolean in ["y", "Y"]:
                    print("[INFO] This may take some time depending on the preset. Please wait")
                    while index < len(values_list):
                        current_entry = values_list[index]
                        # exec script
                        exec_cmd(current_entry)
                        # Increment the index for the next iteration
                        index += 1
                elif continueBoolean in ["n", "N"]:
                    print(f"[WARN] {continueBoolean} was selected. Aborting preset and exiting.")
                else:
                    print("[WARN] Please select a valid option. Aborting preset and exiting.")
                print("[INFO] lp has finished running the preset. Now exiting.")
        else:
            print(f"[WARN] arg2 is required for {arg1} to properly function. Now exiting.")
    else:
        print(f"[WARN] Invalid option: {arg1}, Now Exiting")

if platform.system() == "Linux": # Check if running on Linux, if not, exit.
    if __name__ == "__main__":
        main()
else:
    print("[WARN] lp can only be run on linux-based systems. Now exiting.")

