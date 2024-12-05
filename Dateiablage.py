import wx
import os
import subprocess
import platform
import unicodedata
import pandas as pd

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        # Creating a menu bar
        menu_bar = wx.MenuBar()

        # Creating the File menu
        file_menu = wx.Menu()
        import_item = file_menu.Append(wx.ID_OPEN, "&Importiere e-Learning Definition")
        browse_item = file_menu.Append(wx.ID_ANY, "&Wähle Quellverzeichnis")
        file_menu.Append(wx.ID_EXIT, "&Beenden")
        menu_bar.Append(file_menu, "&Datei")
        
        # Creating the Edit menu
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_COPY, "&Kopieren")
        edit_menu.Append(wx.ID_CUT, "&Ausscheniden")
        edit_menu.Append(wx.ID_PASTE, "&Einfügen")
        menu_bar.Append(edit_menu, "&Bearbeiten")

        # Setting the menu bar
        self.SetMenuBar(menu_bar)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(panel,
                                     style=wx.LC_REPORT
                                     |wx.BORDER_SUNKEN
                                     )
        self.file_listbox = wx.ListBox(panel)

        sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.file_listbox, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        # Binding the Import menu item to the on_import method
        self.Bind(wx.EVT_MENU, self.on_import, import_item)
        # Binding the Browse menu item to the on_browse method
        self.Bind(wx.EVT_MENU, self.on_browse, browse_item)

        # Binding the list control to the on_item_activated method
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        # Binding the list control to the on_file_activated method
        self.file_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.on_file_activated)

    # Method to handle the Browse menu item
    def on_browse(self, event):
        dialog = wx.DirDialog(None, "Select a folder:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.folder_path = dialog.GetPath()  # folder_path will contain the path of the folder you have selected as string
            self.list_files(self.folder_path)
        dialog.Destroy()

    # Method to handle the Import menu item
    def on_import(self, event):
        dialog = wx.FileDialog(self, "Importiere e-Learning Definition", wildcard="CSV files (*.csv)|*.csv|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            self.import_file(file_path)
        dialog.Destroy()

    # Method to import the CSV file
    def import_file(self, file_path):
        try:
            wx.MessageBox(f"Datei erfolgreich importiert: {file_path}", "Success", wx.OK | wx.ICON_INFORMATION)
            definition_csv = pd.read_csv(file_path)
            self.display_data(definition_csv)
        except Exception as e:
            wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Method to display the data in the list control
    def display_data(self, df):
        self.list_ctrl.ClearAll()
        self.list_ctrl.AppendColumn("e-Learning Struktur")

        for index, row in df.iterrows():
            text = row.iloc[0]
            level = row.iloc[1]
            indent = ' ' * ((level * 4) - 4)  # Indent based on the level
            self.list_ctrl.Append([f"{indent}{text}"])

        # Adjusting the column width to fit automatically the content
        self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    # Method to handle the list control item activated event
    def on_item_selected(self, event):
        item_index = event.GetIndex()
        item_text = self.list_ctrl.GetItemText(item_index)
        self.SetTitle(f"Dateiablage - {item_text.strip()}")
        self.list_files(self.folder_path, item_text.strip())
        
    # Method to handle the list control item activated event
    def on_file_activated(self, event):
        file_index = event.GetSelection()
        file_path = self.file_listbox.GetString(file_index)

        if platform.system() == "Windows":
            try:
                os.startfile(f'"{file_path}"')
            except Exception as e:
                wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
        elif platform.system() == "Darwin":  # macOS
            try:
                subprocess.call(["open", file_path])
            except Exception as e:
                wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
        else:  # Linux
            try:
                subprocess.call(["xdg-open", file_path])
            except Exception as e:
                wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
        

    # Method to list the files in the selected folder
    def list_files(self, folder_path, filter_text=None):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for name in dirs:
                dir_path = os.path.join(root, name)
                if filter_text is None:
                    file_list.append(dir_path)
                    files = [
                        f 
                        for f in os.listdir(dir_path)
                    ]
                    file_list.extend(os.path.join(dir_path, f) for f in files)
                else:
                    # Adding all subdirectories of the matching directory
                    normalized_filter_text = unicodedata.normalize('NFC', filter_text)
                    normalized_name = unicodedata.normalize('NFC', name)
                    if normalized_filter_text in normalized_name:
                        for sub_root, sub_dirs, sub_files in os.walk(dir_path):
                            for sub_name in sub_dirs:
                                dir_path = os.path.join(sub_root, sub_name)
                                file_list.append(os.path.join(sub_root, sub_name))
                                sub_files = [
                                    f 
                                    for f in os.listdir(dir_path)
                                ]
                                file_list.extend(os.path.join(dir_path, f) for f in sub_files)

            self.file_listbox.Set(file_list)

# Creating the wx App
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="Dateiablage", size=(1024, 768))
        frame.Show(True)
        return True

# Initializing the wx App
app = MyApp(False)
app.MainLoop()