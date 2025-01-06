import wx
import io
from docx import Document
from src.files import list_files
from src.tasks import import_excel
from src.learning import display_learning

# Method to handle the right click event
def on_right_click(self, event):
    # Create the context menu
    menu = wx.Menu()
    open_item = menu.Append(wx.ID_ANY, "Öffne Datei / Ordner")
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
            convert_srt_to_vtt(self.file_path)
        else:
            wx.MessageBox("Dateiendung wird nicht unterstützt", "Error", wx.OK | wx.ICON_ERROR)
    except Exception as e:
        wx.MessageBox(f"Datei konnte nicht konvertiert werden: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to convert srt into vtt 
def convert_srt_to_vtt(file_path):
    with open(file_path, "r") as f:
        buffer_vtt = io.StringIO()
        buffer_vtt.write("WEBVTT\n\n")
        for line in f:
            if line.strip().isdigit():
                continue
            if "-->" in line:
                line = line.replace(",", ".")
            buffer_vtt.write(line)

        ## To-Do
        #  - Write the converted content to a new file with same name and path
        #    but different extension e.g. (`subtile.srt`` to `subtitle.vtt`)
        #  - Checking if there is already a file with the same name
        #    and ask the user if they want to overwrite it
        print(buffer_vtt.getvalue())

# Method to handle `Über die App` menu item
def on_about(self, event):
    message = (
        "Name der Anwendung:\n" 
        "Dateiablage\n\n"
        "Versionsnummer:\n" 
        "0.1.0\n\n"
        "Das Unternehmen:\n" 
        "© CompuGroup Medical\n\n"
        "**** Beschreibung ****\n"
        "Die Dateiablage ist eine Anwendung zur unkomplizierten Verwaltung von e-Learning-Inhalten und Aufgaben für das medizinische Personal.\n\n"
        "**** Support ****\n"
        "Bei Fragen oder technischen Problemen kontaktieren Sie bitte unseren Support unter:\n"
        "support-dateiablage@cgm.com\n\n"
    )
    wx.MessageBox(message, "Über die App ", wx.OK | wx.ICON_INFORMATION)

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
        if self.file_path_tasks is not None:
            import_excel(self, self.file_path_tasks)
    except Exception as e:
        print(f"Error: {e}")

# Method to handle the Exit menu item
def on_exit(self, event):
    self.Close(True)

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