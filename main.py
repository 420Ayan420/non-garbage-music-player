import tkinter as tk
from tkinter import filedialog, ttk
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import datetime

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Clear the treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Search for .mp3 files, retrieve their info, and add them to the treeview
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(folder_path, file)
                audio = MP3(file_path, ID3=EasyID3)
                
                try:
                    artist = audio['artist'][0]
                except KeyError:
                    artist = 'Unknown'
                
                try:
                    length = str(datetime.timedelta(seconds=int(audio.info.length)))
                except KeyError:
                    length = 'Unknown'
                
                date_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                
                tree.insert("", tk.END, values=(file, "Playlist TBD", artist, date_modified, length))

# Set up the main application window
root = tk.Tk()
root.title("MP3 File Finder")

# Set up the Treeview
tree = ttk.Treeview(root, columns=("Name", "Playlist", "Artist", "Date Modified", "Length"), show='headings')
tree.heading("Name", text="Name")
tree.heading("Playlist", text="Playlist")
tree.heading("Artist", text="Artist")
tree.heading("Date Modified", text="Date Modified")
tree.heading("Length", text="Length")
tree.column("Name", width=150)
tree.column("Playlist", width=100)
tree.column("Artist", width=150)
tree.column("Date Modified", width=150)
tree.column("Length", width=100)
tree.pack(expand=True, fill='both', padx=10, pady=10)

# Add a button to select a folder
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=10)

# Run the application
root.mainloop()
