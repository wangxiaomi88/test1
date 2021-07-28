
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow
import multiprocessing
import friend_viewer_3
import socket
# from queue import Queue, Empty
import time, threading
import random
import test_codec_mes


class Public_Resource:
    sequence_lengh = 100
    ID_sequence = []
    Name_sequence = []
    Portrait_sequence = []
    Friend_relationship=[]

    @classmethod
    def ID_sequence_init(cls):
        for i in range(cls.sequence_lengh):
            cls.ID_sequence.append(i)

    @classmethod
    def Name_sequence_init(cls):
        for i in range(cls.sequence_lengh):
            cls.Name_sequence.append("御坂{}号".format(int(i)))

        cls.Name_sequence[0] = "最后之作"
        cls.Name_sequence[1] = "一方通行"
        cls.Name_sequence[2] = "垣根帝督"
        cls.Name_sequence[3] = "御坂美琴"
        cls.Name_sequence[4] = "麦野沉利"
        cls.Name_sequence[5] = "食蜂操祈"
        cls.Name_sequence[6] = "正体不明"
        cls.Name_sequence[7] = "削板军霸"
        cls.Name_sequence[8] = "小明"
        cls.Name_sequence[9] = "Daisy"

    @classmethod
    def Portrait_sequence_init(cls):
        for i in range(cls.sequence_lengh):
            pic = QPixmap("./window_resources/client_portrait/default.png")
            cls.Portrait_sequence.append(pic)

        cls.Portrait_sequence[0] = QPixmap("./window_resources/client_portrait/0.png")
        cls.Portrait_sequence[1] = QPixmap("./window_resources/client_portrait/1.png")
        cls.Portrait_sequence[2] = QPixmap("./window_resources/client_portrait/2.png")
        cls.Portrait_sequence[3] = QPixmap("./window_resources/client_portrait/3.png")
        cls.Portrait_sequence[4] = QPixmap("./window_resources/client_portrait/4.png")
        cls.Portrait_sequence[5] = QPixmap("./window_resources/client_portrait/5.png")
        cls.Portrait_sequence[6] = QPixmap("./window_resources/client_portrait/6.png")
        cls.Portrait_sequence[7] = QPixmap("./window_resources/client_portrait/7.png")

    @classmethod
    def Friend_relationship_init(cls):
        for i in range(cls.sequence_lengh):
            cls.Friend_relationship.append([0,1,2,3,4,5,6])

        cls.Friend_relationship[1]=[0,2,3]
        cls.Friend_relationship[2]=[1,2,3]
        cls.Friend_relationship[3]=[1,2,3,4,5,6,7,8,9,10,11,12]
        cls.Friend_relationship[4]=[3,4,5]
        cls.Friend_relationship[5]=[2,4,6,8,10,12]






def pub_res_init():
    Public_Resource.ID_sequence_init()
    Public_Resource.Name_sequence_init()
    # Public_Resource.Portrait_sequence_init()
    Public_Resource.Friend_relationship_init()





