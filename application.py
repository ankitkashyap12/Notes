import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file
from flask_wtf.file import FileField
from wtforms import SubmitField, Form
from flask_wtf import Form
from io import BytesIO
#from Flaskform import form

conn = sqlite3.connect("info.db",check_same_thread=False)
cur = conn.cursor()
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
@app.route('/login')
@app.route('/login.html')
def login1():
	return render_template("login.html")

@app.route('/display')
@app.route('/display.html')
def display1():
	return render_template("display.html")

# @app.route('/teacher1')
# @app.route('/teacher')
# @app.route('/teacher.html')
# def teacher1():
#     form1 = UploadForm()
#     return render_template("teacher.html",form=form1)




@app.route('/index')
@app.route("/", methods = ["GET","POST"])
def index():
    flag=0
    form5 = UploadForm()
    if request.method == "GET" :
        return render_template("index.html")
    else:
        sem1 = request.form.get("sem1")
        sub1 = request.form.get("sub1")
        cur.execute("select pdf,teacher_name1,notes_id from notes where sub_name1=?",(sub1,))
        row3 = cur.fetchall()
        conn.commit()
        #print(row3)
        if not row3 :
            flag=1
            return render_template("index.html",flag=flag)
        return render_template("display.html",row3=row3,sem1=sem1,sub1=sub1,form=form5)
        

@app.route("/display", methods = ["GET"])
def display():
    if request.method == "GET" :
        return render_template("display.html")


@app.route("/login", methods = ["GET","POST"])
def login():
    flag1=0
    if request.method == "GET" :
        return render_template("login.html")
    else :
        form2 = UploadForm()
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        if email!="csebit@gmail.com" or pwd!= "cse123":
            flag1=1
            return render_template("login.html",flag1=flag1)
        if email=="csebit@gmail.com" and pwd== "cse123":
            return render_template("teacher.html",form=form2)  



class UploadForm(Form):
    file = FileField()
    submit = SubmitField("submit")
    download = SubmitField("download")

@app.route("/teacher1", methods = ["POST"])
def teacher1():	
    form4 = UploadForm()
    print("helllllloo")
    return render_template("teacher.html",form=form4)


@app.route("/teacher", methods = ["GET","POST"])
def teacher():    
    form3 = UploadForm()
    print("hiiiii")
    name=request.form.get("tname")
    sem=request.form.get("selectsem")
    sub=request.form.get("selectsub")
    print(name,sem,sub)
    cur.execute("select teacher_name, sub_name from subject where teacher_name=? and sub_name=?",(name,sub))
    row1 = cur.fetchall()
    conn.commit()
    print(row1)
    if not row1:
        param = (name,sem,sub)
        print("hhhh")
        cur.execute("insert into subject (teacher_name,sem,sub_name) values(?,?,?)", param)
        conn.commit()
    cur.execute("select t_id from subject where teacher_name=? and sub_name=?",(name,sub))
    row2= cur.fetchall()
    conn.commit()
    print(row2[0])
    if form3.validate_on_submit():
        file_name = form3.file.data
        database(sub,name,row2[0][0],name1=file_name.filename, data=file_name.read())
    return render_template("teacher.html",form=form3)

def database(sub,name,tid,name1, data):
    param2 = (name1,data,sub,name,tid)
    cur.execute("INSERT INTO notes (pdf_name, pdf,sub_name1,teacher_name1,t_id) VALUES (?,?,?,?,?)",param2)
    conn.commit()

class UploadForm(Form):
    file = FileField()
    submit = SubmitField("submit")
    download = SubmitField("download")


@app.route('/selectsem', methods=['GET','POST'])
def selectsem():
    ret = ''
    print('hello')
    seme=request.args.get('semes')
    print(seme)
    cur.execute("select sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8 from semester where sem=?",(seme))
    rows=cur.fetchall()
    conn.commit()
    print(rows)
    for entry in rows[0]:
         ret += "<option value=%s>%s</option>"%(entry,entry)
    ret='<select name="selectsub" class="orderby" id="selectsub"><option value="0">CHOOSE SUBJECT</option>'+ret+'</select>'
    print(ret)
    return ret

