## Global variables for the project
# e-Learning
file_path_elearning = None # storing the path to e-Learning definition file (CSV)
df_elearning = None # storing the dataframe of the e-Learning definition file

# Tasks
df_tasks = None # storing the dataframe of the tasks file

# File Explorer
file_list = [] # storing the list of files in the File Explorer
file_path = None # storing the path to the selected file in the File Explorer
folder_path = None # storing the path to the selected root folder for the File Explorer
folder_path_jira = None # storing the path to the JIRA tickets (multi file import)
folder_path_elearning = None # storing the path to the new e-Learning folder

# Preferences
mapping = False # needed for initial mapping of drive letter
