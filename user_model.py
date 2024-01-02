from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from email_validator import validate_email, EmailNotValidError

db = SQLAlchemy()


class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, unique=True,
                         nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(254))

    @validates('username')
    def validate_username(self, key, username):
        if not username.isalnum():
            raise ValueError("Username must be alphanumeric")
        return username

    @validates('email')
    def validate_user_email(self, key, email):
        try:
            validate_email(
                email,
                check_deliverability=False
            )
            return email
        except EmailNotValidError as e:
            raise ValueError("Invalid email address")
