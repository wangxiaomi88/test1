import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPixmap


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.initGui()
    def initGui(self):
        self.btn1 = QPushButton('打开独立新窗口')
        self.btn1.clicked.connect(self.command)
        self.setCentralWidget(self.btn1)
        self.show()
    def command(self):
        self.console = Console(self)
        self.console.show()

class Console(QMainWindow):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())