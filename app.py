from email import message
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash,check_password_hash

from mybot import Pinsta,S_Pinsta
from helpers import login_required,apology

#Definning the SQL databasecd
db = SQL("sqlite:///logins.db")

#Configuring the application
app = Flask(__name__)

#ensure the auto-roleoad
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Defining routes
#index route
@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    return render_template("index.html")
    
    
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        #checking errors
        if not request.form.get("login") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("invalid username")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords dont match :)")
        if db.execute("SELECT id FROM logins WHERE logins.username like ?;",request.form.get("login")):
            return apology("invalid username")
        # registering the user
        username = request.form.get("login")
        password = generate_password_hash(request.form.get("password"))
        try:
            db.execute("INSERT INTO logins (username,password) VALUES (?,?);",username,password)
        except:
            return apology("invalid username")
        session["user_id"]= db.execute("SELECT id FROM logins WHERE logins.username = ?;",username)[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


#Log in route
@app.route("/login",methods = ["GET","POST"])
def login():
    #forgetting previous user
    session.clear()
    if request.method == "POST":
        #Error checking
        login = request.form.get("username")
        get_password = request.form.get("password")
        if not login or not get_password:
            return apology("Invalid username /or password")
        # Query database for username
        rows = db.execute("SELECT * FROM logins WHERE username = ?", login)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], get_password):
            return apology("invalid username and/or password", 403) 
        session["user_id"] = db.execute("SELECT id FROM logins WHERE username = ?",login)[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
    


#sending a message    
@app.route("/send",methods = ["GET","POST"])
@login_required
def send():
    if request.method == "POST":
        user_id = session["user_id"]
        test = request.form.get("name")
        message = request.form.get("message")
        username = db.execute("SELECT username FROM logins WHERE id = ?",user_id)[0]["username"]
        password = request.form.get("password")
        day = request.form.get("day")
        hour = request.form.get("hour")
        minutes = request.form.get("minutes")
        if not test or not message or not password:
            return apology("Please fill all the boxes")
        
        code = S_Pinsta(day,hour,minutes,username, password, test, message)
        if code == 401: return apology("username used or password doesnt match instagram authentication") 
        elif code == 402: return apology("could not find name of the user check it in your inta messenger")
        elif code == 202 :return redirect("/send")
    else:
        return render_template("send.html")