import wx
import os
import subprocess
import platform
import unicodedata
import pandas as pd
import re
import xml.etree.ElementTree as ET

# Method to handle the Browse menu item
def on_browse_target(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        # The `folder_path` variable contains the path of the folder selected as string
        self.folder_path_elearning = dialog.GetPath()
        
def on_browse_jira(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        # The `folder_path` variable contains the path of the folder selected as string
        self.folder_path_jira = dialog.GetPath()

# Method to import XML file
def import_xml(self, file_paths):
    output_df = pd.DataFrame()
    def xml_to_dict(xml_string):
        root = ET.fromstring(xml_string)
        result = {}
        for child in root:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = xml_to_dict(ET.tostring(child))
        return result
    df_list = []
    counter = 0
    for file_path in file_paths:
        counter += 1
        try:
            with open(file_path, 'r') as file:
                xml_string = file.read()

            dict_task = xml_to_dict(xml_string)
            snippet = dict_task['channel']['item']['description']
            
            # Converting HTML entities like &lt; &gt; to < >
            snippet_decoded = snippet.replace("&lt;", "<").replace("&gt;", ">")
            pattern = re.compile(
                r"<b>Zuordnung:</b>\s*(.*?)</li>.*?"
                r"<b>Typ:</b>\s*(.*?)</li>.*?"
                r"<b>Reihenfolge:</b>\s*(.*?)</li>",
                re.DOTALL
            )
            match = pattern.search(snippet_decoded)
            parent = match.group(1).strip()
            type = match.group(2).strip()
            order = match.group(3).strip()
            df = pd.DataFrame({
                                        'ID': counter,
                                        'Aufgabe': [dict_task['channel']['item']['summary']],
                                        'Zuordnung': [parent],
                                        'Typ': [type],
                                        'Reihenfolge': [order],
                                    })
            df.set_index('ID', inplace = True)
            df_list.append(df)
        except Exception as e:
            wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)
    output_df = pd.concat(df_list)
    output_df.reset_index(drop=True, inplace=True)

    def sanitize_path(path_str):
        # Replacing invalid Windows path chars: < > : " / \ | ? *
        invalid_chars = r'<>:"/\|?*'
        for c in invalid_chars:
            path_str = path_str.replace(c, "_")
        return path_str

    # Building the parent map
    parent_map = {}
    for _, row in output_df.iterrows():
        parent_map[row["Aufgabe"]] = row["Zuordnung"]
    print(parent_map)

    for _, row in output_df.iterrows():
        # Cleaning up invalid Windows path characters, etc. (example: replace ":" with "_")
        parent_folder = sanitize_path(row["Zuordnung"])
        subfolders = sanitize_path(row["Aufgabe"].split("/")[-1])

        # Building the folder path from subfolders
        folder_path = os.path.join(self.folder_path_elearning, parent_folder, subfolders)

        if row["Zuordnung"] != "ROOT":
            os.makedirs(folder_path, exist_ok=True)
            print("Created:", folder_path)

# Method for creating the folder structur
def on_create_folder_structure(self, event):
    file_path_jira = []
    for name in os.listdir(self.folder_path_jira):
        file_path = os.path.join(self.folder_path_jira, name)
        if os.path.isfile(file_path) and name.endswith(".xml"):
            file_path_jira.append(file_path)
    import_xml(self, file_path_jira)

# Method to handle the Browse menu item
def on_browse(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        # The `folder_path` variable contains the path of the folder selected as string
        self.folder_path = dialog.GetPath()
        if self.config.ReadBool("drive_mapping_enabled", True):
            if self.config.Read("drive_mapping_letter") == "":
                letters = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                for letter in letters:
                    if os.path.exists(f"{letter}:"):
                        continue
                    else:
                        try:
                            # Mapping the folder to drive letter
                            subprocess.run(['subst', f"{letter}:", self.folder_path],
                                        check=True)

                            # Writing registry file
                            with open(f"{self.folder_path}\\MapVirtualDrive.reg", "w") as f:
                                path_to_folder = self.folder_path.replace("\\", "\\\\")
                                f.write(
f"""Windows Registry Editor Version 5.00\n\n\
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]
"Virtual Drive"="subst {letter}: \\"{path_to_folder}\\""
""")

                            # Importing registry file
                            subprocess.run(["regedit", "/s", f"{self.folder_path}\\MapVirtualDrive.reg"], check=True)
                        except:
                            continue
                        self.config.Write("drive_mapping_letter", letter)
                        break
            list_files(self, f'{self.config.Read("drive_mapping_letter")}:\\')
        else:
            list_files(self, self.folder_path)
    dialog.Destroy()

# Method to handle selected file
def on_file_selected(self, event):
    file_index = event.GetSelection()
    file_path = self.file_listbox.GetString(file_index)
    self.file_path = file_path
    
    # To-Do Kanjo
    # - Get the file name from the path
    # - Xy
    file_name = os.path.basename(self.file_path)
    print(file_name)

# Method to handle the list control item activated event
def on_file_activated(self, event):
    if platform.system() == "Windows":
        try:
            os.startfile(f'"{self.file_path}"')
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
    elif platform.system() == "Darwin":  # macOS
        try:
            subprocess.call(["open", self.file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:  # Linux
        try:
            subprocess.call(["xdg-open", self.file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to list the files in the selected folder
def list_files(self, folder_path, filter_text=None):
    # Clear the existing file list
    self.file_list = []
    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if filter_text is None:
                self.file_list.append(dir_path)
                files = [
                    f 
                    for f in os.listdir(dir_path)
                ]
                self.file_list.extend(os.path.join(dir_path, f) for f in files)
            else:
                # Adding all subdirectories of the matching directory
                normalized_filter_text = unicodedata.normalize('NFC', filter_text)
                normalized_name = unicodedata.normalize('NFC', name)
                if normalized_filter_text in normalized_name:
                    for sub_root, sub_dirs, sub_files in os.walk(dir_path):
                        for sub_name in sub_dirs:
                            dir_path = os.path.join(sub_root, sub_name)
                            self.file_list.append(os.path.join(sub_root, sub_name))
                            sub_files = [
                                f 
                                for f in os.listdir(dir_path)
                            ]
                            self.file_list.extend(os.path.join(dir_path, f) for f in sub_files)
    self.file_listbox.Set(self.file_list)