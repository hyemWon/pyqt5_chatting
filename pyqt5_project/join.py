
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

import sqlite3

class JoinForm(QDialog):
    def __init__(self, widget):
        super(JoinForm, self).__init__()
        loadUi("join.ui", self)
        self.widget = widget

        self.confirmedId = None

        self.pwEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.checkBtn.clicked.connect(self.check_id)
        self.enrollBtn.clicked.connect(self.enroll_user)
        self.cancleBtn.clicked.connect(self.cancle)


    # id 중복 체크
    def check_id(self):
        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()
        id = self.idEdit.text()
        print(id)

        cur.execute('SELECT * FROM employee_info WHERE user_id=?', (id,))

        if cur.fetchone() is None: # 중복 아님
            self.confirmedId = id
            self.chLabel.setText("This ID can be used")
        else:
            self.chLabel.setText("This ID already exists")

        conn.close()


    def enroll_user(self):
        id = self.idEdit.text()
        pw = self.pwEdit.text()
        confirm = self.confirmEdit.text()

        if len(id)==0 or len(pw)==0 or len(confirm)==0: # 빈 칸이 있을 경우
            self.chLabel.setText("Please input all fields. ")
            print('입력되지 않은 정보가 있습니다.')
        elif pw != confirm: # 패스워드 확인이 일치하지 않는 경우
            self.chLabel.setText("Passwords do not match")
        else:
            if self.confirmedId != id: # 중복 체크된 아이디와 입력된 아이디가 일치하지 않는 경우
                self.chLabel.setText("Please do ID check")
            else:
                conn = sqlite3.connect('employee.db')
                cur = conn.cursor()

                sql = ('INSERT INTO employee_info VALUES(?, ?)')
                cur.execute(sql, (id, pw))

                conn.commit()
                conn.close()

                print("회원가입 완료")
                self.reset_ui()
                self.widget.setCurrentIndex(self.widget.currentIndex() - 1)


    def cancle(self):
        self.reset_ui()
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    def reset_ui(self):
        self.idEdit.clear()
        self.pwEdit.clear()
        self.confirmEdit.clear()
        self.chLabel.clear()

    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # 마지막 값은 기본값

        if ans == QMessageBox.Yes:  # Yes 클릭시 종료
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()



