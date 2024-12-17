import wx # wxPython / Phoenix

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
        self.user_choice = wx.Choice(panel, choices=["Asher", "Benjamin", "Larisa", "Listan", "Mahsa", "Marko", "Sandra"])
        sizer.Add(self.user_choice, 0, wx.ALL, 5)
        # Load saved state
        user_state = self.config.Read("user_choice", "Asher")
        self.user_choice.SetStringSelection(user_state)
        # Bind event to save state
        self.user_choice.Bind(wx.EVT_CHOICE, self.on_user_choice)

        # Adding preference control csv import
        heading_csv = wx.StaticText(panel, label="CSV Import Einstellungen")
        font = heading_csv.GetFont()
        font.PointSize += 2
        heading_csv.SetFont(font)
        sizer.Add(heading_csv, 0, wx.ALL, 5)
        # CSV Import checkbox
        self.csv_checkbox = wx.CheckBox(panel, label="CSV Import")
        sizer.Add(self.csv_checkbox, 0, wx.ALL, 5)
        # Load saved state
        csv_state = self.config.ReadBool("csv_import_enabled", False)
        self.csv_checkbox.SetValue(csv_state)
        # Bind event to save state
        self.csv_checkbox.Bind(wx.EVT_CHECKBOX, self.on_csv_checkbox)

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

        panel.SetSizer(sizer)
        return panel

    # Method to handle the Preferences page user choice
    def on_user_choice(self, event):
        self.config.Write("user_choice", self.user_choice.GetString(self.user_choice.GetSelection()))
        self.config.Flush()

    # Method to handle the Preferences page csv checkbox
    def on_csv_checkbox(self, event):
        self.config.WriteBool("csv_import_enabled", self.csv_checkbox.IsChecked())
        self.config.Flush()

    # Method to handle the Preferences page srt checkbox
    def on_srt_checkbox(self, event):
        self.config.WriteBool("srt_converter_enabled", self.srt_checkbox.IsChecked())
        self.config.Flush()