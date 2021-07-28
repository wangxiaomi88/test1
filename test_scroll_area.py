import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

class MainWindow(QMainWindow):
    def __init__(self, ):
        super(QMainWindow, self).__init__()
        self.number = 0

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)


        self.topFiller = QWidget(self)
        self.topFiller.setMinimumSize(200, 1000)  #######设置滚动条的尺寸


        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.topFiller)

        self.scroll.resize(210,400)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollBar = self.scroll.verticalScrollBar()
        self.scrollBar.setValue(300)


        for filename in range(20):
            self.MapButton = QPushButton(self.topFiller)
            self.MapButton.setText(str(filename))
            self.MapButton.move(10, filename * 40)





        self.statusBar().showMessage("底部信息栏")
        self.resize(300, 500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
