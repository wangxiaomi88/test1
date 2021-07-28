# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'land_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush,QPixmap
from PyQt5.QtWidgets import QMainWindow

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 1000)

        icon = QtGui.QIcon()
        icon_pic=QPixmap("./window_resources/机器人.png")
        icon.addPixmap(icon_pic, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        palette = QtGui.QPalette()
        bk = QPixmap("./window_resources/background.jpg")
        bk = bk.scaled(MainWindow.width(),MainWindow.height())
        palette.setBrush(QtGui.QPalette.Background,QBrush(bk))
        # palette.setBrush(MainWindow.backgroundRole(), QBrush(QPixmap("./window resources/background.png").scaled(MainWindow.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)))
        MainWindow.setPalette(palette)



        self.landButton = QtWidgets.QPushButton(self.centralwidget)
        self.landButton.setGeometry(QtCore.QRect(160, 320, 280, 36))
        self.landButton.clicked.connect(self.callback_of_landbutton)

        self.landButton.setStyleSheet("QPushButton{background:rgb(50,170,220);border-radius:15px;}QPushButton:hover{background:rgb(0,220,255);}")

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.landButton.setFont(font)

        self.landButton.setObjectName("Button_land")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "聊聊--软件界面"))
        self.landButton.setText(_translate("MainWindow", "发 送"))


    def callback_of_landbutton(self):
        print("发送了信息！")



    def main(self):
        app = QtWidgets.QApplication(sys.argv)
        chatwindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(chatwindow)
        chatwindow.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        chatwindow.show()

        sys.exit(app.exec_())
        # chatwindow.close()



if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
    MainWindow.show()

    sys.exit(app.exec_())
    MainWindow.close()

