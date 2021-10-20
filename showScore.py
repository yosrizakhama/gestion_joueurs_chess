# .....................
#! /usr/bin/python
#­*­coding: utf­8 ­*­
#from appwindow import *

from myAppWindow7 import *
from messageBox import *
# .....................
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QSizePolicy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTableWidgetItem
from TableModel import *
#from myql1 import *
from sqllite import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ShowScore:
    def __init__(self, db, window, pl):
        self.win = window
        self.db = db
        self.pl = pl
        self.listP = self.pl.listP
        self.dataEx = []
        self.dataHm = []
        self.dataPr = []
        self.dataEv = []
        self.dataAll = []
        self.dataRank = []
        self.popupNote = MessagePopUp("Add session","do you really want to add session course", 2, 1)
        #self.listP = self.db.selectAllPlayer()
        self.win.listplayerScore.activated[str].connect(lambda:self.changeIndex(1))
        self.win.playerScore.activated[str].connect(lambda:self.changeIndex(2))

        self.win.listplayerScore.currentIndexChanged.connect(lambda:self.showGraph())
        self.win.okRank.clicked.connect(lambda:self.rankPlayer())
        
        
        #self.win.saveScore.clicked.connect(lambda:self.showGraph())
        self.win.okShow.clicked.connect(lambda:self.showGraph())
        
        self.win.save_Presence.clicked.connect(lambda:self.saveExam(3,self.dataPr))
        self.win.save_exam.clicked.connect(lambda:self.saveExam(1,self.dataEx))
        self.win.save_homework.clicked.connect(lambda:self.saveExam(2,self.dataHm))
        self.win.save_event.clicked.connect(lambda:self.saveExam(4,self.dataEv))
        self.win.saveScore.clicked.connect(lambda:self.saveExam(5,self.dataAll))
        self.win.saveRank.clicked.connect(lambda:self.saveExam(6,self.dataRank))
        


        drawLayout = QVBoxLayout()
        self.figureExam = plt.figure()
        
        self.canvasExam = FigureCanvas(self.figureExam)
        drawLayout.addWidget(self.canvasExam)
        self.win.examGraph.addLayout(drawLayout)

        

        drawLayout = QVBoxLayout()
        self.figureHome = plt.figure()
        self.canvasHome = FigureCanvas(self.figureHome)
        drawLayout.addWidget(self.canvasHome)
        self.win.homeWork.addLayout(drawLayout)

        drawLayout = QVBoxLayout()
        self.figurePresence = plt.figure()
        self.canvasPresence = FigureCanvas(self.figurePresence)
        drawLayout.addWidget(self.canvasPresence)
        self.win.presenceGraph.addLayout(drawLayout)

        drawLayout = QVBoxLayout()
        self.figureEvents = plt.figure()
        self.canvasEvents = FigureCanvas(self.figureEvents)
        drawLayout.addWidget(self.canvasEvents)
        self.win.eventGraph.addLayout(drawLayout)

        drawLayout = QVBoxLayout()
        self.figureAll = plt.figure()
        self.canvasAll = FigureCanvas(self.figureAll)
        drawLayout.addWidget(self.canvasAll)
        
        self.win.graphScore.addLayout(drawLayout)

        self.showGraph()

    def rankPlayer(self):
        res =  self.db.selectPlayerLevelRank(int(self.win.levelRank.currentText()))
        self.dataRank =res
        for row in range(self.win.tabRank.rowCount()):
            self.win.listepresence.removeRow(row)
        #self.win.tabRank.clear()
        for row,elt in enumerate(res):
            rowPosition = self.win.tabRank.rowCount()
            if rowPosition<row+1:
                self.win.tabRank.insertRow(rowPosition)
            for i,cel in enumerate(elt):   
                self.win.tabRank.setItem(row,i,QTableWidgetItem(str(cel)))
                
        


    def changeIndex(self,i):
        if i == 1:
            self.win.indexPlayer = self.win.listplayerScore.currentIndex()
        if i == 2:
            self.win.indexPlayer = self.win.playerScore.currentIndex()
        self.win.actualiserPointeurListe()
        self.win.levelShow.setCurrentText(str(self.listP[self.win.indexPlayer][-3]))
        
        self.win.levelRank.setCurrentText(str(self.listP[self.win.indexPlayer][-3]))
        self.showGraph()

    def showGraph(self):
        level = int(self.win.levelShow.currentText())
        self.listP = self.pl.listP
        self.figureExam.clear()
        if self.listP !=[]:
            player = self.listP[self.win.listplayerScore.currentIndex()]
            data =self.db.selectScoreType(player[0],1,level) #player[-3]
            dataEx = [el[3] for el in data]
            time =[el[1][5:] for i,el in enumerate(data)]
            x_ax = self.figureExam.add_axes([0,0,1,1])
            
            ax = self.figureExam.add_subplot(111)
            #plt.xticks(rotation=45)
            
            ax.plot(time, dataEx, "o-", color = 'red')
            for label in ax.xaxis.get_ticklabels():
                label.set_color('red')
                label.set_rotation(25)
                label.set_fontsize(8)
            ax.legend(["Score for exams"], loc ="lower left")
            
            self.canvasExam.draw()
            self.dataEx = [[el[1],el[3]] for el in data]

            self.figureHome.clear()
            data =self.db.selectScoreType(player[0],2,level)#player[-3]
            dataEx = [el[3] for el in data]
            time =[el[1][5:] for i,el in enumerate(data)]
            ax = self.figureHome.add_subplot(111)
            ax.plot(time, dataEx, "o-", color = 'green')
            for label in ax.xaxis.get_ticklabels():
                label.set_color('green')
                label.set_rotation(25)
                label.set_fontsize(8)
            ax.legend(["Score for home work"], loc ="lower left")
            self.canvasHome.draw()
            self.dataHm = [[el[1],el[3]] for el in data]

            self.figurePresence.clear()
            data =self.db.selectScoreType(player[0],3,level)#player[-3]
            dataEx = [el[3] for el in data]
            time =[el[1][5:] for i,el in enumerate(data)]
            ax = self.figurePresence.add_subplot(111)
            ax.plot(time, dataEx, "o-", color = 'blue')
            for label in ax.xaxis.get_ticklabels():
                label.set_color('blue')
                label.set_rotation(25)
                label.set_fontsize(8)
            ax.legend(["Score for presence"], loc ="lower left")
            self.canvasPresence.draw()
            self.dataPr = [[el[1],el[3]] for el in data]

            self.figureEvents.clear()
            data =self.db.selectScoreType(player[0],4,level)#player[-3]
            dataEx = [el[3] for el in data]
            time =[el[1][5:] for i,el in enumerate(data)]
            ax = self.figureEvents.add_subplot(111)
            ax.plot(time, dataEx, "o-", color = 'magenta')
            for label in ax.xaxis.get_ticklabels():
                label.set_color('magenta')
                label.set_rotation(25)
                label.set_fontsize(8)
            ax.legend(["Score for events"], loc ="lower left")
            self.canvasEvents.draw()
            self.dataEv = [[el[1],el[3]] for el in data]

        #---------------
            self.figureAll.clear()
            data =self.db.selectScoreType(player[0],5,level)#player[-3]
            dataEx = [el[3] for el in data]
            time =[el[1] for i,el in enumerate(data)]
            ax = self.figureAll.add_subplot(111)
            ax.plot(time, dataEx, "-", color = 'red')
            for label in ax.xaxis.get_ticklabels():
                label.set_color('blue')
                label.set_rotation(45)
                label.set_fontsize(8)
            ax.legend(["Score"], loc ="lower left")
            #self.canvasAll.setSizeHint(QSizePolicy.Expanding)
            self.canvasAll.draw()
            self.dataAll = [[el[1],el[3]] for el in data]

    def getfiles(self,name):
        
        filename, filter= QFileDialog.getSaveFileName(self.win,'Save crosstable', name, "Excel (*.xlsx);;All Files (*)")#, options=QFileDialog.DontUseNativeDialog
        #print("le nom du fichier est ; ",filename)
        if not filename:
            return ""
        return filename

    def exportDataToExcel(self, file, listDf,type):
        graph = [self.figureExam, self.figureHome, self.figurePresence, self.figureEvents,self.figureAll]
        
        if type == 6:
            columnHeaders = ['Name','Level','Score','Category'] 
        else:
            columnHeaders = ['Day','Score'] 
            graph[type-1].savefig(file[:-4]+"jpg")
        df = pd.DataFrame(listDf, columns=columnHeaders)
        df.to_excel(file, index=True)
            #print('Excel file exported')
        
    def saveExam(self,type,data):
        if type == 6:
            name = "RankLevel"+self.win.levelRank.currentText()+'.xlsx'
        else:
            name = self.win.listplayerScore.currentText()+"_"+str(type)+"_Level_"+self.win.levelShow.currentText()+'.xlsx'
        file = self.getfiles(name)
        if file !='' and  file.find('.xlsx')!=-1:
            self.exportDataToExcel(file,data,type)
        elif file == '':
            self.popupNote.showMsgPopUp(1,"You must choose a file")
        else:
            self.popupNote.showMsgPopUp(1,"{} is not in a regular form, you file must end with {}.xlsx".format(file))
#---------------