@app.route('/sem1', methods=['GET'])
def sem1():
    ret1 = ''
    #print('hello')
    seme1=request.args.get('semes1')
    #print(seme)
    cur.execute("select sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8 from semester where sem=?",(seme1))
    rows1=cur.fetchall()
    conn.commit()
    print(rows1)
    for entry1 in rows1[0]:
         ret1 += '<option value=%s>%s</option>'%(entry1,entry1)
    ret1= '<select name="sub1" class="orderby" id="sub1"><option value="0">CHOOSE SUBJECT</option>'+ret1+'</select>'                                       
    print(ret1)
    return ret1



@app.route('/download/<id1>', methods=["GET", "POST"])
def download(id1):
    form6 = UploadForm()
    if request.method == "POST":
        c = cur.execute("SELECT pdf_name,pdf FROM notes where notes_id=?",(id1,))

        for x in c.fetchall():
            name_v=x[0]
            data_v=x[1]
            break

        conn.commit()
        return send_file(BytesIO(data_v), attachment_filename='untitled.pdf', as_attachment=True)


    return render_template("display.html", form=form6)
@app.route('/indexA', methods=["GET","POST"])
@app.route("/indexA.html", methods = ["GET","POST"])
def indexatt():
        return render_template("indexA.html")


@app.route("/sdisplay", methods = ["POST"])
def sdisplay():
        usn2=request.form.get("usn")
        sem2=request.form.get("selectsem")
        #print(usn2,sem2)
        cur.execute("select * from marks where usn=? and sem= ?",(usn2,sem2))
        row1=cur.fetchall()
        x=len(row1)
        conn.commit()
        print(row1)
        return render_template("sdisplay.html",row1=row1,x=x,usn2=usn2)

    

@app.route("/logout", methods = ["GET","POST"])
def logout():
        return render_template("indexA.html")


@app.route("/loginATT", methods = ["GET","POST"])
def loginATT():
    if request.method == "GET" :
        return render_template("loginATT.html")

@app.route("/teacherATTN", methods = ["GET","POST"])
def teacherATTN():
    if request.method == "GET":
        return render_template("teacherATT.html")
    else:
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        if email=="csebit@gmail.com" and pwd== "cse123":
            return render_template("teacherATT.html")
        else:
            flag1=1
            return render_template("loginATT.html",flag1=flag1)
semg=0
subg=""
markg=""
@app.route("/tdisplay", methods = ["POST"])
def tdisplay():
        global semg,subg,markg
        semg=request.form.get("sem")
        subg=request.form.get("sub")
        markg=request.form.get("mark")
        return render_template("tdisplay.html",sem=semg,sub=subg,mark=markg)

@app.route("/teacher1ATT", methods = ["GET","POST"])
def teacher1ATT():
        print("hello")
        global semg,subg,markg
        for i in range(1,10):
            usn1="1BI16CS00"+str(i)
            sub1=subg
            sem1=semg
            mark1=markg
            mark2=request.form.get("1BI16CS00"+str(i))
            param=(usn1,sub1,sem1,mark2)
            #print(param)
            cur.execute("select * from marks where usn=? and subname=?",(usn1,sub1))
            rows=cur.fetchone()
            # print(rows)
            conn.commit()
            if rows == None:
                # print("hii")
                cur.execute("insert into marks (usn,subname,sem,"+mark1+" ) values(?,?,?,?)",param)
                conn.commit()
            else:
                print("hey")
                param1=(mark2,usn1,sub1)
                cur.execute("update marks set "+mark1+"= ? where usn=? and subname=?",param1)
                conn.commit()
        for i in range(10,21):
            usn1="1BI16CS0"+str(i)
            sub1=subg
            sem1=semg
            mark1=markg
            mark2=request.form.get("1BI16CS0"+str(i))
            param=(usn1,sub1,sem1,mark2)
            if rows == None:
                # print("hii")
                cur.execute("insert into marks (usn,subname,sem,"+mark1+" ) values(?,?,?,?)",param)
                conn.commit()
            else:
                # print("hey")
                param1=(mark2,usn1,sub1)
                cur.execute("update marks set "+mark1+"= ? where usn=? and subname=?",param1)
                conn.commit()
        return render_template("teacherATT.html")





if __name__ == '__main__' :
    app.run(debug=True)
