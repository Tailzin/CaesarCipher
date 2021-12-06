import pymongo
import database
from datetime import datetime
mydb = database.mydb
mycol = database.mycol
#caesar cipher cryptographying function
def cryptography(text,n):
    result = ''
    #iterate through characters
    for i in range(len(text)):
        character = text[i]
        #this cryptographies the spaces of the text
        if character == " ":
            result += chr((ord(character)+n-33)%14 + 33)
            continue   
        elif(character.isupper()):
            result += chr((ord(character)+n-65)%26 + 65)
        else:
            result += chr((ord(character)+n-97)%26 + 97)  

    return result        

#caesar cipher decryptographying function
def decryptography(text):
    text = text.upper()
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    space = '!"#$%&`()*+\'-./,'
    result = []
    for key in range(len(letters)):
        translated = ''
        for symbol in text:
            if symbol in space:
                translated += " "
            elif symbol in letters:
                num = letters.find(symbol)
                num = num - key
                if num < 0:
                    num = num+len(letters)
                translated = translated + letters[num]
            else:
                translated = translated + symbol
        result.append(translated)    
    return result     


ids = mycol.estimated_document_count()+1
manageNumber = ""
while manageNumber != 0:
    print("\n1) Cryptography a text and add to database.")
    print("2) Decryptography a text and add to database.")
    print("3) Delete from database.")
    print("4) Check database.")
    print("0) Quit program.")
    manageNumber = int(input("Choose your action: "))
    if manageNumber == 1:
        text = str(input("\nType what you want to cryptography: "))
        shift = int(input("Type how many times you want to shift: "))
        name = str(input("Name to insert in the database: "))
        cryptoResult = cryptography(text, shift)
        print("Text: {}, Cryptographied text: {}".format(text, cryptoResult))
        databaseInsert = {"_id": ids, "name": "{}".format(name), "cryptographied": ["{}".format(cryptoResult)], "date": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]}
        try:
            find = mycol.find_one({"name": name}, {"_id":1})
            #this returns the id for the database document
            for key,values in find.items():
                id = values
            #updates database to add the results to the same name
            update = mycol.update_one({'_id': id},{ "$push": {"cryptographied": cryptoResult, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}})
        except:
            check = 1
            while check != 0:
                if mycol.find_one({"_id": ids}) == None:
                    insert = mycol.insert_one(databaseInsert)    
                    check = 0
                else:
                    ids+=1
                databaseInsert = {"_id": ids, "name": "{}".format(name), "cryptographied": ["{}".format(cryptoResult)], "date": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]}    
                    
    elif manageNumber == 2:
        text = str(input("\nType what you want to decryptography: "))
        name = str(input("Name to insert in the database: "))
        decryptoResult = decryptography(text)
        print("Text: {}, Decryptography Results: {}".format(text, decryptoResult))
        databaseInsert = {"_id": ids, "name": "{}".format(name), "decryptographied": [decryptoResult], "date": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]}
        try:
            find = mycol.find_one({"name": name}, {"_id":1})
            #this returns the id for the database document
            for key,values in find.items():
                id = values
            #updates database to add the results to the same name
            update = mycol.update_one({'_id': id},{ "$push": {"decryptographied": decryptoResult, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}})
        except:
            check = 1
            while check != 0:
                if mycol.find_one({"_id": ids}) == None:
                    insert = mycol.insert_one(databaseInsert)    
                    check = 0
                else:
                    ids+=1
                databaseInsert = {"_id": ids, "name": "{}".format(name), "decryptographied": [decryptoResult], "date": [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]}        
    
    elif manageNumber == 3:
        name = str(input("\nType your name: "))
        find = mycol.find_one({"name": name})
        if find != None:
            print(find)
            confirmation = str(input("Do you really want to delete this entry?(y or n)"))
            if confirmation == "y" or confirmation == "Y":
                databaseDelete = mycol.delete_one(find)
                print(databaseDelete.acknowledged)
                if databaseDelete.acknowledged:
                    print("\nYour entry was successfully deleted")
                else:
                    print("\nAn error occurred your entry was not deleted")
            else:
                print("\nYour entry was not deleted.")
                print(find)
        else:
            print("\nThat name does not exist in the database.")
        
    elif manageNumber == 4:
        for x in mycol.find():
            print(x)        
    else:
        print("\nThis option does not exist.")        
        