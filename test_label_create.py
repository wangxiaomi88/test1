from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import *

import sys
class A(QWidget):
    def __init__(self):
        super(A,self).__init__()
        self.resize(450, 600)
        self.sendButton = QtWidgets.QPushButton(self)
        self.sendButton.setGeometry(QtCore.QRect(400, 500, 50, 100))
        self.sendButton.setText("发送")
        # self.layout=QGridLayout(self)
        # self.btn=QPushButton('添加')
        # self.addWidget(self.sendButton)
        # self.setLayout(self.layout)
        self.sendButton.clicked.connect(self.btn1)
        self.scale=0;

    def btn1(self):
        # label={}
        # ok,f=QFileDialog.getOpenFileNames(self,'打开','/','png(*.png)')
        # for i,j in enumerate(ok):
        #     label[i]=QLabel(str(i))
        #     label[i].setFixedSize(100,100)
        #     self.layout.addWidget(label[i])
        #     pix=QPixmap(j)
        #     label[i].setPixmap(pix)
        #     self.resize(pix.width(),pix.height())

        sentence = QtWidgets.QLabel(self)
        sentence.setText("haha")
        sentence.move(50,self.scale)
        sentence.show()
        self.scale +=15







if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = A()
    win.show()
    sys.exit(app.exec_())