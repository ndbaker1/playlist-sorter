import re
import os
from glob import glob
from PyQt5.QtWidgets import *

from masterList import MasterList
from controls import ListControls
from playlistView import PlaylistView


class MasterWidget(QSplitter):
    def __init__(self):
        super(MasterWidget, self).__init__()
        self.playlistWidgets = []
        self.masterList = MasterList(self.playlistWidgets)
        self.listControls = ListControls(
            self.addPlaylist,
            self.updateSongDirectory,
            self.masterList
        )

        self.addWidget(self.masterList)
        self.addWidget(self.listControls)

    def addPlaylist(self):
        playlistFile = QFileDialog.getOpenFileName(self, "Select Playlist")[0]
        if not os.path.exists(playlistFile):
            return
        playlist = PlaylistView(
            playlistFile,
            self.masterList.removeSongs
        )
        self.addWidget(playlist)
        self.playlistWidgets.append(playlist)
        self.masterList.loadSongs()

    def updateSongDirectory(self):
        self.masterList.songDirectory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + '/'
        self.masterList.loadSongs()
