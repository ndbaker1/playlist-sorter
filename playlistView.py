from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from songList import SongListWidget
from utilities import clean_string

'''
A Widget Wrapper for manipulating a Playlist File
- Displays songs in a SongListWidget and contains Add, Remove, and Close buttons
'''


class PlaylistView(QWidget):
    def __init__(self, playlistFile, remove_self, take_selected_songs, update_changes):
        super(PlaylistView, self).__init__()

        # Keep a reference of the file path
        self.file = playlistFile

        # Create a list of songs that can be played
        self.song_list_widget = SongListWidget()

        # Load all the song paths that are initially in the playlist file
        with open(self.file, 'r', encoding='utf-8') as playlist:
            for song in [clean_string(line) for line in playlist.readlines()]:
                self.song_list_widget.add_song(song)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self.file))
        layout.addWidget(
            Controls(
                close_playlist=lambda: [
                    remove_self(self.file),
                    self.deleteLater(),
                ],
                add_song=lambda: [
                    [self.song_list_widget.addItem(item) for item in take_selected_songs()],
                    self.song_list_widget.sortItems(),
                    self.write_changes(),
                ],
                remove_song=lambda: [
                    self.song_list_widget.pop_selected_song_items(),
                    self.write_changes(),
                    update_changes()
                ]
            )
        )
        layout.addWidget(self.song_list_widget)

    '''
    Writes the current songlist to the playlist file.
    Used as a post-event callback for all button actions

    - HIGH IMPORTANCE
        if this is not functioning correctly,
        then the state of the playlist cannot be guarenteed
    '''

    def write_changes(self):
        with open(self.file, 'w', encoding='utf-8') as playlist:
            for line in self.song_list_widget.get_song_paths():
                playlist.write(line + '\n')


'''
The UI Button controls for a PlaylistView
    - Close Playlist, Add Song, Remove Song
'''


class Controls(QWidget):
    def __init__(
        self,
        close_playlist,
        add_song,
        remove_song,
    ):
        super(Controls, self).__init__()
        button_layout = QHBoxLayout(self)

        # close button setup
        button = QPushButton(text='Close')
        button.setMinimumHeight(40)
        button.clicked.connect(close_playlist)
        button_layout.addWidget(button)

        # add song button setup
        button = QPushButton(text='Add')
        button.setMinimumHeight(40)
        button.clicked.connect(add_song)
        button_layout.addWidget(button)

        # remove song button setup
        button = QPushButton(text='Remove')
        button.setMinimumHeight(40)
        button.clicked.connect(remove_song)
        button_layout.addWidget(button)
