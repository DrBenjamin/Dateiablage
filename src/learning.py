# `src/learning.py`
# Main application for the RAG on Snow project
# Open-Source, hosted on https://github.com/DrBenjamin/Dateiablage
# Please reach out to ben@seriousbenentertainment.org for any questions
# Modules
import wx
import streamlit as st
import pandas as pd
import src.globals as g
from src.tasks import display_tasks
from src.files import list_files
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from urllib.parse import urlparse
import logging
import os

# Method to establish MiniO session
def connect_to_minio(endpoint_url, access_key, secret_key, secure):
    # Removing any path from endpoint_url (only host:port allowed)
    parsed = urlparse(endpoint_url)
    endpoint = parsed.hostname
    if parsed.port:
        endpoint = f"{endpoint}:{parsed.port}"
    try:
        client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,  # Using HTTP or HTTPS
            cert_check=False
        )
        return client
    except S3Error as e:
        wx.MessageBox(
            f"Fehler beim aufbauen der MinIO-Verbindung: {e}", "Fehler", wx.OK | wx.ICON_ERROR)
    return None

# Method to list buckets
def list_buckets(minio_client):
    try:
        buckets = minio_client.list_buckets()
        return [
            bucket.name.replace('-', ' ').title()
            for bucket in buckets
        ]
    except S3Error as e:
        wx.MessageBox(
            f"Fehler beim auflisten der MinIO-Buckets: {e}", "Fehler", wx.OK | wx.ICON_ERROR)
    return

# Method to list objects in a bucket
def list_objects(minio_client, bucket_name):
    bucket_name = bucket_name.lower().replace(' ', '-')
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        return [
            obj.object_name
            for obj in objects
        ]
    except S3Error as e:
        wx.MessageBox(
            f"Fehler beim auflisten der MinIO-Dateien: {e}", "Fehler", wx.OK | wx.ICON_ERROR)
    return

# Method to upload file
def on_upload_file(self, event):
    wildcard = "Alle Dateien (*.*)|*.*" 
    dialog = wx.FileDialog(self, "Bitte wählen Sie eine Datei aus:",
        wildcard=wildcard,
        style=wx.FD_OPEN | wx.FD_MULTIPLE
    )
    if dialog.ShowModal() == wx.ID_OK:
        g.file_list_import = dialog.GetPaths()
    dialog.Destroy()

# Method to upload files to MinIO bucket
def upload_files(minio_client, bucket_name, files):
    bucket_name = bucket_name.lower().replace(' ', '-')
    for file in files:
        # Reading file
        file_content = file.read()

        # Uploading to MinIO
        minio_client.put_object(
            bucket_name,
            file.name,
            BytesIO(file_content),
            len(file_content)
        )

# Method to refresh and display MinIO bucket files in the learning_ctrl
def refresh_learning_ctrl_with_minio(self):
    try:
        # Connecting to MinIO and listing objects
        minio_client = connect_to_minio(
            st.secrets["MinIO"]["endpoint"],
            st.secrets["MinIO"]["access_key"],
            st.secrets["MinIO"]["secret_key"],
            st.secrets["MinIO"]["secure"].lower() == "true"
        )
        files = list_objects(minio_client, st.secrets["MinIO"]["bucket"])
        if files is None:
            files = []
        display_learning(self, files)
        self.SetTitle(f"Dateiablage - {st.secrets['MinIO']['bucket']}")
    except Exception as e:
        wx.MessageBox(
            f"Fehler beim Laden der MinIO-Dateien: {e}", "Fehler", wx.OK | wx.ICON_ERROR)

# Method to display_learning to accept a list of filenames
def display_learning(self, files):
    self.learning_ctrl.ClearAll()
    self.learning_ctrl.InsertColumn(0, "Filename")
    for file_name in files:
        self.learning_ctrl.InsertItem(
            self.learning_ctrl.GetItemCount(), file_name)
    self.learning_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    # Selecting the first item if available
    if files:
        g.elearning_index = 0
        self.learning_ctrl.Select(0)
        self.learning_ctrl.EnsureVisible(0)

# Method to handle the selection of an item in the learning_ctrl
def on_elearning_item_selected(self, event):
    g.elearning_index = event.GetIndex()
    item_text = self.learning_ctrl.GetItemText(g.elearning_index, 0)
    if g.ticket_chosen:
        g.ticket_chosen = False
        display_tasks(self, g.df_tasks)

    # Optionally, show file details or preview here
    self.SetTitle(
        f"Dateiablage - {getattr(g, 'minio_bucket', '')} - {item_text}")

# Method to handle the activation of an item in the learning_ctrl
def on_elearning_item_activated(self, event):
    item_index = event.GetIndex()
    item_text = self.learning_ctrl.GetItemText(item_index, 0)
    display_tasks(self, g.df_tasks)
    g.ticket_chosen = True

# Method to upload file(s) to MinIO via wx dialog
def on_upload_file_to_minio(self, event):
    """
    Handling file selection and uploading to MinIO bucket.
    """
    wildcard = "Alle Dateien (*.*)|*.*"
    dialog = wx.FileDialog(
        self,
        "Bitte wählen Sie eine oder mehrere Dateien zum Hochladen aus:",
        wildcard=wildcard,
        style=wx.FD_OPEN | wx.FD_MULTIPLE
    )
    if dialog.ShowModal() == wx.ID_OK:
        file_paths = dialog.GetPaths()
        try:
            # Connecting to MinIO
            minio_client = connect_to_minio(
                st.secrets["MinIO"]["endpoint"],
                st.secrets["MinIO"]["access_key"],
                st.secrets["MinIO"]["secret_key"],
                st.secrets["MinIO"]["secure"].lower() == "true"
            )
            bucket_name = st.secrets["MinIO"]["bucket"]

            # Creating bucket if it does not exist
            if not minio_client.bucket_exists(bucket_name):
                minio_client.make_bucket(bucket_name)

            # Uploading each file
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    minio_client.put_object(
                        bucket_name,
                        file_name,
                        BytesIO(file_data),
                        len(file_data)
                    )
            wx.MessageBox(
                f"{len(file_paths)} Datei(en) erfolgreich hochgeladen.",
                "Upload abgeschlossen",
                wx.OK | wx.ICON_INFORMATION
            )
            # Refreshing the learning control to show new files
            self.refresh_learning_ctrl_with_minio()
        except Exception as e:
            wx.MessageBox(
                f"Fehler beim Hochladen zu MinIO: {e}",
                "Fehler",
                wx.OK | wx.ICON_ERROR
            )
    dialog.Destroy()
