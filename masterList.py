import re
from glob import glob
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from songList import SongListWidget
from utilities import clean_string, file_path_exists

# The supported audio formats
MUSIC_FORMATS = ['mp3', 'm4a', 'flac']


'''
A Widget Containing the List of all unassigned Songs

Initially contains all songs found recursively in a given song directory.
When adding a playlist, the set of songs that exists in the playlist
and the masterlist will be removed from the masterlist.
'''


class MasterList(QWidget):
    def __init__(self, masterComponent, song_directory):
        super(MasterList, self).__init__()
        # reference to the config orchestrator
        self.master_component = masterComponent
        # song list widget
        self.song_list_widget = SongListWidget()
        # directroy
        self.song_directory = song_directory
        self.directory_label = QLabel()
        # layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.directory_label)
        layout.addWidget(
            Controls(
                update_song_directory=self.master_component.update_song_directory,
                open_playlist=self.master_component.open_playlist,
            )
        )
        layout.addWidget(self.song_list_widget)

    '''
    Updates the SongList with the correctly filtered songs
    '''

    def load_song_list(self) -> None:
        # only allow loading if a song directory is found
        if len(self.master_component.config['songDirectory']) > 0 and file_path_exists(self.master_component.config['songDirectory']):
            self.directory_label.setText(self.master_component.config['songDirectory'])
            self.song_list_widget.clear()
            for song in self.get_unassigned_songs():
                self.song_list_widget.add_song(song)

    '''
    Finds all file paths with the correct audio extension,
    and then filters out songs found within any of the open playlists
    '''

    def get_unassigned_songs(self) -> list:
        songs = [
            clean_string(f) for f in glob(self.master_component.config['songDirectory'] + '**/*', recursive=True)
            if re.match(f".*\.({ '|'.join(MUSIC_FORMATS) })", f)
        ]
        for path in self.master_component.config['openPlaylists']:
            with open(path, 'r', encoding='utf-8') as playlistFile:
                for line in [clean_string(line) for line in playlistFile.readlines()]:
                    if line in songs:
                        songs.remove(line)
        return songs


'''
UI Button controls for a MasterList
Contains the ability to:
    - Open a new music directory
    - Open a new playlist
'''


class Controls(QWidget):
    def __init__(
        self,
        update_song_directory,
        open_playlist,
    ):
        super(Controls, self).__init__()
        layout = QHBoxLayout(self)

        button = QPushButton(text='Set Music Directory')
        button.setMinimumHeight(40)
        button.clicked.connect(update_song_directory)
        layout.addWidget(button)

        button = QPushButton(text='Open Playlist')
        button.setMinimumHeight(40)
        button.clicked.connect(open_playlist)
        layout.addWidget(button)
