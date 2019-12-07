from sample1.resource import api

from flask_restplus import Resource, fields, marshal
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from sample1.decorators import permission_required
from sample1.upload import allowed_file

from flask import request, abort, jsonify, send_file

from sample1.database.post.post import (
    add_sample1_post,
    get_sample1_post_by_idx,
    get_my_sample1_post_by_idx,
    get_sample1_post_by_writer_idx,
    get_sample1_post_by_writer_idx_last,
    get_newest_posts
)

from sample1.database.post_tag.post_tag import (
    get_all_sample1_post_tag_by_post_idx
)

from time import mktime
import datetime
import xlsxwriter
import io
import os

ns = api.namespace('post', description='Post methods')
'''
sns_page_full_model = ns.clone('FullSNSPageModel', {
    'idx': fields.Integer(required=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'postoption': fields.String(required=True),
    'target_grade': fields.String(required=True),
    'opened_date': fields.DateTime(required=True),
    'profile_image_hashed': fields.String(),
    'profile_image_origin': fields.String(),
    'boss': fields.Nested(sample1_post_user_model)
})


sns_comment_full_model = ns.model('FullSNSCommentModel', {
    'idx': fields.Integer(required=True),
    'posts_idx': fields.Integer(required=True),
    'writer_idx': fields.Integer(required=True),
    'content': fields.String(required=True),
    'posted_date': fields.DateTime(required=True),
})


sns_post_model = ns.model('LightSNSPostModel', {
    'content': fields.String(required=True),
    'existimage': fields.String(required=True),
    'youtubeurl': fields.String(required=True),
    'posted_date': fields.DateTime(required=True)
})
'''

sample1_post_user_model = ns.model('sample1PostUserModel', {
    'idx': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
    'grade': fields.Integer(),
    'klass': fields.Integer(),
    'number': fields.Integer(),
    'serial': fields.String()
})

sample1_post_tag_model = ns.model('sample1PostTagModel', {
    'tag_idx': fields.Integer(required=True),
    'option': fields.String(required=True)
})

sample1_post_tag_full_model = ns.model('sample1PostTagFullModel', {
    'tag_idx': fields.Integer(required=True),
    'tag_name': fields.String(attribute='tag.name', required=True),
    'tag_option': fields.String(required=True)
})

sample1_comment_model = ns.model('sample1CommentModel', {
    'idx': fields.Integer(required=True),
    'target_type': fields.String(required=True),
    'target_idx': fields.Integer(required=True),
    'status': fields.String(required=True),
    'writer': fields.Nested(sample1_post_user_model),
    'wrote_date': fields.Integer(required=True),
    'content': fields.String(required=True)
})

sample1_post_model = ns.model('sample1PostModel', {
    'title': fields.String(required=True),
    'content': fields.String(required=True),
    'tags': fields.List(fields.Nested(sample1_post_tag_model))
})

sample1_post_full_model = ns.model('sample1PostFullModel', {
    'idx': fields.Integer(required=True),
    'posted_date': fields.Integer(),
    'title': fields.String(required=True),
    'writer': fields.Nested(sample1_post_user_model),
    'post_tags': fields.List(fields.Nested(sample1_post_tag_full_model)),
    'content': fields.String(required=True),
    'comments': fields.List(fields.Nested(sample1_comment_model))
})

sample1_post_brief_model = ns.clone('sample1PostBriefMode', {
    'idx': fields.Integer(required=True),
    'posted_date': fields.Integer(required=True),
    'title': fields.String(required=True),
    'writer': fields.Nested(sample1_post_user_model),
    'post_tags': fields.List(fields.Nested(sample1_post_tag_full_model))
})

sample1_post_brief_list_model = ns.clone('sample1PostBriefListMode', {
        'posts': fields.List(fields.Nested(sample1_post_brief_model))
    }
)


@ns.route('s/brief')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class Allsample1PostBriefResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_post_brief_list_model)
    @ns.doc(description='''가장 최근의 포스트 10개의 브리핑 리스트를
                           반환합니다.''',
            responses={200: '글목록을 성공적으로 출력했습니다.'})
    def get(self):
        responses = get_newest_posts()

        for response in responses:
            res_dict = response.__dict__
            res_dict['posted_date'] = mktime(response.posted_date.timetuple())

            if response.writer.user_type == 'S':
                res_dict['writer'] = {
                    'idx': response.writer_idx,
                    'name': response.writer.name,
                    'type': response.writer.user_type,
                    'grade': response.writer.student.grade,
                    'klass': response.writer.student.klass,
                    'number': response.writer.student.number,
                    'serial': response.writer.student.serial
                }
            else:
                res_dict['writer'] = {
                    'idx': response.writer_idx,
                    'name': response.writer.name,
                    'type': response.writer.user_type
                }

        return {'posts': responses}, 200


@ns.route('/<int:post_idx>')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class Allsample1PostResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_post_full_model)
    @ns.doc(description='''해당 idx의 포스트를 줍니다..''',
            responses={200: '포스트를 성공적으로 출력했습니다.'})
    def get(self, post_idx):

        response = get_sample1_post_by_idx(post_idx)
        res_dict = response.__dict__
        res_dict['posted_date'] = mktime(response.posted_date.timetuple())

        if response.writer.user_type == 'S':
            res_dict['writer'] = {
                'idx': response.writer_idx,
                'name': response.writer.name,
                'type': response.writer.user_type,
                'grade': response.writer.student.grade,
                'klass': response.writer.student.klass,
                'number': response.writer.student.number,
                'serial': response.writer.student.serial
            }

        for comment in response.comments:
            com_dict = comment.__dict__
            com_dict['wrote_date'] = mktime(comment.wrote_date.timetuple())
            if comment.writer.user_type == 'S':
                com_dict['writer'] = {
                    'idx': comment.writer_idx,
                    'name': comment.writer.name,
                    'type': comment.writer.user_type,
                    'grade': comment.writer.student.grade,
                    'klass': comment.writer.student.klass,
                    'number': comment.writer.student.number,
                    'serial': comment.writer.student.serial
                }
            else:
                com_dict['writer'] = {
                    'idx': comment.writer_idx,
                    'name': comment.writer.name,
                    'type': comment.writer.user_type
                }

        return response, 200


@ns.route('/')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class Allsample1PostResource(Resource):
    @jwt_required
    @ns.expect(sample1_post_model)
    @ns.doc(description='''새 포스트를 작성합니다.''',
            responses={200: '성공적으로 작성하였습니다.',
                       403: '권한이 없는 태그를 사용하였습니다.',
                       404: '작성자가 소유하지 않은 태그입니다.',
                       405: '없는 옵션입니다.'})
    def post(self):
        return {}, add_sample1_post(
            request.get_json(), get_jwt_identity()[0]['idx'])
