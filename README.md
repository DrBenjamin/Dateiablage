# Dateiablage

Tool for organizing the file storage of e-learning content.

## Setup

[Setup description](https://github.com/DrBenjamin/Dateiablage/blob/main/SETUP.md)

## Execution

```bash
python Dateiablage.py
```

## Building

To build the executable, run the following command:

```bash
# Windows
pyinstaller.bat

# MacOS & Linux
python -m PyInstaller Dateiablage.spec
```

## OS specific notes

### Windows

To remove virtual drives manually, run the following command:

```bash
subst /d <drive letter>
```

### MacOS

To run the executable, you need to allow it after the first start in the Privacy 
settings.

### Linux

Add the icon manaually to the executable.