import os
import sys
from connectApp import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from datetime import datetime, date
import win32gui, win32con


import itertools

from sqllite import *
from principale import *




class Appwindow(QWidget,Ui_connect):
    def __init__(self, args,parent=None):
        

        QWidget.__init__(self)
        self.setupUi(parent)
        self.initUI()
        self.mabase = Mabase(base)
        self.args = args
        self.f = parent
        self.pushButton.clicked.connect(lambda:self.openPrincipale())    
        #self.show()   
        self.wind2=None
        self.popupmessage = MessagePopUp("Connect informations","do you really want to update informations for this exam", 2, 1)
        self.comboBox.clear()
        res = self.mabase.selectNameUsers()
        for elt in res:
            self.comboBox.addItem(elt[0])
        self.changePassWd()
        self.lineEdit.setText(self.comboBox.currentText())
        
    
    def initUI(self):
        self.setWindowTitle('BICA Players')
        self.setWindowIcon(QtGui.QIcon('slogan.png'))

    def openPrincipale(self):
        #print("salut")
        #self.wind2 = Principale(self.mabase,self.args)
        #pr.c.setWindowFlags(Qt.SubWindow)
        #pr.f.show()
        res = self.mabase.selectUser(self.lineEdit.text(),self.lineEdit_2.text()) 
        if res == None:
            self.popupmessage.showMsgPopUp(1, "Sorry login or password is not true")
            return
        else:
            self.f.hide()
            self.wind2 = Principale(self.mabase,self.args,res[-2],self)
            self.wind2.f.show()
            
        # appel de la deuxième fenêtre

    def changePassWd(self):
        convert = {'a':'m'}
        users = self.mabase.selectAllUsers()  
        passwd = [p[2] for p in users[1:]] 
        today = date.today()

        anDay = users[0][-1]
        dt = anDay[8:] + '/'+ anDay[5:7] + '/' + anDay[0:4]
        #print('date : ', dt)
        dayExam = datetime.strptime(dt, '%d/%m/%Y').date()
        days = (today - dayExam).days
        if days > 30:
            for i,ch in enumerate(passwd):
                #print(ch,self.perms(ch))
                data = users[i+1][:2]+(self.perms(ch),)+(users[i+1][3],)+(date.today(),)
                self.mabase.updateUser(data) 
                #print(data)
            
    def perms(self,s):
        intab = "abcdeffhijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        outtab ="rKLqrUstMNuABvwYxCSTDyz012X3EF456789abcJHdeWfQRfhIJijklmOPnVop"
        trantab = s.maketrans(intab, outtab)
        vals = [i for i in range(len(s))]
 
        # perm = itertools.permutations(s)
        # print(list(perm).count)
        return s.translate(trantab)

    

    
        
        



def main(args):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "C:\\Users\\user\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
    mabase = Mabase(base)
   
    a=QApplication(args)
    f=QWidget()
    
    c=Appwindow(args,f) 
    
    f.setAutoFillBackground(True)
    p = f.palette()
    p.setColor(f.backgroundRole(),QColor(0, 150, 255))
    f.setPalette(p)
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide , win32con.SW_HIDE)
    f.show()
    
    
    
    r=a.exec_()
    return r
    # a.exec_()  # Ici une fois suffit.
    # sys.exit(a.exec_())  # Quitte Qt

if __name__=="__main__":
    main(sys.argv) 