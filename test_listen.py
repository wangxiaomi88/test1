# 服务器py文件


import socket
import multiprocessing
from queue import Queue, Empty
import time, threading
import sys
import pygame
from pygame.locals import *
import random

import test_client
import test_codec_mes
from test_public_resource import *

class Client_element:
    def __init__(self, id_num, name="",friend_id_list=[0,1,2,3],land_state="False"):
        self.id_num = id_num
        self.name = name
        self.land_state = land_state
        self.bindword = None
        self.friend_id_list = friend_id_list

    def set_info(self, name="", land_state="", bw=""):
        self.name = name
        self.land_state = land_state
        self.bindword = bw


pub_res_init()
client_all_list = []
for i in range(100):
    member=Client_element(id_num=Public_Resource.ID_sequence[i], name=Public_Resource.Name_sequence[i])
    member.friend_id_list=Public_Resource.Friend_relationship[i]
    client_all_list.append(member)


online_id_list = []
online_name_list = []


def broadcast_everyone(kind="ONLINE"):
    global client_all_list
    global online_id_list
    global online_name_list

    if kind == "ONLINE":
        for c_temp in client_all_list:
            if c_temp.land_state == True:
                mes = test_codec_mes.encode_mes("ONLINE", content=online_id_list)
                mes_to_client = mes.encode('utf-8')
                c_temp.bindword.sendall(mes_to_client)
                time.sleep(0.01)

    elif kind=="IDLEAVE":
        for c_temp in client_all_list:
            if c_temp.land_state == True:
                mes = test_codec_mes.encode_mes("IDLEAVE", content=online_id_list)
                mes_to_client = mes.encode('utf-8')
                c_temp.bindword.sendall(mes_to_client)
                time.sleep(0.01)




def land_check():
    global client_all_list
    global online_id_list
    global online_name_list

    BUF_SIZE = 1024  # 设置缓冲区大小
    # server_addr = ('192.168.1.102', 7500)  # IP和端口构成表示地址

    hostname = socket.gethostname()
    print("Host name: %s" % hostname)
    sysinfo = socket.gethostbyname_ex(hostname)
    ip_addr = sysinfo[2]

    server_addr = (ip_addr[0], 7500)  # IP和端口构成表示地址
    print(server_addr)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 生成一个新的socket对象
    server.bind(server_addr)  # 绑定地址
    print("socket与地址绑定完成……")

    server.listen(15)  # 监听, 最大监听数为5

    # print("服务端状态如下：")
    # if (getattr(server, '_closed') == False):
    #     print("当前socket服务端正在运行中")
    # elif (getattr(server, '_closed') == True):
    #     print("当前socket服务端已经关闭了")


    client_num = 0
    loop_flag = True
    while loop_flag:

        print("正在监听是否有用户连接登陆...", end="\n")

        client, client_addr = server.accept()  # 接收TCP连接, 并返回新的套接字和地址, 阻塞函数
        client_num += 1

        mes = "IFF_ID_NAME"
        mes_to_client = mes.encode('utf-8')
        client.sendall(mes_to_client)  # 发送数据到客户端
        time.sleep(0.01)


        mes_from_client = client.recv(BUF_SIZE)  # 从服务器端接收数据
        mes = mes_from_client.decode('utf-8')



        if mes != "temp_search":
            submark = mes.find("_")
            n = int(mes[0:submark])
            # name = mes[submark + 1:]
            name = client_all_list[n].name

            print('监听到有客户端连接，其地址为：{}，其id为：{}，昵称为：{}'.format(client_addr, str(n), name), end="\n")

            client_all_list[n].set_info(land_state=True, bw=client)
            online_id_list.append(n)
            online_name_list.append(name)

            time.sleep(0.1)
            mes = test_codec_mes.encode_mes("FRIENDS", client_all_list[n].friend_id_list, n)
            print(mes)
            mes_to_client = mes.encode('utf-8')
            client.sendall(mes_to_client)  # 发送数据到客户端
            time.sleep(0.01)

            t_new = threading.Thread(target=receive_from_client, args=(n, client_all_list[n].bindword))
            t_new.start()

            broadcast_everyone()

            if -1 in online_id_list:
                loop_flag = False
                break

    print("服务器监听结束")


