import socket
import threading

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class MainForm(QMainWindow):
    def __init__(self, id):
        super(MainForm, self).__init__()
        loadUi("main.ui", self)

        self.worker_id = id
        self.server = "192.168.0.69"
        self.port = 5050
        self.header = 64
        self.format = 'utf-8'
        self.DISCONNECTED_MESSAGE = "!DISCONNECT"

        self.c_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.c_sock.connect((self.server, self.port))

        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()


        # 메인창 설정
        self.setWindowTitle("4IND")
        self.setFixedWidth(1400)
        self.setFixedHeight(1000)
        self.show()

        self.userLabel.setText(id + '님')

        self.sendBtn.clicked.connect(self.get_text)


    def get_text(self):
        text = self.inputEdit.toPlainText()
        text = "[{}] {}\n".format(self.worker_id, text)
        self.inputEdit.clear()
        self.send(text)


    # 메세지 보내기
    def send(self, msg):
        message = msg.encode(self.format)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.format)
        send_length += b' ' * (self.header - len(send_length))

        self.c_sock.send(send_length)
        self.c_sock.send(message)


    # 받은 채팅을 add_chat 수행
    def recv(self):
        while True:
            recv_msg = self.c_sock.recv(1024).decode(self.format)
            if recv_msg:
                print(recv_msg)
                self.chatEdit.appendPlainText(recv_msg)

    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # 마지막 값은 기본값

        if ans == QMessageBox.Yes:  # Yes 클릭시 종료
            self.send(self.DISCONNECTED_MESSAGE) # 종료시 연결종료 메시지 전송
            self.c_sock.close()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()














