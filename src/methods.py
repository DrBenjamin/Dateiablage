import wx
import io
from docx import Document
from src.files import list_files
from src.tasks import on_import_tasks
from src.learning import display_learning
import os
import webbrowser

# Method to handle the right click event
def on_right_click(self, event):
    # Create the context menu
    menu = wx.Menu()
    open_item = menu.Append(wx.ID_ANY, "Öffnen")
    copy_path = menu.Append(wx.ID_ANY, "Kopiere Pfad")
    convert_item = menu.Append(wx.ID_ANY, "Konvertiere srt in vtt")

    # Binding handlers
    self.Bind(wx.EVT_MENU, self.on_file_activated, open_item)
    self.Bind(wx.EVT_MENU, self.on_copy_path, copy_path)
    self.Bind(wx.EVT_MENU, self.on_convert, convert_item)

    # Show the menu
    self.PopupMenu(menu, event.GetPosition())
    menu.Destroy()

# Method to handle the Copy Path menu item
def on_copy_path(self, event):
    if self.file_path is not None:
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(wx.TextDataObject(self.file_path))
        wx.TheClipboard.Close()
    else:
        wx.MessageBox("Keine Datei ausgewählt", "Error", wx.OK | wx.ICON_ERROR)

# Method to handle the Convert menu item
def on_convert(self, event):
    try:
        if self.file_path.endswith(".srt"):
            convert_srt_to_vtt(self.file_path, overwrite = self.config.ReadBool("srt_converter_overwrite"))
        else:
            wx.MessageBox("Dateiendung wird nicht unterstützt", "Error", wx.OK | wx.ICON_ERROR)
    except Exception as e:
        wx.MessageBox(f"Datei konnte nicht konvertiert werden: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to convert srt into vtt 
def convert_srt_to_vtt(file_path, overwrite = False):
    vtt_file_path = file_path.rsplit(".", 1)[0] + ".vtt"

    if os.path.exists(vtt_file_path):
        file_name = os.path.basename(vtt_file_path)
        if not overwrite:
            response = wx.MessageBox(
                f"Die Datei '{file_name}' existiert bereits. Möchten Sie sie ersetzen?",
                "Datei existiert",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if response == wx.NO:
                return

        os.remove(vtt_file_path)

    with open(file_path, "r") as f, open(vtt_file_path, "w") as vtt_file:
        vtt_file.write("WEBVTT\n\n")
        first_line = True
        for line in f:
            if first_line:
                first_line = False # skip the first line
                continue
            if line.strip().isdigit():  # skip rows wth digits
                continue
            if "-->" in line:  # convert time format "," into "."
                line = line.replace(",", ".")
            vtt_file.write(line)

    file_name = os.path.basename(vtt_file_path)
    wx.MessageBox(
        f"Die Datei wurde erfolgreich konvertiert und gespeichert als:\n{file_name}",
        "Erfolg",
        wx.OK | wx.ICON_INFORMATION
    )

# Method to handle `Über die App` menu item
def on_about(self, event):
    # Creating a new user-defined window
    frame = wx.Frame(None, title="Über die App", size=(500, 400))
    panel = wx.Panel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)

    # Adding message
    message = (
        "Name der Anwendung:\n"
        "Dateiablage\n\n"
        "Versionsnummer:\n"
        "0.1.0\n\n"
        "Das Unternehmen:\n"
        "CompuGroup Medical\n\n"
        "**** Beschreibung ****\n"
        "Die Dateiablage ist eine Anwendung zur unkomplizierten Verwaltung von "
        "e-Learning-Inhalten und Aufgaben für das medizinische Personal.\n\n"
        "**** Support ****\n"
        "Bei Fragen oder technischen Problemen kontaktieren Sie bitte unseren Support.\n\n"
    )
    message_label = wx.StaticText(panel, label=message)
    sizer.Add(message_label, 0, wx.ALL, 10)

    # Adding web link to support page
    support_label = wx.StaticText(panel, label="Weitere Informationen finden Sie auf unserer Support-Seite.")
    support_label.SetForegroundColour((0, 0, 255))  # Link-Farbe (Blau)
    font = support_label.GetFont()
    font.SetUnderlined(True)  # Unterstrichen hinzufügen
    support_label.SetFont(font)

    # Adding click event for the link
    support_label.Bind(wx.EVT_LEFT_DOWN, lambda event: webbrowser.open("https://www.cgm.com/corp_de/unternehmen/kontakt.html"))
    sizer.Add(support_label, 0, wx.ALL, 10)

    # Adding message
    thanks_label = wx.StaticText(panel, label="Vielen Dank, dass Sie unsere Anwendung verwenden!")
    thanks_label.SetForegroundColour((0, 128, 0))  # Grüne Farbe für Freundlichkeit
    sizer.Add(thanks_label, 0, wx.ALL, 10)

    # Setting sizer and display window
    panel.SetSizer(sizer)
    frame.Show()

# Method to handle the Contact menu item
def on_contact(self, event):
    mailto_link = "mailto:support-dateiablage@cgm.com?subject=Supportanfrage&body=Hallo%20Support-Team"
    wx.LaunchDefaultBrowser(mailto_link)

# Method to handle the Refresh menu item
def on_refresh(self, event):
    # Clear the ctrl lists
    self.learning_ctrl.DeleteAllItems()
    self.tasks_ctrl.DeleteAllItems()

    # Refresh the ctrl lists
    try:
        if self.folder_path is not None:
            list_files(self, self.folder_path)
    except Exception as e:
        print(f"Error: {e}")
    try:
        if self.definition_csv is not None:
            display_learning(self, self.definition_csv)
    except Exception as e:
        print(f"Error: {e}")
    try:
        if self.df_tasks is not None:
            on_import_tasks(self, None)
    except Exception as e:
        print(f"Error: {e}")

# Method to handle the Export file list
def on_export(self, event):
    export_docx(self, self.file_list)

# Method to export the file list to a Word document
def export_docx(self, data):
    document = Document()

    # Adding header
    document.add_heading('Dateiliste', 0)
    paragraph = document.add_paragraph()
    paragraph.add_run(data)
    document.add_page_break()

    ## Creating a Word file using python-docx as engine
    buffer = io.BytesIO()
    document.save(buffer)
    with open("Export_Dateiliste.docx", "wb") as docx_file:
        docx_file.write(buffer.getvalue())
    buffer.close()

# Method to handle the Exit menu item
def on_exit(self, event):
    self.Close(True)