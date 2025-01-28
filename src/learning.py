## Description: This file contains the methods to handle the e-Leanring structure list.
## `src/learning.py`
## Modules
import wx
import pandas as pd
import src.globals as g
from src.tasks import display_tasks
from src.files import list_files

# Method to handle the Import learning definition
def on_import_csv(self, event, file_path = None):
    if file_path == None:
        dialog = wx.FileDialog(self, "Importiere e-Learning Definition", wildcard="CSV files (*.csv)|*.csv|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            import_csv(self, file_path)
        dialog.Destroy()
    else:
        import_csv(self, file_path, message = None)

# Method to handle the list control item activated event
def on_item_selected(self, event):
    item_index = event.GetIndex()
    item_text = self.learning_ctrl.GetItemText(item_index, 0)
    ticket = self.learning_ctrl.GetItemText(item_index, 1)
    display_tasks(self, g.df_tasks, ticket)
    list_files(self, g.folder_path, item_text.strip())

# Method to import the CSV file
def import_csv(self, file_path, message = True):
    try:
        g.df_elearning = pd.read_csv(file_path)
        display_learning(self, g.df_elearning)
        g.root_folder_name = g.df_elearning.iloc[0, 0]
        invalid_chars = r'<>:"/\|?*'
        for c in invalid_chars:
            g.root_folder_name = g.root_folder_name.replace(c, "_")
        self.SetTitle(f"Dateiablage - {g.root_folder_name}")
        if message:
            wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Erfolg", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        print(e)
        wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to display the data in the learning control
def display_learning(self, df):
    self.learning_ctrl.ClearAll()
    self.learning_ctrl.InsertColumn(0, "Thema")
    self.learning_ctrl.InsertColumn(1, "Ticket")
    for _, row in df.iterrows():
        text = row.iloc[0]
        ticket = row.iloc[1]
        level = row.iloc[2]
        indent = ' ' * (((level + 4) * 4) - 16)
        index = self.learning_ctrl.InsertItem(self.learning_ctrl.GetItemCount(), f"{indent}{text}")
        self.learning_ctrl.SetItem(index, 1, ticket)

    # Adjusting the column width to fit automatically the content
    self.learning_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
    self.learning_ctrl.SetColumnWidth(1, 0) # hide the ticket column
