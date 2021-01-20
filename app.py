import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from master import MasterWidget

try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath('.')
ICON_PATH = os.path.join(base_path, 'app.ico')
APP_NAME = "Playlist Set Manager"
STYLESHEET_URL = 'https://raw.githubusercontent.com/ColinDuquesnoy/QDarkStyleSheet/master/qdarkstyle/style.qss'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(APP_NAME)
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setStyleSheet(requests.get(STYLESHEET_URL).text)
        self.setCentralWidget(MasterWidget(APP_NAME))
        self.resize(1280, 720)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
