import wx

# Method to handle the Import tasks excel
def on_import_task(self, event, df = None):
    # Filtering the df for the selected user
    if self.config.Read("user_choice") == "Alle":
        if self.config.Read("status_choice") == "Alle":
            display_tasks(self, df)
        else:
            display_tasks(self, df[df['Status'] == self.config.Read("status_choice")])
    else:
        if self.config.Read("status_choice") == "Alle":
            display_tasks(self, df[df['Verantwortlicher'] == self.config.Read("user_choice")])
        else:
            output_df = df[df['Verantwortlicher'] == self.config.Read("user_choice")]
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
