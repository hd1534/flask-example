from sample1.database import MYSQL as db
import datetime
import enum


class User(db.Model):
    __tablename__ = 'user'

    idx = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.String(50))
    email = db.Column(db.String(50))
    user_type = db.Column(db.Enum('T', 'D', 'S', 'P', 'O'))
    gender = db.Column(db.Enum('M', 'F', ''))
    student = db.relationship("Student", uselist=False, back_populates="user")

    sample1_posts_writer = db.relationship('sample1Posts', back_populates='writer')
    sample1_user_tags = db.relationship('sample1UserTags', back_populates='user')
    sample1_comment_writer = db.relationship(
        'sample1Comment', back_populates='writer')
    sample1_tags_owner = db.relationship('sample1Tags', back_populates='owner')


def get_user(user_idx):
    return User.query.filter_by(idx=user_idx).first()


def get_all_user_by_name(user_name):
    return User.query.filter_by(name=user_name).all()


def add_all_user(users_data):
    for user_data in users_data:
        user = User.query.filter_by(idx=user_data['id']).first()
        if user is None:
            db.session.add(User(idx=user_data['id'],
                                name=user_data['name'],
                                id=user_data['username'],
                                email=user_data['email'],
                                user_type=user_data['user_type'],
                                gender=user_data['gender']))
        else:
            user.name = user_data['name']
            user.id = user_data['username']
            user.email = user_data['email']
            user.user_type = user_data['user_type']
            user.gender = user_data['gender']
        db.session.commit()
