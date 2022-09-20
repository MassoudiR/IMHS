import os

import subprocess


"""
current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

print(current_machine_id)       
import socket
print(socket.gethostname())


from cryptography.fernet import Fernet

message = ("hello geeks" )
key = b'3kcuhLtaKhBnDTm2BK8NfTwXvjfYgkC7Tk2yOU3LmY0='
print(key)
 

 
fernet = Fernet(key)
 
# then use the Fernet class instance
# to encrypt the string string must must
# be encoded to byte string before encryption
encMessage = fernet.encrypt(message.encode())
 
print("original string: ", message)
print("encrypted string: ", encMessage)
 
# decrypt the encrypted string with the
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods
decMessage = fernet.decrypt(encMessage).decode()
 
print("decrypted string: ", decMessage)
"""
di = ""
path = "C:/Users/Rayen/Desktop/Dett/pet"
os.makedirs(path, exist_ok = True)
import sqlite3

conn = sqlite3.connect('test_database') 