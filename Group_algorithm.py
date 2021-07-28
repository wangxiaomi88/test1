#!/usr/bin/env python
# coding: utf-8


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow
import time
import re


class Land_Window(QMainWindow):

    signal_update_result=QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_set = []
        self.team_L = []
        self.picked_result = []
        self.result_set=[]
        self.length=0
        self.count = 0

        self.setupUi()



    def setupUi(self):

        self.signal_update_result.connect(self.update_show)
        self.setObjectName("MainWindow")
        self.resize(300, 250)

        icon = QtGui.QIcon()
        icon_pic = QPixmap("./window_resources/present10.png")
        icon.addPixmap(icon_pic, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("严教遍历")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)



        self.font = QtGui.QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(16)

        self.label_id = QtWidgets.QLabel(self.centralwidget)
        self.label_id.setGeometry(QtCore.QRect(10, 210, 80, 36))
        self.label_id.setText("牌号：")
        self.label_id.setFont(self.font)
        # self.label_id.setStyleSheet("color:rgb(220,220,220)")



        self.lineEdit_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_id.setGeometry(QtCore.QRect(80, 210, 210, 36))
        self.lineEdit_id.setText("")
        self.lineEdit_id.setFont(self.font)
        self.lineEdit_id.setFrame(0)
        self.lineEdit_id.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_id.returnPressed.connect(self.group_classify)



        self.resultText = QtWidgets.QTextEdit(self.centralwidget)
        self.resultText.setGeometry(QtCore.QRect(0, 5, 300, 200))
        self.resultText.setReadOnly(True)


        self.resultText.setFont(self.font)
        self.resultText.setStyleSheet("QTextEdit{background-color:rgb(200,200,200);border-radius:5px}")
        self.resultText.setObjectName("result_show")
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)





    def equal_group(self,l1,l2,l3,l4):
        l1=sorted(l1)
        l2=sorted(l2)
        l3=sorted(l3)
        l4=sorted(l4)

        if (l1 == l3) and (l2==l4):
            return True
        elif (l1==l4) and (l2==l3):
            return True
        else:
            return False





    def repetition_judge(self,L,R):
        temp_set=self.result_set[:]
        for temp in temp_set:

            if self.equal_group(temp[0],temp[1],L,R):
                return -1


        return self.length - (len(L)+len(R))







    def find_member(self,target):

        if self.count < 6:
            if sum(self.data_set) == target:
                str_L = ""
                str_R = ""
                for i in self.team_L:
                    k = str(i)

                    if i == 1:
                        k = "A"
                    elif i == 11:
                        k = "J"
                    elif i == 12:
                        k = "Q"
                    elif i == 13:
                        k = "K"

                    str_L += k + " "

                for i in self.data_set:
                    k = str(i)

                    if i == 1:
                        k = "A"
                    elif i == 11:
                        k = "J"
                    elif i == 12:
                        k = "Q"
                    elif i == 13:
                        k = "K"

                    str_R += k + " "

                repeat_flag=self.repetition_judge(self.team_L[:],self.data_set[:])

                if repeat_flag>=0:
                    if repeat_flag==0:
                        print("左边组：", str_L, "右边组：", str_R)
                        # self.signal_update_result.emit("<font color = 'green'>左组："+ str_L+ "；右组："+ str_R+"<br>")
                        self.resultText.insertHtml("<font color = 'green'>左组："+ str_L+ "；右组："+ str_R+"<br>")
                        app.processEvents()

                    elif repeat_flag == 1:
                        print("左边组：", str_L, "右边组：", str_R)
                        # self.signal_update_result.emit("<font color = 'black'>左组：" + str_L + "；右组：" + str_R + "<br>")
                        self.resultText.insertHtml("<font color = 'black'>左组：" + str_L + "；右组：" + str_R + "<br>")
                        app.processEvents()

                    elif repeat_flag > 1:
                        print("左边组：", str_L, "右边组：", str_R)
                        # self.signal_update_result.emit("<font color = 'red'>左组：" + str_L + "；右组：" + str_R + "<br>")
                        self.resultText.insertHtml("<font color = 'red'>左组：" + str_L + "；右组：" + str_R + "<br>")
                        app.processEvents()

                    self.result_set.append((self.team_L[:],self.data_set[:]))
                    self.count += 1

                return


            for n in self.data_set:
                self.team_L.append(n)
                self.data_set.remove(n)
                self.find_member(n + target)
                self.data_set.append(n)
                self.team_L.pop(-1)

        else:
            return





    def pick_from_list(self,d_list, n):

        if n == len(d_list):
            temp = d_list[:]
            self.picked_result.append(temp)
            return

        elif n < len(d_list):
            for i in d_list:
                temp = d_list[:]
                temp.remove(i)
                self.pick_from_list(temp, n)

    def group_classify(self):

        self.resultText.clear()


        self.count = 0
        self.result_set = []
        self.length = 0

        input_judge=re.findall("[^a,j,q,k,t,0-9]",self.lineEdit_id.text())
        if len(input_judge)>0:
            self.resultText.setText("输入非法！")

        else:
            data_ori = []
            for s in self.lineEdit_id.text():

                if (s == "t") or (s == "T") or (s=="0"):
                    a = 10
                elif (s == "j") or (s == "J"):
                    a = 11
                elif (s == "q") or (s == "Q"):
                    a = 12
                elif (s == "k") or (s == "K"):
                    a = 13
                elif (s == "a") or (s == "A"):
                    a=1
                else:
                    a = int(s)
                data_ori.append(a)
            self.length = len(data_ori)
            print("输入长度：{}".format(self.length))
            print(data_ori)

            if self.length>=12:
                data_ori=data_ori[0:11]


            for n in range(len(data_ori), 1, -1):
                self.pick_from_list(data_ori, n)

                for list_temp in self.picked_result:
                    self.data_set = list_temp[:]
                    self.find_member(0)

                self.picked_result = []

        self.lineEdit_id.clear()



    def update_show(self,arg):


        # sentence= QtWidgets.QTextEdit()
        # sentence.setGeometry(QtCore.QRect(0, 5, 300, 50))
        # sentence.setReadOnly(True)
        # sentence.setHtml(arg)
        # sentence.show()

        self.resultText.insertHtml(arg)
        self.resultText.show()















if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    land_window = Land_Window()

    land_window.show()
    sys.exit(app.exec_())
