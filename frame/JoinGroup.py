# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddFriend.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from util import db
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtCore import pyqtSignal


class JoinGroupDialog(QDialog):
    joinSuccessSig = pyqtSignal(int, int)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def setupUi(self):
        self.setObjectName("joinGroup")
        self.resize(416, 137)
        self.id_input = QtWidgets.QLineEdit(self)
        self.id_input.setGeometry(QtCore.QRect(40, 40, 341, 31))
        self.id_input.setObjectName("id_input")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 80, 341, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.confirm = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.confirm.setObjectName("confirm")
        self.confirm.clicked.connect(self.on_confirm_clicked)
        self.horizontalLayout_4.addWidget(self.confirm)
        self.cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancel.setObjectName("cancel")
        self.cancel.clicked.connect(self.close)
        self.horizontalLayout_4.addWidget(self.cancel)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(190, 10, 81, 21))
        self.label.setObjectName("label")
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("joinGroup", "请输入群ID"))
        self.confirm.setText(_translate("joinGroup", "确认"))
        self.cancel.setText(_translate("joinGroup", "取消"))
        self.label.setText(_translate("joinGroup", "群ID"))

    def on_confirm_clicked(self):
        room_id = self.id_input.text()
        if len(room_id) is 0:
            QMessageBox.about(None, '标题', "ID不能为空")
            return
        else:
            res = db.joinGroup(int(room_id), self.token, "群成员")
            if res is True:
                QMessageBox.about(None, '标题', "加群成功")
                # 吐出信号主窗口刷新
                self.joinSuccessSig.emit(int(room_id), 0)
                self.close()
            else:
                QMessageBox.about(None, '标题', "操作失败")
                return
