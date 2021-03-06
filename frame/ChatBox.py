from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QColorDialog, QFontDialog, QDialog
from PyQt5.QtCore import Qt
from util.connect import send_text, send_img
from time import strftime, localtime
from util import db

isImageFile = False


def clearFunc():
    global isImageFile
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


class Ui_ChatBox(QDialog):
    close_signal = QtCore.pyqtSignal(int)

    def __init__(self, use_name, user_id, from_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_name = use_name
        self.user_id = user_id
        self.from_id = from_id
        self.imgCount = 1
        self.file_path = ""
        self.extraMsg = ""
        self.isComplexFormat = False
        db.set_all_read(int(self.user_id), self.from_id)

    def setupUi(self):
        self.setObjectName("ChatBox")
        self.resize(621, 599)

        self.input = myTextEdit(QtWidgets.QTextEdit(self))
        # 连接Enter信号
        self.input.send_text_signal.connect(self.send_message)
        self.input.setObjectName("input")
        self.input.cursorPositionChanged.connect(clearFunc)

        # 将新override的子类加到widget中
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 420, 621, 181))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.input)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 380, 621, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.emoji = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.emoji.setObjectName("emoji")
        self.emoji.clicked.connect(self.sendEmit)
        self.horizontalLayout.addWidget(self.emoji)
        self.modify_color = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # 改颜色
        self.modify_color.clicked.connect(self.change_color)
        self.modify_color.setObjectName("modify_color")
        self.horizontalLayout.addWidget(self.modify_color)
        self.modify_font = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # 改字体
        self.modify_font.clicked.connect(self.change_font)
        self.modify_font.setObjectName("modify_font")
        self.horizontalLayout.addWidget(self.modify_font)
        self.upload_file = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # 上传文件
        self.upload_file.clicked.connect(self.openfile)
        self.upload_file.setObjectName("upload_file")
        self.horizontalLayout.addWidget(self.upload_file)
        self.clear = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear.clicked.connect(self.cls_screen)
        self.clear.setObjectName("clear")
        self.horizontalLayout.addWidget(self.clear)
        self.view = QtWidgets.QTextBrowser(self)
        self.view.setGeometry(QtCore.QRect(0, 0, 621, 381))
        self.view.setObjectName("view")
        self.retranslateUi()

    def retranslateUi(self):
        self.input.setPlaceholderText("Enter键发送")
        self.emoji.setText("发送")
        self.modify_color.setText("字体颜色")
        self.modify_font.setText("调整字体")
        self.upload_file.setText("上传图片")
        self.clear.setText("清空")
        allHistory = db.query_all_history(self.from_id, int(self.user_id))
        for res in allHistory:
            if res[0] != int(self.from_id):
                self.view.append("<font color=\"blue\" size=3>" + '(' + self.user_name + ')' + str(res[3]))
            else:
                self.view.append("<font color=\"green\" size=3>" + '(我)' + str(res[3]))
            if res[2] is not None:
                self.view.append("<img src=%s height='250' width='250'/>" % res[2])
            else:
                self.view.append(res[1])
            self.view.append("<br/>")
        self.view.append("<br/>")
        self.view.append("<font color=\"gray\" size=3>" + "------------------------------------------以上为历史消息------------------------------------------" + "</font> ")
        self.view.append("<br/>")

    def openfile(self):
        global isImageFile
        fileName = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fileName[0]:
            self.file_path = fileName[0]
            self.extraMsg = self.input.toPlainText()
            if len(self.extraMsg) is not 0:
                self.isComplexFormat = True
            self.input.append("<img src=%s height='250' width='250'/>" % self.file_path)
            isImageFile = True
        else:
            isImageFile = False
            return

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.input.setCurrentFont(font)

    def change_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.input.setTextColor(col)

    def send_message(self, msg_type):
        if msg_type is 0:
            content = self.input.toHtml()
            send_text(content=content, to_user=self.user_id)
            self.input.clear()
            self.view.append("<font color=\"green\" size=3>" + "(我)" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
            self.view.append(content)
            self.view.append("<br/>")
            db.add_friend_chat_history(self.from_id, int(self.user_id), content)
        # 发的图片
        else:
            self.input.clear()
            self.view.append("<font color=\"green\" size=3>" + "(我)" + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
            self.view.append("<img src=%s height='250' width='250'/>" % self.file_path)
            self.view.append("<br/>")
            img = open(self.file_path, 'rb')
            img_pack = img.read()
            size = len(img_pack)
            send_img(img_pack, self.user_id, size)
            img.close()
            db.add_friend_chat_history(self.from_id, int(self.user_id), None, path=self.file_path)

    def get_msg(self, from_id, msg):
        # 不是自己
        if from_id is not int(self.user_id):
            return
        self.view.append("<font color=\"blue\" size=3>" + '('+self.user_name + ')' + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
        self.view.append(msg)
        self.view.append("<br/>")

    def receive_img(self, img_bytes, from_id):
        if from_id is not int(self.user_id):
            return
        with open('../history/%d.jpg' % self.imgCount, 'wb') as img:
            img.write(img_bytes)
            img.close()
        self.view.append("<font color=\"blue\" size=3>" + '(' + self.user_name + ')' + strftime("%Y-%m-%d %H:%M:%S", localtime()) + "</font> ")
        self.view.append("<img src=../history/%d.jpg height='250' width='250'/>" % self.imgCount)
        self.view.append("<br/>")
        # TODO fix here
        self.imgCount += 1

    def cls_screen(self):
        self.view.clear()

    def closeEvent(self, event):
        self.close_signal.emit(int(self.user_id))
        event.accept()

    def sendEmit(self):
        global isImageFile
        if not self.input.toPlainText():
            return
        if isImageFile:
            self.send_message(1)
            isImageFile = False
        else:
            self.send_message(0)
