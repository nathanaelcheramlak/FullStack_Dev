from flask import request, jsonify
from config import db, app
from models import storage

from models.user import User
from models.transaction import Transaction

@app.route('/api/v1/users', methods=['GET'])
def users():
    all_users = storage.all('User')
    users = []

    for user in all_users.values():
        users.append(user.to_dict())
    
    return jsonify(users)

@app.route('/api/v1/users/<user_id>', methods=['GET', 'PATCH'])
def get_user(user_id):
    if request.method == 'GET':
        user = storage.get('User', user_id)
        if not user:
            return jsonify({"error":"User not found"}), 404
        return jsonify(user.to_dict()), 200
    
    elif request.method == 'PATCH': # Update User
        data = request.get_json()

        balance = data.get('balance')

        if not balance:
            return jsonify({"error":"Missing balance"}), 400
        
        user = storage.get('User', user_id)
        if not user:
            return jsonify({"error":"User not found"}), 404
        
        user.balance = balance

        try:
            user.save_to_db()
        except:
            return jsonify({"error":"Could not update user"}), 400
        
        return jsonify({"message": "Updated Successfully"}), 200

@app.route('/api/v1/users/sign_up', methods=['POST'])
def create_user():
    data = request.get_json()

    email = data.get('email')
    full_name = data.get('fullName')
    password = data.get('password')
    dob = data.get('DOB')

    if not email or not full_name or not password or not dob:
        return jsonify({"error": "Missing data"}), 400
    
    new_user = User(email=email, full_name=full_name, password=password, dob=dob)

    try:
        new_user.save_to_db()
    except:
        return jsonify({"error":"Could not create user"}), 400
    
    return jsonify(new_user.to_dict()), 201

@app.route('/api/v1/users/delete_user/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error":"Missing data"}), 400
    
    user = storage.get('User', user_id)

    try:
        user.delete()
    except:
        return jsonify({"error":"Could not delete user"}), 400
    
    return jsonify({"message": "User Deleted"}), 200

@app.route('/api/v1/users/<user_id>/transaction', methods=["GET"])
def get_user_transactions(user_id):
    user = storage.get('User', user_id)

    if not user:
        return jsonify({"error":"User not found"}), 404
    
    transactions = user.transactions
    user_transactions = []

    for transaction in transactions:
        user_transactions.append(transaction.to_dict())
    
    return jsonify(user_transactions), 200

@app.route('/api/v1/users/<user_id>/transaction/add_transaction', methods=["POST"])
def add_transaction(user_id):
    data = request.get_json()

    user = storage.get('User', user_id)

    if not user:
        return jsonify({"error":"User not found"}), 404
    
    name = data.get('name')
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date')

    if not name or not amount or not description:
        return jsonify({"error":"Missing data"}), 400
    
    new_transaction = Transaction(user_id=user_id, name=name, amount=amount, description=description, date=date)

    try:
        new_transaction.save_to_db()
    except:
        return jsonify({"error":"Could not create transaction"}), 400
    
    return jsonify(new_transaction.to_dict()), 201

@app.route('/api/v1/users/<user_id>/transaction/<transaction_id>/delete_transaction', methods=["POST"])
def delete_transaction(user_id, transaction_id):
    
    user = storage.get('User', user_id)
    if not user: 
        return jsonify({"error":"User not found"}), 404

    transaction = storage.get('Transaction', transaction_id)
    if not transaction:
        return jsonify({"error":"Transaction not found"}), 404
    
    

    try:
        user.transactions.remove(transaction)
        transaction.delete()
    except:
        return jsonify({"error":"Could not delete transaction"}), 400
    
    return jsonify({"message":"Transaction Deleted"}), 200

# Update Transaction
@app.route('/api/v1/users/<user_id>/transactions/<transaction_id>', methods=["PATCH"])
def update_transaction(user_id, transaction_id):
    data = request.get_json()

    user = storage.get('User', user_id)
    if not user:
        return jsonify({"error":"User not found"}), 404

    transaction = storage.get('Transaction', transaction_id)
    if not transaction:
        return jsonify({"error":"Transaction not found"}), 404
    
    name = data.get('name')
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date')

    if not name or not amount or not description:
        return jsonify({"error":"Missing data"}), 400
    
    transaction.name = name
    transaction.amount = amount
    transaction.description = description
    transaction.date = date
    
    try:
        transaction.save_to_db()
    except:
        return jsonify({"error":"Could not update transaction"}), 400
    
    return jsonify(transaction.to_dict()), 200

@app.teardown_appcontext
def close_db(error):
    storage.close()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)