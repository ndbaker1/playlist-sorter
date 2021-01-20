import re
import os
import json
from appdata import AppDataPaths
from PyQt5.QtWidgets import *

from masterList import MasterList
from playlistView import PlaylistView
from utilities import file_path_exists


class MasterWidget(QSplitter):
    def __init__(self, app_name):
        super(MasterWidget, self).__init__()
        self.init_config(app_name)
        self.master_list = MasterList(self)

        self.addWidget(self.master_list)
        for playlistFile in self.config['openPlaylists']:
            self.addWidget(
                PlaylistView(
                    playlistFile=playlistFile,
                    remove_self=lambda filepath: self.config['openPlaylists'].remove(filepath),
                    take_selected_songs=self.master_list.take_selected_songs,
                    update_changes=self.master_list.load_song_list,
                )
            )
        self.master_list.load_song_list()

    #########################################################
    #   checks for config file and creates one if not found
    #########################################################
    def init_config(self, app_name) -> None:
        self.appdata = AppDataPaths(app_name=app_name, config_ext='json')
        self.appdata.setup(verbose=True)
        configFileSize = os.stat(self.appdata.main_config_path).st_size
        if configFileSize > 0:
            with open(self.appdata.main_config_path, 'r') as configFile:
                self.config = json.load(configFile)
        else:
            with open(self.appdata.main_config_path, 'w') as configFile:
                self.config = {'songDirectory': '', 'openPlaylists': []}
                json.dump(self.config, configFile)

    def open_playlist(self):
        playlistFile = QFileDialog.getOpenFileName(self, "Select Playlist")[0]
        if file_path_exists(playlistFile) and self.config['openPlaylists'].count(playlistFile) == 0:
            playlist = PlaylistView(
                playlistFile=playlistFile,
                remove_self=lambda filepath: self.config['openPlaylists'].remove(filepath),
                take_selected_songs=self.master_list.take_selected_songs,
                update_changes=self.master_list.load_song_list,
            )
            self.addWidget(playlist)
            self.config['openPlaylists'].append(playlistFile)
            self.write_config_changes()

    def update_song_directory(self):
        newSongDirectory = str(QFileDialog.getExistingDirectory(
            self, "Select Directory")) + '/'
        if len(newSongDirectory) > 1 and file_path_exists(newSongDirectory):
            self.config['songDirectory'] = newSongDirectory
            self.write_config_changes()

    def write_config_changes(self) -> None:
        with open(self.appdata.main_config_path, 'w') as configFile:
            json.dump(self.config, configFile)
        self.master_list.load_song_list()
