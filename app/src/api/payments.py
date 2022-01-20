from flask import Blueprint, jsonify, abort, request
from ..models import Payment, User, db

bp = Blueprint('payments', __name__, url_prefix='/payments')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    payments = Payment.query.all()  # ORM performs SELECT query
    result = []
    for p in payments:
        result.append(p.serialize())  # build list of Payments as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Payment.query.get_or_404(id)
    return jsonify(p.serialize())


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def payment_update(id: int):
    payment = Payment.query.get(id)
    payment_type = request.json['payment_type']
    card_number = request.json['card_number']

    payment.payment_type = payment_type
    payment.card_number = card_number

    db.session.commit()
    return jsonify(payment.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and payment_type and card_number
    if 'user_id' not in request.json or 'payment_type' not in request.json or 'card_number' not in request.json:
        return abort(400)

    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'])

    # construct Payment
    p = Payment(
        user_id=request.json['user_id'],
        payment_type=request.json['payment_type'],
        card_number=request.json['card_number']
    )

    db.session.add(p)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(p.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Payment.query.get_or_404(id)
    try:
        db.session.delete(p)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
