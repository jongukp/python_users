from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from user_model import User, db


def init_app(app):
    @app.route('/')
    def home():
        return ("Welcome to the User Management Application. "
                "Navigate to /users to manage users.")

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data or not all(key in data for key in
                               ('username', 'first_name', 'last_name',
                                'email')):
            return jsonify({'message': 'Missing data'}), 400
        try:
            new_user = User(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            db.session.add(new_user)
            db.session.commit()
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'message': 'Username already exists'}), 400
        return jsonify({'message': 'New user created', 'user': data}), 201

    @app.route('/users/<username>', methods=['GET'])
    def get_user(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        sort_by = request.args.get('sort_by', 'username')
        if sort_by not in ['username', 'first_name', 'last_name', 'email']:
            return jsonify({'message': 'Invalid sort_by parameter'}), 400
        users = User.query.order_by(sort_by).all()
        user_list = [
            {'username': user.username,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'email': user.email} for user in users
        ]
        return jsonify({'users': user_list}), 200

    @app.route('/users/<username>', methods=['PUT'])
    def update_user(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Missing data'}), 400
        try:
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']
            db.session.commit()
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
        return jsonify({'message': 'User updated', 'user': username}), 200
