import socket
import threading
import time
import cv2

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot


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

        # 비디오
        self.labelIndex = -1  # 비디오 레이블 인덱스
        self.feedLabel = [self.feedLabel_1, self.feedLabel_2, self.feedLabel_3, self.feedLabel_4]  # 비디오 레이블
        self.feed_list = []
        self.feed = None

        # 메인창 설정
        self.setWindowTitle("4IND")
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        self.show()

        self.userLabel.setText(id + '님')

        self.sendBtn.clicked.connect(self.get_text)
        self.feedBtn.clicked.connect(self.create_video)

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

    # 비디오 생성
    # 비디오가 종료/오류나면 비디오 리스트에서 삭제, labelIndex -= 1
    def create_video(self):
        self.labelIndex += 1
        if self.labelIndex < len(self.feedLabel):
            url = self.urlEdit.text()
            self.feed_list.append(VideoInput(url, self.labelIndex))
            self.feed_list[-1].start()
            self.feed_list[-1].ImageUpdate.connect(self.ImageUpdateSlot)
        else:
            self.chLabel.setText("No longer create video.")

    # 시그널이 올때 실행할 슬롯
    def ImageUpdateSlot(self, Image, idx):  # 업데이트
        self.feedLabel[idx].setPixmap(QPixmap.fromImage(Image))

    # def CancelFeed(self):
    #     self.feed.stop()

    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # 마지막 값은 기본값

        if ans == QMessageBox.Yes:  # Yes 클릭시 종료
            self.send(self.DISCONNECTED_MESSAGE)  # 종료시 연결종료 메시지 전송
            time.sleep(0.5)

            self.c_sock.close()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


# class VideoOutput():
#     def __init__(self):


class VideoInput(QThread):
    ImageUpdate = pyqtSignal(QImage, int)  # 방출할 신호 타입 (QImage를 생성자로 전달)

    def __init__(self, url, idx):
        super().__init__()
        self.idx = idx
        self.url = url

        if url.isdigit():
            self.url = int(url)

        self.ThreadActive = True
        self.cap = cv2.VideoCapture(self.url)

    def run(self):
        # url = 'rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp'
        if not self.cap.isOpened():
            print("비디오 장치 연결 오류")
            self.ThreadActive = False

        while self.ThreadActive:
            ret, frame = self.cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)  # 수직축 뒤집음
                # Q 이미지로 변환
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)  # 종횡비 유지하면서 스케일
                self.ImageUpdate.emit(Pic, self.idx)

    # def stop(self):
    #     self.ThreadActive = False
    #     self.quit()

















