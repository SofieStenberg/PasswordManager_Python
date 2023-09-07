import random
class Ceasar:
    __fixedPwd = "f%5DT/6f2c8!&fdz-G?54gd7"

    def __init__(self):
        pass

    

    def encrypt( plainText, masterHash):
        plainLenth = len(plainText)
        masterLength = len(masterHash)
        fixedLength = len(Ceasar.__fixedPwd)
        encryptedPwd = ""
        ASCIIstart = '!'

        for i in range(plainLenth):
            seed = ord(masterHash[i]) * (ord(Ceasar.__fixedPwd[i+1 % masterLength]))
            random.seed(seed)
            fixedIndex = int(random.random() % fixedLength)

            encryptedIndex = (ord(plainText[i])-ord(ASCIIstart)+ord(Ceasar.__fixedPwd[fixedIndex]) - ord(ASCIIstart)) % 94
            encryptedPwd = encryptedPwd + chr(ord(ASCIIstart)+encryptedIndex)
        
        return encryptedPwd
    
    def decrypt(encText, masterHash):
        encLenth = len(encText)
        masterLength = len(masterHash)
        fixedLength = len(Ceasar.__fixedPwd)
        decryptedPwd = ""
        ASCIIstart = '!'

        for i in range(encLenth):
            seed = ord(masterHash[i]) * (ord(Ceasar.__fixedPwd[i+1 % masterLength]))
            random.seed(seed)
            fixedIndex = random.random() % fixedLength

            decryptedIndex = (94 + (ord(encText[i]) - ord(ASCIIstart)) - (ord(Ceasar.__fixedPwd[int(fixedIndex)])-ord(ASCIIstart))) % 94
            decryptedPwd = decryptedPwd + chr(ord(ASCIIstart) + decryptedIndex)

        return decryptedPwd
        

    
# def main():
#     encrypt = Ceasar.encrypt("testing1", "oksrfngoargn")
#     print(encrypt)

#     decrypt = Ceasar.decrypt(str(encrypt), "oksrfngoargn")
#     print(decrypt)

# if __name__ == "__main__": main()