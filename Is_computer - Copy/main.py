from __init__ import *
from flask import Flask,request,session,render_template,url_for,redirect,send_file
import random,string
import csv

app = Flask(__name__)
letter = string.ascii_letters
secret_key = [''.join(random.choice(letter) for i in range(12))]
app.secret_key = secret_key

#ชื่อไฟล์ที่ใช้ทั้งหมด
history = "templates/History.csv"
bookdata = "templates/BookData.csv"
addlist = "templates/Addlist.csv"
returnlist = "templates/ReturnList.csv"
download = "templates/download.csv"
userdata = "templates/UserData.csv"

@app.route('/')
def Homepage():
    return render_template("index.html")

@app.route('/BorrowBook')
def BorrowBook():
    if os.path.exists(addlist) != True :
        pass
    else:
        os.remove(addlist)
    if os.path.exists(bookdata) != True:
        field = [["ยังไม่มีรายชื่อหนังสือ","รอผุ้ดูแลมาเพิ่มหนังสือก่อนนะ",""]]
    else:
        field = ReadBookData(getheader=False)
    field1 = [item for item in field if item[2] != "Unavailable"]
    return render_template("borrow.html", name=field1)

@app.route('/Addtolist',methods=['GET','POST'])
def Addtolist():
    data = ReadBookData(getheader=False)
    data1 = [item for item in data if item[2] != "Unavailable"]
    Bname = request.values.get("bookname")
    Bpass = request.values.get("bookpas")
    if Bname is None or Bpass is None:
        pass
    else:
        if os.path.exists(addlist) != True:
            df = pd.DataFrame({
                "name":[Bname],
                "password":[Bpass]
                    })
            df.to_csv(addlist,mode="w", index=False)
        else:
            df = pd.DataFrame({
                "name":[Bname],
                "password":[Bpass]
                    })
            df.to_csv(addlist,mode="a",index=False,header=False)
    with open(addlist,"r") as file:
        reader = csv.reader(file,lineterminator="\n")
        header = next(reader);del header
        data2 = [row for row in reader]
        file.close()
    return render_template("borrow.html",lists=data2, name=data1)

@app.route("/Adelete/<string:pw1>",methods=["GET"])
def Adelete(pw1):
    with open(addlist,"r") as file:
        read = csv.reader(file,lineterminator="\n")
        field = [row for row in read]
        for row in field:
            if row[1] == pw1:
                field.remove(row)
        file.close()

    with open(addlist,"w") as file:
        write = csv.writer(file, lineterminator="\n")
        write.writerows(field)
        file.close()

    return redirect(url_for("Addtolist"))

@app.route("/ComfirmBorrow",methods=["GET","POST"])
def ComfirmBorrow():
    try:
        with open(addlist,"r") as file:
            reader = csv.reader(file,lineterminator="\n")
            header = next(reader)
            field1 = [row for row in reader]
            file.close()

        for item in field1:
            writehistory(Bname=item[0],action=True)

        a = ReadBookData(getheader=True)
        field2 = [x for x in a]

        for item in field2:
            for data in field1:
                if data[0] == item[0] and data[1] == item[1] and item[2]=="Available":
                    item[2] = "Unavailable"
                    break

        with open(bookdata,"w",newline='') as file:
            writer = csv.writer(file)
            writer.writerows(field2)  
            file.close()
    except OSError:
        return redirect(url_for("BorrowBook"))
    return redirect(url_for("BorrowBook"))
        
@app.route('/ReturnBook')
def ReturnBook():
    if os.path.exists(returnlist) != True:
        pass
    else:
        os.remove(returnlist)
    if os.path.exists(bookdata) != True:
        field = [["หนังสือทุกเล่มยังอยู่ครบ","ได้เวลาไปยืมหนังสือแล้ว",""]]
    else:
        field = ReadBookData(getheader=False)
    data1 = [item for item in field if item[2] != "Available"]
    return render_template("return.html",name=data1)

@app.route('/Returntolist',methods=['GET','POST'])
def Returntolist():
    data = ReadBookData(getheader=False)
    data1 = [item for item in data if item[2] != "Available"]
    Bname = request.values.get("bookname")
    Bpass = request.values.get("bookpas")
    if Bname is None or Bpass is None:
        pass
    else:
        if os.path.exists(returnlist) != True:
            df = pd.DataFrame({
                    "name":[Bname],
                    "password":[Bpass]
                        })
            df.to_csv(returnlist,mode="w", index=False)
        else:
            df = pd.DataFrame({
                    "name":[Bname],
                    "password":[Bpass]
                        })
            df.to_csv(returnlist,mode="a",index=False,header=False)

    with open(returnlist,"r") as file:
        read = csv.reader(file,lineterminator="\n")
        header = next(read);del  header
        field = [row for row in read] 
        file.close() 
    return render_template("return.html",lists = field, name=data1)

