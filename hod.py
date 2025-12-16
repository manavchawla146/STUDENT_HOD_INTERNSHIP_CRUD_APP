# hod.py
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, jsonify
from models import db, Student, Message

hod_bp = Blueprint("hod", __name__)

def hod_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'HOD':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@hod_bp.route("/hod", methods=["GET", "POST"])
@hod_required
def dashboard():
    if request.method == "POST":
        message_content = request.form.get("message")
        if message_content and message_content.strip():
            # Create new message
            new_message = Message(content=message_content)
            db.session.add(new_message)
            
            # Reset all students' notification status
            Student.query.update({Student.notification_seen: False})
            db.session.commit()
            
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True})
            return redirect("/hod")

    students = Student.query.all()
    return render_template("hod_dashboard.html", students=students)