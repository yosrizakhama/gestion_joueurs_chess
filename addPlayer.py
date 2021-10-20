# .....................
#! /usr/bin/python
#­*­coding: utf­8 ­*­
#from appwindow import *
from myAppWindow7 import *
# .....................
import sys
import os
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPushButton, QMessageBox
#from principale import Appwindow

#from myql1 import *
from sqllite import *
import xlrd
from os import path as os_path


class AddPlayer:
    def __init__(self, db, window, listP):
        self.win = window
        self.db = db
        self.listP = listP
        self.listView = self.win.comboBox
        self.listUpdate = self.win.player_liste_update
        self.updateBtn = self.win.update_player_btn
        self.dateUpdate = self.win.birthday_edit_update
        self.dateAdd = self.win.birthday_edit
        self.addPlayerBtn = self.win.add_player_btn
        self.deleteButton = self.win.delete_player_btn
        self.fileAdd = self.win.picture_edit
        self.fileUpdate = self.win.picture_edit_update
#self.fileAdd.clicked.connect( lambda:self.browseSlot(1))
        self.listUpdate.currentIndexChanged.connect(self.clickListUpdate)
        #self.listView.activated[str].connect(lambda:self.clickListView()) 
        self.listView.currentIndexChanged.connect(self.clickListView)
        self.updateBtn.clicked.connect(lambda:self.clickUpdateBtn()) 
        self.dateUpdate.dateChanged.connect(lambda:self.dateChanged(2))
        self.dateAdd.dateChanged.connect(lambda:self.dateChanged(1)) 
        self.deleteButton.clicked.connect(lambda:self.deleteBtn())
        self.addPlayerBtn.clicked.connect(lambda:self.addPlayerTest())
        self.fileAdd.clicked.connect( lambda:self.browseSlot(1))
        self.fileUpdate.clicked.connect( lambda:self.browseSlot(2))
        
        self.PATH = os_path.abspath(os_path.split(__file__)[0])
        self.index = -1
        self.clubNbr = 0
        self.listClub = self.db.selectListClub()
        ##print('liste des clubs : ',self.listClub)
        self.remplir_list_club()
        today = date.today()
        self.win.birthday_edit_update.setDate(today)
        self.win.birthday_edit.setDate(today)
        self.win.ratingDateAdd.setDate(today)
        self.remplirListJoueur()
        
        

    
        #return super(principale.Appwindow, self).eventFilter(obj, event)
        
    def browseSlot(self,fn):
        file = self.getfiles()
        if fn == 1:
            #print("Add file")
            self.win.picture_add_value.setText(file)
        else:
            #print("Update file")
            self.win.picture_update_value.setText(file)

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Image files (*.jpg *.gif *.png *.tiff *.xpm *.bmp)"])
        #filenames = QStringList()
		
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            #print(filenames)
            return filenames[0]
        

    def remplir_list_club(self):
        for elt in self.listClub:
            self.win.listClub.addItem(elt[0])
            self.win.listClub_2.addItem(elt[0])

    def dateChanged(self, fen):
        if fen == 1:
            self.win.birthday_add_value.setText(self.dateAdd.date().toString('dd/MM/yyyy'))
            birth = datetime.strptime(self.win.birthday_add_value.text(), '%d/%m/%Y').date()
            self.countCategory(birth, self.win.category_add_value)
        else:
            self.win.birthday_update_value.setText(self.dateUpdate.date().toString('dd/MM/yyyy'))
            birth = datetime.strptime(self.win.birthday_update_value.text(), '%d/%m/%Y').date()
            self.countCategory(birth, self.win.category_update_value)
    def clickUpdateBtn(self):
        self.showDialog(1,"Do you really want to update informations for " + self.win.name_update_value.text())
        self.win.actualiserPointeurListe()
        #self.showDialog(2,"We must put all infomations for  " + self.win.name_update_value.text())

# ........................................
    def showDialog(self, type, msg):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon('slogan.png'))
        
        msgBox.setText(msg)
        msgBox.setWindowTitle("Update Player Informations")
        if type in [1,3]:
            if type == 1 and self.index == -1:
                msgBox.setText("Sorry but you must choose a player to update informations ")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setIcon(QMessageBox.Warning)
            else:
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msgBox.setIcon(QMessageBox.Question)
        elif type in [2,4]:
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setIcon(QMessageBox.Warning)
        else:
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setIcon(QMessageBox.Question)

        msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
            ##print('Yes clicked :',self.db.selectNextId())
            if type == 1:
                
                self.update()
                
            elif type==3:
                self.addPlayerDb()
                self.win.indexPlayer = self.win.player_liste_update.currentIndex()
                self.win.actualiserPointeurListe()
            else:
                #print("This player is deleted")
                self.db.deletePlayer(self.listP[self.index][0])
                
                self.remplirListJoueur()
                self.index = -1
                self.win.indexPlayer = 0
                self.win.actualiserPointeurListe()
        else:
            pass
            #print('No clicked')
