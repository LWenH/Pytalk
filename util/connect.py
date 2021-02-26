from socket import *

HOST = '127.0.0.1'
PORT = 8001
BUFFER_SIZE = 1024
server = socket(AF_INET, SOCK_STREAM)

on_line_person = ""


# ipv4,TCP 流协议
# 连接服务器，同时告诉自己是谁
def log_into_server(my_id):
    global on_line_person
    server.connect((HOST, PORT))
    server.send(bytes(my_id, encoding='utf-8'))
    data = server.recv(20).decode('utf-8')
    lookAhead = data[0]
    login_status = lookAhead is not "e"
    # 没人在线
    on_line_person = data if login_status and lookAhead is not "0" else "0"
    return login_status


def send_text(content, to_user):
    # TODO 确认消息类型和长度
    server.send(bytes(to_user+'|2|0|'+content, encoding='utf-8'))


def send_img(img_bytes, to_user, size):
    first_package = bytes(to_user+"|3|"+str(size)+"|", encoding='utf-8')
    # 填充信息
    server.send(first_package+(BUFFER_SIZE-len(first_package))*bytes('0', encoding='utf-8'))
    server.sendall(img_bytes)


def get_conn():
    return server


def get_online_list():
    return on_line_person.split("|")


def send_group_text(room_id, content):
    wrap = str(room_id)+"|4|0|"+content
    server.send(bytes(wrap, encoding='utf-8'))


def send_group_img(img_bytes, room_id, size):
    first_package = bytes(str(room_id) + "|5|" + str(size) + "|", encoding='utf-8')
    server.send(first_package + (BUFFER_SIZE - len(first_package)) * bytes('0', encoding='utf-8'))
    server.sendall(img_bytes)


def send_add_friend_request(to_id):
    server.send(bytes("%s|6|0|0" % to_id, encoding='utf-8'))


def send_friend_confirm(to_id):
    server.send(bytes(str(to_id)+"|7|0|0", encoding='utf-8'))
