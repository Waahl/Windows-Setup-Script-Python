## Python Setup Script

### Descriptions
Downloads programs defined in the common.json file, then runs the setup files to speed up the process of remembering what programs you had installed and where to find them. As of now they are pointing towards the Windows executables, however, I plan on implementing Mac OSX support as well.


### Usage
This script uses Python3, I am not planning on supporting Python2.7 as it will be out of date by 2020.

1. Run `python3 PyWinSetup.py` or `./PyWinSetup.py`, optional arguments are described below.
2. Follow the steps.

Optional Arguments
* `--resources` or `-R`, if you have created your own json file.
* `--no-download` or `-n`, if you wan't to skip the download stage, this is a bit untested.
* `--download-all` or `-y`, if you wan't to download all the files in the json file, e.g accept all download prompts.


### TODO
* Implement Mac OSX Support, .dmg etc.
* ~~Fix other executable files, like .msi etc.~~
* ~~Implement support for .zip files~~
* Implement DWS for Windows, (Destroy Windows Spying)
* Implement support for finding files which may be hidden in folders.
If you have any suggestions you are welcome to commit them to this repository or message me.