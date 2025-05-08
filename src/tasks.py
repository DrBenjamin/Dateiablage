### `src/tasks.py`
### Main application for the RAG on Snow project
### Open-Source, hosted on https://github.com/DrBenjamin/Dateiablage
### Please reach out to ben@seriousbenentertainment.org for any questions
## Modules
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
            wx.MessageBox(f"{len(g.df_tasks)} Elemente aus Datei {file_path} erfolgreich importiert!", "Erfolg", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            print(e)
            wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Loading pandas dataframe from the saved CSV file
    dialog = wx.FileDialog(self, "Importiere offene Aufgaben", wildcard="CSV files (*.csv)|*.csv|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if dialog.ShowModal() == wx.ID_OK:
        file_path = dialog.GetPath()
        import_csv(self, file_path)
    dialog.Destroy()

def on_import_tasks(self, event):
    # Filtering the JIRA tickets dataframe for the selected user and status
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

# Method to handle the list control item selected event
def on_task_item_selected(self, event):
    item_index = event.GetIndex()
    item_text = self.tasks_ctrl.GetItemText(item_index)
    #print("Single Click: ", item_text)

# Method to handle the list control double click event
def on_task_item_activated(self, event):
    item_index = event.GetIndex()
    item_text = self.tasks_ctrl.GetItemText(item_index)
    #print("Double Click: ", item_text)

# Method to display the data in the tasks control
def display_tasks(self, df, ticket = None):
    self.tasks_ctrl.ClearAll()
    df = df.reset_index(drop=True)
    if ticket is not None:
        df = df[df['Ticket'] == ticket]
    for index, row in df.iterrows():
        self.tasks_ctrl.Append([row.iloc[0]]) 
        self.tasks_ctrl.Append([row.iloc[1]])
        self.tasks_ctrl.Append([row.iloc[4]])
        self.tasks_ctrl.Append([row.iloc[5]])
        if index < len(df) - 1:
            self.tasks_ctrl.Append(["-------------"])
    try:
        self.tasks_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
    except Exception as e:
        print(e)