def receive_from_client(id_num, bindword):
    global client_all_list
    global online_id_list
    global online_name_list

    client = bindword

    BUF_SIZE = 1024  # 设置缓冲区大小

    print("开始用户id{}的receive_from_client循环".format(id_num))

    loop_flag = True
    while loop_flag:
        mes_from_client = client.recv(BUF_SIZE)  # 从服务器端接收数据
        mes = mes_from_client.decode('utf-8')
        legal, kind, source, target, content = test_codec_mes.decode_mes(mes)
        print("来自用户{}号对用户{}号的信息：{}".format(str(source), str(target), str(content)))
        print(kind)

        if kind == "COMM":
            if client_all_list[target].land_state:
                print("发送信息{}给目标{}号".format(mes, str(target)))
                mes_to_client = mes.encode('utf-8')
                client_all_list[target].bindword.sendall(mes_to_client)
                time.sleep(0.01)

        if kind == "CHATCLOSE":
            mes_to_client = mes.encode('utf-8')
            client_all_list[id_num].bindword.sendall(mes_to_client)
            time.sleep(0.01)

        if kind == "OFFLINE":
            mes = test_codec_mes.encode_mes(kind="OFFLINE",content="",source=source)
            mes_to_client = mes.encode('utf-8')
            client_all_list[id_num].bindword.sendall(mes_to_client)
            time.sleep(0.01)

            client_all_list[id_num].set_info(name="", land_state=False, bw="")

            submark = online_id_list.index(id_num)
            print("下标：" + str(submark))
            del online_name_list[submark]
            online_id_list.remove(id_num)



            loop_flag = False
            break

    print("用户{}receive_from_client循环结束".format(str(id_num)))
    # broadcast_everyone("IDLEAVE")


# def receive_from_server(id_num,client):

#     BUF_SIZE = 1024 #设置缓冲区的大小

#     n=id_num

#     print("开始服务器对用户id{}的receive_from_server循环".format(n))

#     loop_flag=True
#     while loop_flag:

#         mes_from_client = client.recv(BUF_SIZE) #从服务器端接收数据
#         mes = mes_from_client.decode('utf-8')
#         print(mes,end="\n")

#         if mes == "OFFLINE":
#             loop_flag=False
#             break


#     print("用户{}的receive_from_server循环关闭".format(str(n)))


# def AI_client_leave(id_num,client):

#     print("用户id{}完成登陆，开始睡眠".format(id_num))

#     time.sleep(random.randint(1,30))

#     print("用户id{}结束睡眠，准备离线".format(id_num))


#     mes="OFFLINE"
#     mes_to_server = mes.encode('utf-8')
#     client.sendall(mes_to_server)


# def AI_client_land(id_num):

#     BUF_SIZE = 1024 #设置缓冲区的大小

#     server_addr = ('192.168.1.104', 7500) #IP和端口构成表示地址
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #返回新的socket对象
#     client.connect(server_addr) #连接服务器

#     mes_from_server = client.recv(BUF_SIZE) #从服务器端接收数据
#     mes = mes_from_server.decode('utf-8')
#     if mes == "ID_NAME":
#         mes=str(id_num)
#         mes_to_client = mes.encode('utf-8')
#         client.sendall(mes_to_client) #发送数据到客户端


#     t_new = threading.Thread(target=receive_from_server,args=(id_num,client))
#     t_leave = threading.Thread(target=AI_client_leave,args=(id_num,client))

#     t_new.start()
#     t_leave.start()


# def test_sleep(num):
#     print("进入睡眠子进程{}".format(str(num)))
#     time.sleep(3)
#     print("子进程{}结束".format(str(num)))


def main_input():
    global client_all_list
    global online_id_list
    global online_name_list

    t_listen = threading.Thread(target=land_check)
    t_listen.start()

    count = -1
    loop_flag = True
    while loop_flag:

        #         ####################################
        #         txt=input("请输入a触发AI上线：")

        #         if txt == "q":
        #             id_num = -1
        #             t_client=threading.Thread(target=AI_client_land(id_num))
        #             t_client.start()
        #             loop_flag=False
        #             break

        #         elif txt =="a":
        #             count += 1
        #             id_num=count
        #             t_client=threading.Thread(target=AI_client_land(id_num))
        #             t_client.start()
        #         #######################################

        txt = input("请输入AI客户的id号：")

        try:
            id_num = int(txt)
            p_new = multiprocessing.Process(target=test_client.main, args=("AI", id_num))
            p_new.start()

            #             print("主进程输入端"+str(id_num))

            if id_num == -1:
                loop_flag = False
                break

        except ValueError:
            print("非法id号")
            pass

    print("AI上线功能关闭")


if __name__ == '__main__':
    main_input()
