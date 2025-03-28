## Description: This file contains the main class of the application.
## `Dateiablage.py`
## Modules
import wx # wxPython / Phoenix
import types
import src.globals as g
from src.methods import (
    on_right_click,
    on_copy_path,
    on_convert,
    on_refresh,
    on_about,
    on_contact,
    on_export,
    on_exit,
    on_check_completeness
)
from src.learning import (
    on_import_csv,
    on_elearning_item_selected,
    on_elearning_item_activated
)
from src.tasks import (
    on_import_tasks_from_csv,
    on_import_tasks,
    on_task_item_selected,
    on_task_item_activated
)
from src.files import (
    on_import_files,
    on_date_to_files,
    on_create_folder_structure,
    on_browse_source,
    on_browse_jira,
    on_file_selected,
    on_file_activated
)
from src.creator import on_new_elearning
from src.preferences import on_preferences

# Method to handle the Create e-Learning
def on_import_jira(self, event = None):
    # Calling the `on_browse_jira` method
    self.on_browse_jira(event)

    # Calling the `on_create_folder_structure` method
    self.on_create_folder_structure(event)

    # Calling the `on_browse_source` method
    self.on_browse_source(event, g.folder_path)
    self.SetTitle(f"Dateiablage - {g.root_folder_name}")

    # Calling the `on_import_csv` method
    self.on_import_csv(event, g.file_path_elearning)
    g.file_path_elearning = None

    # Calling the `on_import_tasks` method
    self.on_import_tasks(None)

# Method to handle the Preferences menu item
def on_preferences_open(self, event):
    # Calling the `on_preferences` method
    self.on_preferences(event)

    # Calling the `on_browse_source` method
    if g.mapping:
        self.on_browse_source(event)
        g.mapping = False

# Method to handle the file renmaing
def on_date_to_files_refresh(self, event):
    # Calling the `on_date_to_files` method
    self.on_date_to_files(event)

    # Calling the `on_refresh` method
    self.on_refresh(event)

# Method to handle the import files
def on_import_files_refresh(self, event):
    # Calling the `on_import_files` method
    self.on_import_files(event)

    # Calling the `on_refresh` method
    self.on_refresh(event)

