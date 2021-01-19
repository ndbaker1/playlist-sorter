import os
from PyQt5.QtWidgets import *


class ListControls(QWidget):
    def __init__(self, playlistAdder, songDirectoryUpdater, masterList):
        super(ListControls, self).__init__()
        self.masterList = masterList

        layout = QVBoxLayout(self)

        button = QPushButton(text='Song Directory')
        button.clicked.connect(songDirectoryUpdater)
        layout.addWidget(button)

        button = QPushButton(text='Add Playlist')
        button.clicked.connect(playlistAdder)
        layout.addWidget(button)

        button = QPushButton(text='Play Song')
        button.clicked.connect(self.openSongInPlayer)
        layout.addWidget(button)

    def openSongInPlayer(self):
        os.startfile(self.masterList.songDirectory + self.masterList.listWidget.selectedItems()[0].text())
