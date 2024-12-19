import wx
import pandas as pd
from src.files import list_files

# Method to handle the Import learning definition
def on_import_csv(self, event):
    if self.config.ReadBool("csv_import_enabled", True):
        dialog = wx.FileDialog(self, "Importiere e-Learning Definition", wildcard="CSV files (*.csv)|*.csv|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            import_csv(self, file_path)
        dialog.Destroy()
    else:
        wx.MessageBox("CSV Import ist deaktiviert (siehe Einstellungen)", "Information", wx.OK | wx.ICON_WARNING)

# Method to handle the list control item activated event
def on_item_selected(self, event):
    item_index = event.GetIndex()
    item_text = self.learning_ctrl.GetItemText(item_index)
    self.SetTitle(f"Dateiablage - {item_text.strip()}")
    list_files(self, self.folder_path, item_text.strip())
    
# Method to import the CSV file
def import_csv(self, file_path):
    try:
        self.definition_csv = pd.read_csv(file_path)
        display_learning(self, self.definition_csv)
        wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Erfolg", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to display the data in the learning control
def display_learning(self, df):
    self.learning_ctrl.ClearAll()
    self.learning_ctrl.AppendColumn("e-Learning Struktur")

    for index, row in df.iterrows():
        text = row.iloc[0]
        level = row.iloc[1]
        indent = ' ' * ((level * 4) - 4)  # Indent based on the level
        self.learning_ctrl.Append([f"{indent}{text}"])

    # Adjusting the column width to fit automatically the content
    self.learning_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
