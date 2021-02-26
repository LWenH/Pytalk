from PyQt5.QtWidgets import QWidget, QApplication
import sys
from frame.login import Ui_login_widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_frame = QWidget()
    ui = Ui_login_widget()
    ui.setupUi(login_frame)
    login_frame.show()
    sys.exit(app.exec_())
