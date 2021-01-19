import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from master import MasterWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Playlist Set Manager")
        self.setCentralWidget(MasterWidget())
        self.resize(1080, 720)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
