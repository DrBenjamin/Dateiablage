## Description: This file contains the methods to handle the file operations in the application.
## `src/files.py`
## Modules
import wx
import os
import shutil
import subprocess
import platform
import pandas as pd
import datetime
import re
import html
import xml.etree.ElementTree as ET
import src.globals as g
from bs4 import BeautifulSoup

number_of_items = 0
jira_ticket = None

# Method to import files
def on_import_files(self, event):
    wildcard = "Alle Dateien (*.*)|*.*"  # Beispiel-Wildcard
    dialog = wx.FileDialog(self, "Bitte wählen Sie e-Learning-Dateien aus:",
        wildcard=wildcard,
        style=wx.FD_OPEN | wx.FD_MULTIPLE
    )
    if dialog.ShowModal() == wx.ID_OK:
        g.file_list_import = dialog.GetPaths()
    dialog.Destroy()

    # Copying the files to the target folder
    counter = 0
    for file_path in g.file_list_import:
        try:
            file_name = os.path.basename(file_path)
            _, suffix = os.path.splitext(file_name)
            file_name = f"{os.path.basename(g.folder_path_import)}{suffix}"
            new_file_path = os.path.join(g.folder_path_import, file_name)
            if os.path.isfile(new_file_path):
                wx.MessageBox(f'Datei "{file_name}" existiert bereits im Ziel-Ordner.',
                              "Error", wx.OK | wx.ICON_ERROR)
                continue
            shutil.copy2(file_path, new_file_path)
            counter += 1
        except Exception as e:
            wx.MessageBox(f'Datei "{file_name}" konnte nicht kopiert werden: {e}',
                          "Error", wx.OK | wx.ICON_ERROR)
    wx.MessageBox(f"{counter} Dateien wurden erfolgreich inmportiert.", "Information",
                    wx.OK | wx.ICON_INFORMATION)

# Method to add date to file names
def on_date_to_files(self, event):
    counter = 0
    for file_path in g.file_list:
        if not os.path.isfile(file_path):
            continue

        try:
            file_name = os.path.basename(file_path)
            if re.search(r"\d{4}-\d{2}-\d{2}", file_name): # skipping file names with date in it (e.g. 2021-01-01)
                continue
            if self.config.ReadBool("date_today"):
                file_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            else:
                file_date = os.path.getmtime(file_path)
                file_date_str = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d')
            
            # Splitting the filename into name and extension
            name, ext = os.path.splitext(file_name)
            
            # Creating the new filename with the date string before the extension
            new_file_name = f"{name}_{file_date_str}{ext}"
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
            os.rename(file_path, new_file_path)
            counter += 1
        except Exception as e:
            wx.MessageBox(f'Datei "{name}" konnte nicht umbenannt werden: {e}',
                          "Error", wx.OK | wx.ICON_ERROR)
    wx.MessageBox(f"{counter} Dateien wurden erfolgreich umbenannt.", "Information",
                  wx.OK | wx.ICON_INFORMATION)

# Method to create the folder structur
def on_create_folder_structure(self, event):
    on_browse_target(self, event)
    file_path_jira = []
    if self.config.ReadBool("xml_import_one_file"):
        file_path_jira.append(g.folder_path_jira[0])
    else:
        for name in os.listdir(g.folder_path_jira):
            file_path = os.path.join(g.folder_path_jira, name)
            if os.path.isfile(file_path) and name.endswith(".xml"):
                file_path_jira.append(file_path)
    import_xml(self, file_path_jira)

