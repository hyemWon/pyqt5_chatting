import sqlite3
import sys
import join

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
        print(user_id)
        print(user_pw)

        if len(user_id)==0 or len(user_pw)==0:
            self.chLabel.setText("Please input all fields. ")

        else:
            # conn = sqlite3.connect("fourind.db")
            # cur = conn.cursor()
            self.reset_ui()
            self.widget.setCurrentIndex(self.widget.currentIndex()+2)


    def goto_join(self):
        print("회원가입 화면 띄우기")
        self.reset_ui()
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def reset_ui(self):
        print("화면에 입력된 데이터 없애기")
        self.idEdit.clear()
        self.pwEdit.clear()
        self.chLabel.clear()











