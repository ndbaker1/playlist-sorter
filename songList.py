from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from utilities import play_song

'''
A Widget just for easier insertion and retrieval of QListWidget data
for the purpose of handling file paths for songs
'''


class SongListWidget(QListWidget):
    def __init__(self):
        super(SongListWidget, self).__init__()
        self.itemDoubleClicked.connect(lambda songItem: play_song(songItem.data(0x0100)))

    '''
    Adds a ListItem with the full path as data,
    and the base filename as the display text
    '''

    def add_song(self, song_file_path: str) -> None:
        songItem = QListWidgetItem()
        songItem.setText(song_file_path[song_file_path.rindex('/') + 1:])
        songItem.setData(0x0100, song_file_path)
        self.addItem(songItem)

    '''
    Returns an array of the selected items, which were removed from the current List
    '''

    def pop_selected_song_items(self) -> list:
        return [self.takeItem(item.row()) for item in self.selectedIndexes()]

    '''
    Returns an array of the SongList items mapped to their full song filepath
    '''

    def get_song_paths(self) -> list:
        return [self.item(index).data(0x0100) for index in range(self.count())]
