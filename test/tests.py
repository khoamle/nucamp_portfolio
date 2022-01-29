from app.src.models import Payment
from app.src import create_app
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def create_new_payment(db):
    payment = Payment('visa',123655, 10)
    db.session.add(payment)
    db.session.commit()
    return payment

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def db(app):
    db = SQLAlchemy(app)
    return db

def test_search_payments():
    assert Payment.query.filter(Payment.payment_type=='Visa')