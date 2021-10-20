# .....................
#! /usr/bin/python
#­*­coding: utf­8 ­*­
#from appwindow import *
from matplotlib import colors
from matplotlib.colors import Colormap
from myAppWindow7 import *
# .....................
import sys
import os

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
base = "joueurbica"
#PATH = os_path.abspath(os_path.split(__file__)[0])
#excel_f = PATH+"\joueursdonnees.xls"


class Appwindow(QWidget,Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(parent)
        self.initUI()
        
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
      
    def plot(self,ratings):

        ratings = ratings[::-1]
        #print('teste reverse',ratings)
        
        datac =[el[1] for el in ratings[0:6]]
        time =[el[5] for el in ratings[0:6]]
        #print(time)
        # clearing old figure
        self.figurec.clear()
        # create an axis
        ax = self.figurec.add_subplot(111)
        
        # plot data
        axes = self.figurec.gca()

        datar =[el[2] for el in ratings[0:6]]
        # clearing old figure
        self.figurer.clear()

        datab =[el[3] for el in ratings[0:6]]
       
        datan =[el[4] for el in ratings[0:6]]
        
        self.figuren.clear()
        
       
        
        x = array([1, 3, 4, 6])
        y = array(time)
        ax.plot(time, datac, "o-", color = 'yellow')
        ax.plot(time,datar, "o-", color = 'purple')
        ax.plot(time,datab, "o-", color = 'green')
        ax.plot(time,datan, "o-", color = 'red')
        ax.legend(["Classic","Rapid","Blitz","National"], loc ="lower left")
        self.canvasc.draw()

        

#show() 

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BICA Players')
        #self.setWindowIcon(QIcon("c:\Node JS\W3Schools\directiontechnique\\avec QT\\py files\\pictures\\slogan.png"))
        
        self.show()

def open_excel():
    #print("opening ...")
    excel_f = "joueursdonnees.xls"
    try:
        myBook = xlrd.open_workbook(excel_f)
        mySheet = myBook.sheet_by_index(0)
        #print(mySheet.name)
        print("file opened OK")
        #print(mySheet.row(0)[0])
        #print(mySheet.cell_value(0, 0)) # #OK
        return mySheet
    except:
        print("can't open file !!!")
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

def main():

    app = QApplication(sys.argv)
    ex = Example()
    today = date.today() - 5
    mabase = Mabase(base)
    #mabase.deleteAllTable()
    #mabase.createAllTable()
    feuille = open_excel()
    listeP = listPalyers(mabase)
    # for i in range(len(listeP)):
    #     mabase.deletePlayer(i+1)
    update_players(mabase,feuille,today)
    #print(mabase.selectAllElo())
    #print(listeP)
   
    #print(mabase.selectPlayer(2)[6])
    #print("Today date is: ", today)

    # (1, 'Ferjani Mohamed Islem', 'm', 'TUN', 1, 'BICA', 'GM', 'U12', 5517257, 2500, '', 40, './pictures/notun.jpg')
    
    # data = ('1', 'Ferjani Mohamed Islem', 'm', 'TUN', '1', 'BICA','2011/1/1', 'GM','5517257', 'U12',  '2500',  '40', './pictures/notun.jpg')
    # mabase.updateplayer(data)
    #print(mabase.selectPlayer(2)[6].year, mabase.selectPlayer(2)[6].month, mabase.selectPlayer(2)[6].day)
    sys.exit(app.exec_())


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



def main(args):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "C:\\Users\\user\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
    a=QApplication(args)
    f=QWidget()
    c=Appwindow(f)
    #PATH = os_path.abspath(os_path.split(__file__)[0])
    file = "slogan.png"
    #file = file.replace('\\','/')
    #print("file slogan : ", file)
    print("You are welcome, BICA PLAYERS is an application developped by Zakhama Yosri (zakhyos@gmail.com) from Tunisia since 2021")

    mabase = Mabase(base)
    today = date.today()
    #today = date(2021,7,20)
    feuille = open_excel()
    #listeP = listPalyers(db)
    # for i in range(len(listeP)):
    #     mabase.deletePlayer(i+1)
    #update_players(mabase,feuille,today)
    #dataAddAll(mabase)
    listeP = remplirListJoueur(c,mabase)
    #c.comboBox.activated[str].connect(lambda:onChanged(c,listeP,mabase)) 
    #c.player_liste_update.activated[str].connect(lambda:onChanged_updade(c,listeP,mabase))
    #mabase.deleteTable('TOURNAMENT')
    #mabase.createExamsPlayerTable()
    pl = addPly = AddPlayer(mabase,c,listeP) 
    Exams(mabase, c, pl)
    Emploi(mabase, c,pl)
    Event(mabase, c)
    graph = ShowScore(mabase,c,pl)
    # mabase.delAllTables()
    # mabase.createAllTable()
    # update_players(mabase,feuille,today)
    f.setAutoFillBackground(True)
    p = f.palette()
    p.setColor(f.backgroundRole(),QColor(0, 150, 220))
    f.setPalette(p)
    f.show()
    r=a.exec_()
    return r

class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)
        
        qp.setPen(Qt.black)
        size = self.size()
        
        # Colored rectangles
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(0, 0, 100, 100)
        
        qp.setBrush(QColor(0, 200, 0))
        qp.drawRect(100, 0, 100, 100)
        
        qp.setBrush(QColor(0, 0, 200))
        qp.drawRect(200, 0, 100, 100)
        
        # Color Effect
        for i in range(0,100):
            qp.setBrush(QColor(i*10, 0, 0))
            qp.drawRect(10*i, 100, 10, 32)
            
            qp.setBrush(QColor(i*10, i*10, 0))
            qp.drawRect(10*i, 100+32, 10, 32)
            
            qp.setBrush(QColor(i*2, i*10, i*1))
            qp.drawRect(10*i, 100+64, 10, 32)

if __name__=="__main__":
    main(sys.argv)