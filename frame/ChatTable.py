# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChatTable.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from frame import AddFriend, ChatBox, JoinGroup, CreateGroup, groupChat
from util import db
from PyQt5.QtCore import pyqtSignal
from util.connect import get_conn, get_online_list, send_friend_confirm
from threading import Thread


def get_layout_widget(user_name, arg, num=0, wid_type=0):
    widget = QWidget()
    layout_main = QHBoxLayout()
    map_l = QLabel()  # 头像显示
    map_l.setFixedSize(70, 55)
    if wid_type == 0:
        maps = QPixmap("../icon/1.png").scaled(70, 55)
    else:
        maps = QPixmap("../icon/2.png").scaled(70, 55)
    map_l.setPixmap(maps)

    # 右边的纵向布局
    layout_right = QVBoxLayout()

    # 右下的的横向布局
    layout_right_down = QHBoxLayout()  # 右下的横向布局
    if wid_type == 0:
        if arg:
            layout_right_down.addWidget(QLabel("在线"))
        else:
            layout_right_down.addWidget(QLabel("离线"))
        if num is not 0:
            layout_right_down.addWidget(QLabel(str(num) + "条未读消息"))
    else:
        layout_right_down.addWidget(QLabel("快来畅聊吧"))

    # 按照从左到右, 从上到下布局添加
    layout_main.addWidget(map_l)  # 最左边的头像

    layout_right.addWidget(QLabel(user_name))  # 右边的纵向布局
    layout_right.addLayout(layout_right_down)  # 右下角横向布局

    layout_main.addLayout(layout_right)  # 右边的布局

    widget.setLayout(layout_main)  # 布局给wight
    return widget  # 返回widget


class Ui_origin(QtWidgets.QWidget):
    get_msg_signal = pyqtSignal(int, str)
    login_notify_sig = pyqtSignal(int)
    logout_notify_sig = pyqtSignal(int)
    just_record_sig = pyqtSignal(int)
    open_dialog_sig = pyqtSignal(str, int)
    get_img_sig = pyqtSignal(bytes, int)
    get_group_msg = pyqtSignal(int, int, str)
    get_group_img = pyqtSignal(int, int, bytes)
    request_friend_sig = pyqtSignal(int, str)
    accepted_confirm_sig = pyqtSignal(int, str)

    def __init__(self, token, name):
        super().__init__()
        self.token = token
        self.friend_list = None
        # 在线好友列表
        self.login_friend = []
        self.un_accepted = db.get_unaccepted_friend(self.token)
        # 打开窗口的记录器
        self.open_widget_dict = {}
        # 记录未读消息
        self.record_dict = {}
        self.messageCache = {}
        self.origin = None
        self.name = name
        # 获得连接
        self.conn = get_conn()

        def receive_data():
            while True:
                data = str(self.conn.recv(1024), encoding='utf-8')
                # 吐出接收消息的信号
                package = data.split("|")
                if package[0] is "0":
                    if package[1] is "0":
                        # 登入广播
                        self.login_notify_sig.emit(int(package[3]))
                    else:
                        # 登出广播
                        self.logout_notify_sig.emit(int(package[3]))
                else:
                    msgType = package[1]
                    if msgType == "2":
                        if len(package) is 4:
                            self.get_msg_signal.emit(int(package[0]), package[3])
                        else:
                            temp = package[3]
                            for i in range(4, len(package)):
                                temp += "|" + package[i]
                            self.get_msg_signal.emit(int(package[0]), temp)
                        self.just_record_sig.emit(int(package[0]))
                    elif msgType == "3":
                        # 图片
                        from_id = int(package[0])
                        img_size = int(package[2])
                        img_byte = self.conn.recv(img_size)
                        self.get_img_sig.emit(img_byte, from_id)
                        self.just_record_sig.emit(from_id)
                    elif msgType == "4":
                        if len(package) is 4:
                            self.get_group_msg.emit(int(package[0]), int(package[2]), package[3])
                        else:
                            temp = package[3]
                            for i in range(4, len(package)):
                                temp += "|" + package[i]
                            self.get_group_msg.emit(int(package[0]), int(package[2]), temp)
                    elif msgType == "5":
                        room_id = int(package[3])
                        user_id = int(package[0])
                        img_size = int(package[2])
                        img_byte = self.conn.recv(img_size)
                        self.get_group_img.emit(room_id, user_id, img_byte)
                    elif msgType == '6':
                        from_id = int(package[0])
                        use_name = db.queryUserName(from_id)[0][0]
                        self.request_friend_sig.emit(from_id, use_name)
                    else:
                        from_id = int(package[0])
                        self.record_dict[from_id] = 0
                        use_name = db.queryUserName(from_id)[0][0]
                        self.login_friend.append(from_id)
                        self.friend_list.append((use_name, from_id))
                        self.accepted_confirm_sig.emit(from_id, use_name)

        t = Thread(target=receive_data)
        # 守护线程
        t.setDaemon(True)
        t.start()

    def setupUi(self):
        self.setObjectName("origin")
        self.resize(343, 649)
        self.setFixedSize(343, 649)
        # 获取朋友名称列表
        self.friend_list = list(db.get_friend_list(self.token))
        # 获取群列表
        self.group_list = list(db.get_group_list(self.token))
        self.get_friend_status()
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(0, 50, 351, 601))
        self.listWidget.setObjectName("listWidget")
        # 绑定选中
        self.listWidget.itemDoubleClicked.connect(self.go_to_chat)
        self.horizontalWidget = QtWidgets.QWidget(self)
        self.horizontalWidget.setGeometry(QtCore.QRect(0, 0, 343, 51))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addFriend = QtWidgets.QPushButton(self.horizontalWidget)
        self.addFriend.setObjectName("addFriend")
        self.addFriend.clicked.connect(self.on_add_friend_clicked)
        self.horizontalLayout.addWidget(self.addFriend)
        self.joinGroup = QtWidgets.QPushButton(self.horizontalWidget)
        self.joinGroup.setObjectName("joinGroup")
        self.joinGroup.clicked.connect(self.openJoinGroupDialog)
        self.horizontalLayout.addWidget(self.joinGroup)
        self.createGroup = QtWidgets.QPushButton(self.horizontalWidget)
        self.createGroup.setObjectName("createGroup")
        self.createGroup.clicked.connect(self.on_create_group_clicked)
        self.horizontalLayout.addWidget(self.createGroup)
        self.retranslateUi()
        # 渲染聊天列表
        self.render_chat_list()
        self.login_notify_sig.connect(self.update_friend_login)
        self.logout_notify_sig.connect(self.update_friend_logout)
        self.just_record_sig.connect(self.render_unread)
        self.open_dialog_sig.connect(self.bzero)
        self.request_friend_sig.connect(self.showRequest)
        self.accepted_confirm_sig.connect(self.updateFriendItem)

    def retranslateUi(self):
        self.setWindowTitle(self.name + "的联系人")
        self.addFriend.setText("加好友")
        self.joinGroup.setText("加群")
        self.createGroup.setText("创建群")
        if len(self.un_accepted) is not 0:
            for ask in self.un_accepted:
                res = QMessageBox.question(self, "标题", ask[0] + "请求加您为好友", QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)
                if res == QMessageBox.Yes:
                    self.friend_list.append((ask[0], ask[1]))
                    send_friend_confirm(ask[1])
                    db.updateFriendStatus(self.token, ask[1])
                else:
                    db.remove_friend(self.token, ask[1])

    def on_add_friend_clicked(self):
        self.add_friend_dialog = QDialog()
        self.ui_add_friend = AddFriend.Ui_Dialog(self.token)
        self.ui_add_friend.setupUi(self.add_friend_dialog)
        self.add_friend_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_friend_dialog.show()
        self.add_friend_dialog.exec_()

    def render_chat_list(self):
        # 每一项(好友项)
        # TODO 优化,多次初始化
        self.listWidget.setStyleSheet('QListWidget{border:1px solid gray; background:#edfdc4; }'
                                      'QListWidget::Item{padding-top:-2px; padding-bottom:-1px;}'
                                      "QListWidget::Item:hover{background:lightgray;padding-top:0px; padding-bottom:0px; }"
                                      "QListWidget::item:selected{background:lightgray; color:blue; }")
        for member in self.friend_list:
            item = QListWidgetItem()
            login_arg = self.ensure_login(member[1])
            widget = get_layout_widget(member[0], login_arg)
            item.setSizeHint(QtCore.QSize(0, 70))
            # 绑定好友对应id
            item.setData(QtCore.Qt.UserRole, member[1])
            # 所有未读消息为0
            self.record_dict[member[1]] = 0
            self.open_widget_dict[member[1]] = 0
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

        for group in self.group_list:
            item = QListWidgetItem()
            item.setSizeHint(QtCore.QSize(0, 70))
            widget = get_layout_widget("群" + str(group[0]), True, 0, 1)
            item.setData(QtCore.Qt.UserRole, "#" + str(group[0]))
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

    def go_to_chat(self, item):
        for member in self.friend_list:
            if member[1] is item.data(QtCore.Qt.UserRole):
                self.open_dialog_sig.emit(member[0], member[1])
                new_chat = ChatBox.Ui_ChatBox(member[0], str(member[1]), self.token)
                new_chat.setupUi()
                self.get_msg_signal.connect(new_chat.get_msg)
                self.get_img_sig.connect(new_chat.receive_img)
                new_chat.setWindowTitle(member[0])
                new_chat.close_signal.connect(self.remove_open_dialog)
                new_chat.show()
                new_chat.exec_()
                return

        for group in self.group_list:
            if "#" + str(group[0]) == item.data(QtCore.Qt.UserRole):
                db.set_room_all_read(int(group[0]), self.token)
                newGroupChat = groupChat.Ui_GroupChat(group[0], self.token, group[1])
                newGroupChat.setupUi()
                newGroupChat.setWindowTitle("群" + str(group[0]))
                self.get_group_msg.connect(newGroupChat.get_msg)
                self.get_group_img.connect(newGroupChat.receive_img)
                newGroupChat.show()
                newGroupChat.exec_()

    def get_friend_status(self):
        on_line_person = get_online_list()
        for member in self.friend_list:
            if str(member[1]) in on_line_person:
                self.login_friend.append(member[1])
                continue

    def ensure_login(self, arg):
        return arg in self.login_friend

    # 更新在线
    def update_friend_login(self, user_id):
        for member in self.friend_list:
            if member[1] is user_id:
                for i in range(self.listWidget.count()):
                    if self.listWidget.item(i).data(QtCore.Qt.UserRole) is user_id:
                        new_wid = get_layout_widget(member[0], True, self.record_dict[user_id])
                        self.listWidget.setItemWidget(self.listWidget.item(i), new_wid)
                        # 更新登入列表
                        self.login_friend.append(user_id)
                        break

    # 更新离线
    def update_friend_logout(self, user_id):
        for member in self.friend_list:
            if member[1] is user_id:
                for i in range(self.listWidget.count()):
                    if self.listWidget.item(i).data(QtCore.Qt.UserRole) is user_id:
                        new_wid = get_layout_widget(member[0], False, self.record_dict[user_id])
                        self.listWidget.setItemWidget(self.listWidget.item(i), new_wid)
                        # 退出登录列表
                        try:
                            self.login_friend.remove(user_id)
                            break
                        except Exception:
                            break

    # 关闭窗口
    def remove_open_dialog(self, dialog_id):
        self.open_widget_dict[dialog_id] = 0
        self.record_dict[dialog_id] = 0

    # 未读消息渲染
    def render_unread(self, from_user):
        # 未打开窗口
        if self.open_widget_dict.get(from_user) is not 1:
            self.record_dict[from_user] += 1
            for member in self.friend_list:
                if member[1] is from_user:
                    for i in range(self.listWidget.count()):
                        if self.listWidget.item(i).data(QtCore.Qt.UserRole) is from_user:
                            new_wid = get_layout_widget(member[0], True, self.record_dict.get(from_user))
                            self.listWidget.setItemWidget(self.listWidget.item(i), new_wid)
                            break

    # TODO 删掉未读消息
    def bzero(self, user_name, user_id):
        # 打开窗口,将其在wid_dict的flag设为1
        self.open_widget_dict[user_id] = 1
        # 未读消息数设为0
        self.record_dict[user_id] = 0

    def openJoinGroupDialog(self):
        join_group_dialog = JoinGroup.JoinGroupDialog(self.token)
        join_group_dialog.setupUi()
        join_group_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        join_group_dialog.joinSuccessSig.connect(self.updateGroupItem)
        join_group_dialog.show()
        join_group_dialog.exec_()

    def updateGroupItem(self, room_id, status):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(0, 70))
        widget = get_layout_widget("群" + str(room_id), True, 0, 1)
        item.setData(QtCore.Qt.UserRole, "#" + str(room_id))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)
        if status == 0:
            self.group_list.append((room_id, "群成员"))
        else:
            self.group_list.append((room_id, "群主"))

    def on_create_group_clicked(self):
        create_group_dia = CreateGroup.NewGroup(self.token)
        create_group_dia.setupUi()
        create_group_dia.setWindowModality(QtCore.Qt.ApplicationModal)
        create_group_dia.createSuccessSig.connect(self.updateGroupItem)
        create_group_dia.show()
        create_group_dia.exec_()

    def updateFriendItem(self, user_id, user_name):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(0, 70))
        widget = get_layout_widget(user_name, True, 0, 0)
        item.setData(QtCore.Qt.UserRole, user_id)
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)

    def acceptRequest(self, user_id, user_name):
        self.updateFriendItem(user_id, user_name)
        db.updateFriendStatus(self.token, user_id)
        send_friend_confirm(user_id)
        self.friend_list.append((user_name, user_id))
        self.record_dict[user_id] = 0

    def showRequest(self, user_id, user_name):
        res = QMessageBox.question(self, "标题", user_name+"请求加您为好友", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            self.acceptRequest(user_id, user_name)
            self.login_friend.append(user_id)
        else:
            db.remove_friend(self.token, user_id)
