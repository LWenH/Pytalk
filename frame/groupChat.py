# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupChat.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from util import db
from PyQt5.QtCore import Qt
from time import *
from util.connect import send_group_text, send_group_img

isImageFile = False


class myTextEdit(QtWidgets.QTextEdit):
    send_text_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self)
        self.parent = parent

    # Enter键发送信息
    def keyPressEvent(self, event):
        global isImageFile
        if event.key() == Qt.Key_Return:
            if not self.toPlainText():
                return
            if isImageFile:
                self.send_text_signal.emit(1)
                isImageFile = False
            else:
                self.send_text_signal.emit(0)
        else:
            QtWidgets.QTextEdit.keyPressEvent(self, event)


def get_layout_widget(user_name, pos):
    widget = QWidget()
    layout_main = QHBoxLayout()
    map_l = QLabel()  # 头像显示
    map_l.setFixedSize(70, 55)
    maps = QPixmap("../icon/3.png").scaled(70, 55)
    map_l.setPixmap(maps)

    # 右边的纵向布局
    layout_right = QVBoxLayout()

    # 右下的的横向布局
    layout_right_down = QHBoxLayout()  # 右下的横向布局
    layout_right_down.addWidget(QLabel(pos))
    # 按照从左到右, 从上到下布局添加
    layout_main.addWidget(map_l)  # 最左边的头像

    layout_right.addWidget(QLabel(user_name))  # 右边的纵向布局
    layout_right.addLayout(layout_right_down)  # 右下角横向布局

    layout_main.addLayout(layout_right)  # 右边的布局

    widget.setLayout(layout_main)  # 布局给wight
    return widget  # 返回widget


class Ui_GroupChat(QDialog):
    def __init__(self, room_id, user_id, status):
        super().__init__()
        self.user_id = user_id
        self.room_id = room_id
        self.allHistory = db.query_room_history(self.room_id)
        self.nameList = db.getRoomPeople(self.room_id, user_id, status)
        self.imgCount = 1
        self.file_path = ""

    def setupUi(self):
        self.setObjectName("GroupChat")
        self.resize(861, 601)
        self.setFixedSize(861, 601)
        self.input = myTextEdit(self)
        self.input.send_text_signal.connect(self.send_message)
        self.input.setObjectName("input")
        # 将新override的子类加到widget中
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 420, 661, 181))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.input)

        self.view = QtWidgets.QTextBrowser(self)
        self.view.setGeometry(QtCore.QRect(200, 0, 661, 381))
        self.view.setObjectName("view")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 380, 661, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.emoji = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.emoji.setObjectName("emoji")
        self.horizontalLayout.addWidget(self.emoji)
        self.modify_color = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # 改颜色
        self.modify_color.clicked.connect(self.change_color)
        self.modify_color.setObjectName("modify_color")
        self.horizontalLayout.addWidget(self.modify_color)
        self.modify_font = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.modify_font.setObjectName("modify_font")
        self.modify_font.clicked.connect(self.change_font)
        self.horizontalLayout.addWidget(self.modify_font)
        self.horizontalLayout.addWidget(self.modify_font)
        self.upload_file = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.upload_file.setObjectName("upload_file")
        # 上传文件
        self.upload_file.clicked.connect(self.openfile)
        self.horizontalLayout.addWidget(self.upload_file)
        self.clear = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear.setObjectName("clear")
        self.clear.clicked.connect(self.view.clear)
        self.horizontalLayout.addWidget(self.clear)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 201, 601))
        self.listWidget.setObjectName("listWidget")
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.input.setPlaceholderText(_translate("GroupChat", "Enter键发送"))
        self.emoji.setText(_translate("GroupChat", "发送"))
        self.modify_color.setText(_translate("GroupChat", "字体颜色"))
        self.modify_font.setText(_translate("GroupChat", "调整字体"))
        self.upload_file.setText(_translate("GroupChat", "上传图片"))
        self.clear.setText(_translate("GroupChat", "清空"))
        self.listWidget.setStyleSheet('QListWidget{border:1px solid gray; background:skyblue; }'
                                      'QListWidget::Item{padding-top:-2px; padding-bottom:-1px;}'
                                      "QListWidget::Item:hover{background:lightgray;padding-top:0px; padding-bottom:0px; }"
                                      "QListWidget::item:selected{background:lightgray; color:blue; }")
        for record in self.allHistory:
            # 自己发的
            if record[0] == self.user_id:
                self.view.append("<font color=\"green\" size=3>" + '(我)' + str(record[4]))
                if record[3] is not None:
                    self.view.append("<img src=%s height='250' width='250'/>" % record[3])
                else:
                    self.view.append(record[2])
            else:
                name = record[1]
                self.view.append("<font color=\"blue\" size=3>" + "(" + name + ")" + str(record[4]))
                if record[3] is not None:
                    self.view.append("<img src=%s height='250' width='250'/>" % record[3])
                else:
                    self.view.append(record[2])
            self.view.append("<br/>")

        self.view.append(
            "<font color=\"gray\" size=3 margin-left='30px'>" + "------------------------------------------以上为历史消息------------------------------------------" + "</font> ")
        for member in self.nameList:
            item = QListWidgetItem()
            item.setSizeHint(QtCore.QSize(0, 70))
            widget = get_layout_widget(member[0], member[1])
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

    def openfile(self):
        global isImageFile
        fileName = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fileName[0]:
            self.file_path = fileName[0]
            self.input.append("<img src=%s height='250' width='250'/>" % self.file_path)
            isImageFile = True
        else:
            return

    def change_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.input.setTextColor(col)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.input.setCurrentFont(font)

    def send_message(self, msg_type):
        if msg_type is 0:
            content = self.input.toHtml()
            send_group_text(self.room_id, content)
            self.input.clear()
            self.view.append(
                "<font color=\"green\" size=3>" + "(我)" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
            self.view.append(content)
            self.view.append("<br/>")
            db.add_room_chat_history(self.room_id, self.user_id, content)
        # 发的图片
        else:
            self.input.clear()
            self.view.append(
                "<font color=\"green\" size=3>" + "(我)" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
            self.view.append("<img src=%s height='250' width='250'/>" % self.file_path)
            self.view.append("<br/>")
            img = open(self.file_path, 'rb')
            img_pack = img.read()
            size = len(img_pack)
            send_group_img(img_pack, self.room_id, size)
            img.close()
            db.add_room_chat_history(self.room_id, self.user_id, None, path=self.file_path)

    def get_msg(self, user_id, room_id, content):
        if user_id == self.user_id or self.room_id != room_id:
            return
        user_name = db.queryUserName(user_id)[0][0]
        self.view.append("<font color=\"blue\" size=3>" + '(' + user_name + ')' + strftime("%Y-%m-%d %H:%M:%S",                                                                                      localtime()) + "</font> ")
        self.view.append(content)
        self.view.append("<br/>")

    def receive_img(self, room_id, user_id, img_bytes):
        if room_id != self.room_id or user_id == self.user_id:
            return
        with open('../history/%d.jpg' % self.imgCount, 'wb') as img:
            img.write(img_bytes)
            img.close()
        user_name = db.queryUserName(user_id)[0][0]
        self.view.append("<font color=\"blue\" size=3>" + '(' + user_name + ')' + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
        self.view.append("<img src=../history/%d.jpg height='250' width='250'/>" % self.imgCount)
        self.view.append("<br/>")
        # TODO fix here
        self.imgCount += 1
