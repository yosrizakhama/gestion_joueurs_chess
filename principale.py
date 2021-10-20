# .....................
#! /usr/bin/python
#­*­coding: utf­8 ­*­
#from appwindow import *
from matplotlib import colors
from matplotlib.colors import Colormap
from myAppWindow7 import *
# .....................


from datetime import datetime, date
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from openpyxl import *
#from myql1 import *
from sqllite import *
import xlrd
from os import path as os_path
from pylab import *
from PyQt5.QtCore import Qt
# ...........................
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import random
from addPlayer import *
from emploi import *
from Exams import *
from eventForm import *
from showScore import *
from controlAccess import *
from payment import *

base = "joueurbica"
#PATH = os_path.abspath(os_path.split(__file__)[0])
#excel_f = PATH+"\joueursdonnees.xls"
global mabase

class Appwindow(QWidget,Ui_Form):
    def __init__(self, parent=None):
        
        #QWidget.__init__(self)
        super(Appwindow, self).__init__(parent)
        self.setupUi(parent)
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.indexPlayer = 0
        self.indexSession = 0
        self.indexPresence = 0
        #............
        drawLayout = QVBoxLayout()
        drawLayout.setGeometry(QRect(200, 200, 300, 300))
        
        #............
        self.figurec = plt.figure()
        self.canvasc = FigureCanvas(self.figurec)
        self.canvasc.setGeometry(QRect(200, 200, 300, 300))
        #self.toolbarc = NavigationToolbar(self.canvasc, self)
        
        #drawLayout.addWidget(self.toolbarc)
        drawLayout.addWidget(self.canvasc)

        self.figurer = plt.figure()
        self.canvasr = FigureCanvas(self.figurer)
        #self.toolbarr = NavigationToolbar(self.canvasr, self)
        
        #drawLayout.addWidget(self.toolbarr)
        #drawLayout.addWidget(self.canvasr)
        
        #drawLayout.maximumSize(QSize(700,400))
        

        #......................
        #............
        
        
        #............
        self.figureb = plt.figure()
        self.canvasb = FigureCanvas(self.figureb)
        #self.toolbarb = NavigationToolbar(self.canvasb, self)
        
        #drawLayout.addWidget(self.toolbarb)
        #drawLayout.addWidget(self.canvasb)

        self.figuren = plt.figure()
        self.canvasn = FigureCanvas(self.figuren)
        
        #self.toolbarn = NavigationToolbar(self.canvasn, self)
        
        #drawLayout.addWidget(self.toolbarn)
        #drawLayout.addWidget(self.canvasn)
        drawLayout.setGeometry(QRect(1,1,700,500))
        #drawLayout.maximumSize(QSize(700,400))
        
        drawLayout.setGeometry(QRect(0,0,800,200))
        self.verticalLayout_4.addLayout(drawLayout)
        self.verticalLayout_4.setGeometry(QRect(0,0,800,200))
        #self.verticalLayout_4.addLayout(drawLayout)
        #......................

        #self.horizontalLayout_2.addWidget(self.toolbar)
        #self.horizontalLayout_2.addWidget(self.canvas)
        self.saveg.clicked.connect(self.saveGraph)
        #Êself.test = MessagePopUp("Update user informations","do you really want to update informations for this exam", 2, 1)

    def closeAndReturn(self):
        self.close()
        self.parent().show()
        
    def initUI(self):
        self.setWindowTitle('BICA Players')
        
        file ="fide.png"
        
         # Add paint widget and paint
        # self.m = PaintWidget(self)
        # self.m.move(0,0)
        # self.m.resize(1000,800)
        #self.setWindowIcon(QtGui.QIcon(file))
        #print("this is a file : ",file)
        self.label_4.setPixmap(QtGui.QPixmap(file))
        #self.show()
        
    
    def actualiserPointeurListe(self):
        global mabase
        lp=listPalyers(mabase)
        if lp !=[]:
            self.comboBox.setCurrentIndex(self.indexPlayer)
            self.player_liste_update.setCurrentIndex(self.indexPlayer)
            self.playerExams.setCurrentIndex(self.indexPlayer)
            self.titleExams_2.setCurrentIndex(self.indexPlayer)
            self.playerTournament.setCurrentIndex(self.indexPlayer)
            self.list_player.setCurrentIndex(self.indexPlayer)
            self.list_player_2.setCurrentIndex(self.indexPlayer)
            self.list_player_3.setCurrentIndex(self.indexPlayer)
            self.listplayerScore.setCurrentIndex(self.indexPlayer)
            self.playerScore.setCurrentIndex(self.indexPlayer)
            self.playerPayment.setCurrentIndex(self.indexPlayer)
            self.playerVIP.setCurrentIndex(self.indexPlayer)
            self.levelShow.setCurrentText(str(lp[self.indexPlayer][-3]))
        
    
    def plot(self,ratings):

        ratings = ratings[::-1]
        #print('teste reverse',ratings)
        
        datac =[el[1] for el in ratings]
        time =[el[-1][2:-3] for i,el in enumerate(ratings)]
        #print(time)
        # clearing old figure
        self.figurec.clear()
        # create an axis
        ax = self.figurec.add_subplot(111)
        
        # plot data
        axes = self.figurec.gca()

        datar =[el[2] for el in ratings]
        # clearing old figure
        self.figurer.clear()

        datab =[el[3] for el in ratings]
       
        datan =[el[4] for el in ratings]
        
        self.figuren.clear()
        
       
        
        x = array([1, 3, 4, 6])
        y = array(time)
        ax.plot(time, datac, "o-", color = 'yellow')
        ax.plot(time,datar, "o-", color = 'purple')
        ax.plot(time,datab, "o-", color = 'green')
        ax.plot(time,datan, "o-", color = 'red')
        for label in ax.xaxis.get_ticklabels():
            label.set_color('blue')
            label.set_rotation(15)
            label.set_fontsize(8)
        ax.legend(["Classic","Rapid","Blitz","National"], loc ="lower left")
        self.canvasc.draw()


    def getfiles(self,name):
            
        filename, filter= QFileDialog.getSaveFileName(self,'Save Graph', name, "Image (*.jpg);;All Files (*)")#, options=QFileDialog.DontUseNativeDialog
        #print("le nom du fichier est ; ",filename)
        if not filename:
            return ""
        return filename

    def exportDataToExcel(self, file):
        
        
        self.figuren.savefig(file)
        self.figureb.savefig(file)
        self.figurec.savefig(file)
        
        #print('Excel file exported')
        
    def saveGraph(self):
        name = self.comboBox.currentText()+'.jpg'
        file = self.getfiles(name)
        
        self.exportDataToExcel(file)
        
            
#---------------

        



def open_excel():
    #print("opening ...")
    excel_f = "joueursdonnees.xls"
    try:
        myBook = xlrd.open_workbook(excel_f)
        mySheet = myBook.sheet_by_index(0)
        #print(mySheet.name)
        #print("file opened OK")
        #print(mySheet.row(0)[0])
        #print(mySheet.cell_value(0, 0)) # #OK
        return mySheet
    except  :
        #print("e")
        return None

def formatData(feuille,i):
    data = []
    
    for j,elt in enumerate(feuille.row(i)):
        #if(j not in (8,10,11,12,13)):
        data.append(feuille.cell_value(i,j))
    #print(data[6])
    
    data[6] = datetime.strptime(data[6], '%d/%m/%Y').date()
    #print(data)        
    return data

def update_players(mabase,feuille,currentdate):
    mabase.deleteAllData()
    for i in range(1,feuille.nrows):
        if feuille.cell_value(i, 0)!="":
            id = int(feuille.cell_value(i, 0))
            result = mabase.selectPlayer(id)
            if result == None:
                mabase.insertPlayer(formatData(feuille, i))
            else:
                mabase.updateplayer(formatData(feuille, i))
            #currentdate=datetime.strptime("17/07/2021", '%d/%m/%Y').date()
            result = mabase.selectElo(id,currentdate)
            data=[]
            data.append(feuille.cell_value(i,0))
            data.append(int(feuille.cell_value(i,10)))
            data.append(int(feuille.cell_value(i,11)))
            data.append(int(feuille.cell_value(i,12)))
            data.append(int(feuille.cell_value(i,8)))
            data.append(currentdate)
            if result == None:
                mabase.insertElo(data)
            else:
                mabase.updateElo(data)

        #print(result)
        #print(id,result)
def listPalyers(mabase):
    result = mabase.selectAllPlayer()
    
    return result   




def dataAddAll(db):
    today = date.today()
   
    # db.deleteAllTable()
    # db.createAllTable()
    feuille = open_excel()
    listeP = listPalyers(db)
    # for i in range(len(listeP)):
    #     mabase.deletePlayer(i+1)
    update_players(db,feuille,today)

def remplirListJoueur(app,db):
    listeP = listPalyers(db)
    app.comboBox.clear()
    app.player_liste_update.clear()
    for i,elt in enumerate(listeP):
        
        app.comboBox.addItem(str(i+1)+':'+elt[1])
        app.player_liste_update.addItem(str(i+1)+':'+elt[1])
        
    #print(listeP)
    return (listeP)

class Principale:
    def __init__(self, base,args,view,parent):
        self.mabase = base
        global mabase
        mabase = base
        #a=QApplication(args)

        f=QWidget()
        self.f =f
        c=Appwindow(f)
        
        self.c=c
        file = "slogan.png"
        #print("You are welcome, BICA PLAYERS is an application developped by Zakhama Yosri (zakhyos@gmail.com) from Tunisia since 2021")
        self.parent=parent
        #feuille = open_excel()
        # listeP = listPalyers(mabase)
        # for i in range(len(listeP)):
        #     mabase.deletePlayer(i+1)
        #today =date.today()
        #update_players(mabase,feuille,today)
        #dataAddAll(mabase)
        listeP = remplirListJoueur(c,self.mabase)
        #c.comboBox.activated[str].connect(lambda:onChanged(c,listeP,mabase)) 
        #c.player_liste_update.activated[str].connect(lambda:onChanged_updade(c,listeP,mabase))
        #mabase.deleteTable('TOURNAMENT')
        #mabase.createExamsPlayerTable()
        pl = AddPlayer(self.mabase,c,listeP) 
        Exams(self.mabase, c, pl)
        Emploi(self.mabase, c,pl)
        Event(self.mabase, c)
        ControlAccess(self.mabase,c,view,self.parent)
        graph = ShowScore(self.mabase,c,pl)
        payment = Payment(self.mabase,c,pl)
        # mabase.delAllTables()
        # mabase.createAllTable()
        # update_players(mabase,feuille,today)
        f.setAutoFillBackground(True)
        p = f.palette()
        p.setColor(f.backgroundRole(),QColor(180, 180, 255))
        f.setPalette(p)
        self.f=f
        
        
        #f.show()
        
       
        
       

