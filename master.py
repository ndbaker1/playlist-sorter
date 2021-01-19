import re
import os
import json
from glob import glob
from PyQt5.QtWidgets import *

from masterList import MasterList
from controls import ListControls
from playlistView import PlaylistView

APPDATA_FOLDER = 'PlaylistSorter'


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

        self.initConfig()

        self.addWidget(self.masterList)
        self.addWidget(self.listControls)
        for playlistFile in self.config['openPlaylists']:
            playlist = PlaylistView(
                playlistFile,
                self.masterList.removeSongs
            )
            self.addWidget(playlist)
            self.playlistWidgets.append(playlist)
            self.masterList.loadSongs()
        self.masterList.loadSongs()

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
        self.config['openPlaylists'].append(playlistFile)
        self.writeConfig()

    def updateSongDirectory(self):
        self.masterList.songDirectory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + '/'
        self.config['songDirectory'] = self.masterList.songDirectory
        self.writeConfig()
        self.masterList.loadSongs()

    #########################################################
    #   checks for config file and creates one if not found
    #########################################################
    def initConfig(self):
        appdataPath = os.getenv('APPDATA').replace('\\', '/')
        appdataPath += '/' + APPDATA_FOLDER
        os.makedirs(appdataPath, exist_ok=True)

        self.configFilePath = appdataPath + '/config.json'

        if os.path.exists(self.configFilePath):
            with open(self.configFilePath, 'r') as configFile:
                self.config = json.load(configFile)
                self.masterList.songDirectory = self.config['songDirectory']
        else:
            with open(self.configFilePath, 'w') as configFile:
                self.config = {
                    'songDirectory': '',
                    'openPlaylists': []
                }
                self.writeConfig()

    def writeConfig(self):
        with open(self.configFilePath, 'w') as configFile:
            json.dump(self.config, configFile)
