from flask_app import app
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from flask_bycrpt import Bycrpt

bycrpt = Bycrpt(app)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", user=User.find_by_id(data))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    user = User.find_by_email(request.form)

    if user:
        if not bycrpt.check_password_hash(user.password, request.form["password"]):
            flash("Email/Password combination is incorrect", "login")
            return redirect("/")
        session["user_id"] = user.id
        return redirect("/dashboard")

    flash("Email is not found", "login")
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bycrpt.generate_password_hash(request.form["password"])
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")