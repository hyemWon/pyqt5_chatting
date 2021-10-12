import sqlite3
import sys
import join, main

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class LoginForm(QDialog):
    def __init__(self, widget):
        super(LoginForm, self).__init__()
        loadUi("login.ui", self)
        self.widget = widget

        self.pwEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # 패스워드 모드

        self.loginBtn.clicked.connect(self.goto_login)
        self.joinBtn.clicked.connect(self.goto_join)


    def goto_login(self):
        print("로그인 완료")
        user_id = self.idEdit.text()
        user_pw = self.pwEdit.text()

        if len(user_id)==0 or len(user_pw)==0:
            self.chLabel.setText("Please input all fields. ")

        else:
            conn = sqlite3.connect("employee.db")
            cur = conn.cursor()

            cur.execute('SELECT * FROM employee_info WHERE user_id=?', (user_id,))
            try:
                if user_pw == cur.fetchone()[1]:
                    # self.reset_ui()
                    self.widget.hide() # 숨기기
                    self.main_obj = main.MainForm(user_id)
                    self.main_obj.exec() # 창이 끝날때까지 기다리기
                    self.widget.show()

                    # main_obj.set_worker(user_id)

                    # self.widget.setCurrentIndex(self.widget.currentIndex()+2)
            except:
                self.chLabel.setText("Not correct information")


    # 회원가입 화면 띄우기
    def goto_join(self):
        print("회원가입 화면 띄우기")
        self.reset_ui()
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    # 화면에 입력된 데이터 없애기
    def reset_ui(self):
        self.idEdit.clear()
        self.pwEdit.clear()
        self.chLabel.clear()

    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # 마지막 값은 기본값

        if ans == QMessageBox.Yes:  # Yes 클릭시 종료
            print("클라이언트 종료")
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    login_obj = LoginForm(widget)
    widget.addWidget(login_obj)

    join_obj = join.JoinForm(widget)
    widget.addWidget(join_obj)


    widget.setWindowTitle("4IND")
    widget.setFixedWidth(600)
    widget.setFixedHeight(800)
    widget.show()

    # try:
    #     sys.exit(app.exec_())
    # except:
    #     print("Exiting")

    sys.exit(app.exec_())





