# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddFriend.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from util import db
from util.connect import send_add_friend_request


class Ui_Dialog(object):
    def __init__(self, token):
        self.token = token

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(416, 137)
        Dialog.setFixedSize(416, 137)
        self.Dialog = Dialog
        self.id_input = QtWidgets.QLineEdit(Dialog)
        self.id_input.setGeometry(QtCore.QRect(40, 40, 341, 31))
        self.id_input.setObjectName("id_input")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 80, 341, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.confirm = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.confirm.setObjectName("confirm")
        self.confirm.clicked.connect(self.send_add_request)
        self.horizontalLayout_4.addWidget(self.confirm)
        self.cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancel.setObjectName("cancel")
        self.cancel.clicked.connect(Dialog.close)
        self.horizontalLayout_4.addWidget(self.cancel)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(190, 10, 81, 21))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "请输入好友ID"))
        self.confirm.setText(_translate("Dialog", "确认"))
        self.cancel.setText(_translate("Dialog", "取消"))
        self.label.setText(_translate("Dialog", "好友ID"))

    # 发送添加请求
    def send_add_request(self):
        friend_id = self.id_input.text()
        if len(friend_id) is 0:
            QMessageBox.information(None, '标题', "ID不能为空", QMessageBox.Ok, QMessageBox.Ok)
            return
        # 可能查无此人，fix
        res = db.add_friend(self.token, int(friend_id))
        if res is False:
            return
        db.add_friend(int(friend_id), self.token)
        send_add_friend_request(friend_id)
        QMessageBox.about(None, '标题', "好友请求已发送")
        self.Dialog.close()

