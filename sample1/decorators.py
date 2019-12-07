from functools import wraps

from flask_restplus import abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from sample1.database import MYSQL as db
from sample1.database.permission.permission import Permission
from sample1.exceptions import NoPermissionException


def permission_required(section, level):
    def real_decorator(function):
        @wraps(function)
        @jwt_required
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity is not None:
                idx = identity[0]['idx']
                permission_admin = Permission.query\
                                             .filter(Permission.user_idx ==
                                                     idx)\
                                             .filter(Permission.section ==
                                                     'admin')\
                                             .first()
                permission = Permission.query\
                                       .filter(Permission.user_idx == idx)\
                                       .filter(Permission.section == section)\
                                       .first()
                if permission_admin is None:
                    if permission is None or permission.level < level:
                        raise NoPermissionException()
            else:
                raise NoPermissionException()
            return function(*args, **kwargs)
        return wrapper
    return real_decorator


def teacher_only():
    def real_decorator(function):
        @wraps(function)
        @jwt_required
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity is not None:
                if identity[0]['user_type'] != 'T':
                    raise NoPermissionException()
            else:
                raise NoPermissionException()
            return function(*args, **kwargs)
        return wrapper
    return real_decorator
