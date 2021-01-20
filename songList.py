from PyQt5.QtWidgets import *
from utilities import *


class SongListWidget(QListWidget):
    def __init__(self):
        super(SongListWidget, self).__init__()
        self.itemDoubleClicked.connect(lambda songItem: play_song(songItem.data(0x0100)))

    def add_song(self, song_file_path: str) -> None:
        songItem = QListWidgetItem()
        songItem.setText(song_file_path[song_file_path.rindex('/') + 1:])
        songItem.setData(0x0100, song_file_path)
        self.addItem(songItem)

    def pop_selected_song_items(self) -> list:
        return [self.takeItem(item.row()) for item in self.selectedIndexes()]

    def get_song_paths(self) -> list:
        return [self.item(index).data(0x0100) for index in range(self.count())]
