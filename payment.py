from myAppWindow7 import *
# .....................
import sys
import os
#from datetime import datetime, date
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

class Payment:
    def __init__(self, db, window,pl):
        self.win = window
        self.popupMessage = MessagePopUp("Payment informations","do you really want to update informations for this player", 2, 1)
        self.db = db
        self.pl = pl
        self.df = []
        self.listP = self.db.selectAllPlayer()
        self.win.playerPayment.activated[str].connect(lambda:self.changeIndex(1))
        self.win.playerVIP.activated[str].connect(lambda:self.changeIndex(2))
        self.win.payPayment.clicked.connect(self.addPayment)
        self.win.notPaying.clicked.connect(self.deletePayment)
        self.win.oklistP.clicked.connect(self.afficher_crosstable)
        self.win.savePayment.clicked.connect(lambda:self.savePayment(1))

        self.win.vipPayment.clicked.connect(self.addVIP)
        self.win.okvip.clicked.connect(self.afficher_crosstableVIP)
        self.win.saveVip.clicked.connect(lambda:self.savePayment(2))
#self.popupMessage.showMsgPopUp(1, "Data Added OK")
#result = self.popupMessage.showMsgPopUp(2, "do you really want to update informations for "+ res[1] + "exam")
                        #print("button : ",result)
                        #if result == QMessageBox.Yes:
    
    #---------------
    def getfiles(self,i):
        year = self.win.yearlistP.date().year()
        month = self.win.monthlistP.date().month()
        if i == 1:
            name = "paymentForMonth"+str(month)+"_"+str(year)+".xlsx"
        else:
            name = "VIPs.xlsx"
        filename, filter= QFileDialog.getSaveFileName(self.win,'Payment/VIP', name, "Excel (*.xlsx);;All Files (*)")#, options=QFileDialog.DontUseNativeDialog
        #print("le nom du fichier est ; ",filename)
        if not filename:
            return ""
        return filename

    def exportpaymentToExcel(self, file, listDf,i):
        if i==1:
            columnHeaders = ['NAME','AMOUNT'] 
        else:
            columnHeaders = ['NAME','AMOUNT','MONTH','YEAR','NB MONTHs'] 
        df = pd.DataFrame(listDf, columns=columnHeaders)
        df.to_excel(file, index=True)
        #print('Excel file exported')
        
    def savePayment(self,i):
        file = self.getfiles(i)
        if file !='' and  file.find('.xlsx')!=-1:
            self.exportpaymentToExcel(file,self.df,i)
        elif file == '':
            self.popupMessage.showMsgPopUp(1,"You must choose a file")
        else:
            self.popupMessage.showMsgPopUp(1,"{} is not in a regular form, you file must end with {}.xlsx".format(file))
#---------------

    def afficher_crosstable(self):
        
        year = self.win.yearlistP.date().year()
        month = self.win.monthlistP.date().month()
        result = self.db.selectPaymentView(month,year)
        self.df = result
        
        
        for row in range(self.win.tablePayment.rowCount()+1):
            self.win.tablePayment.removeRow(row)

        self.win.tablePayment.clearContents()
        for li, elt in enumerate(result):

               
            #print('name : ', elt[0])
            rowPosition = self.win.tablePayment.rowCount()
           
            if rowPosition<li+1:
                self.win.tablePayment.insertRow(rowPosition)
            self.win.tablePayment.setItem(li, 0, QTableWidgetItem(elt[0]))
            self.win.tablePayment.setItem(li, 1, QTableWidgetItem(str(elt[1])))
            self.win.tablePayment.setItem(li, 2, QTableWidgetItem(str(elt[2])))

    def afficher_crosstableVIP(self):
        
        result = self.db.selectVipView()
        self.df = result
        
        
        for row in range(self.win.tableVip.rowCount()+1):
            self.win.tableVip.removeRow(row)

        self.win.tableVip.clearContents()
        for li, elt in enumerate(result):

               
            #print('name : ', elt[0])
            rowPosition = self.win.tableVip.rowCount()
           
            if rowPosition<li+1:
                self.win.tableVip.insertRow(rowPosition)
            self.win.tableVip.setItem(li, 0, QTableWidgetItem(elt[0]))
            self.win.tableVip.setItem(li, 1, QTableWidgetItem(str(elt[1])))
            self.win.tableVip.setItem(li, 2, QTableWidgetItem(str(elt[2])))
            self.win.tableVip.setItem(li, 3, QTableWidgetItem(str(elt[3])))
            self.win.tableVip.setItem(li, 4, QTableWidgetItem(str(elt[4])))
            
    
    
    def deletePayment(self):
        if self.win.playerPayment.count() == 0:
            self.popupMessage.showMsgPopUp(1, "Sorry, No player in DataBase")  
            return
        listP = self.db.selectAllPlayer()
        year = self.win.yearPayment.date().year()
        month = self.win.monthPayment.date().month()
        id = listP[self.win.playerPayment.currentIndex()][0]
        res = self.db.deletePayment(id, month, year)
        if res == 1:
                self.popupMessage.showMsgPopUp(1, "Payment deleted")     
        elif res==0:
            self.popupMessage.showMsgPopUp(1, "Sorry, No payment to delete")  

    def addPayment(self):
        listP = self.db.selectAllPlayer()
        data = []
        if self.win.playerPayment.count() == 0:
            self.popupMessage.showMsgPopUp(1, "Sorry, No player in DataBase")  
            return
        else :
            data.append(listP[self.win.playerPayment.currentIndex()][0])
            
            if self.win.amountPayment.text() == "":
                self.popupMessage.showMsgPopUp(1, "Sorry, amount can't be empty") 
                return
            if not self.win.amountPayment.text().isnumeric():
                self.popupMessage.showMsgPopUp(1, "Sorry, amount must be a numeric value") 
                return 
            amount = int(self.win.amountPayment.text())
            month = self.win.monthPayment.date().month()
            year = self.win.yearPayment.date().year()
            day = self.win.dayPayment.date().day()
            #print("player id : ",data[0],month,"/",year," amount : ", amount)
            data += [amount, month, day, year]
            res = self.db.insertPayment(data) 
            if res == 1:
                self.popupMessage.showMsgPopUp(1, "Payment OK")     
            elif res==0:
                self.popupMessage.showMsgPopUp(1, "Payment Updated OK")  
    
    def addVIP(self):
        listP = self.db.selectAllPlayer()
        data = []
        if self.win.playerVIP.count() == 0:
            self.popupMessage.showMsgPopUp(1, "Sorry, No player in DataBase")  
            return
        else :
            data.append(listP[self.win.playerVIP.currentIndex()][0])
            
            if self.win.amountVIP.text() == "":
                self.popupMessage.showMsgPopUp(1, "Sorry, amount can't be empty") 
                return
            if not self.win.amountVIP.text().isnumeric():
                self.popupMessage.showMsgPopUp(1, "Sorry, amount must be a numeric value") 
                return 
            if self.win.numberMonthVIP.text() == "":
                self.popupMessage.showMsgPopUp(1, "Sorry, number of month can't be empty") 
                return
            if not self.win.numberMonthVIP.text().isnumeric():
                self.popupMessage.showMsgPopUp(1, "Sorry, number of month must be a numeric value") 
                return 
            amount = int(self.win.amountVIP.text())
            nbMonth = int(self.win.numberMonthVIP.text())
            month = self.win.monthVIP.date().month()
            year = self.win.yearVIP.date().year()
            #print("player id : ",data[0],month,"/",year," amount : ", amount, " nb months : ",nbMonth)
            data += [amount, month, year, nbMonth]
            res = self.db.insertVip(data) 
            if res == 1:
                self.popupMessage.showMsgPopUp(1, "VIP OK")     
            elif res==0:
                self.popupMessage.showMsgPopUp(1, "VIP Updated OK")  

    
    def changeIndex(self, i):
        if i==1:
            self.win.indexPlayer = self.win.playerPayment.currentIndex()
        else:
            self.win.indexPlayer = self.win.playerVIP.currentIndex()
        self.win.actualiserPointeurListe()