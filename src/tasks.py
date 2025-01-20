import wx
import io
import os
import pandas as pd
import xml.etree.ElementTree as ET

# Method to handle the Import tasks excel
def on_import_task(self, event, df = None):
    if df is None:
        if self.config.ReadBool("xml_import_enabled", True):
            dialog = wx.DirDialog(None, "Wähle einen Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
            if dialog.ShowModal() == wx.ID_OK:
                self.folder_path = dialog.GetPath()
                for name in os.listdir(self.folder_path):
                    file_path = os.path.join(self.folder_path, name)
                    if os.path.isfile(file_path) and name.endswith(".xml"):
                        self.file_path_tasks.append(file_path)
                import_xml(self, self.file_path_tasks)
        else:
            dialog = wx.FileDialog(self, "Importiere Aufgabenliste", wildcard="Excel- oder XML-Datei (*.xlsx;*.xml)|*.xlsx;*.xml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dialog.ShowModal() == wx.ID_OK:
                self.file_path_tasks = dialog.GetPath()
                if self.file_path_tasks.endswith(".xml"):
                    import_xml(self, [self.file_path_tasks])
                else:
                    import_excel(self, self.file_path_tasks)
        dialog.Destroy()
    else:
        # Filtering the df for the selected user
        if self.config.Read("user_choice") == "Alle":
            display_tasks(self, df[df['Status'] == "Neu"])
        else:
            output_df = df[df['Verantwortlicher'] == self.config.Read("user_choice")]
            display_tasks(self, output_df[output_df['Status'] == "Neu"])

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
            if dict_task['channel']['item']['assignee'] == self.config.Read("user_choice") or self.config.Read("user_choice") == "Alle":
                df = pd.DataFrame({
                                            'ID': counter,
                                            'Aufgabe': [dict_task['channel']['item']['summary']],
                                            'Verantwortlicher': [dict_task['channel']['item']['assignee']],
                                            'Status': [dict_task['channel']['item']['status']]
                                        })
                df.set_index('ID', inplace = True)
                df_list.append(df)
        except Exception as e:
            wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)
    output_df = pd.concat(df_list)
    output_df.reset_index(drop=True, inplace=True)
    display_tasks(self, output_df)

# Method to import the Excel file
def import_excel(self, file_path):
    try:
        data = None
        output = [[]]

        # Reading file as bytes
        with open(file_path, 'rb') as file:
            bytes_data = file.read()

        # Creating pandas dataframe, e.g. sheet_name `1` for sheet no. 2 or "Arzt prozessual"
        data = pd.read_excel(io.BytesIO(bytes_data), sheet_name = 1)
        print("Excel: ", data)
        
        # Tasks from Excel
        for index, row in data.iterrows():
            if len(row) > 1:  # Ensure there are at least 2 columns
                # Extract relevant columns (adjust the indices as needed)
                task = str(row.iloc[1]).strip()
                user = str(row.iloc[6]).strip()
                status = str(row.iloc[8]).strip()
                if index >= 5:
                    if self.config.Read("user_choice") == "Alle":
                        if task != "nan":
                            output.append([index, task, user, status])
                    else:
                        if user == self.config.Read("user_choice"):
                            output.append([index, task, user, status])
            else:
                print(f"Row {index} does not have enough columns: {row}")
        print("Output: ", output) # Debugging list of lists `output`
        if output == [[]]:
            output_df = pd.DataFrame({
                                            'ID': "0",
                                            'Aufgabenliste': ['leer'],
                                            'Verantwortlicher': ['leer'],
                                            'Status': ['leer']
                                })
            output_df = output_df.set_index('ID')
        else:
            output_df = pd.DataFrame(output, columns = ['ID', 'Aufgabe', 'Verantwortlicher', 'Status'])
            output_df = output_df.set_index('ID')
            output_df = output_df.drop_duplicates(ignore_index = True)
            output_df = output_df.drop(0, axis = 0)
        print("Pandas df: ", len(output_df)) # Debugging pandas dataframe `output_df`

        display_tasks(self, output_df)
        wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Erfolg", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

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
