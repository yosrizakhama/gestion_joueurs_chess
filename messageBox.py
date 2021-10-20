from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MessagePopUp(QMessageBox):
    def __init__(self, title, msg, type, index ) -> None:
        super().__init__()
        self.title = title
        self.msg = msg
        self.type = type
        self.index = index
        self.setWindowIcon(QIcon('slogan.png'))
        self.setText(self.msg)
        self.setWindowTitle(self.title)

    def showMsgPopUp(self, type, msg):
        self.type = type
        self.msg = msg
        self.setText(self.msg)
        if self.type == 1:
            self.setStandardButtons(QMessageBox.Ok)
            self.setIcon(QMessageBox.Warning)
        else:
            self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.setIcon(QMessageBox.Question)
        
        self.buttonClicked.connect(self.msgButtonClick)

        returnValue = self.exec()
        return returnValue

    def msgButtonClick(self,i):
        #print("Button clicked is:",i.text())
        pass



