from flask import Blueprint, render_template, request, redirect, session
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect("/hod" if user.role == "HOD" else "/student")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", 
                                error="Email already registered. Please use a different email or login.")
        
        # If email doesn't exist, create new user
        new_user = User(
            email=email,
            password=password,
            role="STUDENT"  # Default role for new registrations
        )
        
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            return render_template("register.html", 
                                error="An error occurred. Please try again.")
    
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