@app.route("/delete/<string:pw2>",methods=["GET"])
def delete(pw2):
    with open(returnlist,"r") as file:
        read = csv.reader(file,lineterminator="\n")
        field = [row for row in read]
        for row in field:
            if row[1] == pw2:
                field.remove(row)
        file.close()

    with open(returnlist,"w") as file:
        write = csv.writer(file, lineterminator="\n")
        write.writerows(field)
        file.close()

    return redirect(url_for("Returntolist"))

@app.route("/Comfirmreturn",methods=["GET","POST"])
def Comfirmreturn():
    try:
        with open(returnlist,"r") as file:
            reader = csv.reader(file,lineterminator="\n")
            header = next(reader);del header
            field1 = [row for row in reader]
            file.close()

        for item in field1:
            writehistory(Bname=item[0], action=False)
            
        a = ReadBookData(getheader=True)
        field2 = [x for x in a]

        for item in field2:
            for data in field1:
                if data[0] == item[0] and data[1] == item[1] and item[2]=="Unavailable":
                    item[2] = "Available"
                    break

        with open(bookdata,"w",newline='') as file:
            writer = csv.writer(file)
            writer.writerows(field2)
            file.close()
    except OSError:
        return redirect(url_for("ReturnBook"))

    return redirect(url_for("ReturnBook"))

@app.route('/ShowData')
def ShowBookData():
    if os.path.exists(bookdata) != True:
        data1 = [["ยังไม่มีรายชื่อหนังสือ","รอผุ้ดูแล","มาเพิ่มหนังสือก่อนนะ"]]
    else:
        data1 = ReadBookData(getheader=False)
    return render_template("showdata.html",name=data1)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if os.path.exists(userdata) != False:
        pass
    else:
        return redirect(url_for('Add_user'))

    if request.method == "POST":
        name = request.form.get("username")
        pw = request.form.get("password")
        with open(userdata,"r") as file:
            reader = csv.reader(file,lineterminator="\n")
            header = next(reader);del header
            field = [x for x in reader]
            file.close()
        for data in field:
            if data[0] == name and data[1] == pw:
                session['username'] = name
                data1 = ReadBookData(getheader=False)
                return render_template("bookdata.html",name=data1)

    return render_template('login.html')

@app.route('/BookData')
def BookData():
    if 'username' in session:
        data1 = ReadBookData(getheader=False)
        return render_template("bookdata.html",name=data1)
    return redirect(url_for("login"))

@app.route('/addbook',methods=['GET', 'POST'])
def Addbook():
    if 'username' not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        Bname = request.values.get('AddName')
        Bpass = request.values.get('AddTag')
        check = checkpw(Bpass)
        if check is False:
            AddBook(name=Bname,pw=Bpass)
        return redirect(url_for("Addbook"))            
    else:
        data1 = ReadBookData(getheader=False)
        return render_template("addbookadmin.html",name=data1)

@app.route('/removebook',methods=['GET', 'POST'])
def Removebook():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        try:
            Bname = request.values.get('AddName')
            Bpass = request.values.get('AddTag')
            field = ReadBookData(getheader=True)
            for row in field:
                if Bname in row[0] and Bpass in row[1]:
                    field.remove(row)
                file.close()
            with open(bookdata,'w') as file:
                csvwriter = csv.writer(file,lineterminator="\n")
                csvwriter.writerows(field)
                file.close()
            return redirect(url_for("Removebook"))
        except OSError:
            return "error has occured"            
    else:
        data1 = ReadBookData(getheader=False)
        return render_template("removebook.html",name=data1)

@app.route('/historybook')
def LookData():
    if 'username' not in session:
        return redirect(url_for("login"))
    if os.path.exists(history) != False:
        with open(history,"r") as file:
            read = csv.reader(file,lineterminator="\n")
            header = next(read);del header
            Field = [item for item in read]
            data = Field[::-1]
    else:
        data = []
    return render_template("historybook.html",name=data)

@app.route("/downloads")
def downloads():
    if 'username' not in session:
        return redirect(url_for("login"))

    if os.path.exists(download) != True:
        pass
    else:
        os.remove(download)
    try:
        with open(history,"r") as file:
            reader = csv.reader(file,lineterminator="\n")
            header = next(reader)
            field = [item for item in reader]
            file.close()
    except OSError:
        return redirect(url_for('LookData'))

    with open(download,"w") as file:
        writer = csv.writer(file,lineterminator="\n")
        writer.writerow(header)
        writer.writerows(field[::-1])
    path = "templates/download.csv"
    return send_file(path,as_attachment=True)

@app.route('/adduser',methods=['GET', 'POST'])
def Add_user():
    if request.method == "POST":
        name = request.form.get('username')
        pw = request.form.get('password')
        if checkUserpw(pw) is False:
            AddUser(name=name,pw=pw)
        return redirect(url_for('BookData'))
    return render_template('sign.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('Homepage'))

if __name__ == "__main__":
    app.run(debug=True)