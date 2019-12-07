from flask_jwt_extended import JWTManager
from flask_restplus import abort
from sample1 import app
from .resource import api
import sample1.database.revoked_token
from flask_cors import CORS
import os
import datetime

from sample1.exceptions import NoJwtKeyException


if os.environ['USE_RS256'] == 'True':
    try:
        app.config['JWT_ALGORITHM'] = 'RS256'
        app.config['JWT_PRIVATE_KEY'] = open('sample1/rs256.pem').read()
        app.config['JWT_PUBLIC_KEY'] = open('sample1/rs256.pub').read()
    except FileNotFoundError:
        raise NoJwtKeyException
else:
    # default is HS256
    app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

CORS(app)

jwt = JWTManager(app)

jwt.invalid_token_loader(lambda err: abort(422, err))
jwt.expired_token_loader(lambda: abort(401, 'Token has expired'))
jwt.unauthorized_loader(lambda err: abort(401, err))
jwt.needs_fresh_token_loader(lambda: abort(401, "Fresh token required"))
jwt.revoked_token_loader(lambda: abort(401, "Token has been revoked"))

jwt._set_error_handler_callbacks(api)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return sample1.database.revoked_token.RevokedToken\
        .is_jti_blacklisted(jti)
