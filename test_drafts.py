import test_codec_mes
# mes="a_b_d_f"
# submark = mes.find("_")
# print(submark)


# a=[1,2,3,4]
# s=str(a)
# print(s[0])

# a="COMM>28:hahaha"
# print(a[0:4]=="COMM")
# print(a[5:])




# online_id_list=[1,2,3,4]
# online_name_list=["kk","gh","fg","df"]
# mes = "ONLINEID:" + str(online_id_list) + "_" + "ONLINENAME:" + str(online_name_list)
# print(mes.find("ONLINEID"))
# print("\t")

#
# friend_list=[1,2,3,4]
# mes = str(9)+"-FRIENDS:" + str(friend_list)
# legal, kind, source, target, content = test_codec_mes.decode_mes(mes)
# print(legal, kind, source, target, content)
#
#
# mes = test_codec_mes.encode_mes("FRIENDS",[1,2,6,4,5,7],76)
# legal, kind, source, target, content = test_codec_mes.decode_mes(mes)
# print(legal, kind, source, target, content)

#
# a=[2,4,6,8]
# b=["a","b","c","d","e","f","g","h","i","j","k"];
#
# c=[]
# for item in a:
#    c.append(b[item])
#
# print(c)

#
# class Bag:
#    def __init__(self,v,h=5):
#       self.v=v
#       self.h=h
#
#    def __str__(self):
#       return "v为{}，h为{}".format(str(self.v),str(self.h))
#
# bag_list=[]
# for i in range(9):
#    bag_list.append(Bag(i))

# bag_list=filter(lambda x:x.v in [3,4,5],bag_list)

# print(bag_list)
# for temp in bag_list:
#    print(temp)



#
# mes = test_codec_mes.encode_mes(kind="IDLEAVE",content=[1,2,3])
# print(mes)
# legal, kind, source, target, content = test_codec_mes.decode_mes(mes)
# print(legal, kind, source, target, content)
#
# import socket
# hostname = socket.gethostname()
# print ( "Host name: %s" %hostname)
# sysinfo = socket.gethostbyname_ex(hostname)
#
# ip_addr = sysinfo[2]
# localhost=ip_addr[0]
#
# for i in range(-1,-len(localhost),-1):
#     print(i)
#     if localhost[i]==".":
#         break
#
# print(localhost[:i+1])


# ip_addr1 = ip_addr[0]
# ip_addr2 = ip_addr[1]
# print("IP Address: %s" %ip_addr1,ip_addr2)

# s=''.join(sorted("31t9"))
# print(s)
#
#
#
# a=[1,5,8,7,4]
# b=sorted(a)
# print(a)
# print(b)

# item="haha"
# sales="6"
# print('""'+item+'""'+sales)
# print( '“%s”, %s'%(item,sales))

# list1=[1,2]
# list2=[3,4]
# list3=list1+list2
# print(list3*3)

# list1=[1,2,3,4,5,6]
#
# for i in range(len(list1)-1,-1,-1):
#     print(i)
#     # print(list1[i])
#
# print(list1[-1:-6:-2])

name="西瓜"
value=100.456
count=3

print("{0:10},{1:15.2f},{2:7d}".format(name,value,count))
