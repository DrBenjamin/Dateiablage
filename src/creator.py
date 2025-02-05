## Description: This file contains the methods to handle the file operations in the application.
## `src/creator.py`
## Modules
import wx
import os
import shutil
import subprocess
import platform
import pandas as pd
import src.globals as g

# Method to handle creation of new e-Learning
def on_new_elearning(self, event):
    print(g.root_folder_name)