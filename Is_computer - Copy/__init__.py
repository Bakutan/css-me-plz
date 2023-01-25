import pandas as pd
import os 
from datetime import datetime
import csv

def AddUser(name: str,pw: str):
    check = os.path.exists("templates/UserData.csv")
    if check != True:
        df = pd.DataFrame({
            "name":[name],
            "password":[pw],
        })
        df.to_csv("templates/UserData.csv",mode="w",index=False)
    else:
        df = pd.DataFrame({
        "name":[name],"password":[pw],
            })
        df.to_csv("templates/UserData.csv",mode="a",header=False,index=False)

def AddBook(name: str,pw: str):
    check = os.path.exists("templates/BookData.csv")
    if check != True:
        df = pd.DataFrame({
            "name":[name],
            "password":[pw],
            "status":["Available"]
        })
        df.to_csv("templates/BookData.csv",mode="w",index=False)
    else:
        df = pd.DataFrame({
        "name":[name],
        "password":[pw],
        "status":["Available"]
            })
        df.to_csv("templates/BookData.csv",mode="a",header=False,index=False)

def gettime():
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y/%H:%M:%S")
    return  date_time

def writehistory(Bname:str,action:bool):
    """varible "action" if true = Borrowed otherwise, returned"""
    check = os.path.exists("templates/History.csv")
    time = gettime()

    if action == True:
        actions = "Borrowed"
    else:
        actions = "Returned"

    if check != True:
        df = pd.DataFrame({
            "Book_name":[Bname],
            "action":[actions],
            "time":[time],
        })
        df.to_csv("templates/History.csv",mode="w",index=False)
    else:
        df = pd.DataFrame({
            "Book_name":[Bname],
            "action":[actions],
            "time":[time],
        })
        df.to_csv("templates/History.csv",mode="a",index=False,header=False)

def ReadBookData(getheader:bool):
    if os.path.exists("templates/BookData.csv") != True:
        field = []
        pass
    else: 
        if getheader is True:
            with open("templates/BookData.csv","r") as file:
                reader = csv.reader(file, lineterminator="\n")
                field = [x for x in reader]
                file.close()
        else:
            with open("templates/BookData.csv","r") as file:
                reader = csv.reader(file, lineterminator="\n")
                header = next(reader);del header
                field = [x for x in reader]
                file.close()        
    return field

def checkpw(pw:str):
    """Check if any pass are duplicate 
    True: These are duplicate"""
    if os.path.exists("templates/BookData.csv") != True:
        check = False
    else:
        with open("templates/BookData.csv","r") as file:
            reader = csv.reader(file, lineterminator="\n")
            header = next(reader)
            del header
            field = [x for x in reader]
            check = False
            for row in field:
                if pw in row[1]:
                    check = True
                    break
    return check

def checkUserpw(Userpw:str):
    """Check if any pass are duplicate 
    True: These are duplicate"""
    if os.path.exists("templates/UserData.csv") != True:
        check = False
    else:
        with open("templates/UserData.csv","r") as file:
            reader = csv.reader(file, lineterminator="\n")
            header = next(reader)
            del header
            field = [x for x in reader]
            for row in field:
                if Userpw in row[1]:
                    check = True
                    break
    return check