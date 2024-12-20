import wx
import io
import pandas as pd
import xml.etree.ElementTree as ET

# Method to handle the Import tasks excel
def on_import_excel(self, event):
    dialog = wx.FileDialog(self, "Importiere Aufgabenliste", wildcard="Excel- oder XML-Datei (*.xlsx;*.xml)|*.xlsx;*.xml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if dialog.ShowModal() == wx.ID_OK:
        self.file_path_tasks = dialog.GetPath()
        if self.file_path_tasks.endswith(".xml"):
            import_xml(self, self.file_path_tasks)
        else:
            import_excel(self, self.file_path_tasks)
    dialog.Destroy()

# Method to import XML file
def import_xml(self, file_path):
    def xml_to_dict(xml_string):
        root = ET.fromstring(xml_string)
        result = {}
        for child in root:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = xml_to_dict(ET.tostring(child))
        return result
    try:
        with open(file_path, 'r') as file:
            xml_string = file.read()
        print(xml_string)
        dict_task = xml_to_dict(xml_string)
        output_df = pd.DataFrame({
                                    'ID': "0",
                                    'Aufgabe': [dict_task['channel']['item']['summary']],
                                    'Verantwortlicher': [dict_task['channel']['item']['assignee']],
                                    'Status': [dict_task['channel']['item']['status']]
                                })
        output_df = output_df.set_index('ID')
        display_tasks(self, output_df)
        wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Erfolg", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

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
                    if self.config.Read("user_choice") == user:
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
    for index, row in df.iterrows():
        if index==4:  
            self.tasks_ctrl.Append([row.iloc[0]]) 
            self.tasks_ctrl.Append([row.iloc[1]])
            self.tasks_ctrl.Append([row.iloc[2]])
            text="-------------"
            self.tasks_ctrl.Append([text])
            text="-------------"
            self.tasks_ctrl.Append([text])
            self.tasks_ctrl.SetColumnWidth(0, 200)
            self.tasks_ctrl.SetColumnWidth(1, 200)
            self.tasks_ctrl.SetColumnWidth(2, 200)
        
        elif index >= 5:
            print(row) # Debugging row data
            self.tasks_ctrl.Append([row.iloc[0]]) 
            self.tasks_ctrl.Append([row.iloc[1]])
            self.tasks_ctrl.Append([row.iloc[2]])
            text="-------"
            self.tasks_ctrl.Append([text])
            text="-------"
            self.tasks_ctrl.Append([text])
        