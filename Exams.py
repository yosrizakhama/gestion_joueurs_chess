# .....................
#! /usr/bin/python
#­*­coding: utf­8 ­*­
#from appwindow import *

from myAppWindow7 import *
# .....................
#from addPlayer import remplirListJoueur as fn
import sys
import os
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPushButton, QMessageBox
from TableModel import *

#from myql1 import *
from sqllite import *
import xlrd
from os import path as os_path

from messageBox import *

class Exams:
    def __init__(self, db, window, pl):
        self.win = window
        self.db = db
        self.pl = pl
        self.listE = self.db.selectAllExams()
        self.indexExam = -1
        self.indexNoteExam = -1
        self.indexPlayerExam = -1
        self.indexSowExam = -1
        self.listP = self.db.selectAllPlayer()
        self.updateListExam()
        self.table = TableWidget(self.win.tab_exams)
        self.win.tab_exams.addWidget(self.table)
        self.listView = self.win.titleExams
        self.df = []
        #self.listView.currentIndexChanged.connect(lambda:self.afficher_crosstable(self.listView.currentIndex()))
        #self.listView.activated[str].connect(lambda:self.afficher_crosstable(self.listView.currentIndex()))
        #--------
        #self.win.listExam.currentIndexChanged.connect(lambda:self.changeIndexExam(self.win.listExam.currentIndex()))
        self.win.examExams.currentIndexChanged.connect(lambda:self.changeIndexNoteExam(self.win.examExams.currentIndex()))
        self.win.titleExams.currentIndexChanged.connect(lambda:self.changeIndexShowExam(self.win.titleExams.currentIndex()))
        self.win.playerExams.currentIndexChanged.connect(lambda:self.changeIndexPlayerExam(self.win.playerExams.currentIndex()))
        self.win.listExam.currentIndexChanged.connect(lambda:self.changeIndexListExam())

        #--------
        
        self.win.examExams.activated[str].connect(lambda:self.changeIndexNoteExam(self.win.examExams.currentIndex()))
        self.win.titleExams.activated[str].connect(lambda:self.changeIndexShowExam(self.win.titleExams.currentIndex()))
        self.win.playerExams.activated[str].connect(lambda:self.changeIndexPlayerExam(self.win.playerExams.currentIndex()))
        self.win.typeTest.activated[str].connect(lambda:self.nameExam())
        self.win.comboBox_4.activated[str].connect(lambda:self.nameExam())

        
        #--------        
        self.win.addNewExam.clicked.connect(lambda:self.addExam(1))
        self.win.updateExam.clicked.connect(lambda:self.addExam(2))
        self.win.deleteExam.clicked.connect(lambda:self.addExam(3))
        self.win.seeInfos.clicked.connect(lambda:self.addPlayerExam(3))
        self.win.pushButton_2.clicked.connect(lambda:self.saveExam())
        

        self.win.addScoreExam.clicked.connect(lambda:self.addPlayerExam(1))
        self.win.updateScoreExam.clicked.connect(lambda:self.addPlayerExam(2))

        self.win.notPassedBtn.clicked.connect(lambda:self.showPlayerExam(2))
        self.win.passBtn.clicked.connect(lambda:self.showPlayerExam(1))
        #self.db.deleteAllExams()
        self.updateListExam()
        #print(self.listI)

        self.popupNote = MessagePopUp("Update note for a player","do you really want to update note for this player", 2, 1)
        self.popupExam = MessagePopUp("Update exam informations","do you really want to update informations for this exam", 2, 1)

    def changeIndexListExam(self):
        res = self.db.selectExam(self.listE[self.win.listExam.currentIndex()][0])
        #print(res)
        dt = res[2][8:] + '/'+ res[2][5:7] + '/' + res[2][0:4]
        #print('date : ', dt)
        dayExam = datetime.strptime(dt, '%d/%m/%Y').date()
        #print("date v :",dayExam)
        dt = QDateTime(dayExam.year, dayExam.month, dayExam.day, 21, 30)
        self.win.dateExams.setDateTime(dt)
        self.win.nameExam.setText(res[1])

    def nameExam(self):
        ch =self.win.typeTest.currentText()+"_"+self.win.comboBox_4.currentText()
        res = self.db.selectCountExHW(ch)
        self.win.nameExam.setText(ch+"_"+str(res))

    def changeIndexExam(self,i):
        self.indexExam = i
        #print("indexExam:",self.indexExam )
    def changeIndexNoteExam(self,i):
        self.indexNoteExam = i
        #print("indexNoteExam:",self.indexNoteExam )
    def changeIndexPlayerExam(self,i):
        self.indexPlayerExam = i
        self.win.indexPlayer = i
        self.win.actualiserPointeurListe()

        #print("indexPlayerExam :",self.indexPlayerExam )
    def changeIndexShowExam(self,i):
        self.indexSowExam = i
        #print("indexShowExam :",self.indexSowExam ) 

    def showPlayerExam(self, fn):
        if fn==1:
            self.afficher_crosstable(self.indexSowExam,-1)
            #print("List of players passed the exam")
        elif fn==2:
            self.afficher_crosstable(self.indexSowExam,-8888)
            #print("List of players not passed the exam")
    def addExam(self,fn):
        data=[]
        data.append(self.win.nameExam.text())
        today = self.win.dateExams.date().toString('dd/MM/yyyy')
        dayExam = datetime.strptime(today, '%d/%m/%Y').date()
        data.append(dayExam)
        if fn == 1:
            if data[0]=="":
                self.popupNote.showMsgPopUp(1, "You must put a name for the exam")
                return
            self.db.insertExam(data)
            self.popupNote.showMsgPopUp(1, "Data Added OK")
        elif fn == 2:
            if self.listE != []:
                res = self.db.selectExam(self.listE[self.win.listExam.currentIndex()][0])
                if self.win.nameExam.text()=='':
                    #print("You can't update choose Exam first")
                    self.popupExam.showMsgPopUp(1,"You can't update choose Exam first")

                else :
                    data1 = [res[0]] + data
                    if data1[1] == '':
                        self.popupExam.showMsgPopUp(1, "Sorry, you must put a new title for the exam "+ self.listE[self.indexExam][1] + "exam")    
                    else:
                        result = self.popupExam.showMsgPopUp(2, "do you really want to update informations for "+ res[1] + "exam")
                        #print("button : ",result)
                        if result == QMessageBox.Yes:
                            self.db.updateExam(data1)
                            self.popupNote.showMsgPopUp(1, "Data updated OK")
                            self.indexExam = -1
            else:
                self.popupExam.showMsgPopUp(1,"No Exam to update")
        else :
            if self.win.listExam.currentText() == "":
                self.popupExam.showMsgPopUp(1, "Sorry any exam to delete, you must choose an exam")    
                #print("You can't delete choose Exam first")
            else:
                id = self.listE[self.win.listExam.currentIndex()][0]
                result = self.popupExam.showMsgPopUp(2, "do you really want to delete this exam : "+ self.win.listExam.currentText() )
                #print("button : ",result)
                if result == QMessageBox.Yes:
                    self.db.deleteExam(id)
                    self.indexExam = -1
        self.updateListExam()
        #print('Add/update Exam is pressed ')

    def addPlayerExam(self,fn):

        if self.indexPlayerExam == -1:
            self.popupNote.showMsgPopUp(1, "You must choose a player")
            return 0
        if self.indexNoteExam == -1:
            self.popupNote.showMsgPopUp(1, "You must choose an exam")
            return 0
       
        data = []
        self.listP = self.db.selectAllPlayer()
        data.append(self.listP[self.indexPlayerExam][0])
        data.append(self.listE[self.indexNoteExam][0])
        if self.win.scoreAdd.text() == '':
            data.append(-8888)
        else:
            data.append(self.win.scoreAdd.text())
        #exDay = self.win.dateExams_2.date()
        today = self.win.dateExams_2.date().toString('dd/MM/yyyy')
        dayExam = datetime.strptime(today, '%d/%m/%Y').date()
        dt = QDateTime(dayExam.year, dayExam.month, dayExam.day, 21, 30)
        data.append(dayExam)
        
        if fn == 1:
            if not self.win.scoreAdd.text().isnumeric() and self.win.scoreAdd.text()!='':
                self.popupNote.showMsgPopUp(1, "Score must be a number or an empty value")
                return 0
        
            if self.win.scoreAdd.text()!='':
                if int(self.win.scoreAdd.text())<0 or int(self.win.scoreAdd.text())>100:
                    self.popupNote.showMsgPopUp(1, "Score must be a number beetween 0 and 100")
                    return 0

            res = self.db.selectExamsPlayer(data[0],data[1])
            if not res == []:
                self.popupNote.showMsgPopUp(1, "Player {} is sheduled to the exam {}".format(self.listP[self.indexPlayerExam][1], self.listE[self.indexNoteExam][1]))
                return 0
            ex = self.listE[self.indexNoteExam][1]
            level = "L" + str(self.listP[self.indexPlayerExam][-3])
            #print("exam : ",ex," level : ", level)
            if ex.find(level)!=-1:
                if self.db.selectExamsPlayerDate(data[0],data[3])==[]:
                    self.db.insertExamPlayer(data)
                    #self.popupNote.showMsgPopUp(1, "Data Added OK")
                    res = self.addScore(1)
                    if res == -1:
                        self.popupNote.showMsgPopUp(1, "Please change date of this exam because there is another exam for this player in this date")
                    else:
                        self.popupNote.showMsgPopUp(1, "Data Added OK")
                else:
                    self.popupNote.showMsgPopUp(1, "Please change date of this exam because there is another exam for this player in this date")
                    return 0
            else:
                self.popupNote.showMsgPopUp(1, "This player  {} can't pass this exam {} because its not the same level".format(self.listP[self.indexPlayerExam][1], self.listE[self.indexNoteExam][1]))
                return 0

            #print('Exam added to player ok')
        else :
            res = self.db.selectExamsPlayer(data[0],data[1])
            if res == []:
                self.popupNote.showMsgPopUp(1, "this player {} is not scheduled to take this exam {}".format(self.listP[self.indexPlayerExam][1], self.listE[self.indexNoteExam][1]))
                return 0
            if fn==3:
                self.win.scoreAdd.setText(str(res[0][2]))
            #print((res[0]))
                date = res[0][3].split('-')
            #print(date)
                self.win.dateExams_2.setDateTime(datetime(int(date[0]), int(date[1]), int(date[2])))
            if fn == 2:
                if not data[2].isnumeric() and data[2]!='':
                    self.popupNote.showMsgPopUp(1, "Score must be a number or an empty value")
                    return 0
                if self.win.scoreAdd.text()!='':
                    if int(self.win.scoreAdd.text())<0 or int(self.win.scoreAdd.text())>100:
                        self.popupNote.showMsgPopUp(1, "Score must be a number beetween 0 and 100")
                        return 0
                self.win.scoreAdd.setText(data[2])
                self.win.dateExams_2.setDateTime(dt)
                self.db.updateExamPlayer(data)
                #self.popupNote.showMsgPopUp(1, "Data updated OK")
                
                

                res = self.addScore(2)
                if res == -1:
                    self.popupNote.showMsgPopUp(1, "Please change date of this exam because there is another exam for this player in this date")
                else:
                    self.popupNote.showMsgPopUp(1, "Data updated")
                #print('Exam updated to player ok')
                
            
               
    def addScore(self,fn):
        id = self.listP[self.win.playerExams.currentIndex()][0]
        l = self.listP[self.win.playerExams.currentIndex()][-3]
        nameEv = self.win.examExams.currentText()
        r = 2 if nameEv.find("EXAM")==-1 else 1
        today = self.win.dateExams_2.date().toString('dd/MM/yyyy')
        day = datetime.strptime(today, '%d/%m/%Y').date()
        score = 0 if self.win.scoreAdd.text()=='' or self.win.scoreAdd.text()=='-8888' else  int(self.win.scoreAdd.text())
        res = self.db.selectScore(id,day,r)
        if res!=None and fn==1:
            return -1   
        #print("(id,date,r,score):({},{},{},{})".format(id,day,r,score))
        res1 = self.db.selectScoreType(id,r,l)
        #print("(id,r,l):({},{},{})".format(id,r,l))
        #print("liste des score :",res1)
        self.db.selectAllScore()
        lenR = 0
        if res1!=[]:
            ancienSc = res1[-1][3]
            lenR = len(res1)
        else:
            ancienSc = 0
            lenR = 0
            
        newSc = (ancienSc * lenR + score) // (lenR + 1)
        

        if res==None:    
            #print("(ancien score, nouveau score):({}, {}".format(ancienSc,newSc))
            self.db.insertScorePLayer([id,day,l,newSc,r])    
        else:
             newSc = (ancienSc * (lenR-1) + score) // lenR
             #print("(ancien score, nouveau score):({}, {}".format(ancienSc,newSc))
             self.db.updateScorePlayer(id,newSc,day,r)

        scorePl = self.listP[self.win.playerExams.currentIndex()][-7]-ancienSc+newSc    

        self.db.updateplayerscore([id,scorePl])
        res = self.db.selectScore(id,day,5)
        if res == None:
            self.db.insertScorePLayer([id,day,l,scorePl,5]) 
        else:
            self.db.updateScorePlayer(id,scorePl,day,5)
        #self.pl.remplirListJoueur()
        return 1
    def updateScore(self):
        pass

    def afficher_crosstable(self,index,score):
        self.indexSowExam = index 
        #print(index)
        if(self.win.titleExams.count()==0):
            return 0

        result = self.db.selectExamCross(self.listE[self.indexSowExam][0],score)
        self.df = result
        ligne=[]
        for i,elt in enumerate(result):
            ligne.append("Player N°: "+str(i+1))
        self.table.refresh(result,['Name','Score','Sheduled day'],ligne)   

#---------------
    def getfiles(self):
        name = self.win.titleExams.currentText()+".xlsx"
        filename, filter= QFileDialog.getSaveFileName(self.win,'Save crosstable', name, "Excel (*.xlsx);;All Files (*)")#, options=QFileDialog.DontUseNativeDialog
        #print("le nom du fichier est ; ",filename)
        if not filename:
            return ""
        return filename

    def exportExemToExcel(self, file, listDf):
        columnHeaders = ['Name','Score','Sheduled day'] 
        df = pd.DataFrame(listDf, columns=columnHeaders)
        df.to_excel(file, index=True)
        #print('Excel file exported')
        
    def saveExam(self):
        file = self.getfiles()
        if file !='' and  file.find('.xlsx')!=-1:
            self.exportExemToExcel(file,self.df)
        elif file == '':
            self.popupNote.showMsgPopUp(1,"You must choose a file")
        else:
            self.popupNote.showMsgPopUp(1,"{} is not in a regular form, you file must end with {}.xlsx".format(file))
#---------------

    def updateListeIndex(self):
        self.listI = []
        for elt in self.listE:
            self.listI.append(elt[0])
        #print(self.listE)
        

    def updateListExam(self):
        self.win.listExam.clear()
        self.win.examExams.clear()
        self.win.titleExams.clear()
        self.listE = self.db.selectAllExams()
        self.updateListeIndex()
        ##print(self.listP)
        
        for i,elt in enumerate(self.listE):
            
            self.win.listExam.addItem(elt[1])#str(i+1)+':'+
            self.win.examExams.addItem(elt[1])#str(i+1)+':'+
            self.win.titleExams.addItem(elt[1])
        