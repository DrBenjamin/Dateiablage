import wx # wxPython / Phoenix
import os
import subprocess

# Method to handle the Preferences menu item
def on_preferences(self, event):
    dialog = wx.PreferencesEditor()
    dialog.AddPage(PreferencesPage(self.config))
    dialog.Show(self)

class PreferencesPage(wx.PreferencesPage):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def GetName(self):
        return "Einstellungen"

    def GetIcon(self):
        return wx.BitmapBundle.FromBitmap(wx.Bitmap('images/preferences.png', wx.BITMAP_TYPE_PNG))

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Adding preference control user settings
        heading_user = wx.StaticText(panel, label="Benutzereinstellungen")
        font = heading_user.GetFont()
        font.PointSize += 2
        heading_user.SetFont(font)
        sizer.Add(heading_user, 0, wx.ALL, 5)
        # User choice
        self.user_choice = wx.Choice(panel, choices=["Alle", "Asher", "Benjamin", "Larisa", "Listan", "Mahsa", "Marko", "Sandra"])
        sizer.Add(self.user_choice, 0, wx.ALL, 5)
        # Load saved state
        user_state = self.config.Read("user_choice", "Alle")
        self.user_choice.SetStringSelection(user_state)
        # Bind event to save state
        self.user_choice.Bind(wx.EVT_CHOICE, self.on_user_choice)

        # Adding preference control XML import
        heading_xml = wx.StaticText(panel, label="XML Import Einstellungen")
        font = heading_xml.GetFont()
        font.PointSize += 2
        heading_xml.SetFont(font)
        sizer.Add(heading_xml, 0, wx.ALL, 5)
        # XML Import checkbox
        sizer.Add(wx.StaticText(panel,
                                    label=f'XML statt Excel für die Aufgaben verwenden?'),0, wx.ALL, 5)
        self.xml_checkbox = wx.CheckBox(panel, label="XML Dateien importieren")
        sizer.Add(self.xml_checkbox, 0, wx.ALL, 5)
        # Load saved state
        xml_state = self.config.ReadBool("xml_import_enabled", False)
        self.xml_checkbox.SetValue(xml_state)
        # Bind event to save state
        self.xml_checkbox.Bind(wx.EVT_CHECKBOX, self.on_xml_checkbox)

        # XML Import for JIRA Tickets checkbox
        sizer.Add(wx.StaticText(panel,
                                    label=f'Eine XML Datei statt einzelne JIRA Tickets verwenden?'),0, wx.ALL, 5)
        self.xml_checkbox_jira = wx.CheckBox(panel, label="XML nur eine Datei importieren")
        sizer.Add(self.xml_checkbox_jira, 0, wx.ALL, 5)
        # Load saved state
        xml_state_jira = self.config.ReadBool("xml_import_one_file", False)
        self.xml_checkbox_jira.SetValue(xml_state_jira)
        # Bind event to save state
        self.xml_checkbox_jira.Bind(wx.EVT_CHECKBOX, self.on_xml_jira_checkbox)

        # Adding preference control srt converter
        heading = wx.StaticText(panel, label="SRT Konverter Einstellungen")
        font = heading.GetFont()
        font.PointSize += 2
        heading.SetFont(font)
        sizer.Add(heading, 0, wx.ALL, 5)
        # SRT Konverter checkbox
        self.srt_checkbox = wx.CheckBox(panel, label="SRT Konverter")
        sizer.Add(self.srt_checkbox, 0, wx.ALL, 5)
        # Load saved state
        srt_state = self.config.ReadBool("srt_converter_enabled", False)
        self.srt_checkbox.SetValue(srt_state)
        # Bind event to save state
        self.srt_checkbox.Bind(wx.EVT_CHECKBOX, self.on_srt_checkbox)

        # Adding preference control Drive mapping
        heading_drive = wx.StaticText(panel, label="Virtuelles Laufwerk")
        font = heading_drive.GetFont()
        font.PointSize += 2
        heading_drive.SetFont(font)
        sizer.Add(heading_drive, 0, wx.ALL, 5)
        # Drive mapping checkbox
        self.drive_checkbox = wx.CheckBox(panel, label="Laufwerk mappen")
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
        self.config.WriteBool("srt_converter_enabled", self.srt_checkbox.IsChecked())
        self.config.Flush()

    # Method to handle the Preferences page Drive mapping checkbox
    def on_drive_checkbox(self, event):
        if not self.drive_checkbox.IsChecked():
            try:
                # Unmapping the drive
                subprocess.run(['subst', '/d', f"{self.config.Read('drive_mapping_letter')}:"])

                # Deleting the registry entry `Virtual Drive`
                subprocess.run(["reg", "delete", "HKCU\Software\Microsoft\Windows\CurrentVersion\Run", "/v", "Virtual Drive", "/f"])

                # Setting the variable to default value
                self.config.WriteBool("drive_mapping_enabled", self.drive_checkbox.IsChecked())
                self.config.Write("drive_mapping_letter", "")
            except FileNotFoundError:
                pass
        self.config.WriteBool("drive_mapping_enabled", self.drive_checkbox.IsChecked())
        self.config.Flush()
