import os
import json
from appdata import AppDataPaths
from PyQt5.QtWidgets import QSplitter, QFileDialog

from masterList import MasterList
from playlistView import PlaylistView
from utilities import file_path_exists

'''
Notes:
    Whenever you see (QListWidgetItem).data(_),
    .data(_) takes a Role enum, which we are using 0x0100 for user-controlled data
'''

'''
The Top Level parent of the Widget Tree, which contains all references to the config state
'''


class MasterWidget(QSplitter):
    def __init__(self, app_name):
        super(MasterWidget, self).__init__()
        # Initialize or read config file in appdata path
        self.init_config(app_name)
        # Create MasterList
        self.master_list = MasterList(self, self.config['songDirectory'])
        self.addWidget(self.master_list)
        # Create a PlaylistView for every open playlist in the config
        for playlistFile in self.config['openPlaylists']:
            self.addWidget(self.create_playlist(playlistFile))
        # update the masterlist
        self.master_list.load_song_list()

    '''
    Checks for config file and creates one if not found
    '''

    def init_config(self, app_name) -> None:
        self.appdata = AppDataPaths(app_name=app_name, config_ext='json')
        self.appdata.setup(verbose=True)
        configFileSize = os.stat(self.appdata.main_config_path).st_size
        if configFileSize > 0:
            with open(self.appdata.main_config_path, 'r') as configFile:
                self.config = json.load(configFile)
                for listfile in self.config['openPlaylists']:
                    if not file_path_exists(listfile):
                        self.config['openPlaylists'].remove(listfile)
            # write and possible changes
            with open(self.appdata.main_config_path, 'w') as configFile:
                json.dump(self.config, configFile)
        else:
            with open(self.appdata.main_config_path, 'w') as configFile:
                self.config = {'songDirectory': '', 'openPlaylists': []}
                json.dump(self.config, configFile)

    '''
    Calls Dialog to get playlist file, 
    then adds a new PlaylistView Widget for the file
    '''

    def open_playlist(self):
        playlistFile = QFileDialog.getOpenFileName(self, "Select Playlist")[0]
        if file_path_exists(playlistFile) and len(playlistFile) > 0 and self.config['openPlaylists'].count(playlistFile) == 0:
            playlist = self.create_playlist(playlistFile)
            self.addWidget(playlist)
            self.config['openPlaylists'].append(playlistFile)
            self.write_config_changes()

    '''
    Calls a Dialog to choose a new directory to search for audio files,
    '''

    def update_song_directory(self):
        newSongDirectory = str(QFileDialog.getExistingDirectory(
            self, "Select Directory",  self.config['songDirectory'])) + '/'
        if len(newSongDirectory) > 1 and file_path_exists(newSongDirectory):
            self.config['songDirectory'] = newSongDirectory
            self.write_config_changes()

    '''
    Write any changes in the config to the config file
    * all changes affect the songs, so there is a default update for the MasterList
    '''

    def write_config_changes(self) -> None:
        with open(self.appdata.main_config_path, 'w') as configFile:
            json.dump(self.config, configFile)
        self.master_list.load_song_list()

    '''
    Helper for creating a PlaylistView in one line
    '''

    def create_playlist(self, file_path):
        return PlaylistView(
            playlistFile=file_path,
            remove_self=lambda filepath: [self.config['openPlaylists'].remove(filepath), self.write_config_changes()],
            take_selected_songs=self.master_list.song_list_widget.pop_selected_song_items,
            update_changes=self.master_list.load_song_list,
        )