# (29, 'El Behi Nour', 'f', 'TUN', 1, 'BICA', datetime.date(2014, 1, 1), 'U08',920, 5529093, 1600, 0, 0, 0, '', 40, './pictures/notun.jpg')
    def deleteBtn(self):
        msg = "" if self.win.name_update_value.text()=="" else "or player "+self.win.name_update_value.text()+" not in DataBase"
        if self.index == -1: 
            self.showDialog(2,"Sorry, we must choose one player after deleting "+msg)
        else:
            self.showDialog(5,"Really, you want delete this player : "+self.win.name_update_value.text())
                   
  #----------------
#   ''' NAME = "%s", sex = "%s", fed = "%s", clubnumber = "%s", clubname = "%s", 
#                   birthday = "%s", GATEGORIE = "%s", nelo = "%s", fideno = "%s", celo = "%s",
#                   belo = "%s", relo = "%s", score = "%s", title = "%s",
#                   k = "%s", PICTURE = "%s" '''
  # --------------
    def update(self):
        data = []
        data.append(self.listP[self.index][0])
        data.append(self.win.name_update_value.text())

        if self.win.male_update.isChecked() == True:
            data.append("m")
        else:
            data.append("f")
        data.append(self.win.fed_update_value.text())
        data.append(self.clubNbr)
        data.append(self.win.club_update_value.text())
        if '/' not in self.win.birthday_update_value.text()[6:]:
            birth = datetime.strptime(self.win.birthday_update_value.text(), '%d/%m/%Y').date()
        else:
            d = self.win.birthday_update_value.text()
            dt = d[8:]+ d[4:7] + '/' + d[0:4]
            birth = datetime.strptime(dt, '%d/%m/%Y').date()
        data.append(birth)
        data.append(self.win.category_update_value.text())
        data.append(int(self.win.national_update_value.text()))
        data+=[int(self.win.fideid_update_value.text())] if self.win.fideid_update_value.text()!="" else [0] 
        data.append(int(self.win.classic_update_value.text()))
        data.append(int(self.win.rapid_update_value.text()))
        data.append(int(self.win.blitz_update_value.text()))
        data+=[int(self.win.score_add_update.text())] if self.win.score_add_update.text().isnumeric() else [0]
        data.append(self.win.title_update_value.text())
        data.append(int(self.win.k_update_value.text()))
        data.append(self.win.picture_update_value.text())
        data += [int(self.win.levelUpdate.text())] if self.win.levelUpdate.text().isnumeric() else [0]
        data += [int(self.win.phoneUpdate.text())] if self.win.phoneUpdate.text().isnumeric() else [0]
        data += [self.win.mailUpdate.text()]
        data+=[self.win.cardNumber.text()]
        ##print(data)
        todayR = date.today()
        todayRstr=todayR.strftime('%d/%m/%Y')
        today = self.win.ratingDateAdd.date().toString('dd/MM/yyyy')
        dayUpdate = datetime.strptime(today, '%d/%m/%Y').date()
        ##print(todayRstr,":",today)
        if today==todayRstr:
            self.db.updateplayer(data)
            self.win.indexPlayer = self.win.player_liste_update.currentIndex()
            
            self.showDialog(4, "Data player updated OK")
        else:
            data2=data[0:7]+[data[8]]+data[13:]
            self.db.updateplayerNoRating(data2)
        
        
        data1=[data[0]] + data[10:13]
        data1.append(data[8])
        
        data1.append(dayUpdate)
        result = self.db.selectElo(self.listP[self.index][0],dayUpdate)
        #print(result)
        #print(data1)
        if result == None:
            self.db.insertElo(data1)
        else:
            self.db.updateElo(data1)
        self.remplirListJoueur()
    def msgButtonClick(self,i):
        pass
        #print("Button clicked is:",i.text())
