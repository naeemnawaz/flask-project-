from flask import Flask , render_template
app = Flask(__name__)
from sqlalchemy.orm import defer
from sqlalchemy.orm import undefer

#!/usr/bin/python3
import os
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect, url_for,session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
##postgress
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:naeemA123$@localhost:3306/project"
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    session = db.Column(db.String(100),nullable=False)
    program = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)




class performance(db.Model):
    __tablename__ = "perform"
    id = db.Column(db.Integer,primary_key=True)
    perform = db.Column(db.String(50),primary_key=True)
    cooperate = db.Column(db.String(50),nullable=False)
    behvior = db.Column(db.String(50),nullable=False)
    practical = db.Column(db.String(50),nullable=False)

class performp:
    perform = 0
    cooperate = 0
    behvior = 0 
    practical = 0

@app.route('/',methods=['GET'])

def home():
    return render_template("home.html")

@app.route("/login", methods=['POST','GET'])
def login():
    msg = "Login first"
    if request.method=="POST":
        name = request.form.get("username")
        password = request.form.get("password")
        data = Students.query.filter_by(name=name, password=password).first()
        if not data:
            msg = "Incorrect name or password"
            return render_template("login.html",msg=msg)
        else:
            session["username"] = name
            return render_template("home.html")
    else:
        return render_template("login.html", msg=msg)
#if "username" in session:
#           return redirect(url_for("department"))
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route("/record/feedback/<stud_id>", methods=['GET', 'POST'])
def feedback(stud_id):
    if request.method == "POST":
        print('post is working')        
        perform = request.form.get("perform")
        cooperate = request.form.get("cooperate")
        behvior = request.form.get("behvior")
        practical = request.form.get("practical")
        stud_exp = performance(id=stud_id,perform=perform,cooperate=cooperate,behvior=behvior,
            practical=practical)
        db.session.add(stud_exp)
        db.session.commit()
        redirect("record")
    msg = 'there record sumittied'
    stud =Students.query.filter(Students.id == stud_id).first()
    return render_template('feedback.html',stud=stud,msg=msg)
 
@app.route("/record/perform/<stud_id>", methods=['GET', 'POST'])
def perform(stud_id):
    stud = Students.query.filter(Students.id == stud_id).first()
    exp = performance.query.filter(performance.id == stud_id).first()
    # this is jinja2 program
    #performance.query.filter(performance.id == stud_id).first()
    #render_template('home.html',val=val)
    total = 0
    lst = []
    new = Students.query.filter(Students.id == stud_id).first()
    print('this is new record of python',new.name)
    # new = performance.query.all()
    #for row in new:
    #    print('this the value of stud_id',stud_id)
    #    if stud_id==row.id and row.perform == 'good':
    #        print(stud_id,'this is how much good')

        #print("Id = ", row["id"])
        #print(row.perform)
#        print('this value of id',row.practical)
        #print("cooperate  = ", row["cooperate"])
        #print("cooperate  = ", row["behvior"])
        #print(" behvior = ", row["practical"], "\n")
    """
    n = 3
    while True:
        n = n -1 
        if n == 0:
            break
        lst = []
        for i in new:

            print('this value of perform',i.perform)
            if i.id == 66 and i.perform == 'good':
                print('there are some stuff same',i.id)
                lst = lst.append(i.id)
                total = total + 1
    print('the behvior is ',total)
    print('the value of lisat',lst)
    """
    n = 4
    m = 5
    p = 10
    j = 17
    obj = [n,m,p,j]
    return render_template('perform.html',stud=stud,exp=exp,obj=obj,new=new)

@app.route('/signup',methods=['GET' ,'POST'])
def signup():
    if request.method == "POST":

        id = request.form.get('roll')
        name = request.form.get('name')
        session = request.form.get('session')
        program = request.form.get('program')
        password = request.form.get('password')


        #create new reocrd into databsae
        stud = Students(id =id ,name = name ,session=session,program=program,password=password)
        db.session.add(stud)
        db.session.commit()

        stud = Students.query.all()
        return render_template('record.html',stud=stud )

    return render_template('signup.html')

@app.route('/record',methods=['GET'])
def record():
        if "username" in session:
            stud = Students.query.all()
            return render_template('record.html',stud=stud)
        else:
            m = "first login"
            return render_template("login.html",m=m)

    
@app.route('/team',methods=['GET'])
def team():
    return render_template("team.html")

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=="POST":
        roll = request.form.get("roll")
        name = request.form.get("name")
        session = request.form.get("session")
        program = request.form.get("program")


        stud = Students.query.filter_by(id = id).first()
        stud.id = roll
        stud.name = name
        stud.session = session
        stud.program = program

        db.session.commit()
        return redirect(url_for('record'))
    else:
        stud = Students.query.filter(Students.id == id).first()
        return render_template("update.html", stud=stud, id=id)

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    entry = Students.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    #flash("Department Deleted Successfully")

    return redirect(url_for('record'))


if __name__=="__main__":
    app.run(debug=True)