import os
import random
import sqlite3
from sqlite3 import Error
import hashlib
from Ceasar import *

class PasswordManager:
    __masterhash = ""
    __databasePath = ""

    def __init__(self):
        pass

    # def createMasterFile(path):
    #     masterFile = open(path, 'w')
    #     masterFile.write(PasswordManager.__masterhash)
    #     masterFile.close()

    # values should be a tuple = (x, x, x, x)
    def SQLexecution(sqlStatement, values):
        connection = None
        try:
            connection = sqlite3.connect(PasswordManager.__databasePath)
        except Error as e:
            print(e)
        
        cursor = connection.cursor()
        if (len(values) == 0):
            cursor.execute(sqlStatement)
        else:
            cursor.execute(sqlStatement, values)
        connection.commit()
        connection.close()


    def createDatabase(path, pwd):
        if(os.path.exists(path)):
            print("File already exists..")
            return
        PasswordManager.__databasePath = path

        sqlStatement = """
                        CREATE TABLE IF NOT EXISTS Passwords(
                        id          INTEGER     PRIMARY KEY     AUTOINCREMENT,
                        username    TEXT    NOT NULL,
                        password    TEXT    NOT NULL,
                        description TEXT);
                       """

        PasswordManager.SQLexecution(sqlStatement, ())

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

        PasswordManager.__databasePath = path #database # + ".db"
        PasswordManager.__masterhash = masterHash

        
        
        # display database on treeview!!

    

    # def pwdHashing(pwd):
    #     pass

    def changeMasterPwd(newMasterPwd):
        connection = None
        try:
            connection = sqlite3.connect(PasswordManager.__databasePath)
        except Error as e:
            print(e)
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM Passwords")
        entries = cursor.fetchall()
        id = 1
        newMasterPwd = hashlib.sha3_256(newMasterPwd.encode()).hexdigest()

        for row in entries:
            decryptOld = Ceasar.decrypt(row[0], PasswordManager.__masterhash)
            encryptNew = Ceasar.encrypt(decryptOld, newMasterPwd)
            sqlStatement = "UPDATE Passwords SET password = ? WHERE id = ?"
            values = (encryptNew, id)
            cursor.execute(sqlStatement, values)
            id = id + 1

        connection.commit()
        connection.close()

        PasswordManager.__masterhash = newMasterPwd
        masterFile = open(PasswordManager.__databasePath[:-3]+".txt", 'w')
        masterFile.write(PasswordManager.__masterhash)
        masterFile.close()


    def controlMasterPwd(masterPwd):
        if (PasswordManager.__masterhash == hashlib.sha3_256(masterPwd.encode()).hexdigest()):
            return True
        return False

    def addCredentials(username, pwd, desc):
        encryptedPwd = Ceasar.encrypt(pwd, PasswordManager.__masterhash)
        sqlStatement = "INSERT INTO Passwords (username, password, description) VALUES (?, ?, ?)"
        PasswordManager.SQLexecution(sqlStatement, (username, encryptedPwd, desc))

    # Not sure if I really Need this?
    # def displayEntries():
    #     pass

    def displayPwd():
        pass

    def generatePwd():
        pwdLength = 16
        generatedPwd = ""
        ASCIIstart = '!'
        container = {'A':0, 'a':0, '1':0, '!':0}
        randomNr = 0
        goOn = True

        for i in range(pwdLength):
            randomNr = random.randint(0, 94)
            ASCIIchar = ord(ASCIIstart)+randomNr

            # Don't want the following chars; ', <, >, `
            while (ASCIIchar == 39 or ASCIIchar == 60 or ASCIIchar == 62 or ASCIIchar == 96):
                randomNr = random.randint(0, 94)
                ASCIIchar = ord(ASCIIstart)+randomNr

            if(ASCIIchar <= 90 and ASCIIchar >= 65):
                container['A'] = container['A']+1
                generatedPwd = generatedPwd + chr(ASCIIchar)
            
            elif(ASCIIchar <= 122 and ASCIIchar >= 97):
                container['a'] = container['a']+1
                generatedPwd = generatedPwd + chr(ASCIIchar)

            elif(ASCIIchar <= 57 and ASCIIchar >= 48):
                container['1'] = container['1']+1
                generatedPwd = generatedPwd + chr(ASCIIchar)

            else:
                container['!'] = container['!']+1
                generatedPwd = generatedPwd + chr(ASCIIchar)

        if(container['A'] > 0 and container['a'] > 0 and container['1'] > 0 and container['!'] > 0):
            return generatedPwd
            
        biggestInt = 0
        biggestChar = 0
        goOn = True
        index = 0

        while(goOn):
            if((container['A'] > 0) and (container['a'] > 0) and (container['1'] > 0) and (container['!'] > 0)):
                goOn = False
                break

            for entry in container:
                if(container[entry] > biggestInt):
                    biggestInt = container[entry]
                    biggestChar = entry

            index = PasswordManager.replaceIndex(generatedPwd, biggestChar)
            container[biggestChar] = container[biggestChar]-1

            if(container['A'] == 0):
                randomNr = random.randint(0, 26)
                newChar = chr(ord('A')+randomNr)
                generatedPwd = generatedPwd[:index] + newChar + generatedPwd[index+1:]
                container['A'] = container['A']+1

            elif(container['a'] == 0):
                randomNr = random.randint(0, 26)
                newChar = chr(ord('a')+randomNr)
                generatedPwd = generatedPwd[:index] + newChar + generatedPwd[index+1:]
                container['a'] = container['a']+1
            
            elif(container['1'] == 0):
                randomNr = random.randint(0, 10)
                newChar = chr(ord('1')+randomNr)
                generatedPwd = generatedPwd[:index] + newChar + generatedPwd[index+1:]
                container['1'] = container['1']+1

            else:
                goOn = True
                while(goOn):
                    randomNr = random.randint(0, 94)
                    if ( 
                        ((randomNr >= ord('!')+0) and (randomNr <= ord('!')+6)) or
                        ((randomNr >= ord('!')+7) and (randomNr <= ord('!')+14)) or
                        ((randomNr >= ord('!')+25) and (randomNr <= ord('!')+26)) or
                        (randomNr == ord('!')+28) or
                        ((randomNr >= ord('!')+30) and (randomNr <= ord('!')+31)) or
                        ((randomNr >= ord('!')+58) and (randomNr <= ord('!')+62)) or
                        ((randomNr >= ord('!')+90) and (randomNr <= ord('!')+93))
                        ):
                        goOn = False; 

                newChar = chr(ord('!') + randomNr)
                generatedPwd = generatedPwd[:index] + newChar + generatedPwd[index+1:]
                container['!'] = container['!']+1

        return generatedPwd

    def replaceIndex(generatedPwd, biggestChar):
        pwdLength = len(generatedPwd)

        if(biggestChar == 'A' or biggestChar == 'a'):
            for index in range(pwdLength):
                if((ord(generatedPwd[index]) > (ord(biggestChar)+0)) or (ord(generatedPwd[index]) < (ord(biggestChar)+26))):
                    return index
        
        elif(biggestChar == '1' or biggestChar == '1'):
            for index in range(pwdLength):
                if((ord(generatedPwd[index]) > (ord(biggestChar)+0)) or (ord(generatedPwd[index]) < (ord(biggestChar)+10))):
                    return index
                
        else:
            for index in range(pwdLength):
                if(
                    ((ord(generatedPwd[index]) > (ord(biggestChar)+0)) and (ord(generatedPwd[index]) < (ord(biggestChar)+6))) or
                    ((ord(generatedPwd[index]) > (ord(biggestChar)+7)) and (ord(generatedPwd[index]) < (ord(biggestChar)+14))) or
                    ((ord(generatedPwd[index]) > (ord(biggestChar)+24)) and (ord(generatedPwd[index]) < (ord(biggestChar)+27))) or
                    (ord(generatedPwd[index]) == (ord(biggestChar)+29)) or
                    ((ord(generatedPwd[index]) > (ord(biggestChar)+31)) and (ord(generatedPwd[index]) < (ord(biggestChar)+33))) or
                    ((ord(generatedPwd[index]) > (ord(biggestChar)+59)) and (ord(generatedPwd[index]) < (ord(biggestChar)+64))) or
                    ((ord(generatedPwd[index]) > (ord(biggestChar)+91)) and (ord(generatedPwd[index]) < (ord(biggestChar)+95)))
                ):
                    return index