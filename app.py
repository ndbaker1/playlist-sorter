import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from master import MasterWidget

APP_NAME = "Playlist Set Manager"


class MainWindow(QMainWindow):
    def __init__(self, app_name):
        super(MainWindow, self).__init__()
        self.setWindowTitle(app_name)
        self.setCentralWidget(MasterWidget(app_name))
        self.resize(1280, 720)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(APP_NAME)
    sys.exit(app.exec_())
