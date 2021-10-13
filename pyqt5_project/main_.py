import socket
import threading
import time
import cv2

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot


class MainForm(QMainWindow):
    def __init__(self, id):
        super(MainForm, self).__init__()
        loadUi("main.ui", self)

        self.worker_id = id
        self.server = "192.168.0.69"
        self.port = 5050
        self.header = 64
        self.format = 'utf-8'
        self.connected = True
        self.DISCONNECTED_MESSAGE = "!DISCONNECT"

        self.c_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.c_sock.connect((self.server, self.port))

        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()

        self.video_list = []


        # 메인창 설정
        self.setWindowTitle("4IND")
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        self.show()

        self.userLabel.setText(id + '님')

        self.sendBtn.clicked.connect(self.get_text)
        self.videoBtn.clicked.connect(self.create_video)


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
        while self.connected:
            recv_msg = self.c_sock.recv(1024).decode(self.format)
            if recv_msg:
                if recv_msg == self.DISCONNECTED_MESSAGE:
                    self.connected = False
                print(recv_msg)
                self.chatEdit.appendPlainText(recv_msg)



    @pyqtSlot(QImage)
    def setImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    # 비디오 생성
    def create_video(self):
        url = self.urlEdit.text()
        print(url)

        self.video_list.append(ClientStreaming(self))
        self.video_list[-1].changePixmap.connect(self.setImage)
        self.video_list[-1].start()


    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # 마지막 값은 기본값

        if ans == QMessageBox.Yes:  # Yes 클릭시 종료
            self.send(self.DISCONNECTED_MESSAGE) # 종료시 연결종료 메시지 전송
            time.sleep(0.5)

            self.c_sock.close()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()



class ClientStreaming(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


















