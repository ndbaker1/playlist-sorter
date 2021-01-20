import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from master import MasterWidget

APP_NAME = "Playlist Set Manager"
ICON_PATH = 'icon.ico'
STYLESHEET_URL = 'https://raw.githubusercontent.com/ColinDuquesnoy/QDarkStyleSheet/master/qdarkstyle/style.qss'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setStyleSheet(requests.get(STYLESHEET_URL).text)
        self.setCentralWidget(MasterWidget(APP_NAME))
        self.resize(1280, 720)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
