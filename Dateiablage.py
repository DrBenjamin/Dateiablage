import streamlit as st
import os

st.title("Dateiablage")
st.write("Tool zur Organisation der Dateiablage von e-Learning Inhalten.")

# Construct the path using the generic logged-in user
folder_path = os.path.join(os.path.expanduser("~"), "OneDrive - CGM", "UKE_Videos", "8. Turtorials_Videobearbeitung", "Dateistruktur Neu", "E-Learnings")
st.write(f"Opening folder: {folder_path}")

# List all files and folders recursively
file_list = []
for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        file_list.append(os.path.join(root, name))
    for name in files:
        file_list.append(os.path.join(root, name))

st.write("Files and folders:")
for file in file_list:
    st.write(file)