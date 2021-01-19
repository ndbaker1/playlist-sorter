import re
from glob import glob
from PyQt5.QtWidgets import *


MUSIC_FORMATS = ['mp3', 'm4a']


class MasterList(QWidget):
    def __init__(self, playlistWidgets):
        super(MasterList, self).__init__()
        self.songDirectory = ''
        self.playlistWidgets = playlistWidgets
        self.listWidget = QListWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.listWidget)

    def removeSongs(self):
        return [self.listWidget.takeItem(item.row()) for item in self.listWidget.selectedIndexes()]

    def loadSongs(self):
        self.listWidget.clear()
        self.listWidget.addItems(self.unassignedSongs())

    def unassignedSongs(self) -> list:
        songs = [
            f.replace('\\', '/').replace(self.songDirectory, '')
            for f in glob(self.songDirectory + '**/*', recursive=True)
            if re.match(f".*\.({ '|'.join(MUSIC_FORMATS) })", f)
        ]

        # filter songs by those that are already assigned
        return songs
