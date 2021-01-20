from PyQt5.QtWidgets import *
from utilities import *
from songList import SongListWidget


class PlaylistView(QWidget):
    def __init__(self, playlistFile, remove_self, take_selected_songs, update_changes):
        super(PlaylistView, self).__init__()
        self.file = playlistFile

        self.song_list_widget = SongListWidget()

        with open(self.file, 'r', encoding='utf-8') as playlist:
            for song in [clean_string(line) for line in playlist.readlines()]:
                self.song_list_widget.add_song(song)

        buttons = QWidget()
        button_layout = QHBoxLayout(buttons)

        # close button setup
        button = QPushButton(text='Close')
        button.setMinimumHeight(40)
        button.clicked.connect(lambda: [
            remove_self(self.file),
            update_changes(),
            self.deleteLater()
        ])
        button_layout.addWidget(button)

        # add song button setup
        button = QPushButton(text='Add')
        button.setMinimumHeight(40)
        button.clicked.connect(lambda: [
            [self.song_list_widget.addItem(item) for item in take_selected_songs()],
            self.song_list_widget.sortItems(),
            self.write_changes(),
        ])
        button_layout.addWidget(button)

        # remove song button setup
        button = QPushButton(text='Remove')
        button.setMinimumHeight(40)
        button.clicked.connect(lambda: [
            self.song_list_widget.pop_selected_song_items(),
            self.write_changes(),
            update_changes()
        ])
        button_layout.addWidget(button)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self.file))
        layout.addWidget(self.song_list_widget)
        layout.addWidget(buttons)

    def write_changes(self):
        with open(self.file, 'w', encoding='utf-8') as playlist:
            for line in self.song_list_widget.get_song_paths():
                playlist.write(line + '\n')
