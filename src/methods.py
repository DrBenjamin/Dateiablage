import wx
import io
from docx import Document
from src.files import list_files
from src.tasks import import_excel
from src.learning import display_learning

# Method to handle the Convert menu item
def on_contact(self, event):
    mailto_link = "mailto:benjamin.gross@partner.cgm.com?subject=Supportanfrage&body=Hallo%20Support-Team"
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