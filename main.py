from flask import Flask, render_template, request, redirect
import requests
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from datetime import date, datetime
app=Flask(__name__)

END_POINT="https://api.openweathermap.org/data/2.5/weather"

API_KEY="6ab73d57dd3ea5445996fd55de54ad44"
data={
}


@app.route("/t",methods=["GET","POST"])
def start():
    city_name = "banha"
    if request.method=="POST":
        print("i am in post mode ")
        city_name=request.form.get("city_name")
        print(city_name)
    params = {

        'appid': API_KEY,  
        'q': city_name,  # You can also use 'q' parameter for city name
        "units": "metric"
    }

    response=requests.get(END_POINT,params)
    temp=response.json()
    temp=temp["main"]["temp"]
    print(temp)



    return render_template("index.html",t=int(temp))

@app.route("/")
def s():
    return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():

      if request.method=="POST":
        n=request.form.get("name")
        p=request.form.get("password")
        ph=request.form.get("phone")

        new_user=User(
            phone=ph,password=p,name=n


        )
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")
      return render_template("register.html")


@app.route("/check",methods=["GET","POST"])
def check():
    global variable
    if request.method=="POST":
        user_name=request.form.get("user_name_for_pass")
        print(user_name)
        if user_name in data:
           return redirect("/forget")
        else:
           return redirect("/register")
    return render_template("check.html")

@app.route("/forget",methods=["GET","POST"])
def forget():
    if request.method=="POST":
        print(data)
        new_pass=request.form.get("new_pass")
        user_name=request.form.get("user_name")
        data[user_name]=new_pass
        print(data)
        return redirect("/login")



    return render_template("forget.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        #print(data)
        #print(password)
        if user_name in data and data[user_name]==password:
            return redirect("/t")
        elif user_name in data and data[user_name]!=password:
            return redirect("/check")
        else:
           return redirect("/register")


    return render_template("login.html")


if __name__ =="__main__":
    app.run(debug=True)
