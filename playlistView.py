from PyQt5.QtWidgets import *
from utilities import clean_string


class PlaylistView(QWidget):
    def __init__(self, playlistFile, remove_self, take_selected_songs, update_changes):
        super(PlaylistView, self).__init__()
        self.file = playlistFile

        self.list_widget = QListWidget()
        with open(self.file, 'r', encoding='utf-8') as playlist:
            for song in [clean_string(line) for line in playlist.readlines()]:
                listItem = QListWidgetItem()
                listItem.setText(song[song.rindex('/') + 1:])
                listItem.setData(0x0100, song)
                self.list_widget.addItem(listItem)

        buttons = QWidget()
        button_layout = QHBoxLayout(buttons)

        button = QPushButton(text='Close')
        button.setMinimumHeight(40)
        button.clicked.connect(lambda: [
            remove_self(self.file),
            update_changes(),
            self.deleteLater()
        ])
        button_layout.addWidget(button)

        button = QPushButton(text='Add')
        button.setMinimumHeight(40)
        button.clicked.connect(lambda: [
            [self.list_widget.addItem(item) for item in take_selected_songs()],
            self.list_widget.sortItems(),
            self.write_changes(),
        ])
        button_layout.addWidget(button)

        button = QPushButton(text='Remove')
        button.setMinimumHeight(40)
        button.clicked.connect(lambda: [
            self.remove_selected_items(),
            self.write_changes(),
            update_changes()
        ])
        button_layout.addWidget(button)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self.file))
        layout.addWidget(self.list_widget)
        layout.addWidget(buttons)

    def remove_selected_items(self):
        return [self.list_widget.takeItem(item.row()) for item in self.list_widget.selectedIndexes()]

    def write_changes(self):
        with open(self.file, 'w', encoding='utf-8') as playlist:
            for line in [self.list_widget.item(index).data(0x0100) for index in range(self.list_widget.count())]:
                playlist.write(line + '\n')
