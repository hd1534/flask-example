from sample1.resource import api

from flask_restplus import Resource, fields, marshal
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from sample1.decorators import permission_required
from sample1.upload import allowed_file

from sample1.database.comment.comment import (
    add_sample1_comment,
    get_all_unchecked_comments_by_user_idx,
    update_sample1_comment_by_idx,
    delete_sample1_comment_by_idx
)

from flask import request, abort, jsonify
from time import mktime

ns = api.namespace('comment', description='Comment methods')

sample1_content_model = ns.model('sample1ContentModel', {
    'content': fields.String(required=True)
})

sample1_comment_model = ns.model('sample1CommentModel', {
    'post_idx': fields.Integer(required=True),
    'target_type': fields.String(required=True),
    'target_idx': fields.Integer(required=True),
    'content': fields.String(required=True)
})

sample1_comment_full_model = ns.model('sample1CommentFullModel', {
    'post_idx': fields.Integer(required=True),
    'target_type': fields.String(required=True),
    'target_idx': fields.Integer(required=True),
    'writer_idx': fields.Integer(required=True),
    'status': fields.String(required=True),
    'wrote_date': fields.Integer(required=True),
    'content': fields.String(required=True),
    'has_a_reply': fields.Integer(required=True)
})

sample1_comment_full_list_model = ns.model('sample1CommentFullListModel', {
    'comments': fields.List(fields.Nested(sample1_comment_full_model))
})


@ns.route('/')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class Allsample1TagResource(Resource):
    @jwt_required
    @ns.expect(sample1_comment_model)
    @ns.doc(description='''새 댓글을 작성합니다.
                           target_type 은 'post', 'comment'중 하나여야 합니다.''',
            responses={200: '성공적으로 작성하였습니다.',
                       404: '없는 포스트(댓글) 입니다.'})
    def post(self):
        return {}, add_sample1_comment(
            request.get_json(), get_jwt_identity()[0]['idx'])


@ns.route('/<int:comment_idx>')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class Allsample1TagIdxResource(Resource):
    @jwt_required
    @ns.expect(sample1_content_model)
    @ns.doc(description='''해당 idx의 댓글을 수정합니다.''',
            responses={200: '성공적으로 수정하였습니다.',
                       403: '본인이 아닙니다.',
                       404: '없습니다!'})
    def put(self, comment_idx):
        return update_sample1_comment_by_idx(
            comment_idx,
            request.get_json()['content'],
            get_jwt_identity()[0]['idx'])

    @jwt_required
    @ns.doc(description='''해당 idx의 댓글을 삭제합니다.''',
            responses={200: '성공적으로 삭제하였습니다.',
                       403: '본인이 아닙니다.',
                       404: '해당 idx의 댓글이 없습니다.',
                       409: '이댓글에 댓글이 달려 있습니다.'})
    def delete(self, comment_idx):
        return {}, delete_sample1_comment_by_idx(
            comment_idx, get_jwt_identity()[0]['idx'])


@ns.route('/notices')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class Allsample1TagAllResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_comment_full_list_model)
    @ns.doc(description='''자신에 글에 달린 읽지 않은 댓글들을 알려줍니다.''',
            responses={200: '성공적으로 출력하였습니다.'})
    def get(self):
        responses = get_all_unchecked_comments_by_user_idx(
            get_jwt_identity()[0]['idx'])
        return {'tags': responses}, 200
