from sample1.database import MYSQL as db

from datetime import datetime


class sample1UserTags(db.Model):
    __tablename__ = 'sample1_user_tags'

    idx = db.Column(db.Integer(), primary_key=True,
                    nullable=False, autoincrement=True)

    user_idx = db.Column(db.Integer(),
                         db.ForeignKey('user.idx'), nullable=False)
    user = db.relationship('User', back_populates='sample1_user_tags')

    tag_idx = db.Column(db.Integer(),
                        db.ForeignKey('sample1_tags.idx'), nullable=False)
    tag = db.relationship('sample1Tags', back_populates='user_tag')

    # 자신의 권한
    admin = db.Column(db.Boolean(), nullable=False)
    modification_allowed = db.Column(db.Boolean(), nullable=False)  # 태그 내용수정
    invitation_allowed = db.Column(db.Boolean(), nullable=False)  # 태그 초대
    post_allowed = db.Column(db.Boolean(), nullable=False)  # 포스트에 사용 가능
    acceptance_allowed = db.Column(db.Boolean(), nullable=False)  # 태그 신청자 승인가능

    # forced 는 관리자가 집어 넣은거, waiting 은 태그를 사용자가 채택하기 전
    # accept 는 받은거를 사용자가 허용한거, refuse는 사용자가 불허한거, chosen 은 사용자가 직접 선택한거
    # request는 사용자가 신청한거, accepted 는 관리자가 허락한거, refused 는 관리자가 거절한거
    status = db.Column(
        db.Enum("forced", "waiting", "accept", "refuse",
                "request", "accepted", "refused", "chosen"))


def add_sample1_user_tag_invitation(data):

    user_tag = sample1UserTags.query.filter_by(
        tag_idx=data['tag_idx'], user_idx=data['user_idx'])
    if user_tag.first() is not None:
        if data['status'] == 'forced':
            user_tag.update({'status': 'forced'})
        else:
            return 409
    else:
        db.session.add(sample1UserTags(
            user_idx=data['user_idx'],
            tag_idx=data['tag_idx'],
            status=data['status'],
            modification_allowed=data['modification_allowed'],
            invitation_allowed=data['invitation_allowed'],
            post_allowed=data['post_allowed'],
            acceptance_allowed=data['acceptance_allowed']
        ))
    db.session.commit()
    return 200


def add_sample1_user_tag_request(data, user_idx):

    user_tag = sample1UserTags.query.filter_by(
        tag_idx=data['tag_idx'], user_idx=user_idx)
    if user_tag.first() is not None:
        if data['status'] == 'forced':
            user_tag.update({'status': 'forced'})
        else:
            return 409
    else:
        db.session.add(sample1UserTags(
            user_idx=user_idx,
            tag_idx=data['tag_idx'],
            status=data['status'],
            modification_allowed=data['modification_allowed'],
            invitation_allowed=data['invitation_allowed'],
            post_allowed=data['post_allowed'],
            acceptance_allowed=data['acceptance_allowed']
        ))
    db.session.commit()
    return 200


def get_all_sample1_user_tags_by_user_idx(user_idx):
    return sample1UserTags.query.filter_by(user_idx=user_idx)\
        .filter(or_(sample1UserTags.status == 'forced',
                    sample1UserTags.status == 'accept',
                    sample1UserTags.status == 'accepted',
                    sample1UserTags.status == 'chosen')).all()


def get_all_sample1_user_tags_invitations_by_user_idx(user_idx):
    return sample1UserTags.query.filter_by(user_idx=user_idx)\
            .filter(or_(sample1UserTags.status == 'refuse',
                        sample1UserTags.status == 'waiting')).all()


def get_all_sample1_user_tags_requests_by_user_idx(user_idx):
    return sample1UserTags.query.filter_by(user_idx=user_idx)\
            .filter(or_(sample1UserTags.status == 'refused',
                        sample1UserTags.status == 'request')).all()


def get_sample1_user_tag_by_user_tag_idx(user_idx, tag_idx):
    return sample1UserTags.query\
        .filter_by(user_idx=user_idx, tag_idx=tag_idx).first()


def delete_sample1_user_tag_by_user_tag_idx(user_idx, tag_idx):
    tag = sample1UserTags.query.filter_by(user_idx=user_idx, idx=tag_idx).first()
    if tag is None:
        return 404
    db.session.delete(tag)
    db.session.commit()
