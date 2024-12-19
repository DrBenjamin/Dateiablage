import wx
import os
import subprocess
import platform
import unicodedata

# Method to handle the Browse menu item
def on_browse(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        self.folder_path = dialog.GetPath() # folder_path will contain the path of the folder you have selected as string
        list_files(self, self.folder_path)
    dialog.Destroy()

# Method to handle the list control item activated event
def on_file_activated(self, event):
    file_index = event.GetSelection()
    file_path = self.file_listbox.GetString(file_index)

    if platform.system() == "Windows":
        try:
            os.startfile(f'"{file_path}"')
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
    elif platform.system() == "Darwin":  # macOS
        try:
            subprocess.call(["open", file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:  # Linux
        try:
            subprocess.call(["xdg-open", file_path])
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