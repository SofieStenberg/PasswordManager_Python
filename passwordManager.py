import os
import sqlite3
from sqlite3 import Error
import hashlib

class PasswordManager:
    __masterhash = ""
    __databaseName = ""

    def __init__(self):
        pass

    # def createMasterFile(path):
    #     masterFile = open(path, 'w')
    #     masterFile.write(PasswordManager.__masterhash)
    #     masterFile.close()

    def createDatabase(path, pwd):
        if(os.path.exists(path)):
            print("File already exists..")
            return
        PasswordManager.__databaseName = path
        
        connection = None
        try:
            connection = sqlite3.connect(path)
        except Error as e:
            print(e)

        sqlStatement = """
                        CREATE TABLE IF NOT EXISTS Passwords(
                        id          INTEGER     PRIMARY KEY     AUTOINCREMENT,
                        username    TEXT    NOT NULL,
                        password    TEXT    NOT NULL,
                        description TEXT);
                       """

        cursor = connection.cursor()
        cursor.execute(sqlStatement)
        connection.commit()

        connection.close()

        PasswordManager.__masterhash = hashlib.sha3_256(pwd.encode()).hexdigest()
        # createMasterFile(path[:-3]+".txt")
        masterFile = open(path[:-3]+".txt", 'w')
        masterFile.write(PasswordManager.__masterhash)
        masterFile.close()

    def openDatabase(path, userMasterPwd):
        database = path[:-3].split('/')[-1]
        
        with open(database + ".txt", 'r') as file:
            masterHash = file.read()

        userPwd = hashlib.sha3_256(userMasterPwd.encode()).hexdigest()
        if (userPwd != masterHash):
            return 1

        PasswordManager.__databaseName = path #database # + ".db"
        PasswordManager.__masterhash = masterHash

        
        
        # display database on treeview!!

    

    # def pwdHashing(pwd):
    #     pass

    def changeMasterPwd():
        pass

    def controlMasterPwd():
        pass

    def addCredentials():
        pass

    # Not sure if I really Need this?
    def displayEntries():
        pass

    def displayPwd():
        pass

    def generatePwd():
        pass

    def replaceIndex():
        pass