from PyQt5.QtWidgets import *


class PlaylistView(QWidget):
    def __init__(self, playlistFile, getSelectedItems):
        super(PlaylistView, self).__init__()
        self.file = playlistFile
        self.getSelectedItems = getSelectedItems

        self.listWidget = QListWidget()
        for song in self.readPlaylistFile(self.file):
            self.listWidget.addItem(QListWidgetItem(song))

        layout = QVBoxLayout(self)
        layout.addWidget(self.playlistButtonsWidget())
        layout.addWidget(self.listWidget)

    def readPlaylistFile(self, fileURL):
        with open(fileURL, 'r') as playlistFile:
            return [line.strip() for line in playlistFile.readlines()]

    def playlistButtonsWidget(self):
        buttons = QWidget()
        layout = QHBoxLayout(buttons)

        button = QPushButton(text='Remove')
        layout.addWidget(button)

        button = QPushButton(text='Add')
        button.clicked.connect(lambda: self.listWidget.addItems([item.text() for item in self.getSelectedItems()]))
        layout.addWidget(button)

        button = QPushButton(text='Save')
        layout.addWidget(button)

        button = QPushButton(text='Delete')
        layout.addWidget(button)

        return buttons
