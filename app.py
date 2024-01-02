from flask import Flask
from user_model import db
from controllers import init_app


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    init_app(app)

    return app


if __name__ == '__main__':  # pragma: no cover
    app = create_app()
    app.run(host='localhost', debug=True)
