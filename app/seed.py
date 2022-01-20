"""
Populate ustartnow database with fake data using the SQLAlchemy ORM.
"""

import random
import string
import hashlib
import secrets
from typing import Counter
from faker import Faker
from ustartnow.src.models import User, Payments, Courses, Sections, Videos, Resources, Quizes, db
from ustartnow.src import create_app

COUNT = 50
#PAYMENT_COUNT = 100
# LIKE_COUNT = 400

# assert LIKE_COUNT <= (USER_COUNT * PAYMENT_COUNT)


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )
    salt = secrets.token_hex(16)
    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def random_payment_type():
    type_list = ["Discover", "AMEX", 'Visa', 'Mastercard', 'Bitcoin']
    return random.choice(type_list)


def random_numbers(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def truncate_tables():
    """Delete all rows from database tables"""
    Quizes.query.delete()
    Resources.query.delete()
    Videos.query.delete()
    Sections.query.delete()
    Courses.query.delete()
    Payments.query.delete()
    User.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    last_user = None  # save last user
    for _ in range(COUNT):
        last_user = User(
            username=fake.unique.first_name().lower() + str(random.randint(1, 150)),
            password=random_passhash(),
            instructor=fake.pybool()
        )
        db.session.add(last_user)

    # insert users
    db.session.commit()

    last_payment = None  # save last payment
    for _ in range(COUNT):
        last_payment = Payments(
            payment_type=random_payment_type(),
            card_number=random_numbers(),
            user_id=random.randint(last_user.id - COUNT + 1, last_user.id)
        )
        db.session.add(last_payment)

    # insert payments
    db.session.commit()

    last_course = None  # save last course
    for _ in range(COUNT):
        last_course = Courses(
            certification=fake.sentence(),
            course_topic=fake.sentence(),
            user_id=random.randint(last_user.id - COUNT + 1, last_user.id)
        )
        db.session.add(last_course)

    # insert courses
    db.session.commit()

    last_section = None  # save last section
    for _ in range(COUNT):
        last_section = Sections(
            title=fake.sentence(),
            duration_length=random_numbers(),
            course_id=random.randint(
                last_course.id - COUNT + 1, last_course.id)
        )
        db.session.add(last_section)

    # insert sections
    db.session.commit()

    last_resource = None  # save last resource
    for _ in range(COUNT):
        last_resource = Resources(
            url_link=fake.sentence(),
            document=fake.sentence(),
            section_id=random.randint(
                last_section.id - COUNT + 1, last_section.id)
        )
        db.session.add(last_resource)

    # insert resources
    db.session.commit()

    last_quiz = None  # save last quiz
    for _ in range(COUNT):
        last_quiz = Quizes(
            question=fake.sentence(),
            answer=fake.sentence(),
            score=random_numbers(),
            section_id=random.randint(
                last_section.id - COUNT + 1, last_section.id)
        )
        db.session.add(last_quiz)

    # insert quizes
    db.session.commit()


# run script
main()
