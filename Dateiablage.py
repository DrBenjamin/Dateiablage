import wx
import os

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.browse_button = wx.Button(panel, label="Browse")
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse)
        
        self.file_listbox = wx.ListBox(panel)
        
        sizer.Add(self.browse_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.file_listbox, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)
        
        self.folder_path = os.path.join(os.path.expanduser("~"), "OneDrive - CGM", "UKE_Videos", "8. Turtorials_Videobearbeitung", "Dateistruktur Neu", "E-Learnings")

    def on_browse(self, event):
        dialog = wx.DirDialog(None, "Select a folder:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.folder_path = dialog.GetPath()  # folder_path will contain the path of the folder you have selected as string
            self.list_files(self.folder_path)
        dialog.Destroy()

    def list_files(self, folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for name in dirs:
                file_list.append(os.path.join(root, name))
            for name in files:
                file_list.append(os.path.join(root, name))

        self.file_listbox.Set(file_list)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="Dateiablage", size=(600, 400))
        frame.Show(True)
        return True

# Initialize the wx App
app = MyApp(False)
app.MainLoop()