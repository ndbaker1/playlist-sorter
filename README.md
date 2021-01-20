# Playlist Set Manager
A Playlist Editor for `.m3u` files, which treats playlists as mutually exclusive so that you can sort without overlap.  
> Exclusion occures with open playlists, so there are ways to create intentional overlap between playlists that are not related.

## Libs
`PyQt5` was the GUI library for this project

## Setup
To install all required packages/imports
```
pip install -r requirments.txt
```
_advise using python `venv` for local installations_

## Build executable
using `pyinstaller` build the executable with
```
pyinstaller --onefile --windowed --icon=app.ico --name="Playlist Set Manager" --add-data 'app.ico;.' app.py
```
> Note:  
_--add-data 'app.ico;.' for Windows_  
_--add-data 'app.ico:.' for Linux_
