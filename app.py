from flask import Flask
from models import db, User
from auth import auth_bp
from student import student_bp
from hod import hod_bp

app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(hod_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role="HOD").first():
            db.session.add(User(
                email="hod@ksu.com",
                password="hod123",
                role="HOD"
            ))
            db.session.commit()

    app.run(debug=True)