# ........................................

    def addPlayerTest(self):
        if self.win.name_add_value.text() == "":
            self.showDialog(4, "Sorry, name can't be empty")
            return 
        if self.win.lineEdit.text() == "":
            self.showDialog(4, "Sorry, name can't be empty")
            return 
        if self.win.fed_add_value.text() == "":
            self.showDialog(4, "Sorry, FED can't be empty")
            return 
        if self.win.birthday_add_value.text() == "":
            self.showDialog(4, "Sorry, Birthday can't be empty")
            return 
        if self.win.category_add_value.text() == "":
            self.showDialog(4, "Sorry, Category can't be empty")
            return
        if self.win.phoneNumberAdd.text() == "":
            self.showDialog(4, "Sorry, phoneNumber can't be empty")
            return 
        if self.win.levelAdd.text() == "":
            self.showDialog(4, "Sorry, level can't be empty")
            return 
        self.showDialog(3, "Do you really want to add "+self.win.name_add_value.text()+" to your DataBase")
        
    def addPlayerDb(self):
        ##print("player added ok")
        idPlayer = self.db.selectNextId('PLAYER')
        data = [idPlayer,]
        data += [self.win.name_add_value.text() +" " + self.win.lineEdit.text() ]
        if self.win.femele.isChecked() == True:
            data += ['f']
        else:
            data += ['m']
        data += [self.win.fed_add_value.text()]
        data += [1]
        data += [self.win.club_add_value.text()]
        birth = datetime.strptime(self.win.birthday_add_value.text(), '%d/%m/%Y').date()
        today = date.today()
        year = today.year - birth.day
        data += [birth]

        data += [self.win.category_add_value.text()]
        data += [int(self.win.national_add_value.text())] if self.win.national_add_value.text().isnumeric() else [0]
        data += [int(self.win.fideid_add_value.text())] if self.win.fideid_add_value.text().isnumeric() else [0]
        data += [int(self.win.classic_add_value.text())] if self.win.classic_add_value.text().isnumeric() else [0]
        data += [int(self.win.rapid_add_value.text())] if self.win.rapid_add_value.text().isnumeric() else [0]
        data += [int(self.win.blitz_add_value.text())] if self.win.blitz_add_value.text().isnumeric() else [0]
        data += [int(self.win.score_add_value.text())] if self.win.score_add_value.text().isnumeric() else [0]
        data += [self.win.title_add_value.text()]
        data += [int(self.win.k_add_value.text())] if self.win.k_add_value.text().isnumeric() else [0]
        data += [self.win.picture_add_value.text()]
        data += [int(self.win.levelAdd.text())] if self.win.levelAdd.text().isnumeric() else [0]
        data += [int(self.win.phoneNumberAdd.text())] if self.win.phoneNumberAdd.text().isnumeric() else [0]
        data += [self.win.mailAdd.text()]
        data += [self.win.CardNumber.text()]
       # #print(data)
        data1=[data[0]] + data[10:13]
        data1.append(data[8])
        today = date.today()
        data1.append(today)
        self.db.insertPlayer(data)
        self.db.insertElo(data1)
        self.remplirListJoueur()
        self.showDialog(4, "Player added OK")

    def countCategory(self, birth, obj):
        
        today = date.today()
        year = today.year - birth.year
        month = birth.month
        day = birth.day
        
        #...............Category ......................
        if year<=6:
            obj.setText('U06')
            if month == 1 and day == 1 and year == 6:
                obj.setText('U08')
        elif year<=8:
            obj.setText('U08')
            if month == 1 and day == 1 and year == 8:
                obj.setText('U10')
        elif year<=10:
            obj.setText('U10')
            if month == 1 and day == 1 and year == 10:
                obj.setText('U12')
        elif year<=12:
            obj.setText('U12')
            if month == 1 and day == 1 and year == 12:
                obj.setText('U14')
        elif year<=14:
            obj.setText('U14')
            if month == 1 and day == 1 and year == 14:
                obj.setText('U16')
        elif year<=16:
            obj.setText('U16')
            if month == 1 and day == 1 and year == 16:
                obj.setText('U18')
        elif year<=18:
            obj.setText('U18')
            if month == 1 and day == 1 and year == 18:
                obj.setText('U20')
        elif year<=20:
            obj.setText('U20')
            if month == 1 and day == 1 and year == 20:
                obj.setText('Open')
            
        elif year>60:
            obj.setText('S60')
            
        elif year>50:
            obj.setText('S50')
            if month == 1 and day == 1 and year == 60:
                obj.setText('S60')
        else:
            obj.setText('Open')
            if month == 1 and day == 1 and year == 50:
                obj.setText('S50')
    
    #"""(id,NAME,sex,fed,clubnumber,clubname,birthday,GATEGORIE,nelo,fideno,celo,relo,belo,score,title,k,PICTURE)"""
    def nameList(self,listN):
        str1 = listN.currentText()
        i = str1.find(":")+1
        name = str1[i:]
        index = int(str1[:i-1])-1
        return name,index
    
    def clickListUpdate(self,index):
        ##print("click OK Update")
        #name,self.index = self.nameList(self.listUpdate)
        ##print(self.index,name)
        ##print(self.listP[self.index])
        self.win.indexPlayer = self.listUpdate.currentIndex()
        self.win.actualiserPointeurListe()
        self.index = index
        player = self.listP[self.index]
        #print(player)
        self.win.name_update_value.setText(player[1])
        if player[2]=='m':
            self.win.male_update.setChecked(True)
            self.win.femele_update.setChecked(False)
        else:
            self.win.male_update.setChecked(False)
            self.win.femele_update.setChecked(True)
