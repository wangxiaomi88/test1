# 用户端py文件


import socket
from queue import Queue, Empty
import time, threading
import sys
import pygame
from pygame.locals import *
import random
import test_codec_mes

def receive_from_server(id_num, client):
    global friend_state
    global friend_id
    global friend_name
    global friend_ready

    BUF_SIZE = 1024  # 设置缓冲区的大小

    n = id_num

    print("开始服务器对用户id{}的receive_from_server循环".format(n))

    loop_flag = True
    while loop_flag:

        mes_from_client = client.recv(BUF_SIZE)  # 从服务器端接收数据
        mes = mes_from_client.decode('utf-8')
        legal,kind,source,target,content=test_codec_mes.decode_mes(mes)


        friend_id = str(content)
        friend_name = "ok"

        if legal:
            friend_ready = True

        if kind == "OFFLINE":
            loop_flag = False
            break

    print("用户{}的receive_from_server循环关闭".format(str(n)))


def AI_client_land(id_num, name):
    BUF_SIZE = 1024  # 设置缓冲区的大小

    server_addr = ('192.168.1.102', 7500)  # IP和端口构成表示地址
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 返回新的socket对象
    client.connect(server_addr)  # 连接服务器

    mes_from_server = client.recv(BUF_SIZE)  # 从服务器端接收数据
    mes = mes_from_server.decode('utf-8')
    if mes == "IFF_ID_NAME":
        mes = str(id_num) + "_" + name
        mes_to_client = mes.encode('utf-8')
        client.sendall(mes_to_client)  # 发送数据到客户端
        time.sleep(0.01)

    mes_from_server = client.recv(BUF_SIZE)  # 从服务器端接收数据
    mes = mes_from_server.decode('utf-8')
    legal, kind, source, target, content = test_codec_mes.decode_mes(mes)
    if kind == "FRIENDS":
        print(str(source)+"号的好友列表为："+str(content))
        time.sleep(0.01)


    t_new = threading.Thread(target=receive_from_server, args=(id_num, client))
    t_new.start()

    return client


def chat_screen(id_num, name, client_bw):
    global screen_queue
    global friend_state
    global friend_id
    global friend_name

    client = client_bw

    pygame.init()

    screen = pygame.display.set_mode((600, 200))
    pygame.display.set_caption("用户id{}：{}".format(str(id_num), name))

    bgc = (200, 200, 200)
    screen.fill(bgc)  # 涂背景色

    screen1_refresh = pygame.USEREVENT + 1
    pygame.time.set_timer(screen1_refresh, 20)

    txt_color = (0, 0, 0)
    font = pygame.font.SysFont("SimHei", 24)
    screen_rect = screen.get_rect()

    loop_flag = True
    while loop_flag:

        for event in pygame.event.get():

            if event.type != pygame.QUIT:

                screen.fill(bgc)  # 桌面绘制，涂背景色
                img_txt = font.render(friend_id, True, txt_color, (0, 220, 0))
                img_txt_rect = img_txt.get_rect()
                img_txt_rect.left = screen_rect.left
                img_txt_rect.bottom = screen_rect.height / 2

                screen.blit(img_txt, img_txt_rect)

                img_txt = font.render(friend_name, True, txt_color, (0, 220, 0))
                img_txt_rect = img_txt.get_rect()
                img_txt_rect.left = screen_rect.left
                img_txt_rect.top = screen_rect.height / 2

                screen.blit(img_txt, img_txt_rect)

                pygame.display.flip()  # 本帧图像显示赋值



            else:
                mes = test_codec_mes.encode_mes(kind="OFFLINE",content="",source=id_num)
                mes_to_server = mes.encode('utf-8')
                client.sendall(mes_to_server)  # 发送数据到客户端
                time.sleep(0.01)

                friend_state = "OFFLINE"
                loop_flag = False

                try:
                    pygame.quit()
                    sys.exit(0)
                except:

                    print("Exit Successfully!!")
                else:
                    print("Fail to Exit!!")



def AI_talk(id_num, client_bw):

    time.sleep(15)

    a=random.randint(5,10)
    for i in range(a):
        mes = str(random.randint(3,50))
        mes_to_client = mes.encode('utf-8')
        client_bw.sendall(mes_to_client)  # 发送数据到客户端

        time.sleep(random.uniform(1,3))

    mes = "说完了，共说了{}句话".format(str(a))
    mes_to_client = mes.encode('utf-8')
    client_bw.sendall(mes_to_client)  # 发送数据到客户端




def main(kind="AI", id_num=0):
    global friend_state
    global friend_id
    global friend_name
    global friend_ready

    friend_ready = False
    friend_state = ""
    friend_name = ""

    if kind == "AI":
        name = "游客{}".format(str(id_num))
    elif kind == "web":
        id_num = input("请输入id号：")
        name = input("请输入昵称：")

    friend_list = [0, 1, 4, 8]
    screen_queue = Queue(maxsize=5)

    client_bw = AI_client_land(id_num, name)


    if kind == "AI" and id_num!=-1:
        t_talk = threading.Thread(target=AI_talk, args=(id_num, client_bw,))
        t_talk.start()
        print("AI开始说话")


    while not friend_ready:
        time.sleep(0.1)

    chat_screen(id_num, name, client_bw)




if __name__ == '__main__':
    main("web")