# Method to handle the Browse menu item
def on_browse_source(self, event, folder_path = None):
    if folder_path is None:
        dialog = wx.DirDialog(None, "Wähle einen Quell-Ordner (e-Learnings) aus:",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            g.folder_path = dialog.GetPath()
        dialog.Destroy()
    else:
        g.folder_path = folder_path
    if self.config.ReadBool("drive_mapping_enabled", True):
        if self.config.Read("drive_mapping_letter") == "":
            letters = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            for letter in letters:
                if os.path.exists(f"{letter}:"):
                    continue
                else:
                    try:
                        # Mapping the folder to drive letter
                        subprocess.run(['subst', f"{letter}:", g.folder_path],
                                    check=True)

                        # Writing registry file
                        with open(f"{g.folder_path}\\MapVirtualDrive.reg", "w") as f:
                            path_to_folder = g.folder_path.replace("\\", "\\\\")
                            f.write(
f"""Windows Registry Editor Version 5.00\n\n\
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]
"Virtual Drive"="subst {letter}: \\"{path_to_folder}\\""
""")

                        # Importing registry file
                        subprocess.run(["regedit", "/s",
                                        f"{g.folder_path}\\MapVirtualDrive.reg"],
                                       check = True)
                    except:
                        continue
                    self.config.Write("drive_mapping_letter", letter)
                    break
            list_files(self, f'{self.config.Read("drive_mapping_letter")}:\\')
            return
        list_files(self, g.folder_path)
    else:
        list_files(self, g.folder_path)

# Method to handle the Browse menu item
def on_browse_target(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ziel-Ordner aus:",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        g.folder_path_elearning = dialog.GetPath()

# Method to handle the Import tasks excel
def on_browse_jira(self, event):
    if self.config.ReadBool("xml_import_one_file"):
        dialog = wx.FileDialog(None,
                               "Wähle die JIRA Tickets (aus einer Exportdatei) aus:",
                               wildcard="XML files (*.xml)|*.xml",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            g.folder_path_jira = dialog.GetPaths()
    else:
        dialog = wx.DirDialog(None, "Wähle den Ordner der JIRA Tickets aus:",
                              style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            g.folder_path_jira = dialog.GetPath()

# Method to sanitize path
def sanitize_path(path_str):
    invalid_chars = r'<>:"/\|?*' # removing invalid path chars
    for c in invalid_chars:
        path_str = path_str.replace(c, "_")
    return path_str

# Method to import XML file
def import_xml(self, file_paths):
    output_df = pd.DataFrame()
    def xml_to_dict(xml_string):
        root = ET.fromstring(xml_string)
        result = {}
        for child in root:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = xml_to_dict(ET.tostring(child))
        return result

    # Helper function to parse JIRA ticket
    def parse_jira_ticket(dict_task, customfield_raw, counter):
        jira_ticket = dict_task.get("key", "Leeres Feld")
        snippet = dict_task.get("description", "")
        snippet_decoded = html.unescape(snippet.replace("&lt;", "<").replace("&gt;", ">"))

        # Parse description
        desc_fields = {"Zuordnung": "-", "Typ": "-", "Reihenfolge": "-"}
        soup_desc = BeautifulSoup(snippet_decoded, "html.parser")
        for b_tag in soup_desc.find_all("b"):
            text = b_tag.parent.get_text(strip=True)
            for f_name in desc_fields:
                if text.startswith(f_name + ":"):
                    desc_fields[f_name] = text.split(":", 1)[1].strip()

        # Parse customfield
        snippet_customfield_decoded = html.unescape(customfield_raw).replace("&lt;", "<").replace("&gt;", ">")
        soup_cf = BeautifulSoup(snippet_customfield_decoded, "html.parser")
        cf_fields = {
            "Ort im e-Learning": "-",
            "Medium": "-",
            "System": "-",
            "Station": "-",
            "Einstieg": "-",
            "Beschreibung": "-",
        }
        for li in soup_cf.find_all("li"):
            text = li.get_text(strip=True)
            for f_name in cf_fields:
                if text.startswith(f_name + ":"):
                    cf_fields[f_name] = text.split(":", 1)[1].strip()
                    break

        # Build DataFrame
        return pd.DataFrame({
            "ID": counter,
            "Ticket": jira_ticket,
            "Titel": [dict_task.get("summary", "")],
            "Status": [dict_task.get("status", "")],
            "Verantwortlicher": [dict_task.get("assignee", "")],
            "Aufgabe": [cf_fields["Ort im e-Learning"].split("/")[-1]],
            "Medium": [cf_fields["Medium"]],
            "System": [cf_fields["System"]],
            "Station": [cf_fields["Station"]],
            "Einstieg": [cf_fields["Einstieg"]],
            "Beschreibung": [cf_fields["Beschreibung"]],
            "Zuordnung": [desc_fields["Zuordnung"]],
            "Typ": [desc_fields["Typ"]],
            "Reihenfolge": [desc_fields["Reihenfolge"]],
        }).set_index("ID")

    df_list = []
    counter = 0
    for file_path in file_paths:
        counter += 1
        with open(file_path, 'r') as file:
            xml_string = file.read()

        # Iterating through the XML file (one file)
        if self.config.ReadBool("xml_import_one_file"):
            items = re.findall(r"<item>(.*?)</item>", xml_string, re.DOTALL)
            customfields = re.findall(r'<customfield id="customfield_10083" key="com.atlassian.jira.plugin.system.customfieldtypes:textarea">(.*?)</customfield>', xml_string, re.DOTALL)
            for index, item_block in enumerate(items):
                try:
                    item_xml = f"<item>{item_block}</item>"
                    dict_task = xml_to_dict(item_xml)
                    df = parse_jira_ticket(dict_task, customfields[index], counter)
                    df_list.append(df)
                except Exception as e:
                    wx.MessageBox(f"Ticket `{jira_ticket}` nicht importiert, bitte überprüfen!",
                                  "Error", wx.OK | wx.ICON_ERROR)

            # Setting variable for status message
            number_of_items = index + 1

        # Iterating through the XML files (multi files)
        else:
            try:
                dict_task = xml_to_dict(xml_string)["channel"]["item"]
                customfield_raw = re.findall(r'<customfield id="customfield_10083" key="com.atlassian.jira.plugin.system.customfieldtypes:textarea">(.*?)</customfield>', xml_string, re.DOTALL)[0]
                df = parse_jira_ticket(dict_task, customfield_raw, counter)
                df_list.append(df)

                # Setting variable for status message
                number_of_items = counter
            except Exception as e:
                wx.MessageBox(f"Ticket `{jira_ticket}` nicht importiert, bitte überprüfen!",
                              "Error", wx.OK | wx.ICON_ERROR)
    output_df = pd.concat(df_list)
    output_df.reset_index(drop=True, inplace=True)

    # Method to build hierarchical tree
    def build_hierarchical_tree(output_df):
        item_map = {}
        
        # Normalizing names
        for _, row in output_df.iterrows():
            child_name = row["Aufgabe"].strip()
            parent_name = row["Zuordnung"].strip()
            ticket = row["Ticket"].strip()
            order_number = row["Reihenfolge"].strip()
            item_map[child_name] = {
                "parent": parent_name,
                "ticket": ticket,
                "order": order_number
            }

        # Collecting root
        g.root_folder_name = [
            name
            for name, info in item_map.items()
            if info["parent"] == "ROOT"
        ][0]

        # Method to get children
        def get_children(name, ticket = False):
            children = [
                                child
                                for child, info in item_map.items()
                                if info["parent"] == name
                             ]
            children.sort(key=lambda x: item_map[x]["order"])

            # Building a dictionary
            node_dict = {}
            for child in children:
                node_dict[child] = [get_children(child), item_map[child]["ticket"]]
            return node_dict

        # Building the overall tree
        tree = {}
        root_ticket = item_map[g.root_folder_name]["ticket"]
        tree = {g.root_folder_name: [get_children(g.root_folder_name), root_ticket]}
        return tree

    # Method to create folders
    def create_folders(node_dict, parent_path):
        for name, sub in node_dict.items():
            child_dict, _ticket = sub
            sanitized_name = sanitize_path(name)
            folder_path = os.path.join(parent_path, sanitized_name)
            os.makedirs(folder_path, exist_ok = True)

            # Calling recursivly if there are subfolders
            if child_dict:
                create_folders(child_dict, folder_path)

    # Building the hierarchical tree
    tree = build_hierarchical_tree(output_df)

    # Creating the folder structure
    create_folders(tree, g.folder_path_elearning)

    # Writing the tree to CSV file
    g.folder_path = os.path.join(g.folder_path_elearning,
                                 sanitize_path(g.root_folder_name))
    g.file_path_elearning = os.path.join(g.folder_path,
                                         f"{sanitize_path(g.root_folder_name)}_e-Learning_Definition.csv")
    folders_created = 0
    with open(g.file_path_elearning, "w", encoding = "utf-8", errors = "replace") as f:
        f.write(f'"Thema","Ticket","Order"\n')
        def writing_tree(node_dict, indent = 0):
            for name, sub in node_dict.items():
                f.write(f'"{name}","{sub[1]}",{indent}\n')
                writing_tree(sub[0], indent + 1)
        writing_tree(tree)
        # Counting the length of the file
        f.flush()
        folders_created = len(open(g.file_path_elearning).readlines()) - 2
        f.close()

    # Writing the dataframe to global variable and TXT file
    g.df_tasks = output_df
    g.df_tasks.to_string(os.path.join(g.folder_path_elearning,
                                      sanitize_path(g.root_folder_name),
                                      f"{sanitize_path(g.root_folder_name)}_Protokoll.txt"))
    g.df_tasks.to_csv(os.path.join(g.folder_path_elearning,
                                   sanitize_path(g.root_folder_name),
                                   f"{sanitize_path(g.root_folder_name)}_organisatorische_Aufgaben.csv"),
                      sep = ",", index = False)

    # Informing the user
    wx.MessageBox(f"{number_of_items} Tickets wurden erfasst und im Ordner `{g.root_folder_name}` wurden {folders_created} Unterordner erfolgreich angelegt.",
                  "Information", wx.OK | wx.ICON_INFORMATION)

# Method to handle selected file
def on_file_selected(self, event):
    file_index = event.GetSelection()
    file_path = self.file_listbox.GetString(file_index)
    g.file_path = file_path

# Method to handle the list control item activated event
def on_file_activated(self, event):
    if platform.system() == "Windows":
        try:
            os.startfile(f'"{g.file_path}"')
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}",
                          "Error", wx.OK | wx.ICON_ERROR)
    elif platform.system() == "Darwin":  # macOS
        try:
            subprocess.call(["open", g.file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}",
                          "Error", wx.OK | wx.ICON_ERROR)
    else:  # Linux
        try:
            subprocess.call(["xdg-open", g.file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}",
                          "Error", wx.OK | wx.ICON_ERROR)

# Method to list the files in the selected folder
def list_files(self, folder_path, filter_text = None, level = None):
    if filter_text is not None:
        filter_text = sanitize_path(filter_text)
    if level is not None:
        level = int(level)

    # Clearing the existing file list
    g.file_list = []

    # Iterating through the folder
    for root, dirs, files in os.walk(folder_path):
        if filter_text is None or level < 1:
            for d in dirs:
                g.file_list.append(os.path.join(root, d))
            for f in files:
                g.file_list.append(os.path.join(root, f))
            g.folder_path_import = folder_path

        # Iterating through the folder with a filter
        else:
            for d in dirs:
                if re.fullmatch(filter_text, d):
                    dir_path = os.path.join(root, d)
                    subfiles = []
                    for subroot, subdirs, subf in os.walk(dir_path):
                        for subdir in subdirs:
                            g.file_list.append(os.path.join(subroot, subdir))
                        for sf in subf:
                            subfiles.append(os.path.join(subroot, sf))
                    g.file_list.extend(subfiles)
                    g.folder_path_import = dir_path

    # Sorting the file list
    g.file_list.sort()

    # Displaying in the File Explorer
    self.file_listbox.Set(g.file_list)
