"""
import requests
url = "http://www.muskfoundation.org/"
timeout = 5
try:
	request = requests.get(url, timeout=timeout)
	print("Connected to the Internet")
except (requests.ConnectionError, requests.Timeout) as exception:
	print("No internet connection.")

"""
import sys
import pickle
from pyrebase import *
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

"""
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
"""
"""
path_user = "backup/marketname/Backup.db"
path_db = "DATA/Backup.db"
storage.child("/backup/marketname").download("testfile")
storage.download("backup")
print("okk")

"""
import subprocess , socket
from datetime import *
from datetime import timedelta
DATE = datetime.now().date()

filehandler = open("data.EMH","rb")
object_file = pickle.load(filehandler)
filehandler.close()
print(object_file)
print(object_file["donnee_ex"])
from cryptography.fernet import Fernet
key = b'3kcuhLtaKhBnDTm2BK8NfTwXvjfYgkC7Tk2yOU3LmY0='
fernet = Fernet(key)
ex = fernet.decrypt(object_file["donnee_ex"]).decode()
print(ex)
exx = datetime.strptime(ex,'%Y-%m-%d').date()
print(exx == DATE)
ex_app = fernet.decrypt(object_file["donnee_ex"]).decode()
name_pc = fernet.decrypt(object_file["name_pc"]).decode()
id_pc =  fernet.decrypt(object_file['info_pc']).decode()
current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
name_driver= socket.gethostname()

check_driver = current_machine_id ==id_pc 
check_name =  name_driver == name_pc
print(check_driver)
print(check_name)
    










"""

data = {"Bienvenue sur l'application EMH SMART" : ("Bienvenue sur l'application EMH SMART","aujourd'hui","test messgae",0),"message2" : ("hy","12-12-22","test messgae",0)}
database.child("message").set(data)
print("yess")
message = database.child("message").get().val()
print(dict(message))
"""


########## type message 
#### table_message = {"Message":("Title","date","messge messge messge messge messge messge messge messge messge messge messge messge messge messge messge") }
"""
import Send_mail

##msg = '<html><body><h1>Hello World</h1>' '<img src="icon.ico" >'  '<p>this is hello world from <a href="http://www.python.org">Python</a>...</p>''</body></html>'
##Send_mail.send_mail("rayenmassoudi7@gmail.com","hy",msg)
message = f"<h1>Bonjour cher ami rayen </h1> , Il semble qu'aujourd'hui soit un bon jour pour rembourser votre dette de "
Send_mail.send_mail("rayenmassoudi7@gmail.com","submsg",message)
"""