from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit


class PlaylistPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super(PlaylistPanel, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel('Panel'))


class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        self.setupPanels()

    def setupPanels(self):
        layout = QHBoxLayout(self)
        layout.addWidget(PlaylistPanel())
        layout.addWidget(PlaylistPanel())
        layout.addWidget(PlaylistPanel())
