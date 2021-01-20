import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from master import MasterWidget

APP_NAME = "Playlist Set Manager"
ICON_PATH = 'icon.ico'


class MainWindow(QMainWindow):
    def __init__(self, app_name, icon_path):
        super(MainWindow, self).__init__()
        self.setWindowTitle(app_name)
        self.setWindowIcon(QIcon(icon_path))
        self.setCentralWidget(MasterWidget(app_name))
        self.resize(1280, 720)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(APP_NAME, ICON_PATH)
    sys.exit(app.exec_())
