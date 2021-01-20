import re
import os
from glob import glob
from PyQt5.QtWidgets import *
from utilities import *
from songList import SongListWidget

MUSIC_FORMATS = ['mp3', 'm4a']


class MasterList(QWidget):
    def __init__(self, masterComponent, song_directory):
        super(MasterList, self).__init__()
        self.master_component = masterComponent
        self.song_directory = song_directory
        # song list
        self.song_list_widget = SongListWidget()
        self.directory_label = QLabel()
        # layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.directory_label)
        layout.addWidget(self.song_list_widget)
        layout.addWidget(
            Controls(
                update_song_directory=self.master_component.update_song_directory,
                open_playlist=self.master_component.open_playlist,
            )
        )

    def load_song_list(self) -> None:
        self.directory_label.setText(self.master_component.config['songDirectory'])
        self.song_list_widget.clear()
        for song in self.get_unassigned_songs():
            self.song_list_widget.add_song(song)

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
