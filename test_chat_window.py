import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QDialog
import test_codec_mes
from test_public_resource import *

class Chat_Window(QMainWindow):

    receive_sentence_born = QtCore.pyqtSignal(int,str) #信号定义在类成员中！！！

    def __init__(self, client_bw=None, me=-1, other=-2, parent=None):
        super().__init__(parent=parent)
        self.client = client_bw
        self.me = me
        self.other = other
        self.font = QtGui.QFont()
        self.count=0
        self.scale=0
        self.portrait_pic=Public_Resource.Portrait_sequence[0]
        self.sentence_list=[]
        self.portrait_list=[]
        self.receive_sentence_born.connect(self.receive_sentence_show)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ChatDialog")
        self.resize(450, 600)


        self.font.setFamily("微软雅黑")
        self.font.setPointSize(16)


        icon = QtGui.QIcon()
        # icon_pic = QPixmap("./window_resources/present11.png")
        icon_pic =Public_Resource.Portrait_sequence[self.other]
        icon.addPixmap(icon_pic, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        palette = QtGui.QPalette()
        bk = QPixmap("./window_resources/background.png")
        bk = bk.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QBrush(bk))
        self.setPalette(palette)

        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(400, 500, 50, 100))
        self.sendButton.clicked.connect(self.callback_of_sendButton)


        self.sendButton.setStyleSheet(
            "QPushButton{background:rgb(50,170,220);border-radius:1px;}QPushButton:hover{background:rgb(0,220,255);}")

        self.sendButton.setFont(self.font)
        self.sendButton.setObjectName("sendButton")

        self.setWindowTitle("{}向{}的聊天框".format(str(self.me), str(self.other)))
        self.sendButton.setText("发送")
        self.sendButton.setIcon(QtGui.QIcon(QPixmap(Public_Resource.Portrait_sequence[self.me])))


        self.inputEdit=QtWidgets.QTextEdit(self.centralwidget)
        self.inputEdit.setGeometry(QtCore.QRect(0, 500, 400, 100))
        self.font.setPointSize(12)
        self.inputEdit.setFont(self.font)
        self.inputEdit.setObjectName("inputEdit")

        self.sentence_size_label=QtWidgets.QLabel(self.centralwidget)

        self.topFiller = QtWidgets.QWidget(self.centralwidget)
        self.topFiller.setMinimumSize(self.width(), self.height()-self.inputEdit.height())  #######设置滚动条的尺寸

        self.scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll.setWidget(self.topFiller)

        self.scroll.resize(self.topFiller.width(), self.topFiller.height())
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollBar = self.scroll.verticalScrollBar()
        self.scrollBar.setValue(self.topFiller.height())





        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowModality(QtCore.Qt.NonModal)

    def receive_sentence(self, source, target, data):
        if source == self.other and target == self.me:
            print("{}号对我{}号说：{}".format(str(source), str(target), data))

            self.receive_sentence_born.emit(source,data)



    def receive_sentence_show(self,source,data):

        sentence = QtWidgets.QTextEdit(self.topFiller)

        # sentence.setText("TA（{}号）：".format(source) + data)
        portrait = QtWidgets.QLabel(self.topFiller)
        self.portrait_pic = Public_Resource.Portrait_sequence[source]
        portrait.setGeometry(QtCore.QRect(0, 0, 30, 30))
        portrait.setPixmap(self.portrait_pic)
        portrait.setScaledContents(True)
        portrait.setObjectName("portrait{}".format(str(self.count)))


        sentence.setText(data)
        self.font.setPointSize(12)
        sentence.setFont(self.font)
        sentence.setStyleSheet("QTextEdit{background-color:rgb(250,250,20);border-radius:5px}")
        sentence.setObjectName("sentence{}".format(str(self.count)))

        sentence.resize(300, 100)

        self.sentence_size_label.setText(data)
        self.sentence_size_label.setFont(self.font)
        self.sentence_size_label.setStyleSheet("QTextEdit{background-color:rgb(20,250,20);border-radius:5px}")
        self.sentence_size_label.setWordWrap(True)

        fontMetrics = QtGui.QFontMetrics(self.font)
        textSize = fontMetrics.size(0, sentence.toPlainText())

        if textSize.width()>300:

            self.sentence_size_label.setFixedWidth(300)
            self.sentence_size_label.adjustSize()

            sentence.ensureCursorVisible()  # 游标可用
            cursor = sentence.textCursor()  # 设置游标
            pos = len(sentence.toPlainText())  # 获取文本尾部的位置


            new_height=max(pos,self.sentence_size_label.height())

            cursor.setPosition(pos)  # 游标位置设置为尾部
            sentence.setTextCursor(cursor)  # 滚动到游标位置

            sentence.resize(300,new_height+15)


        else:
            sentence.resize(textSize.width()+10,textSize.height()+10)








        portrait.move(0,self.scale)
        sentence.move(30+5, self.scale)

        self.scale += sentence.height() + 5
        if self.scale+sentence.height()>self.topFiller.height():
            self.topFiller.setFixedHeight(self.scale+sentence.height())
            self.scrollBar.setValue(self.topFiller.height())

        portrait.show()
        sentence.show()
        self.portrait_list.append(portrait)
        self.sentence_list.append(sentence)
        self.count += 1





    def callback_of_sendButton(self):
        txt=self.inputEdit.toPlainText()
        # mes = test_codec_mes.encode_mes("COMM", "用户{}向你问好".format(str(self.me)), self.me, self.other)

        if __name__!="__main__":
            mes = test_codec_mes.encode_mes("COMM", txt, self.me, self.other)
            mes_to_server = mes.encode('utf-8')
            self.client.sendall(mes_to_server)  # 发送数据到客户端
            time.sleep(0.01)


        portrait = QtWidgets.QLabel(self.topFiller)
        self.portrait_pic=Public_Resource.Portrait_sequence[self.me]
        portrait.setGeometry(QtCore.QRect(0, 0, 30, 30))
        portrait.setPixmap(self.portrait_pic)
        portrait.setScaledContents(True)
        portrait.setObjectName("portrait{}".format(str(self.count)))

        sentence = QtWidgets.QTextEdit(self.topFiller)
        sentence.setText(txt)
        sentence.setReadOnly(True)
        self.font.setPointSize(12)

        sentence.setFont(self.font)
        sentence.setStyleSheet("QTextEdit{background-color:rgb(20,250,20);border-radius:5px}")
        sentence.setObjectName("sentence{}".format(str(self.count)))
        sentence.resize(300,100)
        # sentence.setVerticalScrollBar(QtCore.Qt.ScrollBarAlwaysOff)
        # sentence.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.sentence_size_label.setText(txt)
        self.sentence_size_label.setFont(self.font)
        self.sentence_size_label.setStyleSheet("QTextEdit{background-color:rgb(20,250,20);border-radius:5px}")
        self.sentence_size_label.setWordWrap(True)

        fontMetrics = QtGui.QFontMetrics(self.font)
        textSize = fontMetrics.size(0, sentence.toPlainText())


        if textSize.width()>300:

            self.sentence_size_label.setFixedWidth(300)
            self.sentence_size_label.adjustSize()

            sentence.ensureCursorVisible()  # 游标可用
            cursor = sentence.textCursor()  # 设置游标
            pos = len(sentence.toPlainText())  # 获取文本尾部的位置

            new_height=max(pos,self.sentence_size_label.height())

            cursor.setPosition(pos)  # 游标位置设置为尾部
            sentence.setTextCursor(cursor)  # 滚动到游标位置


            # d = sentence.document()
            # d.setTextWidth(300)
            # d.adjustSize()
            # print(d.size().width(), d.size().height())


            sentence.resize(300,new_height+15)

            # if self.sentence_size_label.width()<=420:
            #     sentence.setFixedWidth(self.sentence_size_label.width() + 10)
            #     sentence.setFixedHeight(self.sentence_size_label.height() + 20)
            #
            # else:
            #
            #     d = sentence.document()
            #     d.adjustSize()
            #     print(d.size().width(),d.size().height())
        else:
            sentence.resize(textSize.width()+10,textSize.height()+10)



        portrait.move(self.width() - 20 - portrait.width(), self.scale)
        sentence.move(self.width()-20-portrait.width()-sentence.width()-5,self.scale)


        self.scale += sentence.height()+5
        if self.scale+sentence.height()>self.topFiller.height():
            self.topFiller.setFixedHeight(self.scale+sentence.height())
            self.scrollBar.setValue(self.topFiller.height())

        portrait.show()
        sentence.show()

        self.portrait_list.append(portrait)
        self.sentence_list.append(sentence)
        self.count += 1
        self.inputEdit.clear()


    def closeEvent(self, event):
        if self.client:
            mes = test_codec_mes.encode_mes("CHATCLOSE", "", self.me, self.other)
            mes_to_server = mes.encode('utf-8')
            self.client.sendall(mes_to_server)  # 发送数据到客户端
            time.sleep(0.01)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    pub_res_init()
    Public_Resource.Portrait_sequence_init()

    chat_window = Chat_Window()

    chat_window.show()
    sys.exit(app.exec_())
