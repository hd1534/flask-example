from sample1.database import MYSQL as db


class Permission(db.Model):
    __tablename__ = 'permission'

    idx = db.Column(db.Integer,
                    primary_key=True,
                    nullable=False,
                    autoincrement=True)
    user_idx = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)


def get_permission(user_idx, section):
    return Permission.query\
                     .filter_by(user_idx=user_idx, section=section)\
                     .first()


def get_all_permission(user_idx):
    return Permission.query\
                     .filter_by(user_idx=user_idx)\
                     .all()


def add_permission(permission_data):

    db.session.add(Permission(user_idx=permission_data['user_idx'],
                              section=permission_data['section'],
                              level=permission_data['level']))
    db.session.commit()
