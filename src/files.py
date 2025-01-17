import wx
import os
import subprocess
import platform
import unicodedata
import pandas as pd
import re
import html
import xml.etree.ElementTree as ET

number_of_items = 0
root_folder_name = None

# Method to handle the Browse menu item
def on_browse_source(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Quell-Ordner (e-Learnings) aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        # The `folder_path` variable contains the path of the folder selected as string
        self.folder_path = dialog.GetPath()
        if self.config.ReadBool("drive_mapping_enabled", True):
            if self.config.Read("drive_mapping_letter") == "":
                letters = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                for letter in letters:
                    if os.path.exists(f"{letter}:"):
                        continue
                    else:
                        try:
                            # Mapping the folder to drive letter
                            subprocess.run(['subst', f"{letter}:", self.folder_path],
                                        check=True)

                            # Writing registry file
                            with open(f"{self.folder_path}\\MapVirtualDrive.reg", "w") as f:
                                path_to_folder = self.folder_path.replace("\\", "\\\\")
                                f.write(
f"""Windows Registry Editor Version 5.00\n\n\
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]
"Virtual Drive"="subst {letter}: \\"{path_to_folder}\\""
""")

                            # Importing registry file
                            subprocess.run(["regedit", "/s", f"{self.folder_path}\\MapVirtualDrive.reg"], check=True)
                        except:
                            continue
                        self.config.Write("drive_mapping_letter", letter)
                        break
            list_files(self, f'{self.config.Read("drive_mapping_letter")}:\\')
        else:
            list_files(self, self.folder_path)
    dialog.Destroy()

# Method to handle the Browse menu item
def on_browse_target(self, event):
    dialog = wx.DirDialog(None, "Wähle einen Ziel-Ordner aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        # The `folder_path` variable contains the path of the folder selected as string
        self.folder_path_elearning = dialog.GetPath()

def on_browse_jira(self, event):
    if self.config.ReadBool("xml_import_one_file"):
        dialog = wx.FileDialog(None, "Wähle das JIRA Ticket aus:", wildcard="XML files (*.xml)|*.xml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            # The `folder_path` variable contains the path of the file selected as string
            self.folder_path_jira = dialog.GetPaths()
    else:
        dialog = wx.DirDialog(None, "Wähle den Ordner der JIRA Tickets aus:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            # The `folder_path` variable contains the path of the folder selected as string
            self.folder_path_jira = dialog.GetPath()

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
    df_list = []
    counter = 0
    for file_path in file_paths:
        counter += 1
        try:
            with open(file_path, 'r') as file:
                xml_string = file.read()

            # Iterate through the XML file
            if self.config.ReadBool("xml_import_one_file"):
                items = re.findall(r"<item>(.*?)</item>", xml_string, re.DOTALL)
                customfields = re.findall(r'<customfield id="customfield_10083" key="com.atlassian.jira.plugin.system.customfieldtypes:textarea">(.*?)</customfield>', xml_string, re.DOTALL)
                for index, item_block in enumerate(items):
                    # Reconstruct a valid fragment
                    item_xml = f"<item>{item_block}</item>"
                    dict_task = xml_to_dict(item_xml)  # parse each item separately
                    snippet = dict_task.get("description", "")

                    # Converting HTML entities like &lt; &gt; to < >
                    snippet_decoded = snippet.replace("&lt;", "<").replace("&gt;", ">")
                    pattern = re.compile(
                        r"<b>Zuordnung:</b>\s*(.*?)</li>.*?"
                        r"<b>Typ:</b>\s*(.*?)</li>.*?"
                        r"<b>Reihenfolge:</b>\s*(.*?)</li>",
                        re.DOTALL
                    )
                    match = pattern.search(snippet_decoded)
                    parent = match.group(1).strip()
                    type = match.group(2).strip()
                    order = match.group(3).strip()

                    # Extracting path in the e-learning structure field
                    customfield_raw = customfields[index]
                    snippet_customfield_decoded = html.unescape(customfield_raw.replace("&lt;", "<").replace("&gt;", ">"))
                    pattern_ort = re.compile(r"<li><b>Ort im e-Learning:</b>\s*(.*?)</li>")
                    ort_elearning = pattern_ort.search(snippet_customfield_decoded).group(1).strip()

                    # Extracting the last part of the path if not `ROOT`
                    if "/" in ort_elearning:
                        ort_elearning = ort_elearning.split("/")[-1]

                    # Building the DataFrame
                    df = pd.DataFrame({
                        'ID': counter,
                        'Titel': [dict_task.get("summary", "")],
                        'Status': [dict_task.get("status", "")],
                        'Verantwortlicher': [dict_task.get("assignee", "")],
                        'Aufgabe': [ort_elearning],
                        'Zuordnung': [parent],
                        'Typ': [type],
                        'Reihenfolge': [order]
                    })
                    df.set_index('ID', inplace = True)
                    df_list.append(df)

                # Setting variables for status message and ID
                number_of_items = index + 1
                counter += 1
            else:
                dict_task = xml_to_dict(xml_string)
                snippet = dict_task['channel']['item']['description']
                customfield_raw = re.findall(r'<customfield id="customfield_10083" key="com.atlassian.jira.plugin.system.customfieldtypes:textarea">(.*?)</customfield>', xml_string, re.DOTALL)

                # Converting HTML entities like &lt; &gt; to < >
                snippet_decoded = snippet.replace("&lt;", "<").replace("&gt;", ">")
                pattern = re.compile(
                    r"<b>Zuordnung:</b>\s*(.*?)</li>.*?"
                    r"<b>Typ:</b>\s*(.*?)</li>.*?"
                    r"<b>Reihenfolge:</b>\s*(.*?)</li>",
                    re.DOTALL
                )
                match = pattern.search(snippet_decoded)
                parent = match.group(1).strip()
                type = match.group(2).strip()
                order = match.group(3).strip()

                # Extracting path in the e-learning structure field
                snippet_customfield_decoded = html.unescape(customfield_raw[0].replace("&lt;", "<").replace("&gt;", ">"))
                pattern_ort = re.compile(r"<li><b>Ort im e-Learning:</b>\s*(.*?)</li>",
                                         re.DOTALL)
                match_ort = pattern_ort.search(snippet_customfield_decoded)
                ort_elearning = match_ort.group(1).strip()

                # Extracting the last part of the path if not `ROOT`
                if "/" in ort_elearning:
                    ort_elearning = ort_elearning.split("/")[-1]

                # Building the DataFrame
                df = pd.DataFrame({
                                            'ID': counter,
                                            'Titel': [dict_task['channel']['item']['summary']],
                                            'Status': [dict_task['channel']['item']['status']],
                                            'Verantwortlicher':[dict_task['channel']['item']['assignee']],
                                            'Aufgabe': [ort_elearning],
                                            'Zuordnung': [parent],
                                            'Typ': [type],
                                            'Reihenfolge': [order]
                                        })
                df.set_index('ID', inplace = True)
                df_list.append(df)

                # Setting variable for status message
                number_of_items = counter
        except Exception as e:
            wx.MessageBox(f"Datei nicht importiert: {e}", "Error", wx.OK | wx.ICON_ERROR)
    output_df = pd.concat(df_list)
    output_df.reset_index(drop=True, inplace=True)
    output_df.to_csv(os.path.join(self.folder_path_elearning, "eLearning_Tasks.txt"), sep = "\t", index = False)

    # Method to sanitize path
    def sanitize_path(path_str):
        invalid_chars = r'<>:"/\|?*' # Invalid Windows path chars: < > : " / \ | ? *
        for c in invalid_chars:
            path_str = path_str.replace(c, "_")
        return path_str

    # Method for normalizing names
    def normalize_name(name: str) -> str:
        # Removing everything up to the first colon (":") and any trailing space
        #name = re.sub(r'^.*?:\s*', '', name)
        # Removing specific strings
        #name = name.replace("Anlage ", "")
        #name = name.replace("Kapitel ", "")
        #name = name.replace("Lektion ", "")
        return name.strip()

    # Method to build hierarchical tree
    def build_hierarchical_tree(output_df):
        item_map = {}
        
        # Normalizing names
        for _, row in output_df.iterrows():
            child_name = normalize_name(row["Aufgabe"])
            item_map[child_name] = {
                "parent": row["Zuordnung"],
                "order": row["Reihenfolge"]
            }

        # Method to check if the item is root
        def is_root(name):
            return item_map[name]["parent"] == "ROOT"

        # Collecting all roots (`Zuordnung` == "ROOT")
        roots = [name for name in item_map if is_root(name)]
        roots.sort(key=lambda x: item_map[x]["order"])  # sort top-level items by their order
        if not roots:
            wx.MessageBox(f"Keine Zuordnung mit 'ROOT' gefunden: {e}", "Error", wx.OK | wx.ICON_ERROR)
            return {}
        elif len(roots) > 1:
            wx.MessageBox(f"Mehrfach Zuordnung mit 'ROOT' gefunden: {e}", "Error", wx.OK | wx.ICON_ERROR)
            return {}

        # Method to get children
        def get_children(name):
            # Recursively gather children
            children = [
                child 
                for child, info in item_map.items()
                if info["parent"] == name
            ]
            children.sort(key=lambda x: item_map[x]["order"])  # Sorting siblings by order
            return {child: get_children(child) for child in children} if children else {}

        # Building the overall tree
        tree = {}
        for root in roots:
            tree[root] = get_children(root)

        # Writing the tree to CSV file
        self.root_folder_name = roots[0]
        csv_file_path = os.path.join(self.folder_path_elearning, f"{sanitize_path(roots[0])}.csv")
        with open(csv_file_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(f'"Thema",0\n')
            def writing_tree(node_dict, indent=0):
                for name, sub in node_dict.items():
                    f.write(f'"{name}",{indent}\n')
                    writing_tree(sub, indent + 1)
            writing_tree(tree)
            f.close()

        # Returning the tree
        return tree

    # Method to create folders
    def create_folders(node_dict, parent_path):
        for name, sub in node_dict.items():
            # Sanitize folder names
            sanitized_name = sanitize_path(name)
            folder_path = os.path.join(parent_path, sanitized_name)
            os.makedirs(folder_path, exist_ok=True)
            if sub:  # Only recurse if there are subfolders
                create_folders(sub, folder_path)

    # Building the hierarchical tree
    tree = build_hierarchical_tree(output_df)

    # Creating the folder structure
    create_folders(tree, self.folder_path_elearning)

    # Informing the user
    wx.MessageBox(f"{number_of_items} Ordner wurden in `{self.root_folder_name}` erfolgreich erstellt.", "Information", wx.OK | wx.ICON_INFORMATION)

# Method to create the folder structur
def on_create_folder_structure(self, event):
    on_browse_target(self, event)
    file_path_jira = []
    if self.config.ReadBool("xml_import_one_file"):
        file_path_jira.append(self.folder_path_jira[0])
    else:
        for name in os.listdir(self.folder_path_jira):
            file_path = os.path.join(self.folder_path_jira, name)
            if os.path.isfile(file_path) and name.endswith(".xml"):
                file_path_jira.append(file_path)
    import_xml(self, file_path_jira)

# Method to handle selected file
def on_file_selected(self, event):
    file_index = event.GetSelection()
    file_path = self.file_listbox.GetString(file_index)
    self.file_path = file_path

    # To-Do Kanjo
    # - Get the file name from the path
    # - Xy
    file_name = os.path.basename(self.file_path)
    print(file_name)

# Method to handle the list control item activated event
def on_file_activated(self, event):
    if platform.system() == "Windows":
        try:
            os.startfile(f'"{self.file_path}"')
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
    elif platform.system() == "Darwin":  # macOS
        try:
            subprocess.call(["open", self.file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:  # Linux
        try:
            subprocess.call(["xdg-open", self.file_path])
        except Exception as e:
            wx.MessageBox(f"Datei konnte nicht geöffnet werden: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Method to list the files in the selected folder
def list_files(self, folder_path, filter_text=None):
    # Clear the existing file list
    self.file_list = []
    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if filter_text is None or filter_text is not None:
                self.file_list.append(dir_path)
                files = [
                    f 
                    for f in os.listdir(dir_path)
                ]
                self.file_list.extend(os.path.join(dir_path, f) for f in files)
            else:
                # Adding all subdirectories of the matching directory
                normalized_filter_text = unicodedata.normalize('NFC', filter_text)
                normalized_name = unicodedata.normalize('NFC', name)
                if normalized_filter_text in normalized_name:
                    for sub_root, sub_dirs, sub_files in os.walk(dir_path):
                        for sub_name in sub_dirs:
                            dir_path = os.path.join(sub_root, sub_name)
                            self.file_list.append(os.path.join(sub_root, sub_name))
                            sub_files = [
                                f 
                                for f in os.listdir(dir_path)
                            ]
                            self.file_list.extend(os.path.join(dir_path, f) for f in sub_files)
    self.file_listbox.Set(self.file_list)