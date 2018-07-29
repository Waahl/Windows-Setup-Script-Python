#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Setup Script

# Imports
from subprocess import Popen, CalledProcessError
from sys import platform
import argparse
import json
import os

# External Imports
try:
    import requests
except ModuleNotFoundError:
    print(" [-] Please run `pip install -r requirements.txt`, missing requests")
    exit(1)

try:
    from tqdm import tqdm
except:
    print(" [-] Missing TQDM module, not necessary, will continue anyway.")
    pass


def welcome_msg():
    """ Hello and welcome, enjoy the ride. """
    print("""
          /\_/\\
        =( °w° )=       WINDOWS SETUP SCRIPT
          )   (  //
         (__ __)//
    """)


def confirm_action(msg):
    """ Prompts user for confirmation of action. """
    print(" [*] {}".format(msg))
    prompt = input(" [*] Y/N? ".format(msg)).lower()
    if prompt in ["yes", "y"]:
        return True
    elif prompt in ["no", "n"]:
        return False
    else:
        print(" [-] Please answer with y/n")
        return confirm_action(msg)


def handle_err(func, err, fatal, *args, **kwargs):
    """ Handles functions which may throw errors. """
    try:
        return func(*args, **kwargs)
    except err as e:
        if fatal:
            print(" [-] Fatal error occured: {}".format(e))
            exit(1)
        
        print(" [-] Error occured: {}".format(e))
        pass


def get_files(patterns):
    """ Returns all files in current folder matching a pattern. """
    files = handle_err(os.listdir, OSError, True)
    matches = list()
    for pattern in patterns:
        matches.extend([match for match in files if pattern in match])

    return matches


def execute_file(prog):
    """ Starts an Popen shell and runs a file. """
    proc = Popen([r"{}".format(prog)], shell=True)
    handle_err(proc.communicate, Exception, True)


def guess_name(url, exts):
    """ Try to guess the name of the downloaded file. """
    name = url.split("/")[-1].split("=")[-1]
    for ext in exts:
        if ext in name:
            return name
    
    print(" [-] Unknown file extension: {}, from url: {}".format(name, url))
    print(" [*] Trying to guess file extension")
    return name.split(".")[0] + exts[0]


def download_file(url, path, exts):
    """ Downloads file from a url with a GET request. """
    resp = requests.get(url, stream=True)
    file_size = int(resp.headers["Content-Length"])

    if os.path.exists(path):
        first_byte = os.path.getsize(path)
    else:
        first_byte = 0

    if first_byte >= file_size:
        return file_size

    # TODO: implement a better way to get names, look if request contains it
    name = guess_name(url, exts)
    pbar = handle_err(tqdm, Exception, False, total=file_size,
            initial=first_byte, unit="B", unit_scale=True,
            desc=name)

    if not (100 < resp.status_code < 300):
        print(" [-] Error fetching content from url: {}".format(url))
        print(" [*] Skipping!")
    
    file_path = "{}/{}".format(path, name)
    with open(file_path, "wb") as file_obj:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                handle_err(file_obj.write, OSError, True, chunk)
                handle_err(pbar.update, Exception, False, 1024)

    handle_err(pbar.close, Exception, False)
    del resp


def fetch_files(resources, path, exts, **kwargs):
    """ Fetches the urls from file or argument. """
    download = dict()
    with open(resources, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        
        for category in data.keys():
            print("\n [*] Category: {}".format(category))

            for name in data[category].keys():
                # confirm for each download
                if kwargs["download_all"] or confirm_action("Download {}".format(name)):
                    download[name] = data[category][name] 

    for prog, url in download.items():
        print("\n [+] Downloading: {}".format(prog))
        download_file(url, path, exts)


def run_files(exts):
    """ Fetches and runs the programs that is found. """
    handle_err(os.chdir, (OSError, FileNotFoundError), True, download_path)

    progs = get_files(exts)
    for prog in progs:
        print(" [+] Running program: {}".format(prog))
        execute_file(prog)


if __name__ == "__main__":
    welcome_msg()
    parser = argparse.ArgumentParser(description="Windows Setup Script, "
            "will download and run programs specified in JSON format.")
    parser.add_argument("-R", "--resources", type=str, help="reources file name", default="common.json")
    parser.add_argument("-n", "--no-download", action="store_true" , help="skip the download stage", default=False)
    parser.add_argument("-y", "--download-all", action="store_true", help="download all the programs in json file", default=False)
    args = parser.parse_args()

    print(" [*] Running script")

    if "win32" in platform:
        download_path = r"C:\\Users\\{}\\Downloads".format(os.getlogin())
        exts = [".dmg", ".app"]
    elif "darwin" in platform:
        download_path = r"/Users/{}/Downloads".format(os.getlogin())
        exts = [".exe", ".msi"]

    if not args.no_download:
        if not confirm_action("Correct path for downloads: {}".format(download_path)):
            download_path = input(" [*] Enter path to download: ")

        fetch_files(args.resources, download_path, exts, download_all=args.download_all)

    run_files(exts)
    print(" [*] Done, hope you enjoyed the ride!")
