import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, StringVar

# Create a connection to the database
conn = sqlite3.connect('music_library.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        album TEXT,
        genre TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS playlist_songs (
        playlist_id INTEGER,
        song_id INTEGER,
        FOREIGN KEY (playlist_id) REFERENCES playlists(id),
        FOREIGN KEY (song_id) REFERENCES songs(id)
    )
''')

conn.commit()

def add_song():
    title = entry_title.get()
    artist = entry_artist.get()
    album = entry_album.get()
    genre = entry_genre.get()

    cursor.execute('''
        INSERT INTO songs (title, artist, album, genre)
        VALUES (?, ?, ?, ?)
    ''', (title, artist, album, genre))
    conn.commit()

    refresh_song_list()

def add_playlist():
    playlist_name = entry_playlist_name.get()

    cursor.execute('''
        INSERT INTO playlists (name)
        VALUES (?)
    ''', (playlist_name,))
    conn.commit()

    refresh_playlist_list()

def add_song_to_playlist():
    selected_song = song_listbox.get(song_listbox.curselection())
    selected_playlist = playlist_listbox.get(playlist_listbox.curselection())

    song_id = selected_song.split(':')[0]
    playlist_id = selected_playlist.split(':')[0]

    cursor.execute('''
        INSERT INTO playlist_songs (song_id, playlist_id)
        VALUES (?, ?)
    ''', (song_id, playlist_id))
    conn.commit()

def get_songs():
    cursor.execute('''
        SELECT * FROM songs
    ''')
    return cursor.fetchall()

def get_playlists():
    cursor.execute('''
        SELECT * FROM playlists
    ''')
    return cursor.fetchall()

def get_songs_in_playlist(playlist_id):
    cursor.execute('''
        SELECT songs.* FROM songs
        JOIN playlist_songs ON songs.id = playlist_songs.song_id
        WHERE playlist_songs.playlist_id = ?
    ''', (playlist_id,))
    return cursor.fetchall()

def refresh_song_list():
    song_listbox.delete(0, 'end')
    songs = get_songs()
    for song in songs:
        song_listbox.insert('end', f'{song[0]}: {song[1]} - {song[2]}')

def refresh_playlist_list():
    playlist_listbox.delete(0, 'end')
    playlists = get_playlists()
    for playlist in playlists:
        playlist_listbox.insert('end', f'{playlist[0]}: {playlist[1]}')

# Create the main window
window = Tk()
window.title('Music Library Management')

# Create labels and entry fields for adding songs
lbl_title = Label(window, text='Title:')
lbl_title.grid(row=0, column=0)
entry_title = Entry(window)
entry_title.grid(row=0, column=1)

lbl_artist = Label(window, text='Artist:')
lbl_artist.grid(row=1, column=0)
entry_artist = Entry(window)
entry_artist.grid(row=1, column=1)

lbl_album = Label(window, text='Album:')
lbl_album.grid(row=2, column=0)
entry_album = Entry(window)
entry_album.grid(row=2, column=1)

lbl_genre = Label(window, text='Genre:')
lbl_genre.grid(row=3, column=0)
entry_genre = Entry(window)
entry_genre.grid(row=3, column=1)

# Create a button to add songs
btn_add_song = Button(window, text='Add Song', command=add_song)
btn_add_song.grid(row=4, column=1)

# Create a listbox to display songs
song_listbox = Listbox(window, width=50)
song_listbox.grid(row=5, column=0, columnspan=2)

# Create a scrollbar for the song listbox
song_scrollbar = Scrollbar(window)
song_scrollbar.grid(row=5, column=2, sticky='NS')

# Connect the scrollbar to the song listbox
song_listbox.config(yscrollcommand=song_scrollbar.set)
song_scrollbar.config(command=song_listbox.yview)

# Create labels and entry fields for adding playlists
lbl_playlist_name = Label(window, text='Playlist Name:')
lbl_playlist_name.grid(row=0, column=3)
entry_playlist_name = Entry(window)
entry_playlist_name.grid(row=0, column=4)

# Create a button to add playlists
btn_add_playlist = Button(window, text='Add Playlist', command=add_playlist)
btn_add_playlist.grid(row=1, column=4)

# Create a listbox to display playlists
playlist_listbox = Listbox(window, width=50)
playlist_listbox.grid(row=2, column=3, rowspan=4, columnspan=2)

# Create a scrollbar for the playlist listbox
playlist_scrollbar = Scrollbar(window)
playlist_scrollbar.grid(row=2, column=5, rowspan=4, sticky='NS')

# Connect the scrollbar to the playlist listbox
playlist_listbox.config(yscrollcommand=playlist_scrollbar.set)
playlist_scrollbar.config(command=playlist_listbox.yview)

# Create a button to add songs to playlists
btn_add_to_playlist = Button(window, text='Add to Playlist', command=add_song_to_playlist)
btn_add_to_playlist.grid(row=6, column=2)

# Refresh the song and playlist listboxes
refresh_song_list()
refresh_playlist_list()

# Start the main event loop
window.mainloop()
