from sample1.resource import api
from sample1.exceptions import (
    NoPermissionException,
    NoUserInfoException
)


@api.errorhandler(NoPermissionException)
def permission_handler(error):
    return {'message': 'no permission'}, 403


@api.errorhandler(NoUserInfoException)
def user_info_handler(error):
    return {'message': 'no user info'}, 403


@api.errorhandler
def default_error_handler(error):
    return {'message': str(error)}, getattr(error, 'code', 500)
