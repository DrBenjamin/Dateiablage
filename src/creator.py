## Description: This file contains the methods to handle the file operations in the application.
## `src/creator.py`
## Modules
import wx
import os
import shutil
import src.globals as g

# Method to handle creation of new e-Learning
def on_new_elearning(self, event):
    print(g.root_folder_name)
    self.on_import_files(event)

# Method to import files
def on_import_files(self, event):
    wildcard = "Alle Dateien (*.*)|*.*"  # Beispiel-Wildcard
    dialog = wx.FileDialog(self, "Bitte wählen Sie e-Learning-Dateien aus:",
        wildcard=wildcard,
        style=wx.FD_OPEN | wx.FD_MULTIPLE
    )
    if dialog.ShowModal() == wx.ID_OK:
        g.file_list_import = dialog.GetPaths()
    dialog.Destroy()

    # Copying the files to the target folder
    counter = 0
    for file_path in g.file_list_import:
        try:
            file_name = os.path.basename(file_path)
            _, suffix = os.path.splitext(file_name)
            file_name = f"{os.path.basename(g.folder_path_import)}{suffix}"
            new_file_path = os.path.join(g.folder_path_import, file_name)
            if os.path.isfile(new_file_path):
                wx.MessageBox(f'Datei "{file_name}" existiert bereits im Ziel-Ordner.',
                              "Error", wx.OK | wx.ICON_ERROR)
                continue
            shutil.copy2(file_path, new_file_path)
            counter += 1
        except Exception as e:
            wx.MessageBox(f'Datei "{file_name}" konnte nicht kopiert werden: {e}',
                          "Error", wx.OK | wx.ICON_ERROR)
    wx.MessageBox(f"{counter} Dateien wurden erfolgreich inmportiert.", "Information",
                    wx.OK | wx.ICON_INFORMATION)