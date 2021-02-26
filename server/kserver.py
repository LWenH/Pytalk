from select import kqueue
import select
from socket import *
from util import db

HOST = '127.0.0.1'
PORT = 8001
BUFFER_SIZE = 1024

# ipv4,TCP 流协议
server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
# 最大等待20个链接
server.listen(20)

kq = kqueue()

# 已链接的套接字
connect_list = {}

# 生成kevents列表，监听socket的读操作
even_map = {}

events = [
    select.kevent(server.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD),
]

container = ''

"""
from | type | reserve | message body

from 0 means server send

type 0 means login broadcast
type 1 means logout broadcast
type 2 means regular text
type 3 means picture
type 4 means group text
type 5 means group picture
type 6 means add friend request
type 7 means accepted confirm
"""


def broadcast_login(login_id):
    for conn in connect_list.values():
        conn.send(bytes("0|0|0|" + str(login_id), encoding='utf-8'))


def broadcast_logout(user_id):
    for conn in connect_list.values():
        conn.send(bytes("0|1|0|" + str(user_id), encoding='utf-8'))


# 计算包的个数，拼凑完成发送
def sent_text(package, from_id):
    try:
        pack_list = package.split("|")
        target_id = pack_list[0]
        target_con = connect_list[int(target_id)]
        # 客户端解包
        # 重新打包
        temp = pack_list[3]
        for i in range(4, len(pack_list)):
            temp += "|" + pack_list[i]
        target_con.send(bytes(str(from_id) + "|2|0|" + temp, encoding='utf-8'))
    except Exception:
        print("offline")


def send_img(package, from_id, to_id):
    try:
        con = connect_list[int(to_id)]
        img_size = len(package)
        first_package = bytes(str(from_id) + "|3|" + str(img_size)+"|", encoding='utf-8')
        # 填充信息,这样做防止粘包，或者图片截断
        con.send(first_package + (BUFFER_SIZE - len(first_package)) * bytes('0', encoding='utf-8'))
        con.send(package)
    except Exception:
        print("offline")


def send_group_text(package, room_id, user_id):
    room_member = db.getRoomUserId(int(room_id))
    pack_list = package.split("|")
    # 重新打包
    temp = pack_list[3]
    for i in range(4, len(pack_list)):
        temp += "|" + pack_list[i]
    # 根据群里的人转发
    for tmp in room_member:
        try:
            conn = connect_list[tmp[0]]
            conn.send(bytes(str(user_id)+"|4|"+str(room_id)+"|"+temp, encoding='utf-8'))
            # reserve for room_id
        except Exception:
            continue


def send_group_img(img_pack, room_id, user_id, img_size):
    room_member = db.getRoomUserId(int(room_id))
    first_package = bytes(str(user_id) + "|5|" + str(img_size)+"|"+str(room_id)+"|", encoding='utf-8')
    for tmp in room_member:
        try:
            conn = connect_list[tmp[0]]
            conn.send(first_package + (BUFFER_SIZE - len(first_package)) * bytes('0', encoding='utf-8'))
            conn.send(img_pack)
        except Exception:
            continue


def run_server():
    global container
    while True:
        try:
            # 开始kqueue监听，如果有可执行kevent，则返回对应的kevent列表
            eventList = kq.control(events, 1)
        except select.error:
            print("error")
            continue
        if eventList:
            for evn in eventList:
                # 连接请求,将conn创建kevent放入到events进行监听，将conn放入到conn_list进行保存，key为user_id
                if evn.ident is server.fileno():
                    conn, address = server.accept()
                    print(address, "connected")
                    # 获取登录用户的id
                    user_id = int(conn.recv(5).decode('utf-8'))
                    # 用户已登录
                    if connect_list.get(user_id) and len(connect_list) is not 0:
                        conn.send(bytes("e", encoding='utf-8'))
                        conn.close()
                        continue
                    # 否则返回好友列表
                    else:
                        if not len(connect_list):
                            conn.send(bytes("0", encoding='utf-8'))
                        else:
                            # fix me, low efficiency
                            for k in connect_list.keys():
                                container += str(k) + "|"
                            conn.send(bytes(container, encoding='utf-8'))
                        broadcast_login(user_id)
                        connect_list.update({user_id: conn})
                        # 新的事件
                        new_kevent = select.kevent(conn.fileno(), select.KQ_FILTER_READ,
                                                   select.KQ_EV_ADD, udata=user_id)
                        # 加入监听队列
                        events.append(new_kevent)
                        # 绑定事件
                        even_map.update({user_id: new_kevent})
                else:
                    conn = connect_list[evn.udata]
                    data = conn.recv(BUFFER_SIZE)
                    # 连接断开
                    # TODO 开线程
                    if not data:
                        broadcast_logout(evn.udata)
                        conn.close()
                        events.remove(even_map[evn.udata])
                        connect_list.pop(evn.udata)
                    else:
                        text = data.decode('utf-8').split('|')
                        text_type = text[1]
                        if text_type is '2':
                            sent_text(data.decode('utf-8'), evn.udata)
                        elif text_type is '3':
                            # 如果是图片的话,获取图片大小,收图
                            to_user = text[0]
                            img_size = int(text[2])
                            img_pack = conn.recv(img_size)
                            send_img(img_pack, evn.udata, to_user)
                        elif text_type is '4':
                            send_group_text(data.decode('utf-8'), text[0], evn.udata)
                        elif text_type is '5':
                            room_id = text[0]
                            img_size = int(text[2])
                            img_pack = conn.recv(img_size)
                            send_group_img(img_pack, room_id, evn.udata, img_size)
                        elif text_type is '6':
                            to_user = text[0]
                            try:
                                c = connect_list[int(to_user)]
                                c.send(bytes(str(evn.udata) + "|6|0|0", encoding='utf-8'))
                            except Exception:
                                continue
                        else:
                            to_user = text[0]
                            try:
                                c = connect_list[int(to_user)]
                                c.send(bytes(str(evn.udata) + "|7|0|0", encoding='utf-8'))
                            except Exception:
                                continue

    server.close()


run_server()
