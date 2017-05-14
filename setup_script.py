#!usr/bin/env python3
# -*- coding: utf-8 -*-

# Setup Script
# For personal use only

# Imports
from subprocess import Popen, CalledProcessError, PIPE
import webbrowser as wb
import json
import time
import sys
import os

def json_handler():
    with open("resources.json", "r+", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        if data["RUNS"] > 0:
            print("\n[*] This script may have been run already." +
            "\nIf you wish to only run exes downloaded please input y else n to continue.")
            cont = input("y/n: ")
            if cont.lower() == "y":
                run_exes()
                return
            elif cont.lower() == "n":
                pass
            else:
                print("\n[-] Invalid input please try again.")
                json_handler()

        for link in data["LINKS"]:
            wb.open(link)

        data["RUNS"] += 1

        jsonFile.seek(0)
        json.dump(data, jsonFile)
        jsonFile.truncate()

    # Sleeps whilst waiting for downloads to finish
    time.sleep(10)
    run_exes()

def run_exes():
    # Checks if the current working directory is the download folder
    if os.getcwd() != "c:\\users\\{}\\Downloads".format(os.getlogin()):
        os.chdir("c:\\users\\{}\\Downloads".format(os.getlogin()))

    proc = set(proc for proc in os.listdir() if proc.endswith(".exe"))
    for exe in proc:
        try:
            print("\n[*] EXECUTING: ", exe)
            Popen([exe], stdout=PIPE)
        except CalledProcessError as e:
            print("\n[-] Unexpected Error Occured: ", e)
            exit(1)
        except OSError:
            print("\n[-] Please run the script with elevated privileges!")


if __name__ == "__main__":
    if sys.platform.startswith("win32"):
        print("\n[*] Script starting, Please be aware that your default browser " + \
        "will open several tabs,\n depending on how many links you have in your " + \
        "config file.\n")
        time.sleep(2)
        json_handler()
    else:
        print("[-] This is not a win32 based os!")
