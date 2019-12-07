from sample1.database import MYSQL as db

from datetime import datetime

from sqlalchemy import exc


class sample1Comment(db.Model):
    __tablename__ = 'sample1_comment'

    idx = db.Column(db.Integer(), primary_key=True,
                    nullable=False, autoincrement=True)

    post_idx = db.Column(db.Integer(),
                         db.ForeignKey('sample1_posts.idx'), nullable=False)
    post = db.relationship('sample1Posts', back_populates='comments')

    target_type = db.Column(db.Enum('post', 'comment'), nullable=False)
    target_idx = db.Column(db.Integer(), nullable=False)

    status = db.Column(db.Enum('normal', 'edited', 'censored'))

    writer_idx = db.Column(db.Integer(),
                           db.ForeignKey('user.idx'), nullable=False)
    writer = db.relationship('User', back_populates='sample1_comment_writer')

    wrote_date = db.Column(db.DateTime, nullable=False)

    content = db.Column(db.Text(), nullable=False)

    has_a_reply = db.Column(db.Integer, default=0)

    reply_check = db.Column(db.Boolean, default=True)


def add_sample1_comment(data, writer_idx):

    db.session.add(sample1Comment(
        post_idx=data['post_idx'],
        target_type=data['target_type'],
        target_idx=data['target_idx'],
        status="normal",
        writer_idx=writer_idx,
        wrote_date=datetime.today(),
        content=data['content']
    ))

    db.session.commit()


def get_all_sample1_comments_by_post_idx(post_idx):
    return sample1Comment.query.filter_by(post_idx=post_idx).all()


def get_all_unchecked_comments_by_user_idx(user_idx):
    return sample1Comment.query.filter_by(
        writer_idx=user_idx, reply_chek=False).all()


def update_sample1_comment_by_idx(comment_idx, content, user_idx):
    comment_query = sample1Comment.query.filter_by(idx=comment_idx)
    if comment_query.first() is None:
        return 404

    if comment_query.first().writer_idx != user_idx:
        return 403

    comment_query.update({
        'status': "edited",
        'wrote_date': datetime.today(),
        'content': content
    })
    db.session.commit()


def delete_sample1_comment_by_idx(comment_idx, user_idx):
    comment = sample1Comment.query.filter_by(idx=comment_idx).first()
    if comment is None:
        return 404

    if comment.writer_idx != user_idx:
        return 403

    try:
        db.session.delete(comment)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return 409

    return 200
