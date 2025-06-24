from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    if request.is_json:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        if request.is_json:
            return jsonify({"msg": "Email already exists"}), 409
        else:
            return "Email already exists", 409

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    if request.is_json:
        return jsonify({"msg": "User created successfully"}), 201
    else:
        return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    
    if request.is_json:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        if request.is_json:
            return jsonify({"msg": "Invalid credentials"}), 401
        else:
            return "Invalid credentials", 401

    access_token = create_access_token(identity={"email": user.email})

    if request.is_json:
        return jsonify(access_token=access_token), 200
    else:
        
        return f"Welcome, {user.email}!"
