
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

import sqlite3

class JoinForm(QDialog):
    def __init__(self, widget):
        super(JoinForm, self).__init__()
        loadUi("join.ui", self)
        self.widget = widget

        self.pwEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.enrollBtn.clicked.connect(self.enroll_user)
        self.cancleBtn.clicked.connect(self.cancle)

    def enroll_user(self):
        print("회원가입 버튼")
        id = self.idEdit.text()
        pw = self.pwEdit.text()
        confirm = self.confirmEdit.text()

        if len(id)==0 or len(pw)==0 or len(confirm)==0:
            self.chLabel.setText("Please input all fields. ")
            print('입력되지 않은 정보가 있습니다.')
        elif pw != confirm:
            self.chLabel.setText("Passwords do not match")
        else:
            conn = sqlite3.connect('employee.db')
            cur = conn.cursor()

            #---중복확인 코드 추가하기

            sql = ('INSERT INTO employee_info VALUES(?, ?)')
            cur.execute(sql, (id, pw))

            conn.close() # 연결해제

            print("회원가입이 완료되었습니다.")
            self.reset_ui()
            self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    def cancle(self):
        print("취소 버튼")
        self.reset_ui()
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)


    def reset_ui(self):
        print("화면에 입력된 데이터 없애기")
        self.idEdit.clear()
        self.pwEdit.clear()
        self.confirmEdit.clear()
        self.chLabel.clear()