#     
#     
#       
        date =player[6].replace('-','/')  #.strftime('%d/%m/%Y')

        self.win.fed_update_value.setText(player[3])
        self.win.club_update_value.setText(player[5])
        self.win.birthday_update_value.setText(date)
        self.win.category_update_value.setText(player[7])
        self.win.fideid_update_value.setText(str(player[9]))
        self.win.title_update_value.setText(player[14])
        self.win.classic_update_value.setText(str(player[10]))
        self.win.rapid_update_value.setText(str(player[11]))
        self.win.blitz_update_value.setText(str(player[12]))
        self.win.k_update_value.setText(str(player[15]))
        self.win.national_update_value.setText(str(player[8]))
        self.win.score_add_update.setText(str(player[13]))
        self.win.picture_update_value.setText(player[16])
        self.clubNbr = player[4]
        self.win.levelUpdate.setText(str(player[-4]))

        self.win.mailUpdate.setText(str(player[-2]))
        self.win.phoneUpdate.setText(str(player[-3]))
        self.win.cardNumber.setText(player[20])

        ##print(self.clubNbr)
    
    def clickListView(self,index):
        self.win.indexPlayer = self.listView.currentIndex()
        self.win.actualiserPointeurListe()
        ##print("click OK View")
        #name,index = self.nameList(self.listView)
        # elo = db.selectEloplayer(int(self.listP[index][0]))
        # #print(elo)
        self.win.name_2.setText(self.listP[index][1])
        self.win.club_2.setText(self.listP[index][5])
        self.win.fideid.setText(str(self.listP[index][9]))
        r = str(self.listP[index][10])
        self.win.crating.setText(r)
        self.win.rrating.setText(str(self.listP[index][11]))
        self.win.brating.setText(str(self.listP[index][12]))
        self.win.score.setText(str(self.listP[index][13]))
        self.win.nrating.setText(str(self.listP[index][8]))
        fileStr = self.listP[index][-5]
        if fileStr !='' and fileStr[0]=='.':
            file = self.PATH +'/' + self.listP[index][-5][2:]
        else:
            file = fileStr
        #print("le fichier est:",file)
       
        pixmap = QtGui.QPixmap(file)
        self.win.label_3.setPixmap(pixmap)
        self.win.label_3.resize(pixmap.width(),pixmap.height())
        date =self.listP[index][6].replace('-','/')#.strftime('%d/%m/%Y')
        self.win.date_2.setText(date)
        self.win.category_2.setText(self.listP[index][7])
        self.win.level.setText(str(self.listP[index][17]))
        self.win.phonenumber.setText(str(self.listP[index][18]))
        self.win.mail.setText(self.listP[index][19])
        self.win.card.setText(self.listP[index][20])
        histRating = self.db.selectHistEloplayer(self.listP[index][0])
        ##print(histRating)
        ##print(index,name)
        ##print(self.listP[index])
        self.win.plot(histRating)
        listClub = self.db.selectListClub()
        #print(listClub)
        

    def remplirListJoueur(self):
        self.win.comboBox.clear()
        self.win.player_liste_update.clear()
        self.win.playerExams.clear()
        self.win.list_player.clear()
        self.win.list_player_2.clear()
        self.win.list_player_3.clear()
        self.win.playerTournament.clear()
        self.win.titleExams_2.clear()
        self.win.listplayerScore.clear()
        self.win.playerScore.clear()

        self.win.playerPayment.clear()
        self.win.playerVIP.clear()

        self.listP = self.db.selectAllPlayer()
        self.win.emploi.listP = self.db.selectAllPlayer()
        
        
        ##print(self.listP)
        for i,elt in enumerate(self.listP):
            
            self.win.comboBox.addItem(elt[1])#str(i+1)+':'+
            self.win.player_liste_update.addItem(elt[1])#str(i+1)+':'+
            self.win.playerExams.addItem(elt[1])
            self.win.list_player.addItem(elt[1])
            self.win.list_player_2.addItem(elt[1])
            self.win.list_player_3.addItem(elt[1])
            self.win.playerTournament.addItem(elt[1])
            self.win.titleExams_2.addItem(elt[1])
            self.win.listplayerScore.addItem(elt[1])
            self.win.playerScore.addItem(elt[1])

            self.win.playerPayment.addItem(elt[1])
            self.win.playerVIP.addItem(elt[1])
        self.win.actualiserPointeurListe()    
            
        ##print(listeP)
        return (self.listP)