import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import threading
import pickle
from datetime import *
from datetime import timedelta
DATE = datetime.now().date()
DATEM = datetime.now().date().day
import sys
import os
from win10toast import ToastNotifier
import random


list_date_week = []
for day_w in range(7):
    list_date_week.append(str(DATE - timedelta(days =day_w)))







sender_address = 'emhsmart@gmail.com'
sender_pass = 'Emh-Smart2022mail'


def send_mail(receiver_address,mail_Subject,mail_content):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = mail_Subject
    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def tasks_any():
    db = sqlite3.connect("prodect_list.db")
    cr = db.cursor()
    tasck = cr.execute(f"select * from tasks Where date = '{DATE}' and completed = 'NO' ").fetchall()
    mail = cr.execute(f"select DATA_4 from Setting").fetchone()[0]
    submsg = "Vous avez une tâche aujourd'hui à accomplir"
    if tasck != []:
        try :
            filehandler = open("DATA/message.EMH","rb")
            object_file = pickle.load(filehandler)
            filehandler.close()
        except:
            object_file = {}
        for x in tasck:
            ############ sand mail tasks
            message_text = f"Vous avez aujourd'hui une tâche intitulée '{x[0]}' à terminer, n'oubliez pas"

            send_mail(mail,submsg,message_text)
            ############# notficatio tasck 
            n = ToastNotifier()
            n.show_toast(submsg, message_text, duration = 10,icon_path ="icon.ico")
            
            #################### add to msg list 
            if message_text not in object_file:
                object_file[message_text]= [message_text,str(DATE),submsg,0]
        outfile = open("DATA/message.EMH",'wb')
        pickle.dump(object_file,outfile)
        outfile.close()
    db.close()
def test_prodect_ex():
    db = sqlite3.connect("prodect_list.db")
    cr = db.cursor()
    prdect = cr.execute(f"select Nom,BARRE,Date_exp,Stock from prodect Where Date_exp in {tuple(list_date_week)}  ").fetchall()
    mail = cr.execute(f"select DATA_4 from Setting").fetchone()[0]
    if prdect != [] and prdect != None:
        for x in prdect :
            nubsal = 0
            prodect_sale=  cr.execute(f"select Nomb from prodect_sale Where code_bare ='{x[1]}'").fetchall()
            if prodect_sale != [] and prodect_sale !=None:
                for y in prodect_sale:
                    nubsal += int(y[0])
                        
            if x[3] != None and x[3] != "NULL":
                nomb_rest = int(x[3])- nubsal
            else:
                nomb_rest = "None"     


            if x[2] == str(DATE):
                ############ sand mail tasks
                message_text = f"Vous avez un produit appelé {x[0]} avec un code barre {x[1]} qui expire aujourd'hui "
                if nomb_rest != "None":
                    message_text += f" , et il vous en reste  le stock est de {nomb_rest} packs"
                send_mail(mail,"Vous avez un produit qui expire aujourd'hui",message_text)
                #################### add to msg list 
                try :
                    filehandler = open("DATA/message.EMH","rb")
                    object_file = pickle.load(filehandler)
                    filehandler.close()
                except:
                    object_file = {}
                message_title = f"Avertissement produit {x[0]} N° {x[1]} : expire aujourd'hui"    
                if message_title not in object_file:
                    object_file[message_title]= [message_title,str(DATE),message_text,0]
                    outfile = open("DATA/message.EMH",'wb')
                    pickle.dump(object_file,outfile)
                    outfile.close()


            else:
                message_text = f"Vous avez un produit appelé {x[0]} avec un code barre {x[1]} qui va bientôt expirer"
                if nomb_rest != "None":
                    message_text += f" , et il vous en reste le stock est de {nomb_rest} packs"
                send_mail(mail,"Vous avez un produit qui expire aujourd'hui",message_text)
                message_title = f"Avertissement produit {x[0]} N° {x[1]} : bientôt expirer" 
                try : 
                    filehandler = open("DATA/message.EMH","rb")
                    object_file = pickle.load(filehandler)
                    filehandler.close()
                except:
                    object_file = {}  
                if message_title not in object_file:
                    object_file[message_title]= [message_title,str(DATE),message_text,0]
                    outfile = open("DATA/message.EMH",'wb')
                    pickle.dump(object_file,outfile)
                    outfile.close()
    db.close()            

def test_prodect_sal():
    db = sqlite3.connect("prodect_list.db")
    cr = db.cursor()

    prodect = cr.execute("select BARRE,Nom ,Stock,Stock_minimal from prodect where Stock is not 'NULL'").fetchall()
    mail = cr.execute(f"select DATA_4 from Setting").fetchone()[0]
    if prodect != None and prodect != []:
        for x in prodect:
            nomb_stk = int(x[2])
            numb_sale = 0
            sale = cr.execute(f"select nomb from prodect_sale where code_bare = '{x[0]}'").fetchall()
            if sale != None and sale != []:
                for y in sale:
                    numb_sale += int(y[0])
                nomb_stk -= numb_sale
                if x[3] != "NULL"  and x[3] != None:
                    if nomb_stk <= int(x[3]) and nomb_stk >=0:
                        if nomb_stk ==0:
                            message_title = f"Produit {x[0]} en rupture de stock"
                            message = f"Le produit appelé {x[1]} N°{x[0]} est en rupture de stock"
                            ##############" sand mail"
                            send_mail(mail,message_title,message)
                            ############ message


                        else:
                            message_title = f"Produit {x[0]} Bientôt en rupture de stock"
                            message = f"Le produit appelé {x[1]} N°{x[0]} Bientôt en rupture de stock"
                            ##########" send mail"
                            send_mail(mail,message_title,message)
                        try :
                            filehandler = open("DATA/message.EMH","rb")
                            object_file = pickle.load(filehandler)
                            filehandler.close()
                        except:
                            object_file = {}
                        if message_title not in object_file:
                            object_file[message_title]= [message_title,str(DATE),message,0]
                            outfile = open("DATA/message.EMH",'wb')
                            pickle.dump(object_file,outfile)
                            outfile.close()    

                elif int(x[2]) <= 10 and nomb_stk >=0 :
                    if nomb_stk ==0:
                        message_title = f"Produit {x[0]} en rupture de stock"
                        message = f"Le produit appelé {x[1]} N°{x[0]} est en rupture de stock"
                        ######## send mail 
                        send_mail(mail,message_title,message)
                    else:
                        message_title = f"Produit {x[0]} Bientôt en rupture de stock"
                        message = f"Le produit appelé {x[1]} N°{x[0]} Bientôt en rupture de stock"
                        ########## send mail
                        send_mail(mail,message_title,message)
                    try :
                        filehandler = open("DATA/message.EMH","rb")
                        object_file = pickle.load(filehandler)
                        filehandler.close()
                    except:
                        object_file = {}
                    if message_title not in object_file:
                        object_file[message_title]= [message_title,str(DATE),message,0]
                        outfile = open("DATA/message.EMH",'wb')
                        pickle.dump(object_file,outfile)
                        outfile.close()    

    db.close()

def clien_credit():
    db = sqlite3.connect("prodect_list.db")
    cr = db.cursor()
    list_clien = cr.execute(f"select Name_Clien,Email,Credit from Credit_Cart Where Pyment_date = '{DATEM}' ").fetchall()
    name_store = cr.execute(f"select DATA from Setting").fetchone()[0]
    if list_clien != [] and list_clien != None:
        for x in list_clien:
            mail_of_clien = x[1]
            name_clien = x[0]
            credit = float(x[2])
            if mail_of_clien != "NULL" and mail_of_clien != None:
                if credit > 0:
                    submsg = "Bonjour, nous vous rappelons une dette qui doit être payée"
                    if name_clien != "NULL" and name_clien != None:
                       message = f"<h1>Bonjour cher ami {name_clien}</h1> , Il semble qu'aujourd'hui soit un bon jour pour rembourser votre dette de {credit} dinars dans notre magasin {name_store}"
                    else:
                       message = f"<h1>Bonjour cher ami</h1> , Il semble qu'aujourd'hui soit un bon jour pour rembourser votre dette de {credit} dinars dans notre magasin {name_store}"
                    send_mail(mail_of_clien,submsg,message)

def backup_db():
    try :
        filehandler = open("DATA/backup.EMH","rb")
        backup = pickle.load(filehandler)
        filehandler.close()
    except:
        backup = False
    ###############################
    if int(DATEM) == 12 and backup == False:
        db = sqlite3.connect("prodect_list.db")
        db_back = sqlite3.connect("DATA/Backup.db")
        db.backup(db_back)
    ################################
        backup = True
        outfile = open("DATA/backup.EMH",'wb')
        pickle.dump(backup,outfile)
        outfile.close()
    ############################# 
        return True
    elif int(DATEM) == 8:
        backup = False
        outfile = open("DATA/backup.EMH",'wb')
        pickle.dump(backup,outfile)
        outfile.close()
        return False
    else:
        return False    
        
    
