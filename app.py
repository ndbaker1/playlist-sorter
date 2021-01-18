import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from lib import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Playlist Set Manager')
        self.resize(640, 480)
        self.setCentralWidget(MainWidget())
        self.show()


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
