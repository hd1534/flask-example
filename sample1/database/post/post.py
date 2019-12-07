from sample1.database import MYSQL as db

from datetime import datetime

from ..tag.tag import get_sample1_tag_by_idx
from ..user_tag.user_tag import get_sample1_user_tag_by_user_tag_idx
from ..post_tag.post_tag import add_sample1_post_tag, sample1PostTags


class sample1Posts(db.Model):
    __tablename__ = 'sample1_posts'

    idx = db.Column(db.Integer(), primary_key=True,
                    nullable=False, autoincrement=True)

    writer_idx = db.Column(db.Integer(),
                           db.ForeignKey('user.idx'), nullable=False)
    writer = db.relationship('User', back_populates='sample1_posts_writer')

    post_tags_str = db.Column(db.Text, nullable=False)
    post_tags = db.relationship('sample1PostTags', back_populates='post')

    posted_date = db.Column(db.DateTime, nullable=False)

    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    # sample1_image = db.relationship('sample1Image', back_populates='post')

    comments = db.relationship('sample1Comment', back_populates='post')


def add_sample1_post(post_data, user_idx):

    tags_str = ""

    for tag in post_data['tags']:
        tag = get_sample1_user_tag_by_user_tag_idx(user_idx, tag['tag_idx'])
        if tag is None:
            return 404

        authority = {'admin': 1, 'owner': 2, 'teacher': 3, 'tagged_man': 4}
        if authority[tag.authority] > authority[tag.tag.authority]:
            return 403

    post_tags = []
    for tag in post_data['tags']:
        tag_option = tag['option']
        tag_name = get_sample1_tag_by_idx(tag['tag_idx']).name

        post_tags.append(sample1PostTags(
            tag_idx=tag['tag_idx'],
            tag_option=tag_option
        ))

        if tag_option == 'must':
            tags_str = tags_str + ', *' + tag_name
        elif tag_option == 'or':
            tags_str = tags_str + ', ' + tag_name
        elif tag_option == 'not':
            tags_str = tags_str + ', !' + tag_name
        else:
            return 405

    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(sample1Posts(
        writer_idx=user_idx,
        post_tags_str=tags_str[2:],
        posted_date=date,
        title=post_data['title'],
        content=post_data['content'],
        post_tags=post_tags
    ))
    db.session.commit()

    # 처음에 했던 개뻘짓
    # post = sample1Posts.query.filter_by(
    #     writer_idx=user_idx, posted_date=date)
    # if len(post.all()) > 1:
    #     post = post.filter_by(title=post_data['title'])
    #     if len(post.all()) > 1:
    #         post = post.filter_by(post_tags_str=tags_str)
    #         if len(post.all()) > 1:
    #             post = post.filter_by(content=post_data['content'])
    # post = post.first().idx
    #
    # for tag in post_data['tags']:
    #     add_sample1_post_tag(post, tag['tag_idx'], tag['option'])


def get_sample1_post_by_idx(post_idx):
    return sample1Posts.query.filter_by(idx=post_idx).first()


def get_my_sample1_post_by_idx(post_idx, user_idx):
    return sample1Posts.query.filter_by(idx=post_idx,
                                     writer_idx=user_idx).first()


def get_sample1_post_by_writer_idx(user_idx):
    return sample1Posts.query.filter_by(writer_idx=user_idx).all()


def get_sample1_post_by_writer_idx_last(user_idx):
    return sample1Posts.query.filter_by(writer_idx=user_idx).last()


def get_newest_posts(page=1, page_size=10):
    if page < 1:
        return []
    return sample1Posts.query.order_by(sample1Posts.idx.desc())\
        .offset((page - 1) * page_size).limit(page_size).all()


'''
def get_my_newest_posts(user_idx, page=1, page_size=10):

    tag_filter = "sample1Posts.tag."

    for tag in get_tag_by_user_idx(user_idx):
        tag_filter = tag_filter + tag.~~

    if page < 1:
        return []
    return sample1Posts.query.order_by(sample1Posts.idx.desc())\
        .filter(tag_filter)\
        .offset((page - 1) * page_size).limit(page_size).all()
'''
