import tkinter as tk
import webbrowser

# Replace with your Spotify playlist URL
SPOTIFY_PLAYLIST_URL = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

def open_spotify():
    webbrowser.open(SPOTIFY_PLAYLIST_URL)

# Create the main window
root = tk.Tk()
root.title("Spotify Redirect")

# Set window size
root.geometry("300x150")

# Create a button
btn = tk.Button(root, text="Go to Spotify Playlist", command=open_spotify, font=("Arial", 12), padx=10, pady=5)
btn.pack(pady=50)

# Run the application
root.mainloop()