## Creating the main frame
class MyFrame(wx.Frame):
    def __init__(self, parent, title, size, config):
        super(MyFrame, self).__init__(parent=parent, title=title, size=size)
        self.config = config

        ## Binding of methods from this file
        # Binding function as method to `self`
        self.on_import_jira = types.MethodType(on_import_jira, self)
        self.on_preferences_open = types.MethodType(on_preferences_open, self)
        self.on_date_to_files_refresh = types.MethodType(on_date_to_files_refresh, self)
        self.on_import_files_refresh = types.MethodType(on_import_files_refresh, self)

        ## Binding functions from other files as methods to `self`
        # Methods from `methods.py`
        self.on_check_completeness = types.MethodType(on_check_completeness, self)
        self.on_right_click = types.MethodType(on_right_click, self)
        self.on_copy_path = types.MethodType(on_copy_path, self)
        self.on_convert = types.MethodType(on_convert, self)
        self.on_about = types.MethodType(on_about, self)
        self.on_contact = types.MethodType(on_contact, self)
        self.on_refresh = types.MethodType(on_refresh, self)
        self.on_export = types.MethodType(on_export, self)
        self.on_exit = types.MethodType(on_exit, self)

        # Methods from `learning.py`
        self.on_import_csv = types.MethodType(on_import_csv, self)
        self.on_elearning_item_selected = types.MethodType(on_elearning_item_selected, self)
        self.on_elearning_item_activated = types.MethodType(on_elearning_item_activated, self)

        # Methods from `tasks.py`
        self.on_import_tasks_from_csv = types.MethodType(on_import_tasks_from_csv, self)
        self.on_import_tasks = types.MethodType(on_import_tasks, self)
        self.on_task_item_selected = types.MethodType(on_task_item_selected, self)
        self.on_task_item_activated = types.MethodType(on_task_item_activated, self)

        # Methods from `files.py`
        self.on_import_files = types.MethodType(on_import_files, self)
        self.on_date_to_files = types.MethodType(on_date_to_files, self)
        self.on_create_folder_structure = types.MethodType(on_create_folder_structure, self)
        self.on_browse_source = types.MethodType(on_browse_source, self)
        self.on_browse_jira = types.MethodType(on_browse_jira, self)
        self.on_file_selected = types.MethodType(on_file_selected, self)
        self.on_file_activated = types.MethodType(on_file_activated, self)

        # Methods from `creator.py`
        self.on_new_elearning = types.MethodType(on_new_elearning, self)

        # Method from `preferences.py`
        self.on_preferences = types.MethodType(on_preferences, self)

        ## Creating a menu bar
        menu_bar = wx.MenuBar()

        ## Creating the `Datei` menu
        file_menu = wx.Menu()
        import_definition = file_menu.Append(wx.ID_ANY, "&Wähle e-Learning Definition")
        import_tasks = file_menu.Append(wx.ID_ANY, "&Wähle organisatorische Aufgaben")
        browse_item = file_menu.Append(wx.ID_ANY, "&Wähle Quellverzeichnis")
        file_menu.AppendSeparator()
        exit_app = file_menu.Append(wx.ID_EXIT, "&Beenden")
        menu_bar.Append(file_menu, "&Datei")

        ## Creating the `Bearbeiten` menu
        edit_menu = wx.Menu()
        file_date = edit_menu.Append(wx.ID_ANY, "Datum zum Dateinamen")
        check_messing_files = edit_menu.Append(wx.ID_ANY, "Vollständigkeitsprüfung")
        edit_menu.AppendSeparator()
        copy_path = edit_menu.Append(wx.ID_ANY, "Kopiere Pfad")
        refresh_ctrl_lists = edit_menu.Append(wx.ID_ANY, "Aktualisieren")
        edit_menu.AppendSeparator()
        preferences = edit_menu.Append(wx.ID_PREFERENCES, "Einstellungen")
        menu_bar.Append(edit_menu, "&Bearbeiten")

        ## Creating the `Inhaltserstellung` menu
        content_menu = wx.Menu()
        folder_structure = content_menu.Append(wx.ID_ANY, "Erstelle e-Learning aus JIRA")
        new_elearning = content_menu.Append(wx.ID_ANY, "Erstelle neues e-Learning")
        folder_content = content_menu.Append(wx.ID_ANY, "Importiere Inhalte")
        content_menu.AppendSeparator()
        convert_srt_in_vtt = content_menu.Append(wx.ID_ANY, "Konvertiere Untertitel")
        export_file_list = content_menu.Append(wx.ID_ANY, "Exportiere Dateiliste")
        menu_bar.Append(content_menu, "&Inhaltserstellung")

        ## Creating the `Hilfemenü` menu
        help_menu = wx.Menu()
        help_contact = help_menu.Append(wx.ID_ANY, "&Kontakt")
        help_about = help_menu.Append(wx.ID_ANY, "&Über die App")
        menu_bar.Append(help_menu, "&Hilfe")

        ## Setting the menu bar
        self.SetMenuBar(menu_bar)
        font = wx.Font(
                        12,
                        wx.FONTFAMILY_DEFAULT,
                        wx.FONTSTYLE_NORMAL,
                        wx.FONTWEIGHT_BOLD
                       )
        try:
            menu_bar.SetFont(font)
        except Exception as e:
            print(e)

        ## Creating a panel
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)

        ## Creating a vertical box sizer
        vbox_learning = wx.BoxSizer(wx.VERTICAL)
        vbox_tasks = wx.BoxSizer(wx.VERTICAL)

        ## Creating the list controls
        self.learning_ctrl = wx.ListCtrl(
                                            self.panel,
                                            style=wx.LC_REPORT
                                            |wx.BORDER_SUNKEN
                                            |wx.LIST_ALIGN_SNAP_TO_GRID
                                        )

        self.tasks_ctrl = wx.ListCtrl(
                                        self.panel,
                                        style=wx.LC_LIST
                                        |wx.BORDER_SUNKEN|wx.LIST_ALIGN_SNAP_TO_GRID
                                     )
        self.file_listbox = wx.ListBox(self.panel)

        ## Adding titles for the controls
        learning_title = wx.StaticText(self.panel,
                                       label = "e-Learning",
                                       style = wx.ALIGN_LEFT)
        task_title = wx.StaticText(self.panel,
                                   label = "Aufgaben",
                                   style = wx.ALIGN_RIGHT)
        explorer_title = wx.StaticText(self.panel,
                                       label = "Dateien und Ordner",
                                       style = wx.ALIGN_LEFT)

        ## Setting font style
        learning_title.SetFont(wx.Font(wx.FontInfo(11).Bold()))
        task_title.SetFont(wx.Font(wx.FontInfo(11).Bold()))
        explorer_title.SetFont(wx.Font(wx.FontInfo(11).Bold()))

        ## changing the text color to blue for the titles
        learning_title.SetForegroundColour(wx.Colour(0, 51, 102))
        task_title.SetForegroundColour(wx.Colour(0, 51, 102))
        explorer_title.SetForegroundColour(wx.Colour(0, 51, 102))

        ## Creating a horizontal box sizer
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        ## Adding the list controls to the horizontal box sizer
        vbox_learning.Add(learning_title, 0, wx.ALL | wx.LEFT, 5)
        vbox_learning.Add(self.learning_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        vbox_tasks.Add(task_title, 0, wx.ALL | wx.RIGHT, 5)
        vbox_tasks.Add(self.tasks_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        hbox.Add(vbox_learning, 1, wx.EXPAND)
        hbox.Add(vbox_tasks, 1, wx.EXPAND)

        ## Creating a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        ## Adding the horizontal box sizer and the file listbox to the vertical box sizer
        vbox.Add(hbox, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(explorer_title, 0, wx.ALL | wx.LEFT, 5)
        vbox.Add(self.file_listbox, 1, wx.ALL | wx.EXPAND, 5)

        ## Setting the sizer for the frame and fit the panel
        self.panel.SetSizer(vbox)

        ## Binding of `Datei` methods to menu items
        # Binding the Import CSV menu item to the `on_import_csv`` method
        self.Bind(wx.EVT_MENU, self.on_import_csv, import_definition)
        # Binding the Import tasks menu item to the `on_import_task` method
        self.Bind(wx.EVT_MENU, self.on_import_tasks_from_csv, import_tasks)
        # Binding the Browse menu item to the `on_browse_source` method
        self.Bind(wx.EVT_MENU, self.on_browse_source, browse_item)
        # Binding the Exit menu item to the on_exit method
        self.Bind(wx.EVT_MENU, self.on_exit, exit_app)

        ## Binding of `Bearbeiten` methods to menu items
        # Binding the add date to file menu item to the `on_date_to_file` method
        self.Bind(wx.EVT_MENU, self.on_date_to_files_refresh, file_date)
        # Binding the Check Completeness menu item to the `on_check_completeness` method
        self.Bind(wx.EVT_MENU, self.on_check_completeness, check_messing_files)
        # Binding the Copy menu to the `on_copy` path method
        self.Bind(wx.EVT_MENU, self.on_copy_path, copy_path)
        # Binding the Refresh menu item to the on_refresh method
        self.Bind(wx.EVT_MENU, self.on_refresh, refresh_ctrl_lists)
        # Binding the Preferences menu item to the on_preferences method
        self.Bind(wx.EVT_MENU, self.on_preferences_open, preferences)

        ## Binding of `Inhaltserstellung` methods to menu items
        # Binding the Create e-Learning menu item to the `on_import_jira` method
        self.Bind(wx.EVT_MENU, self.on_import_jira, folder_structure)
        # Binding the Create new e-Learning menu item to the `on_new_elearning` method
        self.Bind(wx.EVT_MENU, self.on_new_elearning, new_elearning)
        # Binding the Import Content menu item to the `on_import_files` method
        self.Bind(wx.EVT_MENU, self.on_import_files_refresh, folder_content)
        # Binding the Convert menu to the `on_convert` method
        self.Bind(wx.EVT_MENU, self.on_convert, convert_srt_in_vtt)
        # Bindung the Export menu item to the `on_export` method
        self.Bind(wx.EVT_MENU, self.on_export, export_file_list)

        ## Binding of `Hilfemenü` methods to menu items
        # Binding the Contact menu to the on_contact method
        self.Bind(wx.EVT_MENU, self.on_contact, help_contact)
        # Binding the über die App menu to the on_about method 
        self.Bind(wx.EVT_MENU, self.on_about, help_about)

        ## Binding the right-click event
        self.file_listbox.Bind(wx.EVT_CONTEXT_MENU, self.on_right_click)

        ## Bindings of events
        # Binding the list control to the  `on_elearning_item_selected` and `on_elearning_item_activated` method
        self.learning_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_elearning_item_selected)
        self.learning_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_elearning_item_activated)
        # Binding the list control to the `on_task_item_selected` and `on_task_item_activated` method
        self.tasks_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_task_item_selected)
        self.tasks_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_task_item_activated)
        # Binding the list control to the on_file_selected method
        self.file_listbox.Bind(wx.EVT_LISTBOX, self.on_file_selected)
        # Binding the list control to the on_file_activated method
        self.file_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.on_file_activated)
        
        ## In MyFrame.__init__ after creating self.panel
        self.Bind(wx.EVT_SIZE, self.on_size)

    # Method to handle the size event
    def on_size(self, event):
        # Refreshing the panel to trigger on_paint
        self.panel.Refresh()
        event.Skip()

    # Method to handle the paint event
    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        bitmap = wx.Bitmap(r"./_internal/images/Hintergrund.png")
        panel_size = self.panel.GetSize()
        image = bitmap.ConvertToImage()
        image = image.Scale(panel_size.width, panel_size.height, wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(image)
        dc.DrawBitmap(scaled_bitmap, 0, 0, True)

## Creating the wx App
class MyApp(wx.App):
    def OnInit(self):
        ## Initializing config
        self.config = wx.Config("Dateiablage")

        # Setting default values if they do not exist
        if not self.config.HasEntry("user_choice"):
            self.config.Write("user_choice", "Alle")
        if not self.config.HasEntry("status_choice"):
            self.config.Write("status_choice", "Alle")
        if not self.config.HasEntry("xml_import_enabled"):
            self.config.WriteBool("xml_import_enabled", True)
        if not self.config.HasEntry("xml_import_one_file"):
            self.config.WriteBool("xml_import_one_file", True)
        if not self.config.HasEntry("srt_converter_overwrite"):
            self.config.WriteBool("srt_converter_overwrite", False)
        if not self.config.HasEntry("drive_mapping_enabled"):
            self.config.WriteBool("drive_mapping_enabled", False)
        if not self.config.HasEntry("drive_mapping_letter"):
            self.config.Write("drive_mapping_letter", "")
        if not self.config.HasEntry("date_today"):
            self.config.WriteBool("date_today", False)

        # Adding os specific settings
        if not wx.Platform == "__WXMSW__":
            self.config.WriteBool("drive_mapping_enabled", False)
            self.config.Write("drive_mapping_letter", "")

        ## Creating the frame
        frame = MyFrame(None, title = "Dateiablage",
                        size = (1024, 768),
                        config = self.config)

        ## Setting icon
        frame.Show(True)
        if wx.Platform == "__WXMAC__":
            frame.SetIcon(wx.Icon("_internal/images/icon.icns", wx.BITMAP_TYPE_ICON))
        else:
            frame.SetIcon(wx.Icon("_internal/images/icon.ico", wx.BITMAP_TYPE_ICO))

        self.SetTopWindow(frame)
        return True

## Initializing the wx App
app = MyApp(False)
print("App start")
app.MainLoop()
