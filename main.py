import tkinter as tk
from tkinter import filedialog, ttk
import os
from mutagen.mp3 import MP3
import pygame
import time

# Initialize Pygame Mixer
pygame.mixer.init()

class MP3Player(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MP3 Player and Metadata Viewer")
        self.geometry("800x600")

        # Setup for file selection and display
        self.setup_file_selection()

        # Control Panel for playback controls
        self.setup_control_panel()

        # Progress Bar and Time Labels
        self.setup_progress_bar()

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Current song path and playback state
        self.current_song = None
        self.is_paused = False

        # Update progress
        self.update_progress()

    def setup_file_selection(self):
        # Frame for folder selection
        selection_frame = tk.Frame(self)
        selection_frame.pack(fill=tk.X)

        # Select Folder button
        select_folder_btn = tk.Button(selection_frame, text="Select Folder", command=self.select_folder)
        select_folder_btn.pack(side=tk.LEFT, padx=10, pady=5)

        # TreeView for displaying files
        self.tree = ttk.Treeview(self, columns=("Name", "Path"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Path", text="Path")
        self.tree.column("Path", width=0, stretch=False)  # Hide the 'Path' column
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def setup_control_panel(self):
        # Frame for playback controls
        self.control_panel = tk.Frame(self)
        self.control_panel.pack(fill=tk.X)

        # Playback Buttons
        tk.Button(self.control_panel, text="Play", command=self.play_selected_file).pack(side=tk.LEFT)
        tk.Button(self.control_panel, text="Pause", command=self.toggle_pause).pack(side=tk.LEFT)
        tk.Button(self.control_panel, text="Stop", command=self.stop_music).pack(side=tk.LEFT)
        tk.Button(self.control_panel, text="Restart", command=self.restart_song).pack(side=tk.LEFT)

    def setup_progress_bar(self):
        # Progress Bar
        self.progress = ttk.Scale(self, orient=tk.HORIZONTAL, length=400)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.progress.bind("<ButtonRelease-1>", self.on_click_progress)

        # Time Labels
        self.song_length_label = tk.Label(self.control_panel, text="0:00")
        self.song_length_label.pack(side=tk.LEFT, padx=10)

        self.elapsed_time_label = tk.Label(self.control_panel, text="0:00")
        self.elapsed_time_label.pack(side=tk.LEFT)

        self.remaining_time_label = tk.Label(self.control_panel, text="-0:00")
        self.remaining_time_label.pack(side=tk.LEFT, padx=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for item in self.tree.get_children():
                self.tree.delete(item)
            for file in os.listdir(folder_path):
                if file.endswith(".mp3"):
                    file_path = os.path.join(folder_path, file)
                    self.tree.insert("", tk.END, values=(file, file_path))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        self.current_song = self.tree.item(selected_item, 'values')[1]
        self.play_music(self.current_song)

    def play_selected_file(self):
        if self.current_song:
            self.play_music(self.current_song)

    def play_music(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.update_song_length(file_path)
        self.is_paused = False

    def toggle_pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.is_paused = not self.is_paused

    def stop_music(self):
        pygame.mixer.music.stop()
        self.progress.set(0)

    def restart_song(self):
        if self.current_song:
            self.play_music(self.current_song)

    def update_song_length(self, file_path):
        audio = MP3(file_path)
        song_length = int(audio.info.length)
        self.progress.configure(to=song_length)
        self.song_length_label.config(text=time.strftime('%M:%S', time.gmtime(song_length)))

    def update_progress(self):
        if not self.is_paused:
            self.progress.set(pygame.mixer.music.get_pos() // 1000)
            elapsed_time = int(self.progress.get())
            self.elapsed_time_label.config(text=time.strftime('%M:%S', time.gmtime(elapsed_time)))
            total_length = int(self.progress.cget("to"))
            remaining_time = total_length - elapsed_time
            self.remaining_time_label.config(text=f"-{time.strftime('%M:%S', time.gmtime(remaining_time))}")
        self.after(1000, self.update_progress)

    def on_click_progress(self, event):
        if self.current_song:
            pygame.mixer.music.play(start=int(self.progress.get()))

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

# Run the application
if __name__ == "__main__":
    app = MP3Player()
    app.mainloop()
