import login

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class MainForm(QMainWindow):
    def __init__(self, widget):
        super(MainForm, self).__init__()
        loadUi("main.ui", self)

        self.widget = widget
        # self.widget.setFixedWidth(1500)
        # self.widget.setFixedHeight(1000)
        # self.widget.resize(1500, 1000)



