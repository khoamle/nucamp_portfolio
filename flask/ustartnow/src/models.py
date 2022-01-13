import datetime
from typing import Text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Reference:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.Boolean, nullable=True)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_type = db.Column(db.Text, nullable=False)
    date_purchase = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    card_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, payment_type: Text, card_number: int, user_id: int):
        self.payment_type = payment_type
        self.card_number = card_number
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'payment_type': self.payment_type,
            'card_number': self.card_number,
            'date_purchase': self.date_purchase.isoformat(),
            'user_id': self.user_id
        }


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    certification = db.Column(db.Text, nullable=True)
    date_created = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    course_topic = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    duration_length = db.Column(db.Integer, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        'courses.id'), nullable=False)


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    binary_data = db.Column(db.Text, nullable=False)
    video_title = db.Column(db.Text, nullable=False)
    duration_length = db.Column(db.Integer, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'sections.id'), nullable=False)


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url_link = db.Column(db.Text, nullable=True)
    document = db.Column(db.Text, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'sections.id'), nullable=False)


class Quiz(db.Model):
    __tablename__ = 'quizes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    score = db.Column(db.Text, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'sections.id'), nullable=False)
