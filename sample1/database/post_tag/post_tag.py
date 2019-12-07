from sample1.database import MYSQL as db

from datetime import datetime


class sample1PostTags(db.Model):
    __tablename__ = 'sample1_post_tags'

    idx = db.Column(db.Integer(), primary_key=True,
                    nullable=False, autoincrement=True)

    post_idx = db.Column(db.Integer(),
                         db.ForeignKey('sample1_posts.idx'), nullable=False)
    post = db.relationship('sample1Posts', back_populates='post_tags')

    tag_idx = db.Column(db.Integer(),
                        db.ForeignKey('sample1_tags.idx'), nullable=False)
    tag = db.relationship('sample1Tags', back_populates='post_tag')

    tag_option = db.Column(db.Enum('must', 'or', 'not'))


def add_sample1_post_tag(post_idx, tag_idx, tag_option):

    db.session.add(sample1PostTags(
        post_idx=post_idx,
        tag_idx=tag_idx,
        tag_option=tag_option
    ))

    db.session.commit()


def get_all_sample1_post_tag_by_post_idx(post_idx):
    return sample1PostTags.query.filter_by(post_idx=post_idx).all()


def delete_sample1_post_tag_by_post_tag_idx(post_idx, tag_idx):
    tag = sample1PostTags.query.filter_by(user_idx=post_idx, idx=tag_idx).first()
    if tag is None:
        return 404
    db.session.delete(tag)
    db.session.commit()
