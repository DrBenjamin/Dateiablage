import wx # wxPython / Phoenix
import types
from src.methods import (
    on_refresh,
    on_export,
    on_exit,
    on_contact,
    on_about,
    on_convert
)
from src.preferences import on_preferences
from src.learning import (
    on_item_selected,
    on_import_csv
)
from src.tasks import on_import_task
from src.files import (
    on_browse,
    on_file_activated
)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        # Assigning imported functions as methods
        self.on_import_csv = types.MethodType(on_import_csv, self)
        self.on_exit = types.MethodType(on_exit, self)
        self.on_refresh = types.MethodType(on_refresh, self)
        self.on_preferences = types.MethodType(on_preferences, self)
        self.on_export = types.MethodType(on_export, self)
        self.on_import_excel = types.MethodType(on_import_task, self)
        self.on_browse = types.MethodType(on_browse, self)
        self.on_item_selected = types.MethodType(on_item_selected, self)
        self.on_file_activated = types.MethodType(on_file_activated, self)
        self.on_contact = types.MethodType(on_contact, self)
        self.on_about = types.MethodType(on_about, self)
        self.on_convert = types.MethodType(on_convert, self)

        # Initialize config
        self.config = wx.Config("Dateiablage")
        # Set default values if they do not exist
        if not self.config.HasEntry("user_choice"):
            self.config.Write("user_choice", "Alle")
        if not self.config.HasEntry("xml_import_enabled"):
            self.config.WriteBool("xml_import_enabled", True)
        if not self.config.HasEntry("srt_converter_enabled"):
            self.config.WriteBool("srt_converter_enabled", True)

        # Definition of global variables
        self.file_path_tasks = []

        # Creating a menu bar
        menu_bar = wx.MenuBar()

        # Creating the `Datei` menu
        file_menu = wx.Menu()
        import_definition = file_menu.Append(wx.ID_ANY, "&Importiere e-Learning Definition")
        import_tasks = file_menu.Append(wx.ID_ANY, "&Wähle Aufgabenliste")
        browse_item = file_menu.Append(wx.ID_OPEN, "&Wähle Quellverzeichnis")
        exit_app = file_menu.Append(wx.ID_EXIT, "&Beenden")
        menu_bar.Append(file_menu, "&Datei")
        
        # Creating the `Bearbeiten` menu
        edit_menu = wx.Menu()
        export_file_list = edit_menu.Append(wx.ID_ANY, "Exportiere Dateiliste")
        convert_srt_in_vtt = edit_menu.Append(wx.ID_ANY, "Konvertiere srt in vtt")
        refresh_ctrl_lists = edit_menu.Append(wx.ID_ANY, "Aktualisieren")
        preferences = edit_menu.Append(wx.ID_PREFERENCES, "Einstellungen")
        menu_bar.Append(edit_menu, "&Bearbeiten")

        # Creating the `Hilfemenü` menu
        help_menu = wx.Menu()
        help_contact = help_menu.Append(wx.ID_ANY, "&Kontakt") # Information on how users can receive support.
        help_about = help_menu.Append(wx.ID_ANY, "&Über die App") # Information about the application.

        menu_bar.Append(help_menu, "&Hilfe")

        # Setting the menu bar
        self.SetMenuBar(menu_bar)

        # Creating a panel
        panel = wx.Panel(self)

        # Creating a vertical box sizer
        vbox_learning = wx.BoxSizer(wx.VERTICAL)
        vbox_tasks = wx.BoxSizer(wx.VERTICAL)

        # Creating the list controls
        self.learning_ctrl = wx.ListCtrl(panel,
                                     style=wx.LC_REPORT
                                     |wx.BORDER_SUNKEN|wx.LIST_ALIGN_SNAP_TO_GRID)
        
        
        self.tasks_ctrl = wx.ListCtrl(panel,
                                     style=wx.LC_LIST
                                     |wx.BORDER_SUNKEN|wx.LIST_ALIGN_SNAP_TO_GRID
                                     )
        self.file_listbox = wx.ListBox(panel)

        # Titles for the controls
        learning_title = wx.StaticText(panel, label="E-learning", style=wx.ALIGN_LEFT)
        task_title = wx.StaticText(panel, label="Aufgaben", style=wx.ALIGN_RIGHT)
        explorer_title = wx.StaticText(panel, label="Dateien und Ordner", style=wx.ALIGN_LEFT)

        # Setting font style
        learning_title.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        task_title.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        explorer_title.SetFont(wx.Font(wx.FontInfo(12).Bold()))

        # Creating a horizontal box sizer
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Adding the list controls to the horizontal box sizer
        vbox_learning.Add(learning_title, 0, wx.ALL | wx.LEFT, 5)
        vbox_learning.Add(self.learning_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        vbox_tasks.Add(task_title, 0, wx.ALL | wx.RIGHT, 5)
        vbox_tasks.Add(self.tasks_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        hbox.Add(vbox_learning, 1, wx.EXPAND)
        hbox.Add(vbox_tasks, 1, wx.EXPAND)

        # Creating a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Adding the horizontal box sizer and the file listbox to the vertical box sizer
        vbox.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(explorer_title, 0, wx.ALL | wx.LEFT, 5)
        vbox.Add(self.file_listbox, 1, wx.ALL | wx.EXPAND, 5)

        # Setting the sizer for the frame and fit the panel
        panel.SetSizer(vbox)

        # Binding the Import menu item to the on_import method
        self.Bind(wx.EVT_MENU, self.on_import_csv, import_definition)
        # Binding the Import menu item to the on_import method
        self.Bind(wx.EVT_MENU, self.on_import_excel, import_tasks)
        # Binding the Browse menu item to the on_browse method
        self.Bind(wx.EVT_MENU, self.on_browse, browse_item)
        # Bindung the Export menu item to the on_export method
        self.Bind(wx.EVT_MENU, self.on_export, export_file_list)
        # Binding the Exit menu item to the on_exit method
        self.Bind(wx.EVT_MENU, self.on_exit, exit_app)
        # Binding the Refresh menu item to the on_refresh method
        self.Bind(wx.EVT_MENU, self.on_refresh, refresh_ctrl_lists)
        # Binding the Preferences menu item to the on_preferences method
        self.Bind(wx.EVT_MENU, self.on_preferences, preferences)
        # Binding the Contact menu to the on_contact method
        self.Bind(wx.EVT_MENU, self.on_contact, help_contact)
        # Binding the über die App menu to the on_about method 
        self.Bind(wx.EVT_MENU, self.on_about, help_about)
        # Binding the Convert menu to the on_convert method
        self.Bind(wx.EVT_MENU, self.on_convert, convert_srt_in_vtt)    
        
        # Binding the list control to the on_item_activated method
        self.learning_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        # Binding the list control to the on_item_activated method
        self.tasks_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        # Binding the list control to the on_file_activated method
        self.file_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.on_file_activated)

# Creating the wx App
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="Dateiablage", size=(1024, 768))
        
        # Setting icon
        frame.Show(True)
        frame.SetIcon(wx.Icon("images/icon.ico", wx.BITMAP_TYPE_ICO))
        self.SetTopWindow(frame)
        return True

# Initializing the wx App
app = MyApp(False)
print("App start")
app.MainLoop()