from sample1.database import MYSQL as db

from datetime import datetime
from ..permission.permission import get_permission

from sqlalchemy import exc, or_


class sample1Tags(db.Model):
    __tablename__ = 'sample1_tags'

    idx = db.Column(db.Integer(), primary_key=True,
                    nullable=False, autoincrement=True)

    name = db.Column(db.String(20), nullable=False)

    owner_idx = db.Column(db.Integer(),
                          db.ForeignKey('user.idx'), nullable=False)
    owner = db.relationship('User', back_populates='sample1_tags_owner')

    created_date = db.Column(db.DateTime, nullable=False)

    description = db.Column(db.Text(), nullable=False)

    # private 은 검색은 되고 해당 태그에 권한을 가진사람의 초대로만.
    # request 는 검색이 되어 지원할 수 있고 이를 해당 태그에 권한을 가진사람이 허락 or 불허
    # free_for_all 은 검색이 되며, 그냥 바로 가입 가능
    join_option = db.Column(
        db.Enum('private', 'request', 'free_for_all'))

    post_tag = db.relationship('sample1PostTags', back_populates='tag')
    user_tag = db.relationship('sample1UserTags', back_populates='tag')


def add_sample1_tag(tag_data, user_idx):
    db.session.add(sample1Tags(
        owner_idx=user_idx,
        name=tag_data['name'],
        created_date=datetime.today(),
        description=tag_data['description'],
        join_option=tag_data['join_option']
    ))
    db.session.commit()


def get_sample1_tag_by_idx(tag_idx):
    tag = sample1Tags.query.filter_by(idx=tag_idx).first()
    if tag is None:
        return 404
    return tag


def get_all_sample1_tags():
    return sample1Tags.query.all()


def search_tags_by_description(word):
    return sample1Tags.query.\
        filter(or_(sample1Tags.description.like('%'+word+'%'),
                   sample1Tags.name.like('%'+word+'%'))).all()


def delete_tags_by_idx(tag_idx, user_idx):
    tag = sample1Tags.query.filter_by(idx=tag_idx).first()
    if tag is None:
        return 404
    if tag.owner_idx != user_idx:
        if get_permission(user_idx, 'admin') is None:
            if get_permission(user_idx, 'sample1') is None:
                return 403

    try:
        db.session.delete(tag)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return 409

    return 200


'''
def delete_sample1_tags(user_idx, tag_idx):
    tag = get_sample1_tag_by_idx(tag_idx)
    if tag is None:
        return 404
    if user_idx != admin:
        if user_idx != tag.owner_idx:
            return 409
    db.session.delete(tag)
    db.session.commit()
'''
