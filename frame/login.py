# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget
from frame import register, ChatTable
from util import db, connect


regex = QtCore.QRegExp("[a-zA-Z0-9]{1,20}")
validator = QtGui.QRegExpValidator(regex)


class Ui_login_widget(object):
    def setupUi(self, login_widget):
        login_widget.setObjectName("login_widget")
        login_widget.resize(600, 360)
        # 对象(自己)设置
        self.widget = login_widget

        self.account = QtWidgets.QLineEdit(login_widget)
        self.account.setGeometry(QtCore.QRect(210, 90, 261, 21))
        self.account.setObjectName("account")
        self.account.setValidator(validator)
        self.passwd = QtWidgets.QLineEdit(login_widget)
        self.passwd.setGeometry(QtCore.QRect(210, 160, 261, 21))
        self.passwd.setObjectName("passwd")
        self.passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label = QtWidgets.QLabel(login_widget)
        self.label.setGeometry(QtCore.QRect(140, 90, 59, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(login_widget)
        self.label_2.setGeometry(QtCore.QRect(140, 160, 59, 16))
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(login_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 90, 51, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(login_widget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(130, 240, 341, 35))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.login_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.login_btn.setObjectName("login_btn")
        self.login_btn.clicked.connect(self.login)
        self.horizontalLayout_3.addWidget(self.login_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.register_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.register_btn.setObjectName("register_btn")
        # 注册点击
        self.register_btn.clicked.connect(self.go_to_register)
        self.horizontalLayout_3.addWidget(self.register_btn)
        self.retranslateUi(login_widget)
        QtCore.QMetaObject.connectSlotsByName(login_widget)

    def retranslateUi(self, login_widget):
        _translate = QtCore.QCoreApplication.translate
        login_widget.setWindowTitle(_translate("login_widget", "登录"))
        self.label.setText(_translate("login_widget", "账号:"))
        self.label_2.setText(_translate("login_widget", "密码:"))
        self.login_btn.setText(_translate("login_widget", "登录"))
        self.register_btn.setText(_translate("login_widget", "注册"))

    def login(self):
        account = self.account.text()
        passwd = self.passwd.text()
        if len(account) is 0 or len(passwd) is 0:
            QMessageBox.information(None, '标题', "信息不能为空", QMessageBox.Ok, QMessageBox.Ok)
            return
        res = db.check_login(account, passwd)
        if res[0] is False:
            QMessageBox.information(None, '标题', "密码不正确", QMessageBox.Ok, QMessageBox.Ok)
            self.passwd.clear()
        # TODO 登录成功,还要链接socket,刷新消息记录，好友信息，请求信息
        else:
            # 连接服务器
            try:
                status = connect.log_into_server(str(res[1]))
            except Exception:
                QMessageBox.information(None, '标题', "网络异常，重新开启聊天", QMessageBox.Ok, QMessageBox.Ok)
                self.widget.close()
                return

            if status is False:
                QMessageBox.information(None, '标题', "您已在线", QMessageBox.Ok, QMessageBox.Ok)
                connect.get_conn().close()
                return
            else:
                self.widget.close()
                ui_chat = ChatTable.Ui_origin(res[1], res[2])
                ui_chat.setupUi()
                ui_chat.show()

    def go_to_register(self):
        self.widget.hide()
        self.register_win = QDialog()
        self.ui = register.Ui_Dialog()
        self.ui.setupUi(self.register_win)
        self.register_win.show()
        self.register_win.exec_()
        self.widget.show()





