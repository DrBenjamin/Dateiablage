import wx
import pandas as pd
import src.globals as g

# Method to handle the opening of JIRA tickets from CSV file
def on_import_tasks_from_csv(self, event):
    # Method to import the CSV file
    def import_csv(self, file_path):
        try:
            open_tasks = pd.read_csv(file_path)
            g.df_tasks = open_tasks
            self.on_import_tasks(event)
            wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Erfolg", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            print(e)
            wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Lading pandas dataframe from the saved CSV file
    dialog = wx.FileDialog(self, "Importiere offene Aufgaben", wildcard="CSV files (*.csv)|*.csv|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if dialog.ShowModal() == wx.ID_OK:
        file_path = dialog.GetPath()
        import_csv(self, file_path)
    dialog.Destroy()

def on_import_tasks(self, event):
    # Filtering the df for the selected user
    if self.config.Read("user_choice") == "Alle":
        if self.config.Read("status_choice") == "Alle":
            display_tasks(self, g.df_tasks)
        else:
            display_tasks(self, g.df_tasks[g.df_tasks['Status'] == self.config.Read("status_choice")])
    else:
        if self.config.Read("status_choice") == "Alle":
            display_tasks(self, g.df_tasks[g.df_tasks['Verantwortlicher'] == self.config.Read("user_choice")])
        else:
            output_df = g.df_tasks[g.df_tasks['Verantwortlicher'] == self.config.Read("user_choice")]
            display_tasks(self, output_df[output_df['Status'] == self.config.Read("status_choice")])

# Method to display the data in the tasks control
def display_tasks(self, df):
    self.tasks_ctrl.ClearAll()

    for _, row in df.iterrows():
        self.tasks_ctrl.Append([row.iloc[0]]) 
        self.tasks_ctrl.Append([row.iloc[1]])
        self.tasks_ctrl.Append([row.iloc[4]])
        self.tasks_ctrl.Append([row.iloc[5]])
        self.tasks_ctrl.Append(["-------------"])
    try:
        self.tasks_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
    except Exception as e:
        print(e)
