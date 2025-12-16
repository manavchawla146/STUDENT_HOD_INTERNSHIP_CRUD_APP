from flask import Blueprint, render_template, request, session, redirect
from models import db, Student, Message

student_bp = Blueprint("student", __name__)

@student_bp.route("/student", methods=["GET", "POST"])
def dashboard():
    if session.get("role") != "STUDENT":
        return redirect("/login")

    student = Student.query.filter_by(user_id=session["user_id"]).first()
    message = Message.query.first()
    
    # Check if there's a message to show
    show_message = False
    if message and not session.get('message_dismissed'):
        show_message = True

    if request.method == "POST":
        # Handle form submission
        if not student:
            student = Student(user_id=session["user_id"])

        for field in request.form:
            setattr(student, field, request.form[field])

        db.session.add(student)
        db.session.commit()
        
        # If this was a message dismissal
        if 'dismiss_message' in request.form:
            session['message_dismissed'] = True
            return jsonify({"success": True})

    return render_template(
        "student_dashboard.html",
        student=student,
        show_message=show_message,
        message=message.content if message and show_message else None
    )