from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from faceanalysis.models.database_manager import get_database_manager
from faceanalysis.models.models import User
from faceanalysis.settings import TOKEN_SECRET_KEY
from faceanalysis.settings import TOKEN_EXPIRATION

auth = HTTPBasicAuth()


login_required = auth.login_required


class DuplicateUser(Exception):
    pass


def generate_auth_token(user, expiration=TOKEN_EXPIRATION):
    serializer = Serializer(TOKEN_SECRET_KEY, expires_in=expiration)
    return serializer.dumps({'id': user.id})


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if user:
        g.user = user
        return True

    db = get_database_manager()
    session = db.get_session()
    user = session.query(User)\
        .filter(User.username == username_or_token)\
        .first()

    if not user or not user.verify_password(password):
        session.close()
        return False

    g.user = user
    session.close()
    return True


def register_user(username, password):
    db = get_database_manager()
    session = db.get_session()
    user = session.query(User) \
        .filter(User.username == username) \
        .first()

    if user is not None:
        session.close()
        raise DuplicateUser()

    user = User(username=username)
    user.hash_password(password)
    session = db.get_session()
    session.add(user)
    db.safe_commit(session)
    return username
