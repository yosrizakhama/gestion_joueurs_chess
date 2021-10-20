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
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTableWidgetItem
from TableModel import *
import pandas as pd
#from myql1 import *
from sqllite import *
import xlrd
from os import path as os_path

from messageBox import *
import pandas as pd

class Emploi:
    def __init__(self, db, window,pl):
        self.win = window
        self.db = db
        self.listE = self.db.selectAllSession()
        self.indexDeleteSession = -1
        self.df = []
        self.titleSession = ""
        self.listTitleSession = ["Monday","8:30","Chess",1]
        self.pl = pl
        #self.listP = self.pl
        self.listP = self.db.selectAllPlayer()
        self.listS = self.db.selectAllSession()
        self.listSforP = self.listS
        self.listSAll = self.listS
        #print("la liste des cours est : ",self.listS)
        self.updateListSession()

        #self.win.day.currentIndexChanged.connect(lambda:self.changeTitleSession(0,self.win.day.currentIndex()))
        self.win.day.activated[str].connect(lambda:self.changeTitleSession(0,self.win.day.currentIndex()))

        #self.win.begin.currentIndexChanged.connect(lambda:self.changeTitleSession(1,self.win.begin.currentIndex()))
        self.win.begin.activated[str].connect(lambda:self.changeTitleSession(1,self.win.begin.currentIndex()))

        #self.win.cours.currentIndexChanged.connect(lambda:self.changeTitleSession(2,self.win.cours.currentIndex()))
        self.win.cours.activated[str].connect(lambda:self.changeTitleSession(2,self.win.cours.currentIndex()))

        #self.win.niveau.currentIndexChanged.connect(lambda:self.changeTitleSession(3,self.win.niveau.currentIndex()))
        self.win.niveau.activated[str].connect(lambda:self.changeTitleSession(3,self.win.niveau.currentIndex()))

        self.win.list_session_3.activated[str].connect(lambda:self.chargePlayersSession())
        #self.win.list_session_3.currentIndexChanged.connect(lambda:self.chargePlayersSession())

        #self.win.list_player_2.currentIndexChanged.connect(lambda:self.changeSession())
        self.win.list_player_2.activated[str].connect(lambda:self.changeSession())
        
        self.win.list_player.activated[str].connect(lambda:self.changeSessionl())

        self.win.list_player_3.activated[str].connect(lambda:self.changeIndex())

        self.win.ADD.clicked.connect(lambda:self.addSession())   
        self.win.print.clicked.connect(lambda:self.saveEmploi())
        self.win.savePresence.clicked.connect(lambda:self.savePresence(1))
        self.win.savePresence_2.clicked.connect(lambda:self.savePresence(2))
        
        self.win.add_presence.clicked.connect(lambda:self.addPresence())
        self.win.delete_presence.clicked.connect(lambda:self.deletePresence())

        self.win.DELETE.clicked.connect(lambda:self.deleteSession())   
        self.win.UPDATE.clicked.connect(lambda:self.updateSession())   
        self.win.add_session.clicked.connect(lambda:self.addSessionPlayer())  
        self.win.delete_session.clicked.connect(lambda:self.deleteSessionPlayer())  
        self.win.showPresence.clicked.connect(lambda:self.showPresence())  
        

         
        
        self.popupSession = MessagePopUp("Add session","do you really want to add session course", 2, 1)
        self.win.emploi.setColumnWidth(0,140)
        self.win.emploi.setColumnWidth(1,140)
        self.win.emploi.setColumnWidth(2,140)
        self.win.emploi.setColumnWidth(3,140)
        self.remplirEmploi()


    def changeIndex(self):
        self.win.indexPlayer = self.win.list_player_3.currentIndex()
        self.win.actualiserPointeurListe()
    
    def chargePlayersSession(self):
        res = self.db.selectPlayerFromSeance(self.listSAll[int(self.win.list_session_3.currentIndex())][0])
        self.showFicheSeance(res)
        #print('list clicker ok')
    
    def showFicheSeance(self, data):
        self.win.listepresence.clearContents()
        self.win.listepresence.setHorizontalHeaderLabels(["NAME", "PRESENT", "EXAM", "HOME WORK"])
        res =[]
        for row in range(self.win.tableWidget.rowCount()):
            self.win.listepresence.removeRow(row)
        for li, elt in enumerate(data):

            elt2=[]    
            #print('name : ', elt[0])
            rowPosition = self.win.listepresence.rowCount()
            elt2 = [elt[0],"","",""]
            if rowPosition<li+1:
                self.win.listepresence.insertRow(rowPosition)
            self.win.listepresence.setItem(li, 0, QTableWidgetItem(elt[0]))
            res.append(elt2)
        self.df = res   
        #data1 = pd.DataFrame(res,columns=["NAME", "PRESENT", "EXAM", "HOME WORK"],index=indexis)
        
        
            
        

    def exportPresenceToExcel(self, file, listDf,type):
        if type==1:
            columnHeaders = ['Session','Time','Day','Present']
        else: 
            columnHeaders = ["NAME", "PRESENT", "EXAM", "HOME WORK"]
        df = pd.DataFrame(listDf, columns=columnHeaders)
        df.to_excel(file, index=True)
        #print('Excel file exported')
        
    def savePresence(self,type):
        if type==1:
            file = self.getfiles(3)
        else:
            file = self.getfiles(2)
        if file !='' and  file.find('.xlsx')!=-1:
            self.exportPresenceToExcel(file,self.df,type)
        elif file == '':
            self.popupSession.showMsgPopUp(1,"You must choose a file")
        else:
            self.popupSession.showMsgPopUp(1,"{} is not in a regular form, you file must end with {}.xlsx".format(file))
    
    def showPresence(self):
        self.win.tableWidget.clearContents()
        for row in range(self.win.tableWidget.rowCount()):
            self.win.tableWidget.removeRow(row)
        if self.listP !=[]:
            data = []
            data.append(self.listP[self.win.list_player_3.currentIndex()][0])
            today = self.win.day1.date().toString('dd/MM/yyyy')
            dayExam = datetime.strptime(today, '%d/%m/%Y').date()
            data.append(dayExam)
            today = self.win.day2.date().toString('dd/MM/yyyy')
            dayExam = datetime.strptime(today, '%d/%m/%Y').date()
            data.append(dayExam)
            res = self.db.selectPresenceFromPlayter(data)
            #print("liste des seances : ",res)
            res2 = []
            #self.win.tableWidget.clear()
            for row,elt in enumerate(res):
                res3 = []
                rowPosition = self.win.tableWidget.rowCount()
                if rowPosition<=row:
                    self.win.tableWidget.insertRow(rowPosition)
                for i,cel in enumerate(elt):   
                    #print("(row,col):","(",row,":",i,") : ",cel)   
                    if i==3 and cel == 0:
                        cel = "NO"  
                    if i==3 and cel == 1:
                        cel = "YES"  
                    if i==3 and cel == 2:
                        cel = "NOT YET"
                    res3.append(cel)  
                    
                    self.win.tableWidget.setItem(row,i,QTableWidgetItem(cel))
                
                
                    
                res2.append(res3)
            self.df = res2
        
    def deletePresence(self):
        if self.listSforP == []:
            self.popupSession.showMsgPopUp(1,"Any session for {} in DataBase".format(self.win.list_player_2.currentText()))
            return
        if self.listP == []:
            self.popupSession.showMsgPopUp(1,"Any player in DataBase")
            return
        today = self.win.firstDay.date().toString('dd/MM/yyyy')
        dayExam = datetime.strptime(today, '%d/%m/%Y').date()
        data = []
        data.append(self.listP[self.win.list_player_2.currentIndex()][0])
        data.append(self.listSforP[self.win.list_session_2.currentIndex()][0])
        data.append(dayExam)
        res = self.db.selectPresence(data)
        if not res == None:
            rep = self.popupSession.showMsgPopUp(2,"Do you really want to delete this course for : {}".format(self.win.list_player_2.currentText()))    
            if rep == QMessageBox.Yes:
                self.db.deletePresence(data)
        else:
            self.popupSession.showMsgPopUp(1,"Any course to delete in DataBase")
   
    def addPresence(self):
        days = ['Monday','Tuesday','Wednesday','Friday','Thursday','Saturday','Sunday']
        if self.listSforP == []:
            self.popupSession.showMsgPopUp(1,"Any session for {} in DataBase".format(self.win.list_player_2.currentText()))
            return
        if self.listP == []:
            self.popupSession.showMsgPopUp(1,"Any player in DataBase")
            return
        

        today = self.win.firstDay.date().toString('dd/MM/yyyy')
        dayExam = datetime.strptime(today, '%d/%m/%Y').date()
        theDay = days[dayExam.weekday()]
        data = []
        player = self.listP[self.win.list_player_2.currentIndex()]
        sessionName = self.listSforP[self.win.list_session_2.currentIndex()][1] 
        if sessionName.find(theDay) == -1:
           self.popupSession.showMsgPopUp(1,"The day of session is {}, but you choose {}, please adjust the day".format(sessionName,theDay))
           return 
        data.append(player[0])
        data.append(self.listSforP[self.win.list_session_2.currentIndex()][0])
        data.append(dayExam)
        res = self.db.selectPresence(data)
        if self.win.absent.isChecked() == True:
            data.append(0)
        elif self.win.present.isChecked() == True:
            data.append(1)
        else:
            data.append(2)
        
        if res == None:
            self.db.insertPresence(data)
            self.popupSession.showMsgPopUp(1,"Data added OK")
            
        else:
            rep = self.popupSession.showMsgPopUp(2,"This course is in DataBase, Do you want to update this course")    
            if rep == QMessageBox.Yes:
                self.db.updatePresence(data)
                self.popupSession.showMsgPopUp(1,"Data updated OK")
        self.db.selectAllPresence()       
        nAb = self.db.selectPresenceStatus(data[0], player[-3],0)
        nPr = self.db.selectPresenceStatus(data[0], player[-3],1)
        div = 1 if nPr+nAb==0 else nPr+nAb
        score = nPr * 100 //div
        res = self.db.selectScore(data[0],dayExam,3)
        scorePl = self.listP[self.win.list_player_2.currentIndex()][-7] + score
        self.db.updateplayerscore([data[0],scorePl])
        #╔self.pl.remplirListJoueur()
        if res == None:
            self.db.insertScorePLayer([player[0],dayExam,player[-3],score,3]) 
        else:
            self.db.updateScorePlayer(player[0], score, dayExam, 3)

        if res == None:
            self.db.insertScorePLayer([id,dayExam,player[-3],scorePl,5]) 
        else:
            self.db.updateScorePlayer(id,scorePl,dayExam,5)

    def changeSessionl(self):
        
        data = self.win.list_player.currentIndex()
        self.win.indexPlayer = self.win .list_player.currentIndex()
        self.win.actualiserPointeurListe()
        data1 = self.listP[data][-3]
        res = self.db.selectSessionl(data1)
        self.listS = res
        self.win.list_session.clear()       
        for elt in res:
            self.win.list_session.addItem(elt[5])
        #self.listSforP = res

    
    def changeSession(self):
        data = self.win.list_player_2.currentIndex()
        self.win.indexPlayer = self.win.list_player_2.currentIndex()
        self.win.actualiserPointeurListe()
        data1 = self.listP[data][0]
        res = self.db.selectSessionFromPlayter(data1)
        self.win.list_session_2.clear()     
        #print("resultat:",res)  
        for elt in res:
            self.win.list_session_2.addItem(elt[1])
        self.listSforP = res
        

        #print(res)
    def addSessionPlayer(self):
        if self.listP != [] and self.listS != []:
            data = [self.win.list_player.currentIndex(),self.win.list_session.currentIndex()]
            #print('index:',data)
            data1 = [self.listP[data[0]][0], self.listS[data[1]][0]]
            
            #print("-Index Player : {} -Index Session : {}".format(data[0],data[1]))
            #print("-Id Player : {} -Id Session : {}".format(data1[0],data1[1]))
            if self.db.selectSessionPl(data1)==None:
                #print("info:", self.listS[data[1]] )
                session = self.listS[data[1]][5]
                level = "_" + str(self.db.selectPlayer(data1[0])[-3])+"_"
                #print("session : ",session," level : ", level)
                if session.find(level)!=-1:
                    self.db.insertSessionPlayer(data1)
                    self.popupSession.showMsgPopUp(1,"Data added OK")
                else:
                    self.popupSession.showMsgPopUp(1, "This player  {} can't be in this session {} because its not the same level".format(self.listP[data[0]][1], session))
                    return 0
            else:
                self.popupSession.showMsgPopUp(1,"this session {} is affected to this player {}".format(self.win.list_session.currentText(),self.win.list_player.currentText()))
        else:
            self.popupSession.showMsgPopUp(1,"There ara nothing for adding")
    def deleteSessionPlayer(self):
        if self.win.list_player.currentText() == "":
            self.popupSession.showMsgPopUp(1,"Any players in DB")
            return
        if self.win.list_session.currentText() == "":
            self.popupSession.showMsgPopUp(1,"Any session in DB")
            return
        res = self.db.deleteSessionPlayer([self.listP[self.win.list_player.currentIndex()][0],self.listS[self.win.list_session.currentIndex()][0]])
        if res == -1:
            self.popupSession.showMsgPopUp(1,"Thid player is not affected to this course")
        else:
            self.popupSession.showMsgPopUp(1,"Data Deleted OK")

    def updateSession(self):
        if self.win.nomseance.text() == '':
            self.popupSession.showMsgPopUp(1,"You must choose session to update")
            return
        data = [self.win.session.currentText(), self.win.day.currentText(), self.win.begin.currentText(), self.win.cours.currentText(), int(self.win.niveau.currentText()),self.win.nomseance.text()] 
        
        result = self.popupSession.showMsgPopUp(2, "do you really want to update  {} session".format(self.win.session.currentText()))
        #print("button : ",result)
        if result == QMessageBox.Yes:
            self.db.updateSession(data)
            self.popupSession.showMsgPopUp(1,"Data updated OK")
            self.updateListSession()
            self.indexDeleteSession = -1

    def deleteSession(self):
        if self.win.session.currentText() == "":
            self.popupSession.showMsgPopUp(1,"Any session to delete")
            return
        title = self.win.session.currentText()
        result = self.popupSession.showMsgPopUp(2, "do you really want to delete  {} session".format(title))
        #print("button : ",result)
        if result == QMessageBox.Yes:
            self.db.deleteSession(title)
            self.updateListSession()
            self.popupSession.showMsgPopUp(1,"Session deleted ok")
        

    def addSession(self):
        if self.win.nomseance.text() == '':
            self.popupSession.showMsgPopUp(1,"Empty name of session")
            return
        res = self.db.selectSessionT(self.win.nomseance.text())
        if res != []:
            self.popupSession.showMsgPopUp(1,"You can't add {} session, this session is in database".format(self.win.nomseance.text()))
            return
        id = self.db.selectNextId("SESSION")
        data = [id, self.win.day.currentText(), self.win.begin.currentText(), self.win.cours.currentText(), int(self.win.niveau.currentText()),self.win.nomseance.text()] 
        self.db.insertSession(data)
        self.popupSession.showMsgPopUp(1,"Data added OK")
        self.updateListSession()
        self.win.nomseance.setText("")
        self.remplirEmploi()

    def changeTitleSession(self, nbr, index):
        self.titleSession = ""
        if nbr == 0:
            self.listTitleSession[nbr] = self.win.day.currentText()
        if nbr == 1:
            self.listTitleSession[nbr] = self.win.begin.currentText()
        if nbr == 2:
            self.listTitleSession[nbr] = self.win.cours.currentText()
        if nbr == 3:
            self.listTitleSession[nbr] = self.win.niveau.currentText()

        for elt in self.listTitleSession:
            self.titleSession = self.titleSession + str(elt) + "_"
        #print(self.titleSession)
        self.win.nomseance.setText(self.titleSession)


    def updateListSession(self):
        self.win.list_session.clear()
        self.win.list_session_2.clear()
        self.win.session.clear()       
        self.listSAll = self.db.selectAllSession()
        self.win.list_session_3.clear()
        
        ##print(self.listP)
        
        for i,elt in enumerate(self.listSAll):
            
            #self.win.list_session.addItem(elt[5])#str(i+1)+':'+
            #self.win.list_session_2.addItem(elt[5])#str(i+1)+':'+
            self.win.session.addItem(elt[5])
            self.win.list_session_3.addItem(elt[5])
        #self.listS = self.db.selectAllSession()
        self.listP = self.db.selectAllPlayer()
        self.remplirEmploi()
        
    def remplirEmploi(self):
        data ={'8:30':[],'10:30':[],'13:30':[],'15:30':[]}
        monday = self.db.selectSession('Monday')
        tuesday = self.db.selectSession('Tuesday')
        wednesday = self.db.selectSession('Wednesday')
        thursday = self.db.selectSession('Thursday')
        friday = self.db.selectSession('Friday')
        saturday = self.db.selectSession('Saturday')
        sunday = self.db.selectSession('Sunday')
        days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
        listDf = []
        for row,day in enumerate(days):
            data ={'8:30':[],'10:30':[],'13:30':[],'15:30':[], '17:30':[]}
            for i,elt in enumerate(day):
                
                data[elt[2]].append(elt[3]+" L"+str(elt[4]))
            dayAdd = []
            for i,elt in enumerate(data):
                #print("\n".join(data[elt]))  
                self.win.emploi.setItem(row,i,QTableWidgetItem("\n".join(data[elt])))
                dayAdd.append("|".join(data[elt]))
            listDf.append(dayAdd)
            #print("DataFrame preparation : ",listDf)
            self.df = listDf
    
    def getfiles(self,i):
        if i==1:
            name = "empoi.xlsx"
        if i==2:
            name = self.win.list_session_3.currentText()+".xlsx"
        if i==3:
            name = self.win.list_player_3.currentText()+".xlsx"
        filename, filter= QFileDialog.getSaveFileName(self.win,'Save shedule', name, "Excel (*.xlsx);;All Files (*)")#, options=QFileDialog.DontUseNativeDialog
        #print("le nom du fichier est ; ",filename)
        if not filename:
            return ""
        return filename

    def exportToExcel(self, table, file, listDf):
        columnHeaders = []
        rowHeaders = []

        # create column header list
        for j in range(table.model().columnCount()):
            columnHeaders.append(table.horizontalHeaderItem(j).text())

        for j in range(table.model().rowCount()):
            rowHeaders.append(table.verticalHeaderItem(j).text())

        #print("index:",rowHeaders)
        df = pd.DataFrame(listDf, index=rowHeaders, columns=columnHeaders)

        # # create dataframe object recordset
        # for row in range(table.rowCount()):
        #     for col in range(table.columnCount()):
        #         if table.item(row, col) != None:
        #             df.at[row, columnHeaders[col]] = table.item(row, col).text()

        df.to_excel(file, index=True)
        #print('Excel file exported')

    def saveEmploi(self):
        file = self.getfiles(1)
        if file !='' and  file.find('.xlsx')!=-1:
            self.exportToExcel(self.win.emploi,file,self.df)
        elif file == '':
            self.popupSession.showMsgPopUp(1,"You must choose a file")
        else:
            self.popupSession.showMsgPopUp(1,"{} is not in a regular form, you file must end with {}.xlsx".format(file))

