import Flask1
from Flask1 import Flask, render_template_string, redirect

app = Flask1(__name__)

# Replace with your Spotify playlist URL
SPOTIFY_PLAYLIST_URL = "https://open.spotify.com/"

@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Spotify Redirect</title>
        </head>
        <body>
            <button onclick="window.location.href='{{ SPOTIFY_PLAYLIST_URL }}'">Go to Spotify Playlist</button>
        </body>
        </html>
    """, SPOTIFY_PLAYLIST_URL=SPOTIFY_PLAYLIST_URL)

@app.route('/redirect')
def redirect_to_spotify():
    return redirect(SPOTIFY_PLAYLIST_URL)

if __name__ == '__main__':
    app.run(debug=True)
