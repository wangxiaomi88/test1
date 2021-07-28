# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'land_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow
import test_codec_mes
import test_chat_window
from test_public_resource import *

class Friend_Viewer_Window(QMainWindow):

    passive_chat_window_born = QtCore.pyqtSignal(int,str)  # 信号定义在类成员中！！！



    def __init__(self, client_bw=None, id_num=0, name="", friend_id_list=[],friend_name_list=[],online_friends_list=[],parent=None):
        super().__init__(parent=parent)
        self.client = client_bw
        self.id_num = id_num
        self.name = name
        self.friend_id_list = friend_id_list
        self.friend_name_list=friend_name_list
        self.friend_online_list=online_friends_list
        self.friend_button_list = []
        self.font=None
        self.passive_chat_window_born.connect(self.passive_chat_window_show)



        self.setupUi()

        self.chat_window = None
        self.chat_window_list = []






    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(300, 600)

        icon = QtGui.QIcon()
        icon_pic = QPixmap("./window_resources/机器人.png")
        icon.addPixmap(icon_pic, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        palette = QtGui.QPalette()
        bk = QPixmap("./window_resources/background.jpg")
        bk = bk.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QBrush(bk))
        # palette.setBrush(MainWindow.backgroundRole(), QBrush(QPixmap("./window resources/background.png").scaled(MainWindow.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

        self.font = QtGui.QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(16)

        self.myportrait_label=QtWidgets.QLabel(self.centralwidget)
        self.myportrait_label.setGeometry(QtCore.QRect(int(self.width()/2-50), 0, 100, 100))
        print(self.id_num)
        self.myportrait_label.setPixmap(QtGui.QPixmap(Public_Resource.Portrait_sequence[self.id_num]))
        self.myportrait_label.setScaledContents(True)

        self.my_name_label=QtWidgets.QLabel(self.centralwidget)
        self.my_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.my_name_label.setGeometry(QtCore.QRect(0, 105, self.width(), 35))
        self.my_name_label.setText(self.name + "  好友列表")
        self.setFont(self.font)

        self.topFiller = QtWidgets.QWidget(self.centralwidget)
        self.topFiller.setMinimumSize(self.width(), self.height()-150)  #######设置滚动条的尺寸

        self.scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll.setWidget(self.topFiller)
        self.scroll.setGeometry(QtCore.QRect(0,150,self.width(),self.height()-150))

        self.scroll.resize(self.topFiller.width(), self.topFiller.height())
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollBar = self.scroll.verticalScrollBar()
        self.scrollBar.setValue(0)
        # self.scrollBar.setValue(self.topFiller.height())


        button_height=80
        h=0
        for i in range(len(self.friend_id_list)):
            if self.friend_id_list[i] != self.id_num:
                button=QtWidgets.QPushButton(self.topFiller)
                button.setFont(self.font)

                if 10+button_height*(h+1)>self.topFiller.height():
                    self.topFiller.setFixedHeight(10+button_height*(h+1))

                label_portrait = QtWidgets.QLabel(self.topFiller)


                button.setGeometry(QtCore.QRect(0, 0+button_height*h, self.width()-20, button_height))
                label_portrait.setGeometry(QtCore.QRect(10, 0+button_height*h+10, button_height-20, button_height-20))
                label_portrait.setPixmap(QtGui.QPixmap(Public_Resource.Portrait_sequence[self.friend_id_list[i]]))
                label_portrait.setScaledContents(True)

                if self.friend_id_list[i] in self.friend_online_list:
                    button.setText(self.friend_name_list[i]+" [在线]")
                    button.setStyleSheet("QPushButton{background:rgb(255,255,255);border-radius:0px;text-align:right}QPushButton:hover{background:rgb(220,220,220);}")
                else:
                    button.setText(self.friend_name_list[i] + " [离线]")
                    button.setStyleSheet("QPushButton{background:rgb(50,50,50);border-radius:0px;text-align:right}QPushButton:hover{background:rgb(100,100,100);}")


                button.setObjectName("FriendButton-{}".format(str(self.friend_id_list[i])))
                button.clicked.connect(self.callback_of_sendButton)


                self.friend_button_list.append(button)
                h += 1


        # if self.friend_button_list[-1].y+button_height>self.topFiller.height():
        #
        #     self.scrollBar.setValue(self.topFiller.height())


        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("亲爱的{}，欢迎来到御坂网络".format(self.name))
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)




    def deal_sentence(self, source, target, data):

        if target == self.id_num:
            for i in range(len(self.chat_window_list)):
                if self.chat_window_list[i].other == source:
                    self.chat_window_list[i].receive_sentence(source, target, data)
                    break
            else:
                self.passive_chat_window_born.emit(source,data)



    def passive_chat_window_show(self,arg1,arg2):
        self.chat_window = test_chat_window.Chat_Window(self.client, self.id_num, arg1, None)
        self.chat_window_list.append(self.chat_window)  # 要把临时生成的friend_window实例变量存起来，否则会被覆盖，无法形成超过2个以上的多进程窗口！！！
        self.chat_window.receive_sentence(arg1, self.id_num, arg2)
        self.chat_window.show()
        print(len(self.chat_window_list))



    def update_online_friend(self, online_friend_list):
        self.friend_online_list=online_friend_list

        print("当前在线好友为：", end=" ")
        for i in online_friend_list:
            print("id{}号".format(i), end="-")
        print("\n")

        for item in self.friend_button_list:
            btn_name = item.objectName()
            s0 = btn_name.find("-")
            temp_id = int(btn_name[s0 + 1:])

            if temp_id in self.friend_online_list:
                item.setStyleSheet("QPushButton{background:rgb(255,255,255);border-radius:0px;text-align:right}QPushButton:hover{background:rgb(220,220,220);}")
            else:
                item.setStyleSheet("QPushButton{background:rgb(50,50,50);border-radius:0px;text-align:right}QPushButton:hover{background:rgb(100,100,100);}")



    def callback_of_sendButton(self):
        btn = self.sender()
        btn_name=btn.objectName()
        s0 = btn_name.find("-")
        target=int(btn_name[s0+1:])

        self.chat_window = test_chat_window.Chat_Window(self.client, self.id_num, target, None)
        self.chat_window_list.append(self.chat_window)  # 要把临时生成的friend_window实例变量存起来，否则会被覆盖，无法形成超过2个以上的多进程窗口！！！
        self.chat_window.show()

    def closeEvent(self, event):
        if self.client:


            while len(self.chat_window_list)>0:
                self.chat_window_list[0].close()

            time.sleep(0.5)

            mes = test_codec_mes.encode_mes(kind="OFFLINE",content="",source=self.id_num)
            print("friend_viewer"+mes)
            mes_to_server = mes.encode('utf-8')
            self.client.sendall(mes_to_server)  # 发送数据到客户端
            time.sleep(0.01)


    def __str__(self):
        return "id号"+str(self.id_num)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pub_res_init()
    Public_Resource.Portrait_sequence_init()

    chat_window = Friend_Viewer_Window(friend_id_list=[1,2,3,4,5,6,7],friend_name_list=["一方通行","桓根帝督","美琴","麦野沉利","食蜂","正体不明","削板军霸"],online_friends_list=[3,4,5])
    chat_window.show()
    sys.exit(app.exec_())
