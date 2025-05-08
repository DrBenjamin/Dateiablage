### `src/globals.py`
### Main application for the RAG on Snow project
### Open-Source, hosted on https://github.com/DrBenjamin/Dateiablage
### Please reach out to ben@seriousbenentertainment.org for any questions
# e-Learning
file_path_elearning = None # storing the path to e-Learning definition file (CSV)
df_elearning = None # storing the dataframe of the e-Learning definition file
ticket_chosen = False # storing if a single ticket was chosen
elearning_index = 0 # storing the index of the chosen item

# Tasks
df_tasks = None # storing the dataframe of the tasks file

# File Explorer
file_list = [] # storing the list of files in the File Explorer
file_list_import = [] # storing the list of files to import in the eLearning
file_path = None # storing the path to the selected file in the File Explorer
folder_path = None # storing the path to the selected root folder for the File Explorer
folder_path_import = None # storing the path to the root folder for the eLearning import
folder_path_jira = None # storing the path to the JIRA tickets (multi file import)
folder_path_elearning = None # storing the path to the new e-Learning folder
root_folder_name = None # storing the name of the root folder for folder creation

# Preferences
mapping = False # needed for initial mapping of drive letter
