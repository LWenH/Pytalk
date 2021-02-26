# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from util import db
from PyQt5.QtWidgets import QMessageBox


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(517, 409)
        self.Dialog = Dialog
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 411, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.account = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.account.setObjectName("account")
        self.horizontalLayout.addWidget(self.account)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 120, 411, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.passwd = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.passwd.setObjectName("passwd")
        self.passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.horizontalLayout_2.addWidget(self.passwd)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(50, 200, 421, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.name = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.name.setObjectName("name")
        self.horizontalLayout_3.addWidget(self.name)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(50, 290, 421, 51))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.register_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.register_btn.clicked.connect(self.on_register_clicked)
        self.register_btn.setObjectName("register_btn")
        self.horizontalLayout_4.addWidget(self.register_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.cancel.setObjectName("cancel")
        self.cancel.clicked.connect(Dialog.close)
        self.horizontalLayout_4.addWidget(self.cancel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "注册"))
        self.label.setText(_translate("Dialog", "账号："))
        self.label_2.setText(_translate("Dialog", "密码："))
        self.label_3.setText(_translate("Dialog", "用户名："))
        self.register_btn.setText(_translate("Dialog", "注册"))
        self.cancel.setText(_translate("Dialog", "取消"))

    def on_register_clicked(self):
        acc = self.account.text()
        passwd = self.passwd.text()
        name = self.name.text()
        if len(acc) is 0 or len(passwd) is 0 or len(name) is 0:
            QMessageBox.information(None, '标题', "信息不能为空", QMessageBox.Ok, QMessageBox.Ok)
            return
        res = db.do_register(acc, passwd, name)
        if res is True:
            QMessageBox.information(None, '标题', "注册成功", QMessageBox.Ok, QMessageBox.Ok)
            self.Dialog.close()
        else:
            msg = "账号已存在"
            QMessageBox.information(None, '标题', msg, QMessageBox.Ok, QMessageBox.Ok)
