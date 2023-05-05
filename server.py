import datetime
from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advertisement, User
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from hashlib import md5
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from schema import CreateUser
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)

@app.before_request
def change_session_lifetime():
    flask.session.permanent = True
    flask.session.permanent_session_lifetime = datetime.timedelta(days=3)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


def get_ad(ad_id: int, session: Session):
    ad = session.get(Advertisement, ad_id)
    if ad is None:
        raise HttpError(404, message='Ad not found')
    return ad


class AdView(MethodView):
    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({
                'id': ad_id,
                'title': ad.title,
                'description': ad.description,
                'creation_time': ad.creation_time,
                'author': ad.author})

    # @login_required
    def post(self):
        json_data = request.json
        with Session() as session:
            new_ad = Advertisement(**json_data)
            session.add(new_ad)
            session.commit()
            return jsonify({
                'id': new_ad.id
            })

    # @login_required
    def patch(self, ad_id: int):
        json_data = request.json
        with Session() as session:
            ad = get_ad(ad_id, session)
            for field, value in json_data.items():
                setattr(ad, field, value)
            session.commit()
            return jsonify({
                'id': ad_id,
                'title': ad.title,
                'description': ad.description,
                'creation_time': ad.creation_time,
                'author': ad.author})

    # @login_required
    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({
                'status': 'success'
            })


def validate(json_data: dict, model_class: Type[CreateUser]):
    try:
        model_item = model_class(**json_data)
        return model_item.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors())


def hash_password(password: str):
    password: bytes = password.encode()
    hashed_password = md5(password).hexdigest()
    return hashed_password


@app.route('/signup', methods=['POST'])
def signup():
    json_data = validate(request.json, CreateUser)
    json_data['password_hash'] = hash_password(json_data['password_hash'])

    with Session() as session:
        new_user = User(**json_data)
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            raise HttpError(409, 'User already exist')
        return jsonify({
            'id': new_user.id
        })


@app.route('/login', methods=['POST'])
def login():
    session = flask.session
    json_data = request.json
    json_data['password_hash'] = hash_password(json_data['password_hash'])
    with Session() as sessions:
        user = sessions.query(User).filter(User.username == json_data['username']).first()
        if user and user.password_hash == json_data['password_hash']:
            login_user(user, remember=True)
            if current_user.is_authenticated:
                return jsonify({
                    'login': 'success', 'username': user.username
                })
        raise HttpError(403, 'Wrong login or password')


@app.route("/logout")
@login_required
def logout():
    logout_user()


app.add_url_rule('/ad/<int:ad_id>', view_func=AdView.as_view('ad_existed'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ad/', view_func=AdView.as_view('ad_new'), methods=['POST'])

if __name__ == '__main__':
    app.run()
