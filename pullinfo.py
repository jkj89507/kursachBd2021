from work_withBD import *
from cryptography.fernet import Fernet
import hashlib

admin = Control("main", "db_creator", "12345Q", "localhost", 5432)
cipher = Fernet(b'NYrglWWXOHXsabMDuxApVIIO0X8NXRLSZBbdmNI9nus=')
salt = 'dsvdsdvs'.encode()


'''
from cryptography.fernet import Fernet
cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)
text = (cipher.encrypt(bytes("23423Gewfe-", 'utf-8')))
print(text)
b'gAAAAABf_I7nW_GUukAT8okQS84uj7m0IAY_8yg2wbx4HgZwJZ2jDAOSb3y83nKuQuIKMkrk2JmpbDh-SM_WfwE7a2cA4OA6hw=='
print(text.decode('utf-8')) #serif
gAAAAABf_I7nW_GUukAT8okQS84uj7m0IAY_8yg2wbx4HgZwJZ2jDAOSb3y83nKuQuIKMkrk2JmpbDh-SM_WfwE7a2cA4OA6hw==
>>> decrypted_text = cipher.decrypt(text)
decrypted_text = cipher.decrypt(text).decode('utf-8') #no_serif
print(decrypted_text)
23423Gewfe-

'''
'''with open('data_login.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 1
    for row in spamreader:
        arr = row[0].split(";")
        admin.createElTable("data_login", (arr[0], hashlib.pbkdf2_hmac('sha256', arr[1].encode(), salt, 100000).hex(), i)) #data_login.csv
        i += 1
        print('data_login: ',i)

        #owner@owner.com;seHut56aegvd

with open('bank_info.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 1
    for row in spamreader:
        arr = row[0].split(";")
        text = cipher.encrypt(bytes(arr[0], 'utf-8'))
        admin.createElTable("bank_info", (i, text.decode("utf-8"), int(arr[1]))) #bank_info.csv
        i += 1
        print('bank_info: ',i)

        #1111-1111-1111-1111;56789

with open('info_user.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 1
    for row in spamreader:
        arr = row[0].split(";")
        admin.createElTable("info_user", (i ,arr[0], arr[1], arr[2], 'user')) #user.csv
        i += 1
        print('info_user: ',i)

        #Sergey Davidov;RF Mari El Volkova apt.149;Mon Aug 27 1989 21:33:33

with open('info_work.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 1
    for row in spamreader:
        arr = row[0].split(";")
        admin.createElTable("info_work", (arr[0], arr[1], arr[2])) #info_work.csv
        i += 1
        print('info_work: ',i)
        #Sergey Davidov; 8(800)555-35-35;Gofast
admin.updateElTable("info_user", "name='Sergey Davidov'", role="'"+"owner"+"'")'''



'''with open('service.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 1
    for row in spamreader:
        arr = row[0].split(";")
        admin.createElTable("service", (i ,arr[0][0:25], arr[1])) #service.csv
        i += 1
'''