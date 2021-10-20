from myAppWindow7 import *
# .....................


from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from openpyxl import *
#from myql1 import *
from sqllite import *
import xlrd
from os import path as os_path
from pylab import *
from PyQt5.QtCore import Qt
from messageBox import *
class ControlAccess:
    def __init__(self, db, window,access,parent):
        self.win = window
        self.db = db
        self.access = access
        
        self.parent = parent
        if self.access == 1:
            self.admin()
        elif self.access == 2:
            self.sAdmin()
        elif self.access == 3:
            self.gUser()
        elif self.access == 4:
            self.user()
        
        self.popupmessage = MessagePopUp("Update user informations","do you really want to update informations for this exam", 2, 1)
        self.updateList()
        self.win.addU.clicked.connect(lambda:self.manipUsers(0))
        self.win.updateU.clicked.connect(lambda:self.manipUsers(1))
        self.win.deleteU.clicked.connect(lambda:self.manipUsers(2))
        
    def updateList(self):
        self.win.listUsers.clear()
        res = self.db.selectNameUsers()
        self.parent.comboBox.clear()
        for elt in res:
            self.win.listUsers.addItem(elt[0])
            self.parent.comboBox.addItem(elt[0])
    def manipUsers(self,fn):
        fonctions = [self.addUser,self.updateUser,self.deleteUser]
        data = [self.db.selectNextId("users"),self.win.user.text(),self.win.passwordUser.text()]
        if self.win.adminU.isChecked() == True:
            data.append(1)
        elif self.win.superU.isChecked() == True:
            data.append(2)
        elif self.win.geniorU.isChecked() == True:
            data.append(3)
        else :
            data.append(4)
        today = date.today()
        data.append(today)
        fonctions[fn](data)
    
    def addUser(self,data):
        if data[1]=='':
            self.popupmessage.showMsgPopUp(1, "Login can't be empty value")
            return
        if data[2]=='':
            self.popupmessage.showMsgPopUp(1, "Password can't be empty value")
            return
        res = self.db.selectUserByName(data[1])
        if res == None:
            self.db.insertUser(data)
            self.updateList()
        else:
            self.popupmessage.showMsgPopUp(1, "This user is in data base")
            return
        pass
    def updateUser(self,data):
        if data[1]=='Administrator':
            self.popupmessage.showMsgPopUp(1, "Sorry, You can not update this super user")
            return
        if data[1]=='':
            self.popupmessage.showMsgPopUp(1, "Login can't be empty value")
            return
        if data[2]=='':
            self.popupmessage.showMsgPopUp(1, "Password can't be empty value")
            return
        res = self.db.selectUserByName(self.win.listUsers.currentText())
        if res == None:
            self.popupmessage.showMsgPopUp(1, "Can't update, No user with login")
            return
        else:
            data[0] = self.db.selectUserByName(self.win.listUsers.currentText())[0]
            
            
            self.db.updateUser(data)

            self.updateList()
    def deleteUser(self,data):
        if data[1]=='Administrator':
            self.popupmessage.showMsgPopUp(1, "Sorry, You can not delete this super user")
            return
        if data[1]=='':
            self.popupmessage.showMsgPopUp(1, "You must choose a user to delete")
            return

        res = self.db.selectUserByName(data[1])
        if res == None:
            self.popupmessage.showMsgPopUp(1, "Can't delete, No user with login")
            return
        else:
            self.db.deleteUser(data[1])
            self.updateList()
        
    
    def user(self):
        self.win.AddPlayer.setEnabled(False)
        self.win.Update.setEnabled(False)
        
        self.win.addScoreExam.setEnabled(False)
        self.win.updateScoreExam.setEnabled(False)
        self.win.addNewExam.setEnabled(False)
        self.win.updateExam.setEnabled(False)
        self.win.deleteExam.setEnabled(False)

        self.win.addResultTournament.setEnabled(False)
        self.win.updateRankTournament.setEnabled(False)
        self.win.addEvent.setEnabled(False)
        self.win.updateEvent.setEnabled(False)
        self.win.deleteEvent.setEnabled(False)

        self.win.ADD.setEnabled(False)
        self.win.UPDATE.setEnabled(False)
        self.win.DELETE.setEnabled(False)
        self.win.add_session.setEnabled(False)
        self.win.delete_session.setEnabled(False)
        self.win.add_presence.setEnabled(False)
        self.win.delete_presence.setEnabled(False)

        self.win.admin.setEnabled(False)

    def sAdmin(self):
        self.win.admin.setEnabled(False)
    def admin(self):
        pass
    def gUser(self):
        
        
        self.win.delete_player_btn.setEnabled(False)
        
        self.win.deleteExam.setEnabled(False)

        
        self.win.deleteEvent.setEnabled(False)

        self.win.ADD.setEnabled(False)
        self.win.UPDATE.setEnabled(False)
        self.win.DELETE.setEnabled(False)
        
        self.win.delete_session.setEnabled(False)
        
        

        self.win.admin.setEnabled(False)




        