import re
import os
from glob import glob
from PyQt5.QtWidgets import *
from utilities import *

MUSIC_FORMATS = ['mp3', 'm4a']


class MasterList(QWidget):
    def __init__(self, masterComponent, song_directory):
        super(MasterList, self).__init__()
        self.master_component = masterComponent
        self.song_directory = song_directory
        # song list
        self.list_widget = QListWidget()
        self.directory_label = QLabel()
        # layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.directory_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(
            Controls(
                update_song_directory=self.master_component.update_song_directory,
                open_playlist=self.master_component.open_playlist,
                play_current_song=lambda: play_song(
                    self.list_widget.selectedItems()[0].data(0x0100)
                    if len(self.list_widget.selectedItems()) > 0
                    else None
                )
            )
        )

    def take_selected_songs(self) -> list:
        return [self.list_widget.takeItem(item.row()) for item in self.list_widget.selectedIndexes()]

    def load_song_list(self) -> None:
        self.directory_label.setText(self.master_component.config['songDirectory'])
        self.list_widget.clear()
        for song in self.get_unassigned_songs():
            listItem = QListWidgetItem()
            listItem.setText(song[song.rindex('/') + 1:])
            listItem.setData(0x0100, song)
            self.list_widget.addItem(listItem)

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
        play_current_song
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

        button = QPushButton(text='Play Song')
        button.setMinimumHeight(40)
        button.clicked.connect(play_current_song)
        layout.addWidget(button)
