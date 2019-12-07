from sample1.resource import api

from flask_restplus import Resource, fields, marshal
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from sample1.decorators import permission_required
from sample1.upload import allowed_file

from sample1.database.tag.tag import (
    add_sample1_tag,
    get_sample1_tag_by_idx,
    get_all_sample1_tags,
    search_tags_by_description,
    delete_tags_by_idx
)

from flask import request, abort, jsonify
from time import mktime

ns = api.namespace('tag', description='Tag methods')

keyword_model = ns.model('KeywordModel', {
    'keyword': fields.String(required=True)
})

sample1_tag_owner_model = ns.model('sample1TagOwnerModel', {
    'idx': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True, attribute='user_type'),
    'grade': fields.Integer(attribute='student.grade'),
    'klass': fields.Integer(attribute='student.klass'),
    'number': fields.Integer(attribute='student.number'),
    'serial': fields.String(attribute='student.serial')
})

sample1_tag_model = ns.model('sample1TagModel', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'join_option': fields.String(required=True)
})

sample1_tag_full_model = ns.model('sample1TagFullModel', {
    'idx': fields.Integer(required=True),
    'name': fields.String(required=True),
    'owner': fields.Nested(sample1_tag_owner_model),
    'created_date': fields.Integer(required=True),
    'description': fields.String(required=True),
    'join_option': fields.String(required=True)
})

sample1_tag_full_list_model = ns.model('sample1TagFullListModel', {
    'tags': fields.List(fields.Nested(sample1_tag_full_model))
})


@ns.route('/')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1TagResource(Resource):
    @jwt_required
    @ns.expect(sample1_tag_model)
    @ns.doc(description='''새 태그를 작성합니다.
                           join option은 'private', 'request',
                           'free_for_all'중 하나여야 합니다.''',
            responses={200: '성공적으로 작성하였습니다.'})
    def post(self):
        return {}, add_sample1_tag(
            request.get_json(), get_jwt_identity()[0]['idx'])


@ns.route('/<int:tag_idx>')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1TagIdxResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_tag_full_model)
    @ns.doc(description='''해당 idx의 태그를 줍니다.''',
            responses={200: '성공적으로 출력하였습니다.'})
    def get(self, tag_idx):
        response = get_sample1_tag_by_idx(tag_idx)
        if response == 404:
            return {}, 404
        response.__dict__['created_date'] =\
            mktime(response.created_date.timetuple())
        return response, 200

    @jwt_required
    @ns.doc(description='''해당 idx의 태그를 삭제합니다.''',
            responses={200: '성공적으로 삭제하였습니다.',
                       403: '권한이 없습니다.',
                       404: '해당 idx의 태그가 없습니다.',
                       409: '''이태그는 이미 많이 쓰이고 있습니다.
                               먼저 태그의 다른 사용자를 추방하세요.'''})
    def delete(self, tag_idx):
        return {}, delete_tags_by_idx(tag_idx, get_jwt_identity()[0]['idx'])


@ns.route('s')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1TagAllResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_tag_full_list_model)
    @ns.doc(description='''모든 태그를 줍니다.''',
            responses={200: '성공적으로 출력하였습니다.',
                       404: '해당 idx의 태그가 없습니다.'})
    def get(self):
        responses = get_all_sample1_tags()
        for response in responses:
            response.__dict__['created_date'] =\
                mktime(response.created_date.timetuple())
        return {'tags': responses}, 200


@ns.route('s/search')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1TagAllResource(Resource):
    @jwt_required
    @ns.expect(keyword_model)
    @ns.marshal_with(sample1_tag_full_list_model)
    @ns.doc(description='''설명이나 제목에 검색어가 들어간 태그를 줍니다.''',
            responses={200: '성공적으로 출력하였습니다.',
                       404: '해당 idx의 태그가 없습니다.'})
    def get(self):
        responses = search_tags_by_description(request.get_json()['keyword'])
        for response in responses:
            response.__dict__['created_date'] =\
                mktime(response.created_date.timetuple())
        return {'tags': responses}, 200
