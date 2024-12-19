import wx
import io

# Method to handle the Import tasks excel
def on_import_excel(self, event):
    dialog = wx.FileDialog(self, "Importiere Aufgabenliste", wildcard="Exceldatei (*.xlsx)|*.xlsx|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if dialog.ShowModal() == wx.ID_OK:
        self.file_path_tasks = dialog.GetPath()
        self.import_excel(self.file_path_tasks)
    dialog.Destroy()

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

        self.display_tasks(output_df)
        wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Erfolg", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to display the data in the tasks control
def display_tasks(self, df):
    self.tasks_ctrl.ClearAll()
    self.tasks_ctrl.AppendColumn("Aufgabenliste")
    for index, row in df.iterrows():
        print(row) # Debugging row data
        text = "Aufgabe: " + row.iloc[0] + " Verantwortlicher: " + row.iloc[1] + " Status: " + row.iloc[2]
        self.tasks_ctrl.Append([text])

    # Adjusting the column width to fit automatically the content
    self.tasks_ctrl.SetColumnWidth(0, 200)
    #self.tasks_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)