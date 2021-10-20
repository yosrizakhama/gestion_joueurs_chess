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

#from myql1 import *
from sqllite import *
import xlrd
from os import name, path as os_path

from messageBox import *

class Event:
    def __init__(self, db, window):
        self.win = window
        self.db = db
       
        self.listP = self.db.selectAllPlayer()
        self.listEv = self.db.selectAllEvents()
        self.win.addEvent.clicked.connect(lambda:self.addEvent(1))
        self.win.updateEvent.clicked.connect(lambda:self.addEvent(2))
        self.win.deleteEvent.clicked.connect(lambda:self.addEvent(3))
        self.win.listEventDelete.activated[str].connect(lambda:self.ch_name())
        self.popupEvent = MessagePopUp("Update events","do you really want to update event ", 2, 1)
        self.popupRankEvent = MessagePopUp("Update result player","do you really want to update result player for this tournament", 2, 1)
        self.win.addResultTournament.clicked.connect(lambda:self.addEventPlayer(1))
        self.win.seeInfosTournament.clicked.connect(lambda:self.addEventPlayer(2))
        self.win.updateRankTournament.clicked.connect(lambda:self.addEventPlayer(3))
        self.win.search.clicked.connect(lambda:self.showFicheEventPlayer())
        self.win.save.clicked.connect(lambda:self.saveEvents())
        self.win.playerTournament.activated[str].connect(lambda:self.changeIndex(self.win.playerTournament))
        self.win.titleExams_2.activated[str].connect(lambda:self.changeIndex(self.win.titleExams_2))
        
        self.df = []
        self.remplirList()

    def changeIndex(self,list):
        self.win.indexPlayer = list.currentIndex()
        self.win.actualiserPointeurListe()

    def exportEventsToExcel(self, file, listDf):
        
        columnHeaders = ["Title", "Classification", "Type", "Date", "Rank", "Points"]
        
        df = pd.DataFrame(listDf, columns=columnHeaders)
        df.to_excel(file, index=True)
        #print('Excel file exported')
        
    def saveEvents(self):
        file = self.getfiles()
        if file !='' and  file.find('.xlsx')!=-1:
            self.exportEventsToExcel(file,self.df)
        elif file == '':
            self.popupEvent.showMsgPopUp(1,"You must choose a file")
        else:
            self.popupEvent.showMsgPopUp(1,"{} is not in a regular form, you file must end with {}.xlsx".format(file))

    def getfiles(self):
        name = self.win.titleExams_2.currentText()+".xlsx"
        filename, filter= QFileDialog.getSaveFileName(self.win,'Save shedule', name, "Excel (*.xlsx);;All Files (*)")#, options=QFileDialog.DontUseNativeDialog
        #print("le nom du fichier est ; ",filename)
        if not filename:
            return ""
        return filename


    def showFicheEventPlayer(self):
        if self.listP != []:
            today = self.win.dateEvent_2.date().toString('dd/MM/yyyy')
            day1 = datetime.strptime(today, '%d/%m/%Y').date()
            today = self.win.dateEvent_3.date().toString('dd/MM/yyyy')
            day2 = datetime.strptime(today, '%d/%m/%Y').date()
            id = self.listP[self.win.titleExams_2.currentIndex()][0]
            data = [id, day1, day2]
            self.win.tableEvent.clear()
            self.win.tableEvent.setHorizontalHeaderLabels(["Title", "Classification", "Type", "Date", "Rank", "Points"])
            data2 = self.db.selectEventsPlayer(data)
            res =[]
            
            for li, elt in enumerate(data2):
                
                #print('name : ', elt)
                rowPosition = self.win.tableEvent.rowCount()
                
                if rowPosition<li+1:
                    self.win.tableEvent.insertRow(rowPosition)
                for j,c in enumerate(elt):
                    #print("element ",li,":",j," is ",c)
                    if j!=5:
                        self.win.tableEvent.setItem(li, j, QTableWidgetItem(str(c)))
                    else:
                        self.win.tableEvent.setItem(li, j, QTableWidgetItem(str(c/10)))
                res.append(elt)
            self.df = res   

    def calculeScore(self, rank):
        listeScore = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50,45,40,35,30,25,20,15,0]
        if rank >= 19:
            return listeScore[18]
        return listeScore[rank - 1]  
        
    def updateScore(self, id, date, level, raison, rank):
        score = self.calculeScore(rank)
        ancienScore = 0
        count = 0
        newScore = 0
        res = self.db.selectScore(id,date,raison)
        resLevel = self.db.selectScoreType(id,raison,level)
        count = 1 if len(resLevel) == 0 else len(resLevel)
        ancienScore = 0 if len(resLevel) == 0 else resLevel[-1][-2]

        if res == None:
            newScore = (ancienScore * count + score)//(count + 1)
            self.db.insertScorePLayer([id,date,level,newScore,raison])
            
        else:
            newScore = (ancienScore * (count-1) + score)//count
            self.db.updateScorePlayer(id,newScore,date,raison)
        
        scorePl = self.listP[self.win.playerTournament.currentIndex()][-7]-ancienScore+newScore    
        self.db.updateplayerscore([id,scorePl])
        if res == None:
            self.db.insertScorePLayer([id,date,level,scorePl,5]) 
        else:
            self.db.updateScorePlayer(id,scorePl,date,5)

    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def addEventPlayer(self, fn):
        if self.win.playerTournament.currentText()=="":
            self.popupEvent.showMsgPopUp(1,"Any player in DB")  
            return
        if self.win.listEvent.currentText()=="":
            self.popupEvent.showMsgPopUp(1,"Any event in DB")  
            return
        if self.win.rank.text()=="" and fn!=2:
            self.popupEvent.showMsgPopUp(1,"You must put rank")  
            return
        if not self.win.rank.text().isnumeric()and fn!=2:
            self.popupEvent.showMsgPopUp(1,"Rank must be a numeric value")  
            return
        if (not self.win.points.text().isnumeric() and not self.isfloat(self.win.points.text()))and fn!=2:
            self.popupEvent.showMsgPopUp(1,"Points must be a numeric value")  
            return
        self.listP = self.db.selectAllPlayer()
        idpl = self.listP[self.win.playerTournament.currentIndex()][0]
        idev = self.listEv[self.win.listEvent.currentIndex()][0]
        if fn!=2 :
            r = int(self.win.rank.text())
            p = float(self.win.points.text())*10
        res = self.db.selectEventPlayer(idpl,idev)
        if fn == 1:
            if res == None:
                self.db.insertEventPLayer([idpl, idev, r, p])
                self.updateScore(idpl,self.listEv[self.win.listEvent.currentIndex()][-1],self.listP[self.win.playerTournament.currentIndex()][-3],4,r)
                self.popupEvent.showMsgPopUp(1,"Data added OK")
                return
            else:
                self.popupEvent.showMsgPopUp(1,"You can't add for another time this tournament for this player")
                return
        elif fn==3:
            if res == None:
                self.popupEvent.showMsgPopUp(1,"This event is not yet played by thi player")
                return
            else:
                self.db.updateEventPlayer([idpl, idev, r, p])
                self.updateScore(idpl,self.listEv[self.win.listEvent.currentIndex()][-1],self.listP[self.win.playerTournament.currentIndex()][-3],4,r)

                self.popupEvent.showMsgPopUp(1,"Data updated OK")
                return
        elif fn==2:
            if res == None:
                self.popupEvent.showMsgPopUp(1,"This event is not yet played by thi player")
                return
            else:
                
                self.win.rank.setText(str(res[2]))  
                self.win.points.setText(str(res[3]/10))  
                return
        self.remplirList()

    def ch_name(self):
        name = self.win.listEventDelete.currentText()
        res = self.db.selectEvent(name)
        self.win.nameEvent.setText(res[1])
        self.win.classEvent.setCurrentText(res[2])
        self.win.typeEvent.setCurrentText(res[3])
        dt = res[4][8:] + '/'+ res[4][5:7] + '/' + res[4][0:4]
        #print('date : ', dt)
        dayExam = datetime.strptime(dt, '%d/%m/%Y').date()
        #print("date v :",dayExam)
        dt = QDateTime(dayExam.year, dayExam.month, dayExam.day, 21, 30)
        self.win.dateEvent.setDateTime(dt)
        
        
    def remplirList(self):
        self.listEv = self.db.selectAllEvents()
        self.win.listEvent.clear()
        self.win.listEventDelete.clear()
        for elt in self.listEv:
            self.win.listEvent.addItem(elt[1])
            self.win.listEventDelete.addItem(elt[1])

    def addEvent(self, fn):
        if fn == 3 and self.win.listEventDelete.count()==0:
            self.popupEvent.showMsgPopUp(1,"Any event to delete")  
            return  
        if self.win.nameEvent.text() == "":
            self.popupEvent.showMsgPopUp(1,"You must add a name for event")
            return
        name = self.win.nameEvent.text()
        res = self.db.selectEvent(name)
        if res != None and fn==1:
            self.popupEvent.showMsgPopUp(1," You can't add this event {} because it's in list of events".format(name)) 
            return
        res = self.db.selectEvent(self.win.listEventDelete.currentText())
        if res == None and fn==2:
            self.popupEvent.showMsgPopUp(1," You can't update this event {} because it's not yet in list of events".format(name)) 
            return
        classif = self.win.classEvent.currentText()
        typeev = self.win.typeEvent.currentText()
        today = self.win.dateEvent.date().toString('dd/MM/yyyy')
        dayEv = datetime.strptime(today, '%d/%m/%Y').date()
        idev = self.db.selectNextId("TOURNAMENT")
        data = [idev, name, classif, typeev, dayEv]
        if fn == 1:
            self.db.insertEvent(data)
            self.popupEvent.showMsgPopUp(1," Event Added OK")
        elif fn==2:
            data[0] = res[0]
            
            rep = self.popupEvent.showMsgPopUp(2,"Do you really want to update this event for : {}".format(data[1]))    
            if rep == QMessageBox.Yes:
                self.db.updateEvent(data)
                self.popupEvent.showMsgPopUp(1,"Event updated")
        else:
            self.win.nameEvent.setText(self.win.listEventDelete.currentText())
            if self.win.listEventDelete.count() != 0:
                id = self.listEv[self.win.listEventDelete.currentIndex()][0]
            rep = self.popupEvent.showMsgPopUp(2,"Do you really want to delete this event for : {}".format(self.win.listEventDelete.currentText()))    
            if rep == QMessageBox.Yes:
                self.db.deleteEvent(id)
                self.popupEvent.showMsgPopUp(1,"Event deleted")
        self.remplirList()