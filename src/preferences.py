import wx # wxPython / Phoenix
import subprocess
import src.globals as g

# Method to handle the Preferences menu item
def on_preferences(self, event):
    dialog = wx.PreferencesEditor()
    dialog.AddPage(PreferencesPage(self.config))
    self.preferences_dialog = dialog
    dialog.Show(self)

class PreferencesPage(wx.StockPreferencesPage):
    def __init__(self, config):
        super().__init__(wx.StockPreferencesPage.Kind_General)
        self.config = config

    def GetName(self):
        return "Einstellungen"

    def GetIcon(self):
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_HELP_SIDE_PANEL, wx.ART_OTHER, (32, 32))
        return wx.BitmapBundle.FromBitmap(bitmap)

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Adding preference control user settings
        heading_user = wx.StaticText(panel, label="Jira")
        font = heading_user.GetFont()
        font.PointSize += 2
        heading_user.SetFont(font)
        sizer.Add(heading_user, 0, wx.ALL, 5)
        # User choice
        sizer.Add(wx.StaticText(panel,
                                    label=f'Tickets für welchen User anzeigen?'),0, wx.ALL, 5)
        self.user_choice = wx.Choice(panel, choices=["Alle", "Asher", "Benjamin", "Kanjo", "Larisa", "Listan", "Mahsa", "Marko", "Sandra M.", "Christian.Weingartner@cgm.com"])
        sizer.Add(self.user_choice, 0, wx.ALL, 5)
        # Load saved state
        user_state = self.config.Read("user_choice", "Alle")
        self.user_choice.SetStringSelection(user_state)
        # Bind event to save state
        self.user_choice.Bind(wx.EVT_CHOICE, self.on_user_choice)
        
        # Ticket status choice
        sizer.Add(wx.StaticText(panel,
                                    label=f'Tickets mit welchem Status anzeigen?'),0, wx.ALL, 5)
        self.status_choice = wx.Choice(panel, choices=["Alle", "Fertig", "In Bearbeitung", "Neu"])
        sizer.Add(self.status_choice, 0, wx.ALL, 5)
        # Load saved state
        status_state = self.config.Read("status_choice", "Alle")
        self.status_choice.SetStringSelection(status_state)
        # Bind event to save state
        self.status_choice.Bind(wx.EVT_CHOICE, self.on_status_choice)

        # Adding preference control XML import
        heading_xml = wx.StaticText(panel, label="Import")
        font = heading_xml.GetFont()
        font.PointSize += 2
        heading_xml.SetFont(font)
        sizer.Add(heading_xml, 0, wx.ALL, 5)
        # XML Import checkbox
        sizer.Add(wx.StaticText(panel,
                                    label=f'XML-Dateien statt Exceldokument für organisatorische Aufgaben?'),0, wx.ALL, 5)
        self.xml_checkbox = wx.CheckBox(panel, label="XML Datei(en) verwenden!")
        sizer.Add(self.xml_checkbox, 0, wx.ALL, 5)
        # Load saved state
        xml_state = self.config.ReadBool("xml_import_enabled", False)
        self.xml_checkbox.SetValue(xml_state)
        # Bind event to save state
        self.xml_checkbox.Bind(wx.EVT_CHECKBOX, self.on_xml_checkbox)

        # XML Import for JIRA Tickets checkbox
        sizer.Add(wx.StaticText(panel,
                                    label=f'Einzelne Datei statt eine Datei pro Ticket verwenden?'),0, wx.ALL, 5)
        self.xml_checkbox_jira = wx.CheckBox(panel, label="Eine Datei mit allen Tickets importieren!")
        sizer.Add(self.xml_checkbox_jira, 0, wx.ALL, 5)
        # Load saved state
        xml_state_jira = self.config.ReadBool("xml_import_one_file", False)
        self.xml_checkbox_jira.SetValue(xml_state_jira)
        # Bind event to save state
        self.xml_checkbox_jira.Bind(wx.EVT_CHECKBOX, self.on_xml_jira_checkbox)

        # Adding preference control srt converter
        heading = wx.StaticText(panel, label="Untertitel Konverter")
        font = heading.GetFont()
        font.PointSize += 2
        heading.SetFont(font)
        sizer.Add(heading, 0, wx.ALL, 5)
        # SRT Konverter checkbox
        sizer.Add(wx.StaticText(panel,
                                    label=f'Automatisches Überschreiben vorhandener `VTT`-Dateien?'),0, wx.ALL, 5)
        self.srt_checkbox = wx.CheckBox(panel, label="Automatisches Überschreiben aktivieren!")
        sizer.Add(self.srt_checkbox, 0, wx.ALL, 5)
        # Load saved state
        srt_state = self.config.ReadBool("srt_converter_overwrite", False)
        self.srt_checkbox.SetValue(srt_state)
        # Bind event to save state
        self.srt_checkbox.Bind(wx.EVT_CHECKBOX, self.on_srt_checkbox)

        # Adding preference control Drive mapping
        if wx.Platform == "__WXMSW__":
            heading_drive = wx.StaticText(panel, label="Virtuelles Laufwerk")
            font = heading_drive.GetFont()
            font.PointSize += 2
            heading_drive.SetFont(font)
            sizer.Add(heading_drive, 0, wx.ALL, 5)
            # Drive mapping checkbox
            self.drive_checkbox = wx.CheckBox(panel, label="Laufwerk mappen!")
            sizer.Add(self.drive_checkbox, 0, wx.ALL, 5)
            # Load saved state
            drive_state = self.config.ReadBool("drive_mapping_enabled", False)
            self.drive_checkbox.SetValue(drive_state)
            # Bind event to save state
            self.drive_checkbox.Bind(wx.EVT_CHECKBOX, self.on_drive_checkbox)
            # Showing drive letter
            if self.drive_checkbox.IsChecked() and self.config.Read("drive_mapping_letter") != "":
                sizer.Add(wx.StaticText(panel,
                                        label=f'Laufwerk {self.config.Read("drive_mapping_letter")} wurde gemappt.'),
                        0, wx.ALL, 5)
            else:
                sizer.Add(wx.StaticText(panel,
                                        label='Kein Laufwerk gemappt.'),
                        0, wx.ALL, 5)

        # Setting the sizer for the panel
        panel.SetSizer(sizer)
        return panel

    # Method to handle the Preferences page user choice
    def on_user_choice(self, event):
        self.config.Write("user_choice", self.user_choice.GetString(self.user_choice.GetSelection()))
        self.config.Flush()

    # Method to handle the Preferences page user choice
    def on_status_choice(self, event):
        self.config.Write("status_choice", self.status_choice.GetString(self.status_choice.GetSelection()))
        self.config.Flush()

    # Method to handle the Preferences page xml checkbox
    def on_xml_checkbox(self, event):
        self.config.WriteBool("xml_import_enabled", self.xml_checkbox.IsChecked())
        self.config.Flush()

    # Method to handle the Preferences page xml checkbox
    def on_xml_jira_checkbox(self, event):
        self.config.WriteBool("xml_import_one_file", self.xml_checkbox_jira.IsChecked())
        self.config.Flush()

    # Method to handle the Preferences page srt checkbox
    def on_srt_checkbox(self, event):
        self.config.WriteBool("srt_converter_overwrite", self.srt_checkbox.IsChecked())
        self.config.Flush()

    # Method to handle the Preferences page Drive mapping checkbox
    def on_drive_checkbox(self, event):
        if self.drive_checkbox.IsChecked():
            self.config.WriteBool("drive_mapping_enabled", self.drive_checkbox.IsChecked())
            self.config.Flush()
            g.mapping = True
        else:
            try:
                # Unmapping the drive
                subprocess.run(['subst', '/d', f"{self.config.Read('drive_mapping_letter')}:"])

                # Deleting the registry entry `Virtual Drive`
                subprocess.run(["reg", "delete", "HKCU\Software\Microsoft\Windows\CurrentVersion\Run", "/v", "Virtual Drive", "/f"])

                # Setting the variable to default value
                self.config.WriteBool("drive_mapping_enabled", self.drive_checkbox.IsChecked())
                self.config.Write("drive_mapping_letter", "")
                self.config.WriteBool("drive_mapping_enabled", self.drive_checkbox.IsChecked())
                self.config.Flush()
            except FileNotFoundError:
                pass
