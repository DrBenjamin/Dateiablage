# Dateiablage

Tool for organizing the file storage of e-learning content.

## Setup

[Setup description](https://github.com/DrBenjamin/Dateiablage/blob/main/SETUP.md)

## Execution

```bash
python Dateiablage.py
```

## Building

Add the following images to the `_internal/images` folder:

- icon.ico (128x128) for Windows
- icon.icns (128x128) for MacOS
- logo.png (not more than 200px either dimension) for the GUI

To build the executables, run the following command:

```bash
# Windows
pyinstaller.bat

# MacOS & Linux
python -m PyInstaller Dateiablage.spec
```

## OS specific notes

All executables are built with PyInstaller and sneed to be build on the target 
system.

### Windows

To remove virtual drives manually, run the `subst` command:

```bash
# Adding folger example 
subst D: "C:\Users\dateiablage\Documents\GitHub\Dateiablage"

# Removing drive letter D:
subst /d D:
```

### MacOS

To run the executable, you need to allow it after the first start in the Privacy 
settings.

### Linux

Add the icon manaually to the executable.