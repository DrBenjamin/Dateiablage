import wx
import os

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        
        # Create a menu bar
        menu_bar = wx.MenuBar()
        
        # Create the File menu
        file_menu = wx.Menu()
        browse_item = file_menu.Append(wx.ID_ANY, "&Wähle Quellverzeichnis")
        file_menu.Append(wx.ID_OPEN, "&Importiere e-Learning Definition")
        file_menu.Append(wx.ID_EXIT, "E&xit")
        menu_bar.Append(file_menu, "&File")
        
        # Create the Edit menu
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_COPY, "&Kopieren")
        edit_menu.Append(wx.ID_CUT, "&Ausscheniden")
        edit_menu.Append(wx.ID_PASTE, "&Einfügen")
        menu_bar.Append(edit_menu, "&Bearbeiten")
        
        # Set the menu bar
        self.SetMenuBar(menu_bar)
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.file_listbox = wx.ListBox(panel)

        sizer.Add(self.file_listbox, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        # Bind the Browse menu item to the on_browse method
        self.Bind(wx.EVT_MENU, self.on_browse, browse_item)
        
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