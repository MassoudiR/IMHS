◘import sys
from time import sleep
import pandas as pd
import sqlite3
import random

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import shutil

from docxtpl import DocxTemplate,InlineImage
import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image
from PySide6 import QtPrintSupport
import pickle
from modules.ui_splash_screen import Ui_SplashScreen
from modules.loginUi4 import Ui_Form_login
from modules.Calc import Calculator
from cryptography.fernet import Fernet


import Send_mail


# notification
from win10toast import ToastNotifier
import threading


from datetime import *
from datetime import timedelta
import os
import win32api
import win32print

from PySide6.QtWidgets import QApplication, QMessageBox

from modules.Add_task import  Ui_Form_add_task as Taskscreen
from modules.ui_main_add_retour import  Ui_Form_add_retour as retourscreen
from modules.ui_main_donne import  Ui_Form_donnee 
from modules.add_admin import Ui_Form as addadmin

import socket

import subprocess


   
counter = 0
DATE = datetime.now().date()

list_date_week = []
list_date_month = []
list_date_years = []
for day_w in range(7):
    list_date_week.append(str(DATE - timedelta(days =day_w)))
for day_m in range(30):
    list_date_month.append(str(DATE - timedelta(days =day_m)))    
for day_y in range(365):
    list_date_years.append(str(DATE - timedelta(days =day_y))) 
  
    


try:
    filehandler = open("DATA/Setting-admin.emh","rb")
    object_file = pickle.load(filehandler)
    filehandler.close()
    mode = object_file[0]
except:
    mode = True



import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "prodect_list.db")

##### check drive 
# ///////////////////////////////
key = b'3kcuhLtaKhBnDTm2BK8NfTwXvjfYgkC7Tk2yOU3LmY0='
fernet = Fernet(key)
try:
    filehandler = open("DATA/data.EMH","rb")
    object_file = pickle.load(filehandler)
    filehandler.close()
    ex_app = fernet.decrypt(object_file["donnee_ex"]).decode()
    name_pc = fernet.decrypt(object_file["name_pc"]).decode()
    id_pc =  fernet.decrypt(object_file['info_pc']).decode()
    if ex_app != "lim":
        exx = datetime.strptime(ex_app,'%Y-%m-%d').date()
        check_ex = exx >= DATE
    else:
        check_ex = True

    #################riel name 
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
    name_driver= socket.gethostname()

    check_driver = current_machine_id ==id_pc or name_driver == name_pc
    


except:
    check_ex = False 
    check_driver = False

# end check driver
#//////////////////////////////////////////////////

# IMPORT / database
# ///////////////////////////////////////////////////////////////


db = sqlite3.connect("prodect_list.db")



cr = db.cursor()


# ///////////////////////////////////////////////////////////////

######## Setting Of Market /////////////////////

Data_market = cr.execute("select * from Setting where Parametre = 'Info Marcket'").fetchone()

Market_Name = Data_market[1]
Market_Phone = Data_market[2]
Market_Phone_2 = Data_market[3]
Market_Fax = Data_market[4]
Market_Mail = Data_market[5]
Market_Maps = Data_market[6]
Market_min_Point = Data_market[7]
Market_to_Point = Data_market[8]

point_param = [float(Market_min_Point),float(Market_to_Point)]



##################### admin
acc_admin = []
###############################     test coonction
import requests
url = "http://www.muskfoundation.org/"
timeout = 5
try:
	request = requests.get(url, timeout=timeout)
	internet = True
except (requests.ConnectionError, requests.Timeout) as exception:
	internet = False
########################### firebase config
from pyrebase import *
upl = Send_mail.backup_db()
if internet:
    config = {
        "apiKey": "AIzaSyA2OOBDmS2Z_JTu2sIWplnBf0CT7LkGElE",
        "authDomain": "emhs-72d44.firebaseapp.com",
        "databaseURL": "https://emhs-72d44-default-rtdb.firebaseio.com",
        "projectId": "emhs-72d44",
        "storageBucket": "emhs-72d44.appspot.com",
        "messagingSenderId": "728939811426",
        "appId": "1:728939811426:web:8fbe47ddf75661c375773b",
        "measurementId": "G-Q0RRH6DVW1"
        }

    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    storage = firebase.storage()
    
    message = dict(database.child("message").get().val())
    for ms in message.keys():
        try :
            filehandler = open("DATA/message.EMH","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
            if ms in object_file:
                message[ms]=object_file[ms]
        except:
            pass

    outfile = open("DATA/message.EMH",'wb')
    pickle.dump(message,outfile)
    outfile.close()
    Send_mail.tasks_any()
    Send_mail.test_prodect_ex()
    Send_mail.test_prodect_sal()    
    Send_mail.clien_credit()
    
    if upl == True:
        path_user = f"backup/{Market_Name}/Backup.db"
        path_db = "DATA/Backup.db"
        storage.child(path_user).put(path_db)
      

    

    
    


    





######## /Setting Of Market /////////////////////


# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from modules import Payment_screen1
from modules import add_delet
from modules import edit_supp_addpromo

# IMPORT / pandas excel
# ///////////////////////////////////////////////////////////////
##df = pd.read_excel("prodect_list.xlsx")
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):



    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "IMH"
        description = "Inventory management hawk."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        widgets.tableWidget.doubleClicked.connect(self.add_edit_fc)
        widgets.tableitem.doubleClicked.connect(self.edit_suppr_fc)

    ########################################
    #             ACC ADMIN
    ########################################
        self.admin = cr.execute(f"select * from admin Where User_name = '{acc_admin[0]}' AND Password = '{acc_admin[1]}'").fetchone()

        self.acc_add = self.admin[2] == "True"

        
        self.acc_edit = self.admin[3] == "True"
        self.acc_Stat =  self.admin[4]  == "True"
        self.acc_Dep =  self.admin[5]  == "True"
        self.acc_Fact =  self.admin[6]  == "True"
        self.acc_Rap =  self.admin[7]  == "True"
        self.acc_Gar =  self.admin[8]  == "True"
        self.acc_Ret =  self.admin[9]  == "True"
        self.acc_Donn = self.admin[10]  == "True"

    ########################################
    #             / ACC ADMIN
    ########################################

        ##### //////////////////// auto //////////////####

        self.mini_stats()
        self.big_any("all")

        self.supp_offre_auto() 
        self.auto_activet_promo()

        




        

        #####//////////////////////// /auto ///////////////////###


        ##### --------- auto complet -------------------###
        cat_auto_complet=[]

        
        cat=["ALL"]
        cat_1 = cr.execute("SELECT DISTINCT Category from prodect ")
        cat_2 = cat_1.fetchall()
        

        for xc in range(len(cat_2)):
            cat.append (cat_2[xc][0])
            cat_auto_complet.append(cat_2[xc][0])
            
            
        completer = QCompleter(cat_auto_complet)
        widgets.input_cat.setCompleter(completer)

        widgets.comboBox.addItems(cat)
        widgets.comboBox.currentTextChanged.connect(self.SearchshowItemCAT)
        widgets.update_btn.clicked.connect(self.showItem)
        widgets.btn_print.clicked.connect(self.backup_clear_data)




        



        
        self.showItem()
        self.addItem()
      
        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        widgets.btn_ajouter.clicked.connect(self.addProdect)
        widgets.anl_btn.clicked.connect(self.Annulation)
        widgets.pushButton_3.clicked.connect(self.CONFER)
        #### add cart credit screen btn ----
        widgets.pushButton_2.clicked.connect(self.open_add_cart_credit_screen )
        #### ---- add dpenses btn ---

        widgets.pushButton.clicked.connect(self.Ajouter_dépenses_screen)
       
        #### ---- naw task btn ----
        widgets.pushButton_12.clicked.connect(self.task_show)
        ##### retour btn ---

        widgets.pushButton_6.clicked.connect(self.retour_prodect_screen)
            
        #### donnné clien -------

        widgets.pushButton_9.clicked.connect(self.Donnee_clien_screen)
                
        #### Cart fid ---------
        widgets.pushButton_4.clicked.connect(self.fid_cart_screen)
        #### garanter screen btn -------

        widgets.pushButton_5.clicked.connect(self.garantie_screen)
         
        #### facture screen btn ---------

        widgets.pushButton_11.clicked.connect(self.Facture)
        
        #### Rapports screen btn --------

        widgets.pushButton_10.clicked.connect(self.rapports_screen)

        



        widgets.checkBox.toggled.connect(lambda :self.auto_code(widgets.sku2,"short") )

        


        widgets.pushButton_13.clicked.connect(self.save_cart_credit)
        ###widgets.pushButton_6.clicked.connect(self.add_edit_fc)

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_save_2.clicked.connect(self.buttonClick)
        widgets.btn_message.clicked.connect(self.msg_list)
        widgets.btn_share.clicked.connect(self.parametre_screen)
        widgets.btn_adjustments.clicked.connect(self.parametre_imp)
        widgets.btn_more.clicked.connect(self.parametre_admin)



        widgets.input_cb1.returnPressed.connect(self.listupdat)
        widgets.input_sku1.returnPressed.connect(self.skulistupdat)


       #############---------------search table-------------------####
        widgets.lineEdit.returnPressed.connect(self.SearchshowItemBarre)
        widgets.lineEdit_2.returnPressed.connect(self.SearchshowItemSKU)
        widgets.lineEdit_4.returnPressed.connect(self.add_point_cart)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        widgets.btn_exit.clicked.connect(lambda : calc.show())
        


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            if self.acc_add == True :
                widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            else:
                msg1=QMessageBox()
                msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
                msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
                msg1.exec_()

            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            if self.acc_edit :
                
                widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            else:
                msg1=QMessageBox()
                msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
                msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
                msg1.exec_()                
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
           
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            if self.acc_Stat:
                widgets.stackedWidget.setCurrentWidget(widgets.Statistics)
            else:
                msg1=QMessageBox()
                msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
                msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
                msg1.exec_()

            UIFunctions.resetStyle(self, btnName)
           

            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_save_2":
            widgets.stackedWidget.setCurrentWidget(widgets.Outic)
            UIFunctions.resetStyle(self, btnName)
           

            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))            

 
    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()
    # PRINT MOUSE EVENTS
    ## -------------------------Add a new product-------------------------------------------#
    def addProdect(self):
        hach = 0
        
        SKU=widgets.sku2.text()
        CODE_BAR=widgets.cd2.text()
        NOM=widgets.input_nm.text()
        CATEGORY=widgets.input_cat.text()
        PRIX=widgets.prix_achat.text()
        PRIX_ACHAT=widgets.input_vente.text()
        TVA=widgets.input_tva.text()
        STOCK=widgets.input_qes.text()
        MARQUE=widgets.input_marque.text()
        DATE_EX=widgets.date_ex.text()
        DATE_AJ=widgets.date_aj.text()
        STOCK_MIN=widgets.stock_min.text()
        OFFRE=widgets.offre.text()
        POINT=widgets.point_merci.text()
        OPTION=widgets.options.text()
        FOURN=widgets.info_forn.text()
        FACT=widgets.N_facture.text()
        REM=widgets.remarque.toPlainText()
        
        
        datadb = cr.execute("select SKU,BARRE from prodect").fetchall()
        if CODE_BAR !="" and SKU !="" and NOM  !="" and PRIX !="" :
            if CATEGORY == "":
                CATEGORY = "Category Inconnue"
            if PRIX_ACHAT =="":
                PRIX_ACHAT= "NULL"    
            if TVA =="":
                TVA = "0%"
            if STOCK =="":
                STOCK = "NULL"
            if MARQUE =="":
                MARQUE = "Marque Inconnue"  
            if DATE_EX == "12-12-2021":
                DATE_EX = "NULL" 
            if DATE_AJ == "10-10-2020":
                DATE_AJ = str(DATE)
            if STOCK_MIN == "" or "10" :
                STOCK_MIN = "NULL"
            if OFFRE == "":
                OFFRE = "NULL" 
            if POINT == "":
                POINT = "NULL" 
            if OPTION =="":
                OPTION="NULL"   
            if FOURN =="":
                FOURN = "NULL"
            if FACT == "":
                FACT = "NULL"
            if REM =="":
                REM = "NULL"  
            if len(datadb) == 0 :
                datadb = [("demo","demo")]     
               
           

            for bb in range(len(datadb)):
                print(bb)
                ddb = datadb[bb]
                
                if CODE_BAR == ddb[1] or SKU == ddb[0]:
                    
                    msg1=QMessageBox()
                    #msg1.setIcon(QMessageBox.NoIcon)
                    msg1.setText("Le code bar ou Sku saisi n'a pas été reconnu         ")
                    msg1.setInformativeText("Ce code est invalide ou n'a pas été enregistré dans la base de données")
                    msg1.setWindowTitle("Erreur d'entrée")
                    #msg1.setDetailedText("The details are as follows:")
                    msg1.exec_()
                    hach = 1

                    break
                    
                
            if hach == 0 :        
                cr.execute(f"INSERT INTO prodect(SKU, BARRE, Nom, Category, Prix_achat, Prix_vente, TVA, Stock, Marque, Date_exp, Date_ajout, Stock_minimal, Offre, Points, Options, Fournisseur, N_Facture, Remarque) (values)('{SKU}', '{CODE_BAR}', '{NOM}','{CATEGORY}', '{PRIX}', '{PRIX_ACHAT}', '{TVA}', '{STOCK}','{MARQUE}', '{DATE_EX}', '{DATE_AJ}','{STOCK_MIN}', '{OFFRE}', '{POINT}', '{OPTION}', '{FOURN}', '{FACT}','{REM}')")
                db.commit()

                datadb = cr.execute("select SKU,BARRE from prodect").fetchall()

                

                widgets.statut.setText("enregistré avec succès")
                widgets.statut.setStyleSheet("font-size:15px;""color:green;")
                widgets.info_forn.clear()
               
                
                self.showItem()
            
                    
                    
                    
                    
              
                    
        else:
            msger=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msger.setText("Veuillez remplir les champs obligatoires       ")
            msger.setInformativeText("les champs obligatoires : SKU CODE | CODE BARE | NOM DE PRODUIT | PRIX D ACHAT ")
            msger.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msger.exec_()
            

    ## -------------------------Show product-------------------------------------------------#  
    def showItem(self):
        while widgets.tableitem.rowCount() > 0:
            widgets.tableitem.removeRow(0)
        cr.execute("select SKU,BARRE,Nom,Category,Prix_achat,Prix_vente,Stock,Marque from prodect")
        listitem= cr.fetchall()
        
        for row_index,row_data in enumerate(listitem):
            widgets.tableitem.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableitem.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))
    ## -------------------------Search Show product-------------------------------------------------#  
    def SearchshowItemBarre(self):
        h1 = widgets.lineEdit.text() 
        
        while widgets.tableitem.rowCount() > 0:
            widgets.tableitem.removeRow(0)
           
        cr.execute(f"select SKU,BARRE,Nom,Category,Prix_achat,Prix_vente,Stock,Marque from prodect WHERE  BARRE='{h1}' ")
        listitem= cr.fetchall()
        
        for row_index,row_data in enumerate(listitem):
            widgets.tableitem.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableitem.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))   
    def SearchshowItemSKU(self):
        h1 = widgets.lineEdit_2.text() 

        
        while widgets.tableitem.rowCount() > 0:
            widgets.tableitem.removeRow(0)
           
        cr.execute(f"select SKU,BARRE,Nom,Category,Prix_achat,Prix_vente,Stock,Marque from prodect WHERE  SKU='{h1}' ")
        listitem= cr.fetchall()
        
        for row_index,row_data in enumerate(listitem):
            widgets.tableitem.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableitem.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))                              
    def SearchshowItemCAT(self):
        h1 = widgets.comboBox.currentText()

        if h1 != "ALL":
            while widgets.tableitem.rowCount() > 0:
                widgets.tableitem.removeRow(0)
            
            cr.execute(f"select SKU,BARRE,Nom,Category,Prix_achat,Prix_vente,Stock,Marque from prodect WHERE  Category='{h1}' ")
            listitem= cr.fetchall()
            
            for row_index,row_data in enumerate(listitem):
                widgets.tableitem.insertRow(row_index)
                for colm_index , colm_data in enumerate(row_data):
                    widgets.tableitem.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data))) 
        else:
            while widgets.tableitem.rowCount() > 0:
                widgets.tableitem.removeRow(0)
            
            cr.execute(f"select SKU,BARRE,Nom,Category,Prix_achat,Prix_vente,Stock,Marque from prodect ")
            listitem= cr.fetchall()
            
            for row_index,row_data in enumerate(listitem):
                widgets.tableitem.insertRow(row_index)
                for colm_index , colm_data in enumerate(row_data):
                    widgets.tableitem.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))               

    ## -------------------------Store Item-----------------------------------------------------# 
    addlist= []
    prixtoutal=0 
    N_point = 0
    def listupdat(self):
        h1=widgets.input_cb1.text()
        offre = cr.execute(f"select code_bar,offre,quantity,new_price,total_price,Offre_statut from prodect_offre WHERE code_bar='{h1}'").fetchall()
        
        if h1 in str(cr.execute("select BARRE from prodect").fetchall()) :

            for c1,n1 in enumerate(self.addlist) :
                n2=list(n1)
                
                
               
                if h1 ==n2[0]:
                    n2[3]=int(n2[3]) + 1
                #####------------ promo_applicer -------------------####    
                if offre == []:
                    offre = ['0000000000000000000','NULL',"1555","00","False"] 
                                      
                if h1 == str(offre[0][0]) and offre[0][1] == "Réduction De Prix" and offre[0][2]!=0 and offre[0][5] == "True"   :
                     
                    
                    if n2[3] == offre[0][2]:    
                        n2[2] = offre[0] [3] 
                        n2[4]=float(n2[2]) * int(n2[3]) 
                        n1=tuple(n2)
                        self.addlist[c1]=n1  
                        self.addItem()   
                        self.prixtoutal=0 
                    else:
                        n2[4]=float(n2[2]) * int(n2[3]) 
                        n1=tuple(n2)
                        self.addlist[c1]=n1  
                        self.addItem()   
                        self.prixtoutal=0
                    for pi in range(len(self.addlist)):
                        self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                    widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")

                    
                elif h1 == str(offre[0][0]) and offre[0][1] == "Réduction de quantité" and offre[0][2]!=0 and offre[0][5] == "True": 
                    if n2[3] == offre[0][2]  : 

                        n2[3] += int(offre[0] [3]) 
                        n2[4]=float(n2[2]) * int(n2[3]) 
                        n2[4] = n2[4] - (float(n2[2]) *  int(offre[0] [3]))
                        n1=tuple(n2)
                        self.addlist[c1]=n1  
                        self.addItem()   
                        self.prixtoutal=0 

                    elif n2[3] > int(offre[0][2]) and n2[3]%int(offre[0][2]) !=0  :

                        n2[4]+= float(n2[2])
                        n1=tuple(n2)
                        self.addlist[c1]=n1  
                        self.addItem()   
                        self.prixtoutal=0

                    elif n2[3] > int(offre[0][2]) and (n2[3])   %  int(offre[0][2]) == 0  :
                        


                        n2[4]+= float(n2[2])
                        n1=tuple(n2)
                        self.addlist[c1]=n1  
                        self.addItem()   
                        self.prixtoutal=0


                     

                    else:
                        n2[4]=float(n2[2]) * int(n2[3])
                         
                        n1=tuple(n2)
                        self.addlist[c1]=n1  
                        self.addItem()   
                        self.prixtoutal=0
                    for pi in range(len(self.addlist)):
                        self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                    widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")                                                                                              


                #####------------ /promo _applicer -------------------####   
                    
                else:    
                                             
                    n2[4]=float(n2[2]) * int(n2[3]) 
                    n1=tuple(n2)
                    self.addlist[c1]=n1



                    self.addItem()   
                    self.prixtoutal=0

                    for pi in range(len(self.addlist)):
                        self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                    widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
            if h1 not in str(self.addlist):
                query1=cr.execute(f"select BARRE,NOM,Prix_achat from prodect WHERE BARRE='{h1}'")
                query2=query1.fetchall()
                ##############----- offre--------------###
                if offre == []:
                    offre = ['0000000000000000000','NULL',"1555","000","False"]

                if h1 == str(offre[0][0]) and offre[0][1] == "Réduction De Prix" and offre[0][2]<=1 and offre[0][5] == "True" :
                    try:
                        codebar=((query2[0])[0],(query2[0])[1],offre[0][3], 1 ,offre[0][3])
                        
                        
                        self.addlist.append(codebar)
                        self.addItem()
                        self.prixtoutal=0 
                        for pi in range(len(self.addlist)):
                            self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                        widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
                        
                    except:
                        msg1=QMessageBox()
                        #msg1.setIcon(QMessageBox.NoIcon)
                        msg1.setText("Le code saisi n'a pas été reconnu         ")
                        msg1.setInformativeText("Le code saisi n'est pas reconnu ou le produit n'est pas trouvé dans la base de données")
                        msg1.setWindowTitle("Erreur d'entrée")
                        #msg1.setDetailedText("The details are as follows:")
                        msg1.exec_()
                   
                else:
                
                    try:
                        codebar=((query2[0])[0],(query2[0])[1],(query2[0])[2], 1 ,(query2[0])[2])
                        
                        
                        self.addlist.append(codebar)
                        self.addItem()
                        
                    except:
                        msg1=QMessageBox()
                        #msg1.setIcon(QMessageBox.NoIcon)
                        msg1.setText("Le code saisi n'a pas été reconnu   1      ")
                        msg1.setInformativeText("Le code saisi n'est pas reconnu ou le produit n'est pas trouvé dans la base de données")
                        msg1.setWindowTitle("Erreur d'entrée")
                        #msg1.setDetailedText("The details are as follows:")
                        msg1.exec_()


                

                    self.prixtoutal=0 
                    for pi in range(len(self.addlist)):
                        self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                    widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
            self.point(h1)
        else:
            msg1=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msg1.setText("Le code saisi n'a pas été reconnu         ")
            msg1.setInformativeText("Ce code est invalide ou n'a pas été enregistré dans la base de données")
            msg1.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg1.exec_()
            widgets.input_cb1.setText("")
    def skulistupdat(self):
        h1=widgets.input_sku1.text()
        if h1 in str(cr.execute("select SKU from prodect").fetchall()) :
            h1=(cr.execute(f"select BARRE from prodect WHERE SKU='{h1}'").fetchall()[0])[0]
            for c1,n1 in enumerate(self.addlist) :
                n2=list(n1)
                if h1 ==n2[0]:
                    n2[3]=int(n2[3]) + 1
                    n2[4]=float(n2[2]) * int(n2[3])
                    prr=float(n2[4]) 
                    n1=tuple(n2)
                    self.addlist[c1]=n1
                    self.addItem()   
                    self.prixtoutal=0
                    for pi in range(len(self.addlist)):
                        self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                    widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
            if h1 not in str(self.addlist):
                query1=cr.execute(f"select BARRE,NOM,Prix_achat from prodect WHERE BARRE='{h1}'")
                query2=query1.fetchall()
                

                codebar=((query2[0])[0],(query2[0])[1],(query2[0])[2], 1 ,(query2[0])[2])
                
                self.addlist.append(codebar)
                self.addItem()
                

                self.prixtoutal=0 
                for pi in range(len(self.addlist)):
                    self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
                widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
        else:
            msg1=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msg1.setText("Le code saisi n'a pas été reconnu         ")
            msg1.setInformativeText("Ce code est invalide ou n'a pas été enregistré dans la base de données")
            msg1.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg1.exec_()
            widgets.input_cb1.setText("")
            widgets.input_sku1.setText("")
    def addItem(self):
        while widgets.tableWidget.rowCount() > 0:
            widgets.tableWidget.removeRow(0)
        for row_index,row_data in enumerate(self.addlist):
            widgets.tableWidget.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableWidget.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))
        widgets.input_cb1.setText("")  
        widgets.input_sku1.setText("")                      
    ## -------------------------ANNULATION BTN-----------------------------------------------------# 
    def Annulation(self):
        while widgets.tableWidget.rowCount() > 0:
            widgets.tableWidget.removeRow(0)
        self.prixtoutal=0
        self.addlist= []
        widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
        widgets.input_cb1.setText("")
        widgets.input_sku1.setText("")
    ## -------------------------CONFERMATION BTN-----------------------------------------------------# 
    
    def CONFER(self):   
        if mode == True:
            poro.setupUi(poro)
            self.retern(False)
            poro.label.setText(str(self.prixtoutal))

            poro.pushButton_8.clicked.connect(self.pay_by_points)

            poro.pushButton_6.clicked.connect(self.credit_screen)
 
            
            ###--------- ticket -----------###
            poro.pushButton_7.clicked.connect(lambda : self.save_sale("Ticket"))

            #### --------------- D17 ---------------###
            poro.pushButton_5.clicked.connect(self.d17)
            
            poro.pushButton_9.clicked.connect(lambda : self.save_sale("Cash") )
               

            poro.show()

        else:
            self.save_sale("Cash")
            
    ## -------------------------btn_rest_dt -----------------------------------------------------# 
    def btn_rest_dt(self,x):
        poro.setupUi(poro)
        poro.label.setText(str(self.prixtoutal))
        self.retern(False) 
        if self.prixtoutal <= x :
            poro.stackedWidget.setCurrentWidget(poro.page_2)
            rest= x - self.prixtoutal
            poro.label_2.setText(f"Le reste du montant : {rest} DT ")  
                         
    def retern(self,y):
        if poro.stackedWidget.currentIndex() == 0 and y==True:
            poro.close()
        else:
            poro.setupUi(poro)
            poro.stackedWidget.setCurrentWidget(poro.page)
        poro.pushButton.clicked.connect(lambda: self.btn_rest_dt(5000.0))
        poro.pushButton_2.clicked.connect(lambda:self.btn_rest_dt(10000.0))
        poro.pushButton_3.clicked.connect(lambda:self.btn_rest_dt(20000.0))
        poro.pushButton_4.clicked.connect(lambda:self.btn_rest_dt(50000.0))
        poro.pushButton_10.clicked.connect(lambda : self.retern(True))     
        
            
    def save_sale(self,y):

        for x in range(len(self.addlist)):
                datao = self.addlist[x] 
                db_promo= cr.execute(f"SELECT code_bar ,offre_title,quantity FROM prodect_offre WHERE code_bar ='{datao[0]}' ").fetchall()
                if db_promo !=[] :
                    if db_promo[0][2] == 0 or db_promo[0][2] == 1:
                        offre_name = db_promo[0][1]
                    elif db_promo[0][2] >= datao[3] :
                        offre_name = db_promo[0][1]
                    else: 
                        offre_name = "NULL"  
                else:
                    offre_name = "NULL"            

                cr.execute(f"INSERT INTO prodect_sale(code_bare,nom,prix,nomb,prix_total,offre,Mode_pay,date) values('{datao[0]}','{datao[1]}','{datao[2]}','{datao[3]}','{datao[4]}','{offre_name}','{y}','{DATE}')")
        db.commit()
        poro.close()
        self.Annulation()   


###------------------------add_edit_screen-------------------------------------------##        
    def add_edit_fc(self):

        try:
            row = widgets.tableWidget.currentRow()
            currentproductid = (widgets.tableWidget.item(row, 0).text() )
            
            


            for x in range(len(self.addlist)):
                if str((self.addlist[x])[0])==str(currentproductid):
                  
                    
                    
                    add.setupUi(add)
                    #---------------------------------------------------
                    add.label.setText(currentproductid)
                    
                    
                    
                    add.pushButton.clicked.connect(lambda:self.removelable(x))
                    

                    add.spinBox.valueChanged.connect(lambda : self.updateLabel(x
                    )) 
                    
                    add.spinBox.setValue(int((self.addlist[x])[3]))
                    #---------------------------------------------------
                    
                    add.show()
                    
                    
                    

                    break
                    
        except:
            msg3=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msg3.setText("Le code saisi n'a pas été reconnu         ")
            msg3.setInformativeText("Ce code est invalide ou n'a pas été enregistré dans la base de données")
            msg3.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg3.exec_()
    def updateLabel(self,x):
        if add.spinBox.value() != 0:   
            lev = list(self.addlist[x])
            offre = cr.execute(f"select code_bar,offre,quantity,new_price,total_price from prodect_offre WHERE code_bar='{lev[0]}'").fetchall()
            lev[3] = add.spinBox.value()
            #####------------ promo _applicer -------------------####
            if offre == []:
                offre = ['0000000000000000000','NULL',"1555"]    
            print(lev[0])                    
            if lev[0] == str(offre[0][0]) and offre[0][1] == "Réduction De Prix" and offre[0][2]!=0  :
                
                if add.spinBox.value() == offre[0][2]:
                    lev[2] = offre[0] [3]
            #--------------- /promo_applicer --------------------####                      
        
            lev[4] = float(lev[2])*int(lev[3])
        

            self.addlist[x] = tuple(lev)
            
            print(self.addlist)
            self.addItem()
            self.prixtoutal=0 
            for pi in range(len(self.addlist)):
                self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
            widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
            
            

        else:
            print("no")
    def removelable(self,x): 
        self.addlist.pop(x)
        self.addItem()
        self.prixtoutal=0 
        for pi in range(len(self.addlist)):
            self.prixtoutal= self.prixtoutal + float((self.addlist[pi])[4])
        widgets.toutal_prix.setText(f"TOUTAL :{self.prixtoutal}TND")
        add.close()
###------------------------/add_edit_screen-------------------------------------------## 
    def edit_suppr_fc(self):
         row = widgets.tableitem.currentRow()
         currentproductid = (widgets.tableitem.item(row, 1).text() )
         add_suppr.setupUi(add_suppr)
         add_suppr.label.setText(f"Code Bar : {currentproductid}")
         add_suppr.label_12.setText(f"CODE BARE : {currentproductid}")
         add_suppr.label_11.setText(f"CODE BARE : {currentproductid}")
         


         ##--------------btn---------------##
         add_suppr.pushButton_2.clicked.connect(lambda: self.suppr_prodect(currentproductid))
         
         add_suppr.pushButton.clicked.connect(lambda : self.edit_prodect_fc(currentproductid) )
         
         add_suppr.pushButton_7.clicked.connect(lambda : self.prodect_stats(currentproductid))
         add_suppr.pushButton_18.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.pagesContainer_2))


         
         add_suppr.pushButton_3.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.page))
         add_suppr.pushButton_8.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.pagesContainer_2))
         add_suppr.pushButton_14.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.pagesContainer_2))
         add_suppr.pushButton_13.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.pagesContainer_2))
         add_suppr.pushButton_16.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.pagesContainer_2))
         add_suppr.pushButton_10.clicked.connect(lambda : self.add_promo_qua(currentproductid))
         add_suppr.pushButton_4.clicked.connect(lambda : self.add_stock(currentproductid))
         add_suppr.pushButton_9.clicked.connect(lambda : self.add_promo_price(currentproductid))
        

         ##-----------------/btn---------------------#


         add_suppr.show()
    def suppr_prodect(self,x):
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        msgBox.setButtonText(QMessageBox.Apply  ,"Suppr")
        msgBox.setButtonText(QMessageBox.Cancel  ,"Exit")
        msgBox.setButtonText
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec_()
        if ret == QMessageBox.Apply :
            cr.execute(f"DELETE FROM prodect WHERE BARRE='{x}'")
            db.commit()
            self.showItem()
            add_suppr.close()


    def edit_prodect_fc(self,x):

        add_suppr.lineEdit_2.setText(str(x))
        query1=cr.execute(f"select SKU,NOM,Category,Prix_achat,Prix_vente,Date_exp,Marque from prodect WHERE BARRE='{str(x)}'")
        query2=query1.fetchone()
        add_suppr.lineEdit.setText(str(query2[0]))
        add_suppr.lineEdit_3.setText(str(query2[1]))
        add_suppr.lineEdit_4.setText(str(query2[2]))
        add_suppr.lineEdit_5.setText(str(query2[4]))
        add_suppr.lineEdit_6.setText(str(query2[3]))
        add_suppr.lineEdit_7.setText(str(query2[5]))
        add_suppr.lineEdit_8.setText(str(query2[6]))
        add_suppr.pushButton_6.clicked.connect(lambda : add_suppr.pagesContainer.setCurrentWidget(add_suppr.pagesContainer_2))
        add_suppr.pushButton_5.clicked.connect(lambda : self.edit_prodect_btn_edit(x))





        
        
        add_suppr.pagesContainer.setCurrentWidget(add_suppr.edit)
        
    def edit_prodect_btn_edit(self, x):
        cr.execute(f"UPDATE prodect SET NOM = '{add_suppr.lineEdit_3.text()}',Category='{add_suppr.lineEdit_4.text()}',Prix_achat='{add_suppr.lineEdit_5.text()}',Prix_vente='{add_suppr.lineEdit_6.text()}',Date_exp='{add_suppr.lineEdit_7.text()}',Marque='{add_suppr.lineEdit_8.text()}'  WHERE BARRE='{str(x)}'  ")
        db.commit()
        self.showItem()
        add_suppr.close()
    def mini_stats(self):
        ####---------------max prodect sale--------------###
        
        max_Produit_sale = cr.execute("select DISTINCT code_bare from prodect_sale")
        max_Produit_sale_1 = max_Produit_sale.fetchall()
        nombre_sale = {}
        for xv in range(len(max_Produit_sale_1)):
            nombre_sale[f"{max_Produit_sale_1[xv][0]}"] = 0
        list_sale = cr.execute("select code_bare,nomb,nom,date from prodect_sale").fetchall() 

        if list_sale !=[]:
            for xvv in range(len(list_sale)):
                nombre_sale[f"{list_sale[xvv][0]}"] += list_sale[xvv][1]
            maxxi = max(nombre_sale.values())
            for xvv , xcc in nombre_sale.items():
                if xcc == maxxi:
                    nom_of_prodet = cr.execute(f"select nom from prodect_sale WHERE code_bare = {xvv}").fetchone()[0]
                    widgets.label_18.setText(f"Produit le plus vendu :{nom_of_prodet}")
                    widgets.label_18.setToolTip(f"code bare {xvv}")
                    break
            ####---------------min prodect sale--------------###   
            minni = min(nombre_sale.values())  
            for xvv , xcc in nombre_sale.items():
                if xcc == minni:
                    nom_of_prodet = cr.execute(f"select nom from prodect_sale WHERE code_bare = {xvv}").fetchone()[0]
                    widgets.label_19.setText(f"Produit le plus vendu :{nom_of_prodet}")
                    widgets.label_19.setToolTip(f"code bare {xvv}")
                    break
            ####---------------moy prodect sale--------------###  
            date_list = cr.execute("select DISTINCT date from prodect_sale").fetchall()
            sort_by_date = {}
            for dl in range(len(date_list)):
                sort_by_date[date_list[dl][0]] = 0 
            for xbb in range(len(list_sale)):
                sort_by_date[f"{list_sale[xbb][3]}"] += list_sale[xbb][1]
            moy_of_sale = sum(sort_by_date.values()) / len(sort_by_date.items())
            moy_of_sale_test=  f"Ventes Quotidiennes Moyennes :{round(moy_of_sale)} - {round(moy_of_sale) + 5} "
            widgets.label_20.setText(moy_of_sale_test)  
        ####---------------Expiry_soon--------------###  
        Expiry_date = {}
        num_of_produit_ex = 0
        num_of_produit_ex_soon = 0

        list_prod = cr.execute(f"select BARRE,Date_exp from prodect ").fetchall()
        for dx in range(len(list_prod)):
            if list_prod[dx][1] != "NULL":
                try:
                    date_time_obj = datetime.strptime(list_prod[dx][1], '%d-%m-%y').date()
                    

                    
                    
                    if DATE >= date_time_obj or (DATE + timedelta(days =10) >= date_time_obj )   :
                        

                        if (date_time_obj-DATE) <= timedelta(days =0 ):  
                           
                            Expiry_date.update({list_prod[dx][0]: [str((date_time_obj - DATE).days),"expired"]})
                            num_of_produit_ex += 1
                            

                    else : 
                        Expiry_date.update({list_prod[dx][0]: [str((date_time_obj - DATE).days),"expired soon"]})
                        num_of_produit_ex_soon += 1 
                        print(num_of_produit_ex_soon)  


                    

                except:
                    
                    pass
        print(Expiry_date)        
        widgets.label_22.setText(f"Produits proches de la péremption: {num_of_produit_ex_soon}")
        widgets.label_27.setText(f"Stock en rupture : {num_of_produit_ex}")
        #####-------------------- prodect_stats------------------####
    def prodect_stats(self,currentproductid):
        add_suppr.pagesContainer.setCurrentWidget(add_suppr.prodect_stat)
        prodect_sale_list = cr.execute(f"select code_bare,nomb from prodect_sale WHERE code_bare ='{currentproductid}' ").fetchall()
        
        prodect_list = cr.execute(f"select BARRE,Stock,Stock_minimal,date_exp from prodect WHERE BARRE='{currentproductid}'").fetchall()
        
        prodect_sale_list_dec = {} 
        for cco in prodect_sale_list:
            prodect_sale_list_dec[cco[0]] = 0
        for cco in prodect_sale_list:
            prodect_sale_list_dec[cco[0]] += cco[1]   
        try:
            add_suppr.label_16.setText(f"Nombre de ventes : {prodect_sale_list_dec[cco[0]]}") 
            ##### The daily sales rate is calculated as follows: Total number of sales / week (7 days) 
            add_suppr.label_18.setText(f"Ventes quotidiennes moyennes : {round(prodect_sale_list_dec[cco[0]] / 7)}")
            try:
                if prodect_list[0][1]  != "NULL":
                    nomb_rest = prodect_list[0][1]-(prodect_sale_list_dec[(prodect_list[0][0])])
                    add_suppr.label_20.setText(f"Sera en rupture de stock dans : {round(nomb_rest / (prodect_sale_list_dec[cco[0]] / 7)) } Jour")
                    add_suppr.label_21.setText("Le produit expirera et vous avez : Aucune")


                     
            except:
                add_suppr.label_20.setText(f"Sera en rupture de stock dans : Aucune")
                add_suppr.label_21.setText("Le produit expirera et vous avez : Aucune")
            
            
        except:  
            add_suppr.label_16.setText(f"Nombre de ventes : 0") 
            add_suppr.label_18.setText(f"Ventes quotidiennes moyennes : Aucune ")
             
        if prodect_list[0][3] != "NULL" :
            try :
                to_date = datetime.strptime(prodect_list[0][3], '%d-%m-%y').date() - DATE
                
                if to_date.days == 0 :
                    add_suppr.label_19.setStyleSheet("color: red ; font-size:15px")
                    add_suppr.label_19.setText(f"Expiré aujourd'hui ")
                elif to_date.days < 0:
                    add_suppr.label_19.setStyleSheet("color: red ; font-size:15px")
                    add_suppr.label_19.setText(f"Expiré depuis {abs(to_date.days)} Jours  ")
                    add_suppr.label_19.setStyleSheet("color: red  ; font-size:15px")
                elif to_date.days > 0 and  to_date.days < 10 :
                    add_suppr.label_19.setStyleSheet("color: #FEAD00 ; font-size:15px")
                    add_suppr.label_19.setText(f"Expire après : {to_date.days} Jours  ")                     

                else:
                    add_suppr.label_19.setStyleSheet("color: green ; font-size:15px")
                    add_suppr.label_19.setText(f"Expire après : {to_date.days} Jours  ") 
                
                   
                SEF= nomb_rest - abs((round(prodect_sale_list_dec[cco[0]] / 7) ) * to_date.days)
                add_suppr.label_22.setText(f"Nous vous conseillons de continuer ainsi")
                if SEF <= 0:
                    add_suppr.label_21.setText(f"Le produit expirera et vous avez : 0 PIES")  
                else:
                    add_suppr.label_21.setText(f"Le produit expirera et vous avez : {SEF } PIES") 
                    if  SEF > 0 and SEF <= 20  :
                        add_suppr.label_22.setText(f"Nous recommandons une réduction de 20 %")  
                    elif SEF > 20 and SEF <= 60:
                        add_suppr.label_22.setText(f"Nous recommandons une réduction de 30 %") 
                    elif SEF > 60 :
                        add_suppr.label_22.setText(f"Nous recommandons une réduction de 45 %")     
                    


                

            except : 
                add_suppr.label_19.setText(f"Expire après : Aucune  ")
                add_suppr.label_21.setText("Le produit expirera et vous avez :  Aucune ")
        else:
           add_suppr.label_19.setText(f"Expire après : Aucune  ")  
           add_suppr.label_21.setText("Le produit expirera et vous avez :  Aucune ")   

        
        try:
            
            for ccg in prodect_list:
                
                if ccg[1] != "NULL":
                    
                    if ccg[0] in prodect_sale_list_dec.keys() :
                        
                        add_suppr.label_16.setText(f"Nombre de ventes : {prodect_sale_list_dec[cco[0]]}")
                        in_stk=ccg[1] - prodect_sale_list_dec[ccg[0]]
                        add_suppr.label_17.setText(f"Nombre restant : {in_stk}")
                        

                        if ccg[2]!="NULL":
                            if (ccg[1]-prodect_sale_list_dec[cco[0]]) <= ccg[2] :
                                add_suppr.label_16.setText(f"Nombre de ventes : {prodect_sale_list_dec[cco[0]]}")
                                
                                add_suppr.label_15.setText("État du produit : près de s'épuiser")
                            else:   
                                
                                add_suppr.label_16.setText(f"Nombre de ventes : {prodect_sale_list_dec[cco[0]]}")
                                
                                add_suppr.label_15.setText("État du produit : Disponible") 

                        else:
                            if (ccg[1]-prodect_sale_list_dec[cco[0]]) <= 30 :
                                if (ccg[1]-prodect_sale_list_dec[cco[0]]) <= 0 :
                                    add_suppr.label_15.setText("État du produit : Non Disponible")
                                else: 
                                    add_suppr.label_16.setText(f"Nombre de ventes : {prodect_sale_list_dec[cco[0]]}")
                                    
                                    add_suppr.label_15.setText("État du produit : près de s'épuiser")
                            else:  
                                
                                add_suppr.label_16.setText(f"Nombre de ventes : {prodect_sale_list_dec[cco[0]]}") 
                                
                                add_suppr.label_15.setText("État du produit : Disponible")

                else:
                    add_suppr.label_15.setText("État du produit : Aucune")
                    add_suppr.label_17.setText(f"Nombre restant : Aucune")
                    add_suppr.label_20.setText(f"Sera en rupture de stock dans : Aucune")
                    add_suppr.label_22.setText("Il n'y a pas assez de données pour vous conseiller")  



        except:
            
            add_suppr.label_15.setText("État du produit : Aucune")
            add_suppr.label_17.setText(f"Nombre restant : Aucune") 
     #####-------------------- add_stock_fc and btn------------------####
    def add_stock(self,currentproductid):
        add_suppr.pagesContainer.setCurrentWidget(add_suppr.add_stock)
        prodect_sale_list = cr.execute(f"select code_bare,nomb from prodect_sale WHERE code_bare ='{currentproductid}' ").fetchall()
        prodect_list = cr.execute(f"select BARRE,Stock,Stock_minimal,date_exp from prodect WHERE BARRE='{currentproductid}'").fetchall()
        prodect_sale_list_dec = {} 
        for cco in prodect_sale_list:
            prodect_sale_list_dec[cco[0]] = 0
        for cco in prodect_sale_list:
            prodect_sale_list_dec[cco[0]] += cco[1]
           
        try:
            add_suppr.lineEdit_10.setText(f"{prodect_sale_list_dec[currentproductid]}")      
        except:  
            add_suppr.lineEdit_10.setText("0") 
        try:
            add_suppr.lineEdit_9.setText(f"{prodect_list[0][1]}")


            add_suppr.lineEdit_17.setText(f"{int(prodect_list[0][1]) - int(add_suppr.lineEdit_10.text()) }") 

        except:
            add_suppr.lineEdit_9.setText("Aucune")
            add_suppr.lineEdit_17.setText("Aucune")     

        add_suppr.pushButton_15.clicked.connect(lambda : self.btn_add_stock(currentproductid,prodect_list))
    def btn_add_stock(self,currentproductid,prodect_list):
        add_nub = add_suppr.lineEdit_18.text()  
        if add_nub != "":
            try: 
                add_nub = int(add_nub)
                if prodect_list[0][1] != "NULL":
                    prodect_num = int(prodect_list[0][1])
                    add_nub +=  prodect_num

                cr.execute(f"UPDATE prodect SET Stock = '{add_nub}' WHERE BARRE = {currentproductid} ")
                db.commit()
                add_suppr.close()

            except:
                msg1=QMessageBox()
                #msg1.setIcon(QMessageBox.NoIcon)
                msg1.setText("Le numéro n'est pas reconnu         ")
                msg1.setInformativeText("Le champ doit contenir un entier, par exemple : 300, 400, 10")
                msg1.setWindowTitle("Erreur d'entrée")
                #msg1.setDetailedText("The details are as follows:")
                msg1.exec_()
        else:
            msg1=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msg1.setText("Le champ de saisie est vide         ")
            msg1.setInformativeText("Veuillez remplir le champ obligatoire avec le nombre de produits ajoutés")
            msg1.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg1.exec_()  
    ####------------------------ add_promo_price------------------------##
    def add_promo_price(self,currentproductid):
        add_suppr.pagesContainer.setCurrentWidget(add_suppr.addpromo)

        prodect_list = cr.execute(f"select BARRE,Prix_achat,Prix_vente,date_exp from prodect WHERE BARRE='{currentproductid}'").fetchall()

        add_suppr.lineEdit_11.setText(f"{prodect_list[0][1]}")
        if prodect_list[0][2] != "NULL":
            add_suppr.lineEdit_13.setText(f"{prodect_list[0][2]}")
        else:
            add_suppr.lineEdit_13.setText(f"NULL")
        add_suppr.lineEdit_16.setText(f"{DATE}")   
        add_suppr.lineEdit_12.textChanged.connect(self.text_changed)
        add_suppr.checkBox.toggled.connect(self.text_changed)
        add_suppr.pushButton_12.clicked.connect(lambda : self.add_promo_btn(currentproductid) )
        add_suppr.lineEdit_14.setPlaceholderText("2024-12-31")

    def text_changed(self):
        
        if add_suppr.checkBox.isChecked():
            porsentage = add_suppr.lineEdit_12.text()

            add_suppr.lineEdit_24.setText(f"Offre -{porsentage}%")
        else:
            old_price = add_suppr.lineEdit_11.text()
            new_price = add_suppr.lineEdit_12.text()
            try:
                porsentage = str(((float(old_price) - float(new_price)) / float(old_price)) * 100 )

                add_suppr.lineEdit_24.setText(f"Offre - {porsentage} %")
            except:
                add_suppr.lineEdit_24.setText(f"Offre -0%")
    def add_promo_btn(self,currentproductid):
        
        data_offre = cr.execute(f"select code_bar from prodect_offre WHERE code_bar='{currentproductid}'").fetchall()

        if data_offre == []:
            data_offre = ["this test","this test","this test"]

        if currentproductid != str(data_offre[0][0]):

            if add_suppr.lineEdit_12.text() != "":
                if add_suppr.checkBox.isChecked():
                    new_price = round (float(add_suppr.lineEdit_11.text())- (float(add_suppr.lineEdit_11.text()) / 100) * float(add_suppr.lineEdit_12.text())) 
                else:
                    new_price = add_suppr.lineEdit_12.text()   
                if add_suppr.lineEdit_16.text() != "":
                    offre_date = add_suppr.lineEdit_16.text()
                else:
                    offre_date = DATE
                if add_suppr.lineEdit_14.text() != "":
                    expiry_date = add_suppr.lineEdit_14.text()
                else:
                    expiry_date=  "NULL"   
                if add_suppr.lineEdit_15.text() != "":
                    quantity = add_suppr.lineEdit_15.text()
                else:
                    quantity = 0
                if add_suppr.lineEdit_23.text() != "": 
                    total_price = add_suppr.lineEdit_23.text()
                else:
                    total_price = "NULL" 
                offre_title= add_suppr.lineEdit_24.text() 
                if offre_date == str(DATE) :
                    offre_statut = "True"
                else:
                    offre_statut = "True"



                cr.execute(f"INSERT INTO prodect_offre('code_bar','offre','offre_date','expiry_date','quantity','new_price','total_price','offre_title','Offre_statut') VALUES ('{currentproductid}','Réduction De Prix','{offre_date}','{expiry_date}','{quantity}','{new_price}','{total_price}','{offre_title}','{offre_statut}')")
                db.commit()
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("La réduction a été enregistrée avec succès ")
                
                if offre_date == str(DATE) :
                    
                    
                    if expiry_date != "NULL" :
                        msg1.setInformativeText(f"La réduction commencera à partir d'aujourd'hui jusqu'au{expiry_date}")
                    else: 
                        msg1.setInformativeText("La réduction commencera à partir d'aujourd'hui Jusqu'à une durée indéterminée")   
                else : 
                    if expiry_date != "NULL" :
                        msg1.setInformativeText(f"La réduction commencera à partir {offre_date} jusqu'au{expiry_date}")
                    else: 
                        msg1.setInformativeText(f"La réduction commencera à partir {offre_date} Jusqu'à une durée indéterminée")   
                msg1.setWindowTitle("Complété avec succès")
                #msg1.setDetailedText("The details are as follows:")
                msg1.exec_()


            else:
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Critical)
                msg1.setText("Le champ obligatoire doit être rempli ")
                msg1.setInformativeText("Le nouveau champ de prix est obligatoire")
                msg1.setWindowTitle("Erreur d'entrée")
                #msg1.setDetailedText("The details are as follows:")
                msg1.exec_()
        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Critical)
            msg1.setText("Ce produit est déjà inscrit dans la liste des remises ")
            msg1.setInformativeText("Ce produit fait l'objet d'une remise, il n'est pas possible d'ajouter une autre remise")
            msg1.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg1.exec_()

    def supp_offre_auto(self):
        prodect_offre= cr.execute("select expiry_date from prodect_offre").fetchall()
        if prodect_offre == []:
            prodect_offre = ["NULL","NULL"]
        for x in prodect_offre:
            if x[0] == "NULL" :
                print(x[0])
            else:

                try:
                    dateofend =  datetime.strptime(x[0],'%Y-%m-%d').date()
                    

                    if dateofend <= DATE  :
                        dateofend = dateofend.strftime("%Y-%m-%d")
                        cr.execute(f"DELETE from prodect_offre WHERE expiry_date ='{str(dateofend)}' ")
                        db.commit()

                        

                        t=threading.Thread(target=lambda : toast.show_toast("La réduction est terminée","Il y a une réduction qui expire aujourd'hui",duration=20) )
                        t.start()
                except:
                    pass        
    def auto_activet_promo(self):
        prodect_offre= cr.execute("select offre_date,Offre_statut from prodect_offre").fetchall()

        if prodect_offre != []:
            
            for x in prodect_offre:
                try:
                    dateofstart =  datetime.strptime(x[0],'%Y-%m-%d').date() 
                    
                    statut = x[1]
                    if dateofstart <= DATE and statut == "True":
                        pass
                    elif dateofstart <= DATE and statut == "False":
                        
                        
                        dateofstart = dateofstart.strftime("%Y-%m-%d")
                        print(dateofstart)
                        

                        cr.execute(f"UPDATE prodect_offre SET Offre_statut ='True'  WHERE offre_date = '{str(dateofstart)}' ")
                        
                        

                        db.commit()
                        t1=threading.Thread(target=lambda : toast.show_toast("Il y a une réduction à partir d'aujourd'hui être prêt",duration=40,msg="être prêt") )
                        t1.start()



                except:
                    pass   

            
           

                        
   ##### -------------------- add_promo_quantité ------------------------####
    def add_promo_qua(self,currentproductid):
        add_suppr.pagesContainer.setCurrentWidget(add_suppr.page_2)
        prodect_list = cr.execute(f"select BARRE,Prix_achat,Prix_vente,date_exp from prodect WHERE BARRE='{currentproductid}'").fetchall()
        add_suppr.lineEdit_25.setText(f"{prodect_list[0][2]}")
        add_suppr.lineEdit_19.setText(f"{prodect_list[0][1]}")
        add_suppr.lineEdit_22.setText(f"{DATE}") 
        add_suppr.lineEdit_21.setText(f"1")
        add_suppr.lineEdit_26.setPlaceholderText("2024-12-31")
        add_suppr.lineEdit_28.setPlaceholderText("Ex : 4 +  (1 Gratuit) ")
        add_suppr.lineEdit_20.textChanged.connect(self.add_promo_qua_text_change)
        add_suppr.lineEdit_21.textChanged.connect(self.add_promo_qua_text_change)
        add_suppr.pushButton_17.clicked.connect(lambda: self.add_promo_qua_btn(currentproductid))
    def add_promo_qua_text_change(self):
        free_piece = add_suppr.lineEdit_20.text()
        piece_oblg = add_suppr.lineEdit_21.text()
        if piece_oblg == "" or piece_oblg==0 or piece_oblg== 1:
            piece_oblg = 1
        if free_piece == "" or piece_oblg==0 or piece_oblg== 1:
            free_piece = 0     

        add_suppr.lineEdit_28.setText(f"{piece_oblg} + ({free_piece} Gratuit ) ")
    def add_promo_qua_btn(self,currentproductid):
        
        data_offre = cr.execute(f"select code_bar from prodect_offre WHERE code_bar='{currentproductid}'").fetchall()
        if data_offre == []:
            data_offre = ["this test","this test","this test"]

        if currentproductid != str(data_offre[0][0]):
                
            if add_suppr.lineEdit_20.text() != "":
                free_piece = add_suppr.lineEdit_20.text()
  
                if add_suppr.lineEdit_22.text() != "":
                    offre_date = add_suppr.lineEdit_22.text()
                else:
                    offre_date = DATE
                if add_suppr.lineEdit_26.text() != "":
                    expiry_date = add_suppr.lineEdit_26.text()
                else:
                    expiry_date=  "NULL"   
                if add_suppr.lineEdit_21.text() != "":
                    quantity = add_suppr.lineEdit_21.text()
                else:
                    quantity = 0

                offre_title= add_suppr.lineEdit_28.text() 
                if offre_date == str(DATE) :
                    offre_statut = "True"
                else:
                    offre_statut = "False"


                cr.execute(f"INSERT INTO prodect_offre('code_bar','offre','offre_date','expiry_date','quantity','new_price','offre_title','Offre_statut') VALUES ('{currentproductid}','Réduction de quantité','{offre_date}','{expiry_date}','{quantity}','{free_piece}','{offre_title}','{offre_statut}')")
                print(currentproductid)
                db.commit()
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("La réduction a été enregistrée avec succès ")
                
                if offre_date == str(DATE) :
                    
                    
                    if expiry_date != "NULL" :
                        msg1.setInformativeText(f"La réduction commencera à partir d'aujourd'hui jusqu'au{expiry_date}")
                    else: 
                        msg1.setInformativeText("La réduction commencera à partir d'aujourd'hui Jusqu'à une durée indéterminée")   
                else : 
                    if expiry_date != "NULL" :
                        msg1.setInformativeText(f"La réduction commencera à partir {offre_date} jusqu'au{expiry_date}")
                    else: 
                        msg1.setInformativeText(f"La réduction commencera à partir {offre_date} Jusqu'à une durée indéterminée")   
                msg1.setWindowTitle("Complété avec succès")
                #msg1.setDetailedText("The details are as follows:")
                msg1.exec_()


            else:
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Critical)
                msg1.setText("Le champ obligatoire doit être rempli ")
                msg1.setInformativeText("Le nouveau champ de prix est obligatoire")
                msg1.setWindowTitle("Erreur d'entrée")
                #msg1.setDetailedText("The details are as follows:")
                msg1.exec_()
        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Critical)
            msg1.setText("Ce produit est déjà inscrit dans la liste des remises ")
            msg1.setInformativeText("Ce produit fait l'objet d'une remise, il n'est pas possible d'ajouter une autre remise")
            msg1.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg1.exec_()        

            

    ## -------------------------point_calc-----------------------------------------------------#  
    def point(self,h1):

        points = cr.execute(f"select Points from prodect WHERE BARRE='{h1}'").fetchall()
        if points[0][0] != "NULL" and points[0][0] != None :
            self.N_point += points[0][0]
        else:
            self.N_point += 0 

        widgets.label_5.setText(f"{self.N_point} Point")      
    ## -------------------------add_point_for_user-----------------------------------------------------#  
    def add_point_cart(self):
        N_cart = widgets.lineEdit_4.text()
        id_cart = cr.execute(f"SELECT Cart_id,Points from fidelity_cart WHERE Cart_id='{N_cart}' ").fetchall()
        if id_cart != []:
            toutal_point = id_cart[0][1] + self.N_point
            cr.execute(f"UPDATE fidelity_cart SET Points = '{toutal_point}'  WHERE Cart_id='{N_cart}'  ")
            db.commit()
            widgets.lineEdit_4.setText("")
            widgets.label_5.setText("0 point")
        else:
            msg1=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msg1.setText("Il n'y a pas de carte avec ce numéro        ")
            msg1.setInformativeText("Il semble que la carte appartienne à un autre magasin, soit expirée ou ne soit pas répertoriée dans la base de données")
            msg1.setWindowTitle("Erreur d'entrée")
            #msg1.setDetailedText("The details are as follows:")
            msg1.exec_()
    #### -------------------------Pay by points----------------------------#############
    def pay_by_points(self):
        poro.stackedWidget.setCurrentWidget(poro.Cart)
        poro.cart_id.returnPressed.connect(self.cart_info)
       
    def cart_info(self):
        if poro.cart_id.text() != "":
            id_cart = cr.execute(f"SELECT Cart_id,Points from fidelity_cart WHERE Cart_id='{poro.cart_id.text()}' ").fetchall()
            if id_cart != []:
                N_point = id_cart[0][1]
                poro.label_3.setText(f"Le nombre de points de la carte  : {N_point} ")
                if N_point < point_param[0] :
                    poro.label_5.setText("Données de la carte  :  N'a pas dépassé le paiement minimum")
                else:
                    poro.label_5.setText("Données de la carte  :  Utilisable")

                poro.label_4.setText(f"Valeur des points en millimètres  : {N_point * point_param[1]} ") 
                point_to_tnd = N_point * point_param[1]
                if point_to_tnd >= self.prixtoutal:
                    poro.label_6.setText(f"Points restants  : {(point_to_tnd - self.prixtoutal)/point_param[1] } ")
                    x = (point_to_tnd - self.prixtoutal)/point_param[1]
                    y = poro.cart_id.text()
                    poro.label_7.setText(f"Doit compléter le montant : 0 ") 
                    poro.pushButton_9.clicked.connect(lambda : self.btn_point(x,y))
                else:
                    poro.label_6.setText(f"Points restants  : 0 ")
                    poro.label_7.setText(f"Doit compléter le montant : {self.prixtoutal-point_to_tnd} ")
                    y = poro.cart_id.text()
                    poro.pushButton_9.clicked.connect(lambda : self.btn_point(0,y))
    def btn_point(self,x,y):
        cr.execute(f"UPDATE fidelity_cart set Points ='{x}' WHERE Cart_id = '{y}'")
        db.commit()
        self.save_sale("Points")

    #### -------------------------- Pay_credit -----------------------------------#####
    etat_cart = False
    def credit_screen(self):
        poro.stackedWidget.setCurrentWidget(poro.Credit) 
        list_name_clien = []
        list_name_clien_db = cr.execute("select Name_Clien from Credit_Cart").fetchall()
        for x in list_name_clien_db:
            list_name_clien.append (x[0])
        list_name_clien.append("Ajouter Client")    
        poro.comboBox.addItems(list_name_clien)
        poro.lineEdit_2.setText(f"{self.prixtoutal}") 
        #---------------------------------------------------------------
        poro.lineEdit.returnPressed.connect(lambda : self.id_carte("1"))
        poro.comboBox.currentTextChanged.connect(lambda : self.id_carte("2")) 
        
        poro.pushButton_9.clicked.connect(self.btn_credit)
        poro.lineEdit_2.textChanged.connect(lambda : self.id_carte("2"))
         
    def id_carte(self,x):
        if poro.lineEdit.text() != "" or x == "2":
            if x == "1":
                h1 = poro.lineEdit.text()
                cart_clien = cr.execute(f"select N_cart,Name_Clien,Max_credit,Credit from Credit_Cart WHERE N_cart = '{h1}' ").fetchall()
                
            elif x == "2":
                h1 = poro.comboBox.currentText()
                cart_clien = cr.execute(f"select N_cart,Name_Clien,Max_credit,Credit from Credit_Cart WHERE Name_Clien = '{h1}' ").fetchall()   
            if cart_clien != []:
                poro.comboBox.setCurrentText(str(cart_clien[0][1]))
                poro.lineEdit.setText(str(cart_clien[0][0]))
                last_credit = cart_clien[0][3]
                if cart_clien[0][2] !="NULL":
                    Max_credit = float(cart_clien[0][2])
                try:
                    prex_add = float(poro.lineEdit_2.text())
                except:
                    prex_add = float(0)  
            
                New_credit = prex_add + float(last_credit)

                if cart_clien[0][2] !="NULL":
                    if last_credit != Max_credit:
                        if New_credit <= Max_credit:
                            poro.label_13.setText("État de la carte  : Disponible")
                            self.etat_cart = True

                        else:
                            poro.label_13.setText("État de la carte  : Il n'est pas possible d'ajouter le montant total")
                            self.etat_cart = False

                    else:
                        poro.label_13.setText("État de la carte  : Cette carte a atteint la limite d'endettement maximale")
                        self.etat_cart = False
                    poro.label_9.setText(f"Le montant de la dette antérieure : {last_credit}") 
                    poro.label_11.setText(f"Le montant total de la dette : {New_credit}")  
            else:
                #####-----------This message appears if the card code does not exist in the database
                msg1=QMessageBox()
                #msg1.setIcon(QMessageBox.NoIcon)
                msg1.setText("Cette carte n'est pas enregistrée         ")
                msg1.setInformativeText("Cette carte n'est pas disponible ou a été traitée")
                msg1.setWindowTitle("Erreur d'entrée")
                msg1.exec_()

        else:
            pass
    def btn_credit(self):
        if self.etat_cart == True:
            h1 = poro.lineEdit.text()
            cart_clien = cr.execute(f"select N_cart,Name_Clien,Max_credit,Credit from Credit_Cart WHERE N_cart= '{h1}' ").fetchall()  
            
            last_credit = cart_clien[0][3]
            New_credit = float(poro.lineEdit_2.text()) + float(last_credit)

            
            cr.execute(f"UPDATE Credit_cart SET Credit = '{New_credit}' WHERE N_cart = '{h1}' ")
            

            db.commit()
            self.save_sale("Credit")
            
            
            


        else:
            msg1=QMessageBox()
            #msg1.setIcon(QMessageBox.NoIcon)
            msg1.setText("Aucune information de carte valide         ")
            msg1.setInformativeText("Veuillez insérer une carte de débit valide ou choisir un autre mode de paiement")
            msg1.setWindowTitle("Erreur d'entrée")
            msg1.exec_()
    ##### --------------------------- Tecket_Pay  ---------------- ####

    #### ------------------------------ D17 --------------------###
    def d17 (self):
        poro.stackedWidget.setCurrentWidget(poro.d17) 
        
        poro.pushButton_9.clicked.connect(lambda : self.save_sale("D17") )
    ### ------------------------------- Big  anylse  ------------- ####
    def big_any(self,date):
        if date == "all":
            prodect_sale_code = cr.execute("select DISTINCT code_bare from prodect_sale").fetchall()
            Revenu = cr.execute("select prix_total,nomb from prodect_sale")
            Revenu_total = 0
            nomb_sale = 0 
            prodect_rupture = []
            prodect_ex = []

            if Revenu != []:
                for x in Revenu:
                    Revenu_total += float(x[0])
                    
                    nomb_sale += int(x[1])


                widgets.label_31.setText(f"{Revenu_total} TND") 
                widgets.label_39.setText(str(nomb_sale))
            produit_in_stock = len(cr.execute("select nom from prodect").fetchall())
            widgets.label_40.setText(str(produit_in_stock))
            ######## ////////////// out of stock //////////////// ######

                # ---- "Expired products out of stock are recorded in the variable '
                # prodect_rupture' with the title'Bientot rupture de stock/En rupture de stock'"
            if prodect_sale_code != []:
                numb_prodct_sale = 0
                for y in prodect_sale_code:
                     
                    instock = cr.execute(f"select Stock,Stock_minimal,Nom from prodect WHERE BARRE ='{y[0]}' ").fetchall()
                    if instock !=[]:
                        if instock[0][0] !="NULL":
                            nom_de_prodect = instock[0][2]
                            numb_sale = cr.execute(f"select nomb from prodect_sale WHERE code_bare ='{y[0]}'")
                            for c in numb_sale: 
                                numb_prodct_sale += int(c[0])
                            numb_rest = int(instock[0][0]) -  numb_prodct_sale  
                            ####### soon out of stock by minstock 
                            if instock[0][1] != "NULL" and instock[0][1] != None:

                                if numb_rest <= int(instock[0][1]) and numb_rest > 0:
                                    prodect_rupture.append((nom_de_prodect,y[0],numb_rest,"Bientot rupture de stock"))
                                ####### out of stock by minstock
                                elif numb_rest <= int(instock[0][1]) and numb_rest <= 0:
                                    prodect_rupture.append((nom_de_prodect,y[0],numb_rest,"En rupture de stock"))
                            ####### soon out of stock auto         
                            else :
                                if numb_rest <= 30 and numb_rest > 0:
                                    prodect_rupture.append((nom_de_prodect,y[0],numb_rest,"Bientot rupture de stock"))
                                ####### out of stock by auto
                                elif numb_rest <= 0:
                                    prodect_rupture.append((nom_de_prodect,y[0],numb_rest,"En rupture de stock"))  
                        #####print GUI
                        if len(prodect_rupture) != 0:
                            print(prodect_rupture)
                            widgets.label_48.setText(str(len(prodect_rupture)))
                #  ---------- Table -------#
                """
                while widgets.tableWidget_2.rowCount() > 0:
                    widgets.tableWidget_2.removeRow(0)
                for row_index,row_data in enumerate(prodect_rupture):
                    widgets.tableWidget_2.insertRow(row_index)
                    for colm_index , colm_data in enumerate(row_data):
                        widgets.tableWidget_2.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))
                """


            ######## ////////////// Expired //////////////////// ###### 
            # ---- "Expired products out of stock are recorded in the variable '
            # prodect_ex' with the title'Expiré/Expiré Bientot'"               
            all_prodect = cr.execute("select BARRE,Date_exp from prodect")
            
            try:
                for a in all_prodect:
                    if a[1] != "NULL":
                        date_time_obj = datetime.strptime(a[1] , '%d-%m-%Y').date()
                        
                        if date_time_obj <= (DATE + timedelta(days =10)) :
                            if date_time_obj <= DATE:
                                prodect_ex.append((a[0],a[1],"Expiré"))
                            else : 
                                prodect_ex.append((a[0],a[1],"Expiré Bientot")) 
                #### print GUI
                widgets.label_45.setText(str(len(prodect_ex)))
            except:
                pass
          

            #### //////////////////// Nombre de clients emprunteurs ////////// ###
            credit =  cr.execute("select N_cart,Pyment_date,App_surplus,Max_credit,Credit from Credit_Cart")
            len_credit = 0
            montant_toutal = 0
            pass_limit = []
            for a1 in credit:
                len_credit +=1
                credit_mont = a1[4]
                
                
 
                

                montant_toutal += float(credit_mont)

                if a1[3] != "NULL" and a1[3] != None :
                    if float(a1[4])>= float(a1[3]):
                        pass_limit.append((a1[0],a1[3],a1[4]))




            widgets.label_37.setText(str(len_credit))  
            widgets.label_35.setText(f"{montant_toutal} TND" )


            ##### ////////////// Retour /////////////////////////////////###

            retour_list = cr.execute("select * from Retoure").fetchall()
            
            widgets.label_43.setText(str(len(retour_list)))


            ### /////////////////////// D17 STAT //////////////// ####

            ######################## dep
            dep = cr.execute("select PRIX from dépenses").fetchall()
            dep_mont = 0
            if dep != [] and dep != None:
                for dd in dep:
                    dep_mont+=float(dd[0])
            widgets.label_32.setText(f"{dep_mont} TND")        

   ##### ----------------- add card Credit -------------------------- ####
    def save_cart_credit(self):
        if widgets.lineEdit_5.text() !="" and widgets.lineEdit_10.text() :
            
            N_cart = widgets.lineEdit_10.text()
            name= widgets.lineEdit_5.text()
            pra = 0
            if widgets.lineEdit_7.text() != "":
                payment_date = widgets.lineEdit_7.text()
                pra =+ 1
            else:
                payment_date = "NULL"
            if widgets.lineEdit_8.text() != "":
                Sur_plus = widgets.lineEdit_8.text()
            else:
               Sur_plus = "NULL"  
            if widgets.lineEdit_9.text() != "":
                max_credit = widgets.lineEdit_9.text()
               
            else:
                max_credit = "NULL"       

            tax_retart = "NULL" 
            if widgets.lineEdit_12.text() != "":
                n_phone = widgets.lineEdit_12.text()
                
            else:
                n_phone = "NULL"
            if widgets.lineEdit_19.text() != "":
                email = widgets.lineEdit_19.text()
            else :
                email = "NULL" 
                
            if pra == 3 or pra == 0 or pra == 1 :
                data_id = cr.execute(f"SELECT N_cart from Credit_Cart WHERE N_cart = '{N_cart}'").fetchall()
                if data_id ==[] :
                    cr.execute(f"INSERT INTO Credit_Cart (N_cart,Name_clien,Number,Email,Pyment_date,Surplus,Max_Credit,Credit) VALUES ('{N_cart}','{name}','{n_phone}','{email}','{payment_date}','{Sur_plus}','{max_credit}','0') ")  
                    db.commit()
                    ### msg suc
                    msg1=QMessageBox()
                    msg1.setIcon(QMessageBox.NoIcon)
                    msg1.setText("enregistré avec succès ") 
                    msg1.exec_() 
                    pass
                else:
                    msg1=QMessageBox()
                    msg1.setIcon(QMessageBox.Information)
                    msg1.setText("Le numéro de carte semble être identique au numéro d'une autre carte pré-enregistrée ") 
                    msg1.exec_()     
            else:
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("Pour préciser les taxes de retard, le champ Date de paiement doit être renseigné ") 
                msg1.exec_()
        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Les champs obligatoires doivent être remplis 'Nom du client' - 'ID Cart' ")
            msg1.exec_()             
    def list_clien_credit(self):
        list_name_clien = []
        info_clien=[]
        list_name_clien_db = cr.execute("select Name_Clien,N_cart,Surplus,Max_credit,Credit from Credit_Cart").fetchall()
        list_name_clien.append ('TOUT')
        for x in list_name_clien_db:

            list_name_clien.append (x[0])
            info_clien.append(x)

           
        widgets.comboBox_5.addItems(list_name_clien)

        ### ------- table --------
        while widgets.tableWidget_5.rowCount() > 0:
            widgets.tableWidget_5.removeRow(0)
        for row_index,row_data in enumerate(info_clien):
            widgets.tableWidget_5.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableWidget_5.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))
    def fetch_clien_credi(self,x):
        info_clien = []
        if x == "bar" :
            a = widgets.lineEdit_3.text()   
            if a != "":
                list_name_clien_db = cr.execute(f"select Name_Clien,N_cart,Surplus,Max_credit,Credit from Credit_Cart WHERE N_cart ='{a}' ").fetchall() 
            else: 
                list_name_clien_db = cr.execute(f"select Name_Clien,N_cart,Surplus,Max_credit,Credit from Credit_Cart ").fetchall()   
        elif x == "name":
            a = widgets.comboBox_5.currentText()
            if a != "TOUT":
                list_name_clien_db = cr.execute(f"select Name_Clien,N_cart,Surplus,Max_credit,Credit from Credit_Cart WHERE Name_Clien ='{a}' ").fetchall()
            else:
                list_name_clien_db = cr.execute(f"select Name_Clien,N_cart,Surplus,Max_credit,Credit from Credit_Cart  ").fetchall()

        for x in list_name_clien_db:

            info_clien.append(x)

        ### ------- table --------
        while widgets.tableWidget_5.rowCount() > 0:
            widgets.tableWidget_5.removeRow(0)
        for row_index,row_data in enumerate(info_clien):
            widgets.tableWidget_5.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableWidget_5.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))               
    def cart_payy(self):
        row = widgets.tableWidget_5.currentRow()
        currentproductid = (widgets.tableWidget_5.item(row, 1).text() )
        list_name_clien = cr.execute(f"select Name_Clien,N_cart,Surplus,Max_credit,Credit from Credit_Cart WHERE N_cart = '{currentproductid}' ").fetchall()
        widgets.lineEdit_6.setText(f"{list_name_clien[0][0]}")
        widgets.lineEdit_15.setText(f"{list_name_clien[0][1]}")
        widgets.lineEdit_21.setText(f"{list_name_clien[0][4]}")
        if list_name_clien[0][2] == "NULL" or list_name_clien[0][2] == None :
            r = 0
        else : 
            r = list_name_clien[0][2]  
        widgets.lineEdit_23.setText(f"{r}")  

        if widgets.checkBox_3.isChecked():
            widgets.lineEdit_24.setText()
        widgets.lineEdit_24.setText(str(list_name_clien[0][4]))    


        widgets.lineEdit_25.textChanged.connect(lambda : widgets.lineEdit_26.setText(f"{float(widgets.lineEdit_24.text()) - float(widgets.lineEdit_25.text()) }"))

  

        widgets.stackedWidget_2.setCurrentWidget(widgets.page_4)
        widgets.pushButton_18.clicked.connect(self.delet_clien)
    def open_add_cart_credit_screen(self):
        widgets.checkBox_3.toggled.connect(self.surplus)

        widgets.pushButton_15.clicked.connect(lambda :self.auto_code(widgets.lineEdit_10,"long") )
        widgets.pushButton_13.clicked.connect(self.save_cart_credit)
        self.list_clien_credit()
        widgets.tableWidget_5.doubleClicked.connect(self.cart_payy)


        widgets.lineEdit_5.textChanged.connect(lambda : widgets.label_79.setText(widgets.lineEdit_5.text()))
        widgets.lineEdit_10.textChanged.connect(lambda : widgets.label_86.setText(widgets.lineEdit_10.text()))

        widgets.lineEdit_7.textChanged.connect(lambda : widgets.label_87.setText(widgets.lineEdit_7.text()))


        widgets.lineEdit_3.returnPressed.connect(lambda : self.fetch_clien_credi("bar"))
        widgets.comboBox_5.currentTextChanged.connect(lambda :  self.fetch_clien_credi("name") ) 
        widgets.pushButton_23.clicked.connect(lambda : widgets.stackedWidget_2.setCurrentWidget(widgets.page_3)) 
        widgets.stackedWidget.setCurrentWidget(widgets.page)
        widgets.stackedWidget_2.setCurrentWidget(widgets.page_2)


        widgets.pushButton_14.clicked.connect(lambda : widgets.stackedWidget_2.setCurrentWidget(widgets.page_2) )
        widgets.pushButton_16.clicked.connect(lambda : widgets.stackedWidget_2.setCurrentWidget(widgets.page_2) )
        widgets.pushButton_26.clicked.connect(self.exportToExcel_credit)


        widgets.pushButton_24.clicked.connect(lambda : widgets.stackedWidget.setCurrentWidget(widgets.Outic))  

        widgets.pushButton_17.clicked.connect(self.payment_credit)            
        
    def delet_clien(self):
        x = widgets.lineEdit_15.text()

        cr.execute(f"DELETE FROM Credit_Cart WHERE N_cart='{x}'")
        db.commit()  
        widgets.stackedWidget_2.setCurrentWidget(widgets.page_2)
        self.list_clien_credit()
    def surplus (self):
        if widgets.checkBox_3.isChecked():
            toutal = float(widgets.lineEdit_23.text())+ float(widgets.lineEdit_21.text())
            widgets.lineEdit_24.setText(str(toutal))
        else :
            toutal =  float(widgets.lineEdit_21.text())
            widgets.lineEdit_24.setText(str(toutal))
    def payment_credit(self):
        id = widgets.lineEdit_15.text()
        cr.execute(f"UPDATE Credit_Cart SET App_surplus ='0',Credit='{widgets.lineEdit_26.text()}' WHERE N_cart = '{id}'")
        db.commit()
        widgets.pushButton_14.clicked.connect(lambda : widgets.stackedWidget_2.setCurrentWidget(widgets.page_2) )
    def exportToExcel_credit(self):
     
        columnHeaders = []

        # create column header list
        for j in range(widgets.tableWidget_5.model().columnCount()):
            columnHeaders.append(widgets.tableWidget_5.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columnHeaders)

        # create dataframe object recordset
        for row in range(widgets.tableWidget_5.rowCount()):
            for col in range(widgets.tableWidget_5.columnCount()):
                df.at[row, columnHeaders[col]] = widgets.tableWidget_5.item(row, col).text()
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File',".xlsx", "DOC (*.xml *.xlsx)")[0]
        except:
            pass  

    
        if name != "":
            df.to_excel(name, index=False)
        else :
            df.to_excel(f"{DATE}.xlsx", index=False)     

   #### -------------------------- auto_code -------------------------####
    def auto_code(self,x,y):
        if y == "long":
            gen = random.randint(10000000000, 999999999999) 
            x.setText(f"{gen}")
        else:
            gen = random.randint(100000, 999999) 
            x.setText(f"{gen}")

   ########### --------------- outic screen -----------------###
    def Ajouter_dépenses_screen(self):
        if self.acc_Dep:
            widgets.stackedWidget.setCurrentWidget(widgets.page_5)
            dépenè_db = cr.execute("SELECT * FROM dépenses")
            dépenè_list=[]
            Toutal = 0
            for x in dépenè_db:
                dépenè_list.append(x)
                Toutal += float(x[1])
            widgets.label_89.setText(f"Total :  {Toutal} TND")    

            ### ------- table --------
            while widgets.tableWidget_6.rowCount() > 0:
                widgets.tableWidget_6.removeRow(0)
            for row_index,row_data in enumerate(dépenè_list):
                widgets.tableWidget_6.insertRow(row_index)
                for colm_index , colm_data in enumerate(row_data):
                    widgets.tableWidget_6.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))  
            widgets.lineEdit_11.setText(str(DATE))
            widgets.lineEdit_11.setInputMask("0000-00-00") 
            widgets.pushButton_20.clicked.connect(self.conf_Ajouter_dépenses)
            widgets.pushButton_21.clicked.connect(lambda : widgets.stackedWidget.setCurrentWidget(widgets.Outic))
            widgets.tableWidget_6.doubleClicked.connect(self.supp_dep)
            #### --------- filtre 
            widgets.comboBox_6.currentTextChanged.connect(self.date_filtre_dep)
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()                 
    def date_filtre_dep(self):
        y = widgets.comboBox_6.currentText()
        if y == "Filtre":
            dépenè_db = cr.execute(f"SELECT * FROM dépenses ")
        if y == "Aujourd'hui":
            dépenè_db = cr.execute(f"SELECT * FROM dépenses WHERE DATE ='{DATE}'")
        elif y =="Semaine":
            dépenè_db = cr.execute(f"SELECT * FROM dépenses WHERE DATE IN {tuple(list_date_week)}  ")
        elif y =="Mois":
            dépenè_db = cr.execute(f"SELECT * FROM dépenses WHERE DATE IN {tuple(list_date_month)}  ")  
        elif y =="Année":
            dépenè_db = cr.execute(f"SELECT * FROM dépenses WHERE DATE IN {tuple(list_date_years)}  ")              


        dépenè_list=[]
        Toutal = 0
        for x in dépenè_db:
            dépenè_list.append(x)
            Toutal += float(x[1])
        widgets.label_89.setText(f"Total :  {Toutal} TND")    

        ### ------- table --------
        while widgets.tableWidget_6.rowCount() > 0:
            widgets.tableWidget_6.removeRow(0)
        for row_index,row_data in enumerate(dépenè_list):
            widgets.tableWidget_6.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableWidget_6.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))  
        widgets.lineEdit_11.setText(str(DATE))
        widgets.lineEdit_11.setInputMask("0000-00-00") 
        widgets.pushButton_20.clicked.connect(self.conf_Ajouter_dépenses)
        widgets.pushButton_21.clicked.connect(lambda : widgets.stackedWidget.setCurrentWidget(widgets.Outic))
        widgets.tableWidget_6.doubleClicked.connect(self.supp_dep)
    def conf_Ajouter_dépenses(self):
        if widgets.lineEdit_11.text() !="":
            date = widgets.lineEdit_11.text()
        else :
            date = str(DATE)   
        if widgets.lineEdit_14.text() !="":
            note = widgets.lineEdit_14.text()
        else :
            note = "NULL"    
        if widgets.lineEdit_13.text() !='':
            prix = widgets.lineEdit_13.text() 
            cr.execute(f"insert into dépenses (DATE,PRIX,Note) values ('{date}','{prix}','{note}') ")
            db.commit()
            self.Ajouter_dépenses_screen()

            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("            Enregistré avec succès      ") 
            msg1.exec_() 

        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("  Le champ obligatoire doit être rempli   ") 
            msg1.exec_()  
            pass   
    def supp_dep(self):
        row = widgets.tableWidget_6.currentRow()
        curdate = (widgets.tableWidget_6.item(row,0).text() )
        curment = (widgets.tableWidget_6.item(row,1).text() )
        note = (widgets.tableWidget_6.item(row,2).text() )
        print(curdate , curment , note )
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)
        msgBox.setButtonText(QMessageBox.Apply  ,"Suppr")
        msgBox.setButtonText(QMessageBox.Cancel  ,"Exit")
        msgBox.setButtonText
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec_()
        if ret == QMessageBox.Apply :
            cr.execute(f"DELETE FROM dépenses WHERE DATE ='{curdate}' and PRIX ='{curment}' and Note = '{note}'")
            db.commit()
            self.Ajouter_dépenses_screen()
            
   
           
       ### ------------- task ------------####
    def task_show(self):
        tasksc.setupUi(tasksc)
        tasksc.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        tasksc.saveButton.clicked.connect(self.saveChanges)
        tasksc.addButton.clicked.connect(self.addNewTask)
        tasksc.show()
    def calendarDateChanged(self):
        dateSelected = tasksc.calendarWidget.selectedDate().toPython()
        self.updateTaskList(dateSelected)        
    def updateTaskList(self, date):
        tasksc.tasksListWidget.clear()



        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cr.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            tasksc.tasksListWidget.addItem(item)        
    def saveChanges(self):

        date = tasksc.calendarWidget.selectedDate().toPython()

        for i in range(tasksc.tasksListWidget.count()):
            item = tasksc.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cr.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec() 
    def addNewTask(self):
   

        newTask = str(tasksc.taskLineEdit.text())
        if newTask != "":
            date = tasksc.calendarWidget.selectedDate().toPython()

            query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
            row = (newTask, "NO", date,)

            cr.execute(query, row)
            db.commit()
            self.updateTaskList(date)
            tasksc.taskLineEdit.clear()
      ### ------------ /task ------------##
      ### ----------- retoure screen ----------- ###
    def retour_prodect_screen(self):
        if self.acc_Ret:
            retoursc.setupUi(retoursc)
            retoursc.dateEdit.setDate(DATE)
            retoursc.saveButton.clicked.connect(self.save_retour)
            retoursc.show()
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()                       
    def save_retour(self):
        if retoursc.lineEdit_31.text() != "" :
            id_prodect = retoursc.lineEdit_31.text()
            validator_prodect = cr.execute(f"SELECT Nom from prodect WHERE BARRE = '{id_prodect}'").fetchall()
            if validator_prodect != []:
                nom = validator_prodect[0][0]
                date = retoursc.dateEdit.text() 
                Qunt = retoursc.spinBox.text()
                Recov = retoursc.comboBox_7.currentText()
                act = retoursc.comboBox_8.currentText()
                if retoursc.lineEdit_34.text() !="":
                    Raison = retoursc.lineEdit_34.text()
                else:
                    Raison = "Inconnu"
                cr.execute(f"Insert into Retoure (Code_barre,Nom,Date_retoure,Quantity,Cas,Recovery,Act) Values ('{id_prodect}','{nom}','{date}','{Qunt}','{Raison}','{Recov}','{act}') ") 
                db.commit() 
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("            Enregistré avec succès      ") 
                msg1.exec_()                      
            else:
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText(" Il semble que le produit retourné ne soit pas répertorié dans la base de données ou n'appartient pas à votre boutique") 
                msg1.exec_()  
        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Le produit doit être entré") 
            msg1.exec_()             
      ### --------------- /retour screen ------- ###
      #### ----------- Donneé clien --------------###
    def Donnee_clien_screen(self):
        if self.acc_Donn:
            dataclien_credit_db = cr.execute("SELECT Name_Clien,Number,Email from Credit_Cart ").fetchall()
            dataclien_fidelity_db = cr.execute("SELECT Name,Numbre,Email from fidelity_cart ").fetchall()
            dataclien = []
            name_list = []
            if dataclien_credit_db != []:
                for x in dataclien_credit_db :
                    dataclien.append((x[0],x[1],x[2]))  
                    name_list.append(x[0]) 
            
            if dataclien_fidelity_db != []:    
                for y in dataclien_fidelity_db :    
                    dataclien.append((y[0],y[1],y[2])) 
                    name_list.append(y[0])
                

            ### ------- table --------
            while donnee_clien.tableWidget.rowCount() > 0:
                donnee_clien.tableWidget.removeRow(0)
            for row_index,row_data in enumerate(dataclien):
                donnee_clien.tableWidget.insertRow(row_index)
                for colm_index , colm_data in enumerate(row_data):
                    donnee_clien.tableWidget.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data))) 


            
            donnee_clien.comboBox.addItems(name_list)
            donnee_clien.comboBox.currentTextChanged.connect(lambda : self.donnee_clien_fetch("name"))
            donnee_clien.lineEdit.returnPressed.connect(lambda : self.donnee_clien_fetch("code") )
            donnee_clien.comboBox_2.currentTextChanged.connect(lambda : self.donnee_clien_fetch("cat"))
            
            
            donnee_clien.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            
            
            donnee_clien.show()
            donnee_clien.activateWindow() 
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()           
            
    def donnee_clien_fetch(self,y):
        if y == "name":
            name = donnee_clien.comboBox.currentText()
            dataclien_credit_db = cr.execute(f"SELECT Name_Clien,Number,Email from Credit_Cart WHERE Name_Clien=('{name}')   ").fetchall()
            dataclien_fidelity_db = cr.execute(f"SELECT Name,Numbre,Email from fidelity_cart WHERE Name =('{name}') ").fetchall()
        elif y == "code":
            name = donnee_clien.lineEdit.text()
            dataclien_credit_db = cr.execute(f"SELECT Name_Clien,Number,Email from Credit_Cart WHERE Name_Clien=('{name}')   ").fetchall()
            dataclien_fidelity_db = cr.execute(f"SELECT Name,Numbre,Email from fidelity_cart WHERE Name =('{name}') ").fetchall()   
        elif y == "cat" :
            if donnee_clien.comboBox_2.currentText() =="Credit":
                dataclien_fidelity_db =[]
                dataclien_credit_db = cr.execute(f"SELECT Name_Clien,Number,Email from Credit_Cart  ").fetchall()
            elif donnee_clien.comboBox_2.currentText() =="Fidelity":
                dataclien_credit_db = []
                dataclien_fidelity_db = cr.execute(f"SELECT Name,Numbre,Email from fidelity_cart  ").fetchall() 
            else :
                dataclien_credit_db = cr.execute("SELECT Name_Clien,Number,Email from Credit_Cart ").fetchall()
                dataclien_fidelity_db = cr.execute("SELECT Name,Numbre,Email from fidelity_cart ").fetchall()            





        dataclien = []
        
        if dataclien_credit_db != []:
            for x in dataclien_credit_db :
                dataclien.append((x[0],x[1],x[2]))  
                
        
        if dataclien_fidelity_db != []:    
            for y in dataclien_fidelity_db :    
                dataclien.append((y[0],y[1],y[2])) 
                
            

        ### ------- table --------
        while donnee_clien.tableWidget.rowCount() > 0:
            donnee_clien.tableWidget.removeRow(0)
        for row_index,row_data in enumerate(dataclien):
            donnee_clien.tableWidget.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                donnee_clien.tableWidget.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data))) 
          

      ###### Fidelite Cart--------------------
    def fid_cart_screen(self):
        
        widgets.pushButton_32.clicked.connect(self.fid_cart_btn)
        widgets.pushButton_34.clicked.connect(lambda :self.auto_code(widgets.lineEdit_37,"long"))
        widgets.lineEdit_29.textChanged.connect(lambda : widgets.label_122.setText(widgets.lineEdit_29.text()))
        widgets.lineEdit_37.textChanged.connect(lambda : widgets.label_123.setText(widgets.lineEdit_37.text()))

        widgets.pushButton_33.clicked.connect(lambda : widgets.stackedWidget.setCurrentWidget(widgets.Outic) )
        widgets.stackedWidget.setCurrentWidget(widgets.Fidelite) 
    def fid_cart_btn(self):
        if widgets.lineEdit_29.text() != "" and widgets.lineEdit_37.text() != "":
            cart_id = widgets.lineEdit_37.text()
            name = widgets.lineEdit_29.text()
            vali = cr.execute(f"select * from fidelity_cart WHERE  Cart_id =('{cart_id}') ").fetchall()
            if vali == [] :
                if widgets.lineEdit_47.text() != "":
                    phone = widgets.lineEdit_47.text()
                else :
                    phone = "NULL" 
                if widgets.lineEdit_39.text() != "":
                    email = widgets.lineEdit_39.text()
                else :
                    email = "NULL"     
                if widgets.lineEdit_48.text() != "":
                    sold = widgets.lineEdit_48.text()
                else :
                    sold = 0 
                cr.execute(f"Insert into fidelity_cart (Cart_id,Points,Name,Numbre,Email) Values ('{cart_id}','{sold}','{name}','{phone}','{email}')")
                db.commit()  
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("            Enregistré avec succès        ") 
                msg1.exec_() 
            else:    
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("            Enregistré avec succès 2      ") 
                msg1.exec_()     
        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("            Enregistré avec succès 1     ") 
            msg1.exec_()                                 
     #### /Fidelite Cart ---------
     ### Garantie -------------
    def garantie_screen(self):
        if self.acc_Gar:
            widgets.stackedWidget.setCurrentWidget(widgets.Garante)
            widgets.pushButton_25.clicked.connect(lambda : widgets.stackedWidget.setCurrentWidget(widgets.Outic))   
            widgets.pushButton_22.clicked.connect(self.save_garantie) 
            self.auto_code(widgets.lineEdit_30,"long")
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()                   
    def save_garantie(self):
        nom = widgets.lineEdit_16.text()
        cin = widgets.lineEdit_17.text()
        vab = widgets.lineEdit_20.text()
        nom_prod = widgets.lineEdit_22.text() 
        marq_prod = widgets.lineEdit_27.text()
        sr_num = widgets.lineEdit_28.text() 
        code = widgets.lineEdit_30.text()

                 
        if nom !="" or cin != "":
            if nom =="":
                nom = "_______________"
            if cin =="":
                cin = "_______________"
            if vab == "":
                vab = "_______________"
            if nom_prod =="":
                nom_prod = "_______________"
            if marq_prod == "":
                marq_prod ="_______________"
            if sr_num  == "":
                sr_num = "_______________"
            if widgets.checkBox_6.isChecked() :
                url = pyqrcode.create(code) 
                url.png('DATA/myqr.png', scale = 3)
  
            doc = DocxTemplate("Doc-template/template.docx")
            
        
            ###doc.replace_pic('myqr.png','myqr.png')
            imgqr = InlineImage(doc, 'DATA/myqr.png')
            context = { 'NOM' : nom, "CIN": cin ,'nomproduit': nom_prod, 'ns':sr_num ,'vdate': vab , 'code':code , 'Date':DATE , 'QR': imgqr}
            doc.render(context)
            namedoc =str(code) + ".docx"
            
            try:
                name = QFileDialog.getSaveFileName(self, 'Save File',namedoc, "DOC (*.docx)")[0]
            except:
                pass  
            if name != "":
                doc.save(name)
                
            else :
                doc.save(namedoc) 
            #####------------------ printing    



    ##### facture --------------------
    list_sale_fac=[]
    list_sale_sans_tva = []

    
    def Facture(self):
        if self.acc_Fact:
            widgets.input_cb1_3.returnPressed.connect(lambda :  self.fetch_prodect("barre"))
            widgets.input_cb1_4.returnPressed.connect(lambda :  self.fetch_prodect("SKU"))
            widgets.checkBox_8.toggled.connect(lambda : self.block_input(widgets.checkBox_8,widgets.lineEdit_33))
            widgets.checkBox_9.toggled.connect(self.app_remise)
            widgets.lineEdit_34.textChanged.connect(self.app_remise)
            widgets.checkBox_6.toggled.connect(lambda : self.add_tva("check"))
            widgets.label_118.setText("Prix Net : 00 DT")
            widgets.label_115.setText("TVA : 00 DT")
            widgets.label_116.setText("Offre : 0 %")
            widgets.label_117.setText("Global : 00 DT")



            

            widgets.dateEdit.setDate(DATE)
            self.Auto_n_facture()
            
    
            widgets.checkBox_8.setChecked(True)  
            widgets.checkBox_8.toggled.connect(self.Auto_n_facture) 
            widgets.pushButton_39.clicked.connect(self.save_facture)




            widgets.pushButton_40.clicked.connect(self.retoure_btn_2 )
            widgets.stackedWidget.setCurrentWidget(widgets.Facture) 
        else:    
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()                   
    def fetch_prodect(self,y):

        if y =="barre":
            h1 = widgets.input_cb1_3.text()
            produit = cr.execute(f"select  Nom,Prix_achat,TVA from prodect WHERE BARRE ='{h1}'").fetchall()
        else:
            h1 = widgets.input_cb1_4.text()
            produit = cr.execute(f"select  Nom,Prix_achat,TVA from prodect WHERE SKU ='{h1}'").fetchall()
        if produit != []:

            nom = produit[0][0]
            prix = float(produit[0][1])
            tva = float(produit[0][2])
            Quantity = 1 
            check = 0
            if tva == "" or tva == "NULL":
                tva = 0 
            if len(self.list_sale_fac) != 0 : 
                for x in range(len(self.list_sale_fac)):
                    if self.list_sale_fac[x][0] == nom and self.list_sale_fac[x][1] == prix :
                        
                        Quantity = int(self.list_sale_fac[x][2]) + 1
                        prix_net = (prix * Quantity) 
                        prix_tva = (prix_net / 100) * tva
                        prix_global = prix_net + prix_tva 
                        self.list_sale_fac[x]=(nom,prix,Quantity,prix_net,tva,prix_global)
                        ##### _______ sans tva________________
                        self.list_sale_sans_tva[x] = (nom,prix,Quantity,prix_net,0,prix_net)

                        widgets.input_cb1_3.setText("")
                        widgets.input_cb1_4.setText("")
                        break
                    elif self.list_sale_fac[x][0] != nom and self.list_sale_fac[x][1] != prix:
                        check += 1
                        if check == len(self.list_sale_fac):
                            prix_net = (prix * Quantity) 
                            prix_tva = (prix_net / 100) * tva
                            prix_global = prix_net + prix_tva 
                            self.list_sale_fac.append((nom,prix,Quantity,prix_net,tva,prix_global)) 
                            self.list_sale_sans_tva.append((nom,prix,Quantity,prix_net,0,prix_net)) 

                            widgets.input_cb1_3.setText("")
                            widgets.input_cb1_4.setText("")
                            break

            
                    
            else :    
                prix_net = (prix * Quantity) 
                prix_tva = (prix_net / 100) * tva
                prix_global = prix_net + prix_tva 
                self.list_sale_fac.append((nom,prix,Quantity,prix_net,tva,prix_global))
                self.list_sale_sans_tva.append((nom,prix,Quantity,prix_net,0,prix_net)) 

                widgets.input_cb1_3.setText("")
            ##### ------------ table ---------
            if widgets.checkBox_6.isChecked():   
                ls = self.list_sale_fac
            else :
                ls = self.list_sale_sans_tva     
            while widgets.tableWidget_7.rowCount() > 0:
                widgets.tableWidget_7.removeRow(0)
            for row_index,row_data in enumerate(ls):
                widgets.tableWidget_7.insertRow(row_index)
                for colm_index , colm_data in enumerate(row_data):
                    widgets.tableWidget_7.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))  
            self.add_tva("glob") 
        else:
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Ce produit n'a pas été trouvé dans la base de données") 
            msg1.exec_()     
                 
    def add_tva(self,t):
        prix_net_glob = 0
        tva_glob = 0
        prix_global = 0
        for y in self.list_sale_fac:
            prix_net_glob += y[3]
            if widgets.checkBox_6.isChecked():
                tva_glob += (y[5] - y[3])
                prix_global += y[5]
            else: 
                tva_glob = 0    

                prix_global += y[3]
    


        widgets.label_118.setText(f"Prix Net :{prix_net_glob} TND") 
        widgets.label_115.setText(f"TVA : {tva_glob} TND") 
        widgets.label_117.setText(f"Global : {prix_global} TND") 
        if t == "check":  
            if widgets.checkBox_6.isChecked():   
                ls = self.list_sale_fac
            else :
                ls = self.list_sale_sans_tva     
            while widgets.tableWidget_7.rowCount() > 0:
                widgets.tableWidget_7.removeRow(0)
            for row_index,row_data in enumerate(ls):
                widgets.tableWidget_7.insertRow(row_index)
                for colm_index , colm_data in enumerate(row_data):
                    widgets.tableWidget_7.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data))) 
        self.app_remise()           

    def block_input(self,x,y):
        if x.isChecked() :
            y.setEnabled(False)
            y.setStyleSheet("background-color : #e0e0e0")
        else:
            y.setEnabled(True)  
            y.setStyleSheet("background-color : none")  
    
    def Auto_n_facture(self):
        list_facture = cr.execute("SELECT max(N_facture) FROM Facture ").fetchall()
        print(list_facture)

        

        if list_facture != [] and list_facture != [(None,)] :
            n_fact= int(list_facture[0][0]) + 1
            n_facture = "{:06d}".format(n_fact)
        else: 
            n_facture = "{:06d}".format(1) 

        widgets.lineEdit_33.setText(n_facture)

    def app_remise (self):
        if widgets.checkBox_9.isChecked():
            if widgets.lineEdit_34.text() == "":
                remise = 0
            else :
                remise = float(widgets.lineEdit_34.text())  
            widgets.label_116.setText(f"Offre : {remise} %") 

            prix_net_glob = 0
            tva_glob = 0
            prix_global = 0
            
            for y in self.list_sale_fac:
                prix_net_glob += y[3]
                if widgets.checkBox_6.isChecked():
                    tva_glob += (y[5] - y[3])
                    prix_global += y[5]
                else: 
                    tva_glob = 0    

                    prix_global += y[3]
        

            prix_global_and_offre = prix_global - ((prix_global/100)*remise)
            widgets.label_118.setText(f"Prix Net :{prix_net_glob} TND") 
            widgets.label_115.setText(f"TVA : {tva_glob} TND") 
            widgets.label_117.setText(f"Global : {prix_global_and_offre} TND") 

    def save_facture(self):
        ##### info_clien 
        if self.list_sale_fac != []:
            if widgets.lineEdit_18.text() != "":
                nom = widgets.lineEdit_18.text()
            else :
                nom = "____________"
            if widgets.lineEdit_30.text() != "":  
                nom_com  = widgets.lineEdit_30.text()   
            else:
                nom_com= "____________"  
            if widgets.lineEdit_31.text() != "":  
                phone  = widgets.lineEdit_31.text()   
            else:
                phone= "____________"    
            if widgets.lineEdit_32.text() != "":  
                adresse  = widgets.lineEdit_32.text()   
            else:
                adresse= "____________"                
            mode_payment = widgets.comboBox_7.currentText()
            date_ech = widgets.dateEdit.date().toPython()
            #### info_facture
            if widgets.lineEdit_33.text() != "" :
                n_fact = widgets.lineEdit_33.text()
            else :
                n_fact = "____________"   
            if widgets.checkBox_6.isChecked():   
                ls = self.list_sale_fac
            else :
                ls = self.list_sale_sans_tva  
            prix_net = 0
            prix_global = 0
            tva_global = 0
            table_prodect = []
            for x in ls :
                prix_net += float(x[3])
                prix_global += float(x[5]) 
                tva = float(x[5])  - float(x[3])
                tva_global += tva
            if widgets.checkBox_9.isChecked():
                if widgets.lineEdit_34.text() != "":
                    offre = widgets.lineEdit_34.text()
                else : 
                    offre = 0
            else:
                offre = 0        
            prix_global = prix_global - ((prix_global / 100 )  * float(offre) ) 
            if widgets.checkBox_7.isChecked():
                Qr = random.randint(10000000000, 999999999999)
            else:
                Qr = "NULL"         
            cr.execute(f"INSERT INTO Facture (N_facture,Nom,Date,Date_valid,Tva,Global,qr) values('{n_fact}','{nom}','{DATE}','{date_ech}','{tva_global}','{prix_global}','{Qr}')") 
            db.commit()
            if widgets.checkBox_10.isChecked():
                for y in ls:
                    id_prodect = cr.execute(f"select BARRE from prodect WHERE nom ='{y[0]}' and Prix_achat ='{int(y[1])}'").fetchall()
                    table_prodect.append({'name':y[0],'prix':y[1],'qua':y[2],'prixnet':y[3],'tva':y[4],'prixtout':y[5]})
             
                    prix_prodect_with_offre = (y[5]- (y[5]/100) * float(offre))
                    
                    cr.execute(f"INSERT INTO prodect_sale(code_bare,nom,prix,nomb,prix_total,offre,Mode_pay,date) values('{id_prodect[0][0]}','{y[0]}','{y[1]}','{y[2]}','{prix_prodect_with_offre }','{offre}' , '{mode_payment}' , '{DATE}')")
                    db.commit()
            ###### facture word 
            doc = DocxTemplate("Doc-template/Templatefacture.docx")
            if widgets.checkBox_7.isChecked():
                url = pyqrcode.create(Qr) 
                url.png('DATA/myqr.png', scale = 3)
                imgqr = InlineImage(doc, 'DATA/myqr.png')

                context = {'COMPANY' : Market_Name, 'Address':Market_Maps,'Phone':Market_Phone,'EMail': Market_Mail, 'No' : n_fact, "date": DATE,'Name': nom, 'comp':nom_com ,'Adress': adresse , 'NT':phone , 'toutalnet':prix_net , 'toutaltva': tva_global,'offer' : offre,'global':prix_global,'datepay':date_ech  , 'items':table_prodect,'Qr':imgqr}
            else:
                context = {'COMPANY' : Market_Name, 'Address':Market_Maps,'Phone':Market_Phone,'EMail': Market_Mail, 'No' : n_fact, "date": DATE,'Name': nom, 'comp':nom_com ,'Adress': adresse , 'NT':phone , 'toutalnet':prix_net , 'toutaltva': tva_global,'offer' : offre,'global':prix_global,'datepay':date_ech  , 'items':table_prodect}
            doc.render(context)
            namedoc =str(Qr) + ".docx"
            
            try:
                name = QFileDialog.getSaveFileName(self, 'Save File',namedoc, "DOC (*.docx)")[0]
            except:
                pass  
            if name != "":
                doc.save(name)
                
            else :
                doc.save(namedoc)         
            doc.save("testfacure1.docx")
            ##### ------------- print page
            #
            #
            #####-------------------------------


            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("La facture a été enregistrée avec succès") 
            msg1.exec_() 
            widgets.lineEdit_18.clear()
            widgets.lineEdit_30.clear()
            widgets.lineEdit_31.clear()
            widgets.lineEdit_32.clear()
            widgets.lineEdit_34.clear()
            self.list_sale_fac=[]
            self.list_sale_sans_tva = []
            while widgets.tableWidget_7.rowCount() > 0:
                widgets.tableWidget_7.removeRow(0)
            self.Auto_n_facture()

    def retoure_btn_2(self):
        widgets.stackedWidget.setCurrentWidget(widgets.Outic)
        widgets.lineEdit_18.clear()
        widgets.lineEdit_30.clear()
        widgets.lineEdit_31.clear()
        widgets.lineEdit_32.clear()
        widgets.lineEdit_34.clear()
        self.list_sale_fac=[]
        self.list_sale_sans_tva = []
        while widgets.tableWidget_7.rowCount() > 0:
            widgets.tableWidget_7.removeRow(0)
        self.Auto_n_facture()
    ##### Rapports -------------------
    def rapports_screen(self):
        if self.acc_Rap:
            widgets.stackedWidget.setCurrentWidget(widgets.Rapport)
            widgets.pushButton_28.clicked.connect(lambda : widgets.stackedWidget.setCurrentWidget(widgets.Outic))
            self.date_change()
            widgets.comboBox_8.currentTextChanged.connect(self.date_change)
            widgets.pushButton_27.clicked.connect(self.create_rapport)
            n = 1000
            self.auto_code(widgets.lineEdit_35,"short")
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()               

    def date_change(self):
        if widgets.comboBox_8.currentText() == "Journalier":
            widgets.dateEdit_2.setDate(DATE)
            widgets.dateEdit_3.setDate(DATE)
            widgets.dateEdit_2.setEnabled(False)
            widgets.dateEdit_3.setEnabled(False)
        elif widgets.comboBox_8.currentText() == "Hebdomadaire" :
            widgets.dateEdit_2.setDate(DATE - timedelta(days =7))
            widgets.dateEdit_3.setDate(DATE )
            widgets.dateEdit_2.setEnabled(False)
            widgets.dateEdit_3.setEnabled(False)
        elif widgets.comboBox_8.currentText() == "Mensuel" :  
            widgets.dateEdit_2.setDate(DATE - timedelta(days =30))
            widgets.dateEdit_3.setDate(DATE )
            widgets.dateEdit_2.setEnabled(False)
            widgets.dateEdit_3.setEnabled(False)
        elif widgets.comboBox_8.currentText() == "Annuel" :  
            widgets.dateEdit_2.setDate(DATE - timedelta(days =365))
            widgets.dateEdit_3.setDate(DATE )
            widgets.dateEdit_2.setEnabled(False)
            widgets.dateEdit_3.setEnabled(False)  
        else :  
            widgets.dateEdit_2.setEnabled(True)
            widgets.dateEdit_3.setEnabled(True)                        




    def create_rapport(self):
        doc = DocxTemplate("Doc-template/Template-Rapport.docx")
        d1 = widgets.dateEdit_2.date().toPython()
        d2 = widgets.dateEdit_3.date().toPython()
        n_rapport = widgets.lineEdit_35.text()
        context = {"date":DATE,"date_1":d1 ,"date_2":d2,"N_rapport": n_rapport,"company": Market_Name, }
        depo = 0
        ##### --------- revu
        rev_tout = 0
        rev_cash = 0
        rev_check = 0
        rev_credit = 0
        rev_aut = 0
        vende_moyeen = 0
        ##### --------------- /rev 
        ############## dépenses
        if widgets.checkBox_11.isChecked():
            if widgets.comboBox_8.currentText() == "Journalier":
                dip = cr.execute(f"select PRIX from dépenses WHERE DATE = {DATE}").fetchall()
                sales = cr.execute(f"select prix_total,Mode_pay from prodect_sale WHERE date = {DATE}").fetchall()
            elif widgets.comboBox_8.currentText() == "Hebdomadaire" :
                dip = cr.execute(f"select PRIX from dépenses WHERE DATE IN {tuple(list_date_week)}").fetchall()
                sales = cr.execute(f"select prix_total,Mode_pay from prodect_sale WHERE date IN {tuple(list_date_week)}").fetchall()

            elif widgets.comboBox_8.currentText() == "Mensuel" :  
                dip = cr.execute(f"select PRIX from dépenses WHERE DATE IN {tuple(list_date_month)}").fetchall() 
                sales = cr.execute(f"select prix_total,Mode_pay from prodect_sale WHERE date IN {tuple(list_date_month)}").fetchall()

            elif widgets.comboBox_8.currentText() == "Annuel" :  
                dip = cr.execute(f"select PRIX from dépenses WHERE DATE IN {tuple(list_date_years)}").fetchall()
                sales = cr.execute(f"select prix_total,Mode_pay from prodect_sale WHERE date IN {tuple(list_date_years)}").fetchall()

            else:
                dt1 = widgets.dateEdit_3.date().toPython()
                dt2 = widgets.dateEdit_2.date().toPython() 
                dey_calc = (dt1 - (dt2- timedelta(days =1)) ).days
                date_perso = []
                for day_y in range(int(dey_calc)):
                    date_perso.append(str(dt1 - timedelta(days =day_y))) 

                if len(date_perso) <= 1 :
                    dip = cr.execute(f"select PRIX from dépenses WHERE DATE = '{date_perso[0]}'").fetchall() 
                    sales = cr.execute(f"select prix_total,Mode_pay from prodect_sale WHERE date  = '{date_perso[0]}' ").fetchall()

                else:    

                
                    dip = cr.execute(f"select PRIX from dépenses WHERE DATE IN {tuple(date_perso)}").fetchall()
                    sales = cr.execute(f"select prix_total,Mode_pay from prodect_sale WHERE date IN {tuple(date_perso)}").fetchall()

                    print(dip)

            for i in dip:
                depo += float(i[0])
            ######## cont    
            context["rapport_rev" ] = "yes"
            context["dép" ] = depo

            ######## /cont
            for ii in sales:
                rev_tout += float(ii[0])
                if ii[1] == 'Cash':
                    rev_cash += float(ii[0]) 
                elif ii[1] == 'Chèque':
                    rev_check += float(ii[0]) 
                elif ii[1] == 'Credit':
                    rev_credit += float(ii[0])
                else:
                    rev_aut += float(ii[0])
            context["rvt" ] = rev_tout
            context["cash" ] = rev_cash
            context["cheq" ] = rev_check
            context["credit" ] = rev_credit
            context["aut" ] = rev_aut
            ######### graphic
            try:
                if widgets.checkBox_19.isChecked():
                    context["graph" ] = "yes"
                    x = [rev_cash, rev_check, rev_credit, rev_aut]
                    labels = ['Espèc', 'Chèque', 'Crédit', 'Autres moyens']

                    fig, ax = plt.subplots()
                    ax.pie(x, labels=labels, autopct='%.1f%%',wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
                    ##plt.setp(ax, color='white', fontweight='bold')
                    ax.set_title('Statistiques sur les méthodes de paiement')
                    print("yes save 1")
            
                    plt.savefig('Graphic/graph1.png',dpi=75,transparent=True,pad_inches = 0, bbox_inches='tight')
                    plt.close()
                    graph1 = InlineImage(doc, 'Graphic/graph1.png')

                    context["gr3" ] = graph1
                    ######### /graphic
            except:
                pass        
        if widgets.checkBox_12.isChecked():
            context["rapport_vend" ] = "yes"
            jour = 0
            list_barre ={}
            list_cat = {}
            top_5_prodect=[]
            dect_top_5={}
            min_5_prodect =[]
            if widgets.comboBox_8.currentText() == "Journalier":
                sales = cr.execute(f"select DISTINCT code_bare from prodect_sale WHERE date = {DATE}").fetchall()
                
                jour = 1
            elif widgets.comboBox_8.currentText() == "Hebdomadaire" :
                sales = cr.execute(f"select DISTINCT code_bare from prodect_sale WHERE date IN {tuple(list_date_week)}").fetchall()
                jour = 7
            elif widgets.comboBox_8.currentText() == "Mensuel" :  
                sales = cr.execute(f"select DISTINCT code_bare from prodect_sale WHERE date IN {tuple(list_date_month)}").fetchall()
                jour = 30

            elif widgets.comboBox_8.currentText() == "Annuel" :  
                sales = cr.execute(f"select DISTINCT code_bare from prodect_sale WHERE date IN {tuple(list_date_years)}").fetchall()
                jour = 365

            else:
                dt1 = widgets.dateEdit_3.date().toPython()
                dt2 = widgets.dateEdit_2.date().toPython() 
                dey_calc = (dt1 - (dt2- timedelta(days =1)) ).days
                jour = int(dey_calc)
                date_perso = []
                for day_y in range(int(dey_calc)):
                    date_perso.append(str(dt1 - timedelta(days =day_y))) 
                if len(date_perso) <= 1 :
                    sales = cr.execute(f"select DISTINCT code_bare from prodect_sale WHERE date  = '{date_perso[0]}' ").fetchall()
                else:    
                    sales = cr.execute(f"select DISTINCT code_bare from prodect_sale WHERE date IN {tuple(date_perso)}").fetchall()
                
            for x in sales:
                list_barre[x[0]] = 0
            for y in tuple( list_barre.keys()):
                sales1 = cr.execute(f"select nomb from prodect_sale WHERE code_bare = {y}").fetchall()
                for yy in sales1:
                    list_barre[y] += int(yy[0])
            vende_moyeen = sum(tuple(list_barre.values())) / jour  
            ls_val = list(list_barre.values())


            tp5 = self.N_max_elements(ls_val,5)
            for h in tp5:
                for barre, Quan in list_barre.items(): 
                    if Quan == h:
                        cbarre = barre
                prod_name =cr.execute(f"select nom from prodect_sale WHERE code_bare = {cbarre}").fetchall()[0][0]       
                top_5_prodect.append({'v1':h,'m1': int(h/jour),'c1':cbarre,'n1': prod_name})
            context["v_m" ] = int(vende_moyeen)
            ############# table top 5 vente
            try:
                
                val = list(top_5_prodect[0].values())
                context["n1" ] = str(val[3])
                context["c1" ] = val[2]
                context["m1" ] = val[1]
                context["v1" ] = val[0]
            except:
                pass 
            try:
                
                val = list(top_5_prodect[1].values())
                context["n2" ] = str(val[3])
                context["c2" ] = val[2]
                context["m2" ] = val[1]
                context["v2" ] = val[0]
            except:
                pass   
            try:
                val = list(top_5_prodect[2].values())
                context["n3" ] = str(val[3])
                context["c3" ] = val[2]
                context["m3" ] = val[1]
                context["v3" ] = val[0]
            except:
                pass  
            try:
                val = list(top_5_prodect[3].values())
                context["n4" ] = str(val[3])
                context["c4" ] = val[2]
                context["m4" ] = val[1]
                context["v4" ] = val[0]
            except:
                pass     
            try:
                val = list(top_5_prodect[4].values())
                context["n5" ] = str(val[3])
                context["c5" ] = val[2]
                context["m5" ] = val[1]
                context["v5" ] = val[0]
            except:
                pass    
            ######### moin 5 vendu
            ls_val = list(list_barre.values())

            mn5 = self.N_min_elements(ls_val,5)
            for h in mn5:
                for barre, Quan in list_barre.items(): 
                    if Quan == h:
                        cbarre = barre
                prod_name =cr.execute(f"select nom from prodect_sale WHERE code_bare = {cbarre}").fetchall()[0][0]       
                min_5_prodect.append({'v1':h,'m1': int(h/jour),'c1':cbarre,'n1': prod_name})
            ############# table top 5 vente
            try:
                val = list(min_5_prodect[0].values())
                context["nn1" ] = str(val[3])
                context["cc1" ] = val[2]
                context["mm1" ] = val[1]
                context["vv1" ] = val[0]
            except:
                pass 
            try:
                
                val = list(min_5_prodect[1].values())
                context["nn2" ] = str(val[3])
                context["cc2" ] = val[2]
                context["mm2" ] = val[1]
                context["vv2" ] = val[0]
            except:
                pass   
            try:
                val = list(min_5_prodect[2].values())
                context["nn3" ] = str(val[3])
                context["cc3" ] = val[2]
                context["mm3" ] = val[1]
                context["vv3" ] = val[0]
            except:
                pass  
            try:
                val = list(min_5_prodect[3].values())
                context["nn4" ] = str(val[3])
                context["cc4" ] = val[2]
                context["mm4" ] = val[1]
                context["vv4" ] = val[0]
            except:
                pass     
            try:
                val = list(min_5_prodect[4].values())
                context["nn5" ] = str(val[3])
                context["cc5" ] = val[2]
                context["mm5" ] = val[1]
                context["vv5" ] = val[0]
            except:
                pass 

            if widgets.checkBox_19.isChecked():
                context["graph" ] = "yes"
                for io in top_5_prodect:
                    print(io)
                    nom = io["n1"]
                    num = io['v1']
                    dect_top_5[nom] = num
                courses = list(dect_top_5.keys())
                values = list(dect_top_5.values())
                
                
                
                # creating the bar plot
                try:
                    plt.bar(courses, values, color ='blue',
                            width = 0.4)
                    
                    plt.xlabel("statistiques de vente")
                    plt.ylabel("Le nombre de ventes durant cette période")
                    plt.title("Statistiques de vente") 
                    plt.savefig('Graphic/graph2.png',dpi=75,transparent=True, bbox_inches='tight')
                    plt.close()
                    graph2 = InlineImage(doc, 'Graphic/graph2.png')

                    context["gr1" ] = graph2
                except:
                    pass       

        if widgets.checkBox_14.isChecked():
            context["rapport_dette"] = "yes"
            monton_credit = 0
            credit_l =[]
            credit_list = cr.execute("select Name_Clien , Number,Max_credit,Credit from Credit_Cart where Credit > 0 ").fetchall()
            for nw in credit_list:
                monton_credit += float(nw[3]) 
                credit_l.append({"namec": nw[0],"phonee":nw[1],"max":nw[2],"credit":nw[3] })

            context["credit"] = monton_credit  
            print(credit_l)   

            context["credits"] = credit_l
        ### etat

        if widgets.checkBox_13.isChecked():
            context["stat_produits"] = "yes" 
            stat_pr = []  
            stat_pr_dect = []
            numbre_prodect_ex=0
            ########################## Date exper
            pod = cr.execute("select Date_exp,BARRE,Stock,nom from prodect").fetchall()
            for x in pod:  
                if x[0] != "NULL" and x[0] != None:
                    print(x[0])
                    date_time_obj = datetime.strptime(x[0], '%d-%m-%Y').date()
                    if date_time_obj <= DATE:
                        ############ ----------- numbre prodect in stock
                        if x[2] != "NULL" and x[2] != None :
                            n_in_sal=int(x[2])

                            pr_sl = cr.execute(f"select nomb from prodect_sale where code_bare = {x[1]} ").fetchall()
                            for xb  in pr_sl :
                                n_in_sal -= int(xb[0])
                        else:
                            n_in_sal=0
                        ############### --------------- end numbre in stock    


                        stat_pr.append((x[1],x[0],n_in_sal,"a expiré",x[3]))
                        numbre_prodect_ex =+1
                    elif  date_time_obj <= (DATE + timedelta(days =10)) :
                        ############ ----------- numbre prodect in stock
                        if x[2] != "NULL" and x[2] != None :
                            n_in_sal=int(x[2])

                            pr_sl = cr.execute(f"select nomb from prodect_sale where code_barre = {x[1]} ").fetchall()
                            for xb  in pr_sl :
                                n_in_sal -= int(xb[0])
                        else:
                            n_in_sal=0
                        ############### --------------- end numbre in stock                            


                        stat_pr.append((x[1],x[0],n_in_sal,"Expire bientot",x[3]))
                    else:
                        pass 
                else : 
                    pass  

            for ml in stat_pr :
                stat_pr_dect.append({"name7" : ml[4] ,"barre7":ml[0],"ninstock7":ml[2],"statut7":ml[3]})

            print(context)
            context["n_p"] = numbre_prodect_ex 
            context["perimie"] = stat_pr_dect 
            print(context) 
            ######################## end Date exper   
            ######################## in stock 
            in_stk = cr.execute("select Stock , BARRE ,Stock_minimal, nom from prodect where Stock > 0").fetchall()
            st_list_dect = []
            n_rept = 0
            for ooe in in_stk:
                sl_list= cr.execute(f"select nomb from prodect_sale where code_bare = {ooe[1]} ").fetchall()
                in_stock = 0

                num_sal = 0
                for iio in sl_list:
                    num_sal += int(iio[0])
                in_stock = int(ooe[0]) -  num_sal
                if in_stock <= 0:
                    st_list_dect.append({"name4":ooe[3],"barre":ooe[1],"ninstock":in_stock,"statut":'Rupture de stock'})
                    n_rept += 1
                else:
                    if ooe[2] != "NULL" and ooe[2] != None:
                        if in_stock <= int(ooe[2]):
                            st_list_dect.append({"name4":ooe[3],"barre":ooe[1],"ninstock":in_stock,"statut":"Rupture de stock Bientot "})
                    elif in_stock <= 30:
                            st_list_dect.append({"name4":ooe[3],"barre":ooe[1],"ninstock":in_stock,"statut":"Rupture de stock Bientot "})
            context["repture"] = st_list_dect  
            context["n_r"] = n_rept     



        doc.render(context)
        namedoc = "rappoert.docx"
        
        try:
            name = QFileDialog.getSaveFileName(self, 'Save File',namedoc, "DOC (*.docx)")[0]
        except:
            pass  
        if name != "":
            doc.save(name)
            
        else :
            doc.save(namedoc) 
        
    
        print("yes save")
        
    def N_max_elements(self,list, N):
        result_list = []
    
        for i in range(0, N): 
            maximum = 0
            
            for j in range(len(list)):     
                if list[j] > maximum:
                    maximum = list[j]
            try:
                list.remove(maximum)
                result_list.append(maximum)
            except:
                pass    
            
        return result_list
    def N_min_elements(self,list1,N):
        list2 = list1 
        min_n = []  
        for x in range(N):
            try:
                y = min(list2)
                min_n.append(y)
                list1.remove(y)
            except:
                pass
        return min_n         
    def msg_list(self):
        widgets.stackedWidget.setCurrentWidget(widgets.Page_message)
        widgets.stackedWidget_5.setCurrentWidget(widgets.page_11)

        filehandler = open("DATA/message.EMH","rb")
        object_file = pickle.load(filehandler)
        filehandler.close()
        table_message = object_file

        titre = []

        for mm in table_message.keys():
            if table_message[mm][3] != 1:
                titre.append([mm])
 
            


        while widgets.tableWidget_3.rowCount() > 0:
            widgets.tableWidget_3.removeRow(0)
        for row_index,row_data in enumerate(titre):
            widgets.tableWidget_3.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableWidget_3.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data)))
   

        widgets.tableWidget_3.doubleClicked.connect(self.showmsg)
    def showmsg(self):
        row =  widgets.tableWidget_3.currentRow()
        currentproductid = ( widgets.tableWidget_3.item(row, 0).text() ) 
        filehandler = open("DATA/message.EMH","rb")
        object_file = pickle.load(filehandler)
        filehandler.close()
        table_message = object_file
        widgets.label_70.setText((table_message[currentproductid])[0])
        widgets.label_71.setText((table_message[currentproductid])[1])
        widgets.textBrowser.setText((table_message[currentproductid])[2])
        widgets.stackedWidget_5.setCurrentWidget(widgets.page_12)
        widgets.pushButton_41.clicked.connect(lambda: widgets.stackedWidget_5.setCurrentWidget(widgets.page_11))
        widgets.pushButton_47.clicked.connect(lambda: self.remove_msg(currentproductid))

    def remove_msg(self,y):
        filehandler = open("DATA/message.EMH","rb")
        object_file = pickle.load(filehandler)
        filehandler.close()

        table_message = object_file
        vu=table_message[y][3]=1

        filehandler = open("DATA/message.EMH","wb")
        pickle.dump(table_message,filehandler)
        filehandler.close()
        
        self.msg_list()





  

        








    def parametre_screen(self):
        if acc_admin[0] == "Superadmin" or acc_admin[0] == "SuperUser" or acc_admin[0] == "admin":
            widgets.lineEdit_49.setText(Market_Name)
            widgets.lineEdit_50.setText(Market_Phone)
            widgets.lineEdit_54.setText(Market_Fax)
            widgets.lineEdit_51.setText(Market_Mail)
            widgets.lineEdit_52.setText(Market_Maps)
            widgets.lineEdit_55.setText(str(Market_min_Point))
            widgets.lineEdit_53.setText(str(Market_to_Point))

            widgets.frame_191.setStyleSheet(u"background-image: url(./DATA/logo.png);")
            
            widgets.pushButton_29.clicked.connect(self.setlogo)
            widgets.pushButton_30.clicked.connect(self.conf_change)
            widgets.stackedWidget.setCurrentWidget(widgets.page_8)
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()      
    def conf_change(self):
        name_market = widgets.lineEdit_49.text()
        phone_market = widgets.lineEdit_50.text()
        fax_market = widgets.lineEdit_54.text()
        mail_market = widgets.lineEdit_51.text()
        map_market = widgets.lineEdit_52.text()
        point_market = widgets.lineEdit_53.text()
        min_point = widgets.lineEdit_55.text()
        cr.execute(f"UPDATE Setting SET DATA = '{name_market}',DATA_1='{phone_market}',DATA_3='{fax_market}',DATA_4='{mail_market}',DATA_5='{map_market}',DATA_6='{min_point}',DATA_7='{point_market}'")

        db.commit()
        msg1=QMessageBox()

        msg1.setIcon(QMessageBox.Information)
        msg1.setText("Les informations ont été mises à jour avec succès. Veuillez redémarrer le programme")
        msg1.setWindowTitle("Enregistré avec succès")
        msg1.exec_()        





    def parametre_imp(self):
        
        choices = [printer[2] for printer in win32print.EnumPrinters(2)]
        widgets.pushButton_43.clicked.connect(self.ann_imp)

        widgets.comboBox_9.addItems(choices)
        widgets.comboBox_10.addItems(choices)
        widgets.pushButton_44.clicked.connect(self.select_print)
        widgets.pushButton_45.clicked.connect(self.select_print)
        widgets.pushButton_42.clicked.connect(self.save_imp)
        try:
            filehandler = open("DATA/Setting-imp.emh","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
            
            widgets.checkBox_15.setChecked(object_file[0])
            widgets.comboBox_9.setCurrentText(object_file[1])
            widgets.checkBox_16.setChecked(object_file[2])
            widgets.checkBox_17.setChecked(object_file[3])
            widgets.comboBox_10.setCurrentText(object_file[4])
            if object_file[5] == "Défaut":
                widgets.radioButton.setChecked(True)
            elif object_file[5] == "Bleu":
                widgets.radioButton_3.setChecked(True)   
            elif object_file[5] == "Vert":
                widgets.radioButton_4.setChecked(True)     
            elif object_file[5] == "Jaune":
                widgets.radioButton_5.setChecked(True)  
            elif object_file[5] == "Roug":
                widgets.radioButton_6.setChecked(True)  
            else:
                pass 
        except:
            pass       


        widgets.stackedWidget.setCurrentWidget(widgets.Parametre_imp)
    def save_imp(self):
        imp_facture = widgets.checkBox_15.isChecked()
        imp_facture_name = widgets.comboBox_9.currentText()
        add_logo = widgets.checkBox_16.isChecked()
        imp_doc = widgets.checkBox_17.isChecked()
        imp_doc_name = widgets.comboBox_10.currentText()  

        if widgets.radioButton.isChecked():
            model_facture = "Défaut"
        if widgets.radioButton_3.isChecked():
            model_facture = "Bleu"
        if widgets.radioButton_4.isChecked():
            model_facture = "Vert"
        if widgets.radioButton_5.isChecked():
            model_facture = "Jaune"
        if widgets.radioButton_6.isChecked():
            model_facture = "Roug"              
        filename = 'DATA/Setting-imp.emh'

        outfile = open(filename,'wb')
        pickle.dump((imp_facture,imp_facture_name,add_logo,imp_doc,imp_doc_name,model_facture),outfile)
        outfile.close()
        msg1=QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setText("Les informations d'impression ont été mises à jour avec succès")
        msg1.setWindowTitle("Enregistré avec succès")
        msg1.exec_()   
        pass      
    def ann_imp(self):
        try:
            filehandler = open("DATA/Setting-imp.emh","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
            
            widgets.checkBox_15.setChecked(object_file[0])
            widgets.comboBox_9.setCurrentText(object_file[1])
            widgets.checkBox_16.setChecked(object_file[2])
            widgets.checkBox_17.setChecked(object_file[3])
            widgets.comboBox_10.setCurrentText(object_file[4])
            if object_file[5] == "Défaut":
                widgets.radioButton.setChecked(True)
            elif object_file[5] == "Bleu":
                widgets.radioButton_3.setChecked(True)   
            elif object_file[5] == "Vert":
                widgets.radioButton_4.setChecked(True)     
            elif object_file[5] == "Jaune":
                widgets.radioButton_5.setChecked(True)  
            elif object_file[5] == "Roug":
                widgets.radioButton_6.setChecked(True)  
            else:
                pass 
        except:
            pass      



    def parametre_admin(self):
        widgets.pushButton_51.clicked.connect(self.ann_adm)
        try:
            filehandler = open("DATA/Setting-admin.emh","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
            
            widgets.checkBox_18.setChecked(object_file[0])
            widgets.checkBox_23.setChecked(object_file[1])
            widgets.checkBox_20.setChecked(object_file[2])
            widgets.checkBox_21.setChecked(object_file[3])
            widgets.checkBox_22.setChecked(object_file[4])
            widgets.checkBox_24.setChecked(object_file[5])

        except:
            pass    
        widgets.pushButton_50.clicked.connect(lambda : self.add_admin_screen("add"))
        widgets.stackedWidget.setCurrentWidget(widgets.Parameter_admin) 

        ########### table admin 
        table_admin = cr.execute("Select User_name,add_prodect,Modefie,Statsitque,Dep,Facture,Rapport,Gar,Retour,Donne from admin").fetchall()
        while widgets.tableWidget_2.rowCount() > 0:
            widgets.tableWidget_2.removeRow(0)
        for row_index,row_data in enumerate(table_admin):
            widgets.tableWidget_2.insertRow(row_index)
            for colm_index , colm_data in enumerate(row_data):
                widgets.tableWidget_2.setItem(row_index,colm_index,QTableWidgetItem(str(colm_data))) 
           
        widgets.tableWidget_2.doubleClicked.connect(lambda : self.add_admin_screen("edit") ) 
        widgets.pushButton_46.clicked.connect(self.admin_save_btn)
    def admin_save_btn (self):
        modesmart = widgets.checkBox_18.isChecked()
        backup = widgets.checkBox_23.isChecked()
        autorun =widgets.checkBox_20.isChecked()
        r_email= widgets.checkBox_21.isChecked()
        rappl =widgets.checkBox_22.isChecked()
        notf =  widgets.checkBox_24.isChecked()
        filename = 'DATA/Setting-admin.emh'

        outfile = open(filename,'wb')
        pickle.dump((modesmart,backup,autorun,r_email,rappl,notf),outfile)
        outfile.close()
        msg1=QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setText("Les informations d'administrateur et d'utilisateur ont été enregistrées avec succès")
        msg1.setWindowTitle("Enregistré avec succès")
        msg1.exec_()          
    def ann_adm(self):
        try:
            filehandler = open("DATA/Setting-admin.emh","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
            
            widgets.checkBox_18.setChecked(object_file[0])
            widgets.checkBox_23.setChecked(object_file[1])
            widgets.checkBox_20.setChecked(object_file[2])
            widgets.checkBox_21.setChecked(object_file[3])
            widgets.checkBox_22.setChecked(object_file[4])
            widgets.checkBox_24.setChecked(object_file[5])

        except:
            pass   



    def setlogo(self):
        name = QFileDialog.getOpenFileName(filter="Image (*.png)")[0]
        if name != "":
            shutil.copy2(name, 'DATA/logo.png')
            widgets.label_144.setText(name)
            im = Image.open(name)
            im = im.resize((100, 100), Image.ANTIALIAS)
            im.save('DATA/logo.png') 

            widgets.frame_191.setStyleSheet(u"background-image: url(./DATA/logo.png);")

        else:
            pass

    def select_print(self):
        choices = [printer[2] for printer in win32print.EnumPrinters(2)]

        dialog = QtPrintSupport.QPrintDialog()
        dialog.exec_()
        printername = dialog.printer().printerName()
        if printername in choices:
            pass
        else:
            choices.append(printername)

        widgets.comboBox_9.clear()
        widgets.comboBox_9.clear()

        widgets.comboBox_9.addItems(choices)
        widgets.comboBox_10.addItems(choices)

    def add_admin_screen(self,y):
        if acc_admin[0] == "Superadmin" or acc_admin[0] == "SuperUser" or acc_admin[0] == "admin":
            add_momb.setupUi(add_momb)
            if y == "add":
                add_momb.pushButton_51.hide()
                add_momb.comboBox_7.currentTextChanged.connect(self.check)
                add_momb.saveButton.clicked.connect(self.add_admin_btn)
            else :
                row = widgets.tableWidget_2.currentRow()
                currentproductid = (widgets.tableWidget_2.item(row, 0).text() ) 
                infoadmin=cr.execute(f"select * from admin WHERE User_name= '{currentproductid}'").fetchone()
                add_momb.lineEdit_31.setText(infoadmin[0])
                add_momb.lineEdit_32.setText(infoadmin[1])
                if infoadmin[2] == "True":
                    add_momb.checkBox.setChecked(True)
                else:
                    add_momb.checkBox.setChecked(False) 
                if infoadmin[3] == "True":
                    add_momb.checkBox_2.setChecked(True)
                else:
                    add_momb.checkBox_2.setChecked(False) 
                if infoadmin[4] == "True":
                    add_momb.checkBox_4.setChecked(True)
                else:
                    add_momb.checkBox_4.setChecked(False)  
                if infoadmin[5] == "True":
                    add_momb.checkBox_5.setChecked(True)
                else:
                    add_momb.checkBox_5.setChecked(False)  
                if infoadmin[6] == "True":
                    add_momb.checkBox_6.setChecked(True)
                else:
                    add_momb.checkBox_6.setChecked(False) 
                if infoadmin[7] == "True":
                    add_momb.checkBox_7.setChecked(True)
                else:
                    add_momb.checkBox_7.setChecked(False)                                                                                        
                if infoadmin[8] == "True":
                    add_momb.checkBox_8.setChecked(True)
                else:
                    add_momb.checkBox_8.setChecked(False)
                if infoadmin[9] == "True":
                    add_momb.checkBox_9.setChecked(True)
                else:
                    add_momb.checkBox_9.setChecked(False)
                if infoadmin[10] == "True":
                    add_momb.checkBox_10.setChecked(True)
                else:
                    add_momb.checkBox_10.setChecked(False)                


                add_momb.pushButton_51.show()
                add_momb.saveButton.setText("Edit")
                
                add_momb.saveButton.clicked.connect(self.edit_admin_btn)
                add_momb.pushButton_51.clicked.connect(self.delet_admin)

            add_momb.show()
        else:
            msg1=QMessageBox()
            msg1.setText("Vous n'êtes pas autorisé à accéder à cette section")
            msg1.setWindowTitle("Vous n'avez pas assez d'autorisations")
            msg1.exec_()               
    def check(self):
        if add_momb.comboBox_7.currentText() == "Administrateur":
           
            add_momb.checkBox.setChecked(True)
            add_momb.checkBox_2.setChecked(True)
            add_momb.checkBox_4.setChecked(True)
            add_momb.checkBox_5.setChecked(True)
            add_momb.checkBox_6.setChecked(True)
            add_momb.checkBox_7.setChecked(True)
            add_momb.checkBox_8.setChecked(True)
            add_momb.checkBox_9.setChecked(True)
            add_momb.checkBox_10.setChecked(True)
        elif add_momb.comboBox_7.currentText() == "Vendeur":

            add_momb.checkBox.setChecked(False)
            add_momb.checkBox_2.setChecked(False)
            add_momb.checkBox_4.setChecked(False)
            add_momb.checkBox_5.setChecked(False)
            add_momb.checkBox_6.setChecked(True)
            add_momb.checkBox_7.setChecked(False)
            add_momb.checkBox_8.setChecked(True)
            add_momb.checkBox_9.setChecked(True)
            add_momb.checkBox_10.setChecked(False)     

        elif add_momb.comboBox_7.currentText() == "Comptable":
            print("vend")

            add_momb.checkBox.setChecked(False)
            add_momb.checkBox_2.setChecked(False)
            add_momb.checkBox_4.setChecked(True)
            add_momb.checkBox_5.setChecked(True)
            add_momb.checkBox_6.setChecked(False)
            add_momb.checkBox_7.setChecked(True)
            add_momb.checkBox_8.setChecked(False)
            add_momb.checkBox_9.setChecked(False)
            add_momb.checkBox_10.setChecked(False)   

        else:


            add_momb.checkBox.setChecked(False)
            add_momb.checkBox_2.setChecked(False)
            add_momb.checkBox_4.setChecked(False)
            add_momb.checkBox_5.setChecked(False)
            add_momb.checkBox_6.setChecked(False)
            add_momb.checkBox_7.setChecked(False)
            add_momb.checkBox_8.setChecked(False)
            add_momb.checkBox_9.setChecked(False)
            add_momb.checkBox_10.setChecked(False)                                   

    def add_admin_btn(self):
        if add_momb.lineEdit_31.text() =="" or add_momb.lineEdit_32.text() =="":
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Les champs obligatoires doivent être remplis")
            msg1.setWindowTitle("Erreur d'entrée")
            msg1.exec_()   
        else:
            username = add_momb.lineEdit_31.text()
            password = add_momb.lineEdit_32.text()
            if add_momb.checkBox.isChecked():
                acc_add_prodect = True
            else:
                acc_add_prodect = False
            if add_momb.checkBox_5.isChecked():
                acc_add_dep = True
            else:
                acc_add_dep = False            
            if add_momb.checkBox_2.isChecked():
                acc_edit_prod = True
            else:
                acc_edit_prod = False         
            if add_momb.checkBox_4.isChecked():
                acc_stat = True
            else:
                acc_stat = False    
            if add_momb.checkBox_6.isChecked():
                acc_fact = True
            else:
                acc_fact = False          
            if add_momb.checkBox_7.isChecked():
                acc_rapp = True
            else:
                acc_rapp = False    
            if add_momb.checkBox_8.isChecked():
                acc_gar = True
            else:
                acc_gar = False 
            if add_momb.checkBox_9.isChecked():
                acc_ret = True
            else:
                acc_ret = False      
            if add_momb.checkBox_10.isChecked():
                acc_donne = True
            else:
                acc_donne = False     
            cr.execute(f"INSERT INTO Admin (User_name,Password,add_prodect,Modefie,Statsitque,Dep,Facture,Rapport,Gar,Retour,Donne) Values('{username}','{password}','{acc_add_prodect}','{acc_edit_prod}','{acc_stat}','{acc_add_dep}','{acc_fact}','{acc_rapp}','{acc_gar}','{acc_ret}','{acc_donne}')")   
            db.commit()  
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Un nouveau membre a été enregistré avec succès")
            msg1.setWindowTitle("Enregistré avec succès")
            msg1.exec_()   
            self.parametre_admin()

    def edit_admin_btn(self):
        if add_momb.lineEdit_31.text() =="" or add_momb.lineEdit_32.text() =="":
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Les champs obligatoires doivent être remplis")
            msg1.setWindowTitle("Erreur d'entrée")
            msg1.exec_()   
        else:
            username = add_momb.lineEdit_31.text()
            password = add_momb.lineEdit_32.text()
            if add_momb.checkBox.isChecked():
                acc_add_prodect = True
            else:
                acc_add_prodect = False
            if add_momb.checkBox_5.isChecked():
                acc_add_dep = True
            else:
                acc_add_dep = False            
            if add_momb.checkBox_2.isChecked():
                acc_edit_prod = True
            else:
                acc_edit_prod = False         
            if add_momb.checkBox_4.isChecked():
                acc_stat = True
            else:
                acc_stat = False    
            if add_momb.checkBox_6.isChecked():
                acc_fact = True
            else:
                acc_fact = False          
            if add_momb.checkBox_7.isChecked():
                acc_rapp = True
            else:
                acc_rapp = False    
            if add_momb.checkBox_8.isChecked():
                acc_gar = True
            else:
                acc_gar = False 
            if add_momb.checkBox_9.isChecked():
                acc_ret = True
            else:
                acc_ret = False      
            if add_momb.checkBox_10.isChecked():
                acc_donne = True
            else:
                acc_donne = False     
            cr.execute(f"Update Admin Set User_name = '{username}' , Password ='{password}',add_prodect='{acc_add_prodect}',Modefie = '{acc_edit_prod}',Statsitque='{acc_stat}',Dep='{acc_add_dep}',Facture='{acc_fact}',Rapport='{acc_rapp}',Gar='{acc_gar}',Retour='{acc_ret}',Donne='{acc_donne}'")   
            db.commit()  
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Les données des membres ont été enregistrées et mises à jour avec succès")
            msg1.setWindowTitle("Mis à jour avec succés")
            msg1.exec_()  
            self.parametre_admin()


    def delet_admin(self):
        if add_momb.lineEdit_31.text() =="" or add_momb.lineEdit_32.text() =="":
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Les champs obligatoires doivent être remplis")
            msg1.setWindowTitle("Erreur d'entrée")
            msg1.exec_()   
        else:
            username = add_momb.lineEdit_31.text()
            password = add_momb.lineEdit_32.text()
            cr.execute(f"DELETE FROM Admin WHERE User_name = '{username}' and Password ='{password}' ")
            db.commit()
            msg1=QMessageBox()
            msg1.setIcon(QMessageBox.Information)
            msg1.setText("Utilisateur supprimé avec succès")
            msg1.setWindowTitle("Effacé avec succès")
            msg1.exec_()   
            add_momb.close()
            self.parametre_admin()
          
    def backup_clear_data(self):
        if acc_admin[0] == "Superadmin" or acc_admin[0] == "SuperUser" or acc_admin[0] == "admin":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("S'il vous plaît soyez prudent avant de confirmer cette étape, cela effacera toutes vos données ... Nous vous fournissons la fonctionnalité d'importation de la copie de sauvegarde, à travers laquelle vous pouvez importer les données de la semaine écoulée si une erreur s'est produite, pour annuler veuillez cliquer sur le bouton annuler")
            msg.setWindowTitle("Efface les données")   
            msg.setStandardButtons( QMessageBox.Cancel |QMessageBox.Ok |QMessageBox.Retry)   
            msg.setButtonText(QMessageBox.Cancel, " annulation" ) 
            msg.setButtonText(QMessageBox.Ok, " Réinitialiser" )
            msg.setButtonText(QMessageBox.Retry, " Récupération de sauvegarde" ) 
            msg.setDefaultButton(QMessageBox.Cancel)
            ret = msg.exec_()
            if ret == QMessageBox.Ok:
                cr.execute("DELETE FROM prodect")
                cr.execute("DELETE FROM prodect_sale")
                cr.execute("DELETE FROM prodect_offre")
                cr.execute("DELETE FROM Facture")
                cr.execute("DELETE FROM Credit_Cart")
                cr.execute("DELETE FROM Retoure")
                cr.execute("DELETE FROM dépenses")
                cr.execute("DELETE FROM fidelity_cart")
                cr.execute("DELETE FROM tasks")
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Information)
                msg1.setText("Toutes les données ont été effacées avec succès, si vous rencontrez le moindre problème, veuillez contacter notre équipe de support et nous essaierons de résoudre le problème rapidement")
                msg1.setWindowTitle("Opération terminée avec succès")
                msg1.exec_()   
            elif ret ==  QMessageBox.Retry:
                try:
                    request = requests.get(url, timeout=timeout)
                    internet = True
                except (requests.ConnectionError, requests.Timeout) as exception:
                    internet = False
                if internet :
                    try : 
                        dbback = sqlite3.connect("DATA/Backup.db")
                        dbback.backup(db)
                        msg1=QMessageBox()
                        msg1.setIcon(QMessageBox.Information)
                        msg1.setText("Sauvegarde importée avec succès,Si vous rencontrez le moindre problème avec le programme, n'hésitez pas à contacter l'équipe support")
                        msg1.setWindowTitle("Opération terminée avec succès")
                        msg1.exec_() 

                    except:
                        try:
                            path_user = f"backup/{Market_Name}/Backup.db"
                            storage.child(path_user).download("DATA/Backup.db") 
                            msg1=QMessageBox()
                            msg1.setIcon(QMessageBox.Information)
                            msg1.setText("Sauvegarde importée avec succès,Si vous rencontrez le moindre problème avec le programme, n'hésitez pas à contacter l'équipe support")
                            msg1.setWindowTitle("Opération terminée avec succès")
                            msg1.exec_() 
                        except:    
                            msg1=QMessageBox()
                            msg1.setIcon(QMessageBox.Information)
                            msg1.setText("Il semble qu'il n'y ait pas de sauvegarde ou que l'appareil ne soit pas connecté à Internet. Veuillez réessayer après avoir redémarré le programme")
                            msg1.setWindowTitle("Il y a un problème lors de l'importation des données")
                            msg1.exec_() 
                else:
                    msg1=QMessageBox()
                    msg1.setIcon(QMessageBox.Information)
                    msg1.setText("Il semble qu'il n'y ait pas de sauvegarde ou que l'appareil ne soit pas connecté à Internet. Veuillez réessayer après avoir redémarré le programme")
                    msg1.setWindowTitle("Pas de connexion Internet")
                    msg1.exec_()

   
                

    

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ########################################################################

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>BIENVENUE </strong> À EMH SMART")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> BASE DE DONNÉES"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> INTERFACE UTILISATEUR"))


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        

        global counter

        # SET VALUE TO PROGRESS BAR
        
        
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
 
        if counter > 100 :
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()

            self.close()
            
            # CLOSE SPLASH SCREEN
        self.addcon()
    def addcon(self):
        global counter

        counter += 1




        # INCREASE COUNTER

        
        

class LoginScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Form_login()
        self.ui.setupUi(self)
        
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        #####################" config"
        
        self.ui.pushButton.clicked.connect(self.login)
        m = True
        while m :
            self.show()
            m = False


        try:
            filehandler = open("DATA/Last_Login.emh","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
            self.ui.lineEdit.setText(object_file)
        except:
            pass    
        self.ui.lineEdit_2.returnPressed.connect(self.login)
        
    def login(self):
        admin = cr.execute("select * from admin").fetchall()
        if admin == []:

            self.close()
            m = True
            while m :
                SplashScreen()
                m=False
        else:
            admin = cr.execute(f"select * from admin Where User_name = '{self.ui.lineEdit.text()}' AND Password = '{self.ui.lineEdit_2.text()}'").fetchone()
            if admin == [] or admin == None :
                msg1=QMessageBox()
                msg1.setIcon(QMessageBox.Warning)
                msg1.setText("identifiant ou mot de passe incorrect         ")
                msg1.setWindowTitle("Les informations sont incorrectes")
                msg1.exec_()
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
            else :
                
                
                
                username = admin[0]
                password = admin[1]

                filename = 'DATA/Last_Login.emh'
                outfile = open(filename,'wb')
                pickle.dump(username,outfile)
                outfile.close()

                acc_admin.append(username)
                acc_admin.append(password)

                
             
                self.close()

                SplashScreen()


                  





                                                              

                            
                               


                                    





    
addo=add_delet.Ui_add_delet
if __name__ == "__main__":
    app = QApplication(sys.argv)

    poro=Payment_Screen()

    app.setWindowIcon(QIcon("icon.ico"))
    if check_driver and check_ex:
        add_suppr = edit_supp_addpromo.Ui_MainWindow()
        toast = ToastNotifier()

        calc = Calculator()
        window = LoginScreen()


        add_momb = addadmin()

        add= addo()
        tasksc = Taskscreen()
        retoursc = retourscreen()
        donnee_clien = Ui_Form_donnee()
    else:
        try:
            os.startfile("imhservice.exe") 
        except:
            
            pass  

    
    
    sys.exit(app.exec_())
