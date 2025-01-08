import wx
import os
import sys
import ctypes
import subprocess
import platform
import unicodedata

# Method to handle the Browse menu item
def on_browse(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        # `folder_path`` contains the path of the folder selected as string
        self.folder_path = dialog.GetPath()
        if self.config.ReadBool("drive_mapping_enabled", True):
            print("Stored letter: ", self.config.Read("drive_mapping_letter"))
            print(self.config.Read("drive_mapping_letter"))
            if self.config.Read("drive_mapping_letter") == "":
                letters = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                for letter in letters:
                    if os.path.exists(f"{letter}:"):
                        print("Existing: ", letter)
                        continue
                    else:
                        try:
                            # Mapping the folder to drive letter
                            print("Mapping: ", letter)
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
                            print("Registry file imported")

                        except:
                            print("Existing: ", letter)
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