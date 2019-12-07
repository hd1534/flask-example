from sample1.resource import api

from flask_restplus import Resource, fields, marshal
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from sample1.decorators import permission_required

from sample1.database.user_tag.user_tag import (
    add_sample1_user_tag_invitation,
    add_sample1_user_tag_request,
    get_all_sample1_user_tags_by_user_idx,
    get_all_sample1_user_tags_invitations_by_user_idx,
    get_all_sample1_user_tags_requests_by_user_idx,
    get_sample1_user_tag_by_user_tag_idx,
    delete_sample1_user_tag_by_user_tag_idx
)

from flask import request, abort, jsonify
from time import mktime

from ..tag.tag import sample1_tag_full_list_model

ns = api.namespace('user_tag', description='User Tag methods')

sample1_tag_idx_model = ns.model('sample1TagIdxMode', {
    'tag_idx': fields.Integer(required=True)
})

sample1_user_tag_model = ns.model('sample1UserTagModel', {
    'user_idx': fields.Integer(required=True),
    'tag_idx': fields.Integer(required=True),
    'admin': fields.Boolean(required=True),
    'modification_allowed': fields.Boolean(required=True),
    'invitation_allowed': fields.Boolean(required=True),
    'post_allowed': fields.Boolean(required=True),
    'acceptance_allowed': fields.Boolean(required=True)
})

sample1_user_tag_full_model = ns.model('sample1UserTagFullModel', {
    'idx': fields.Integer(required=True),
    'user_idx': fields.Integer(required=True),
    'tag_idx': fields.Integer(required=True),
    'status': fields.String(required=True),
    'admin': fields.Boolean(required=True),
    'modification_allowed': fields.Boolean(required=True),
    'invitation_allowed': fields.Boolean(required=True),
    'post_allowed': fields.Boolean(required=True),
    'acceptance_allowed': fields.Boolean(required=True)
})


@ns.route('/invitation')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagInvitationResource(Resource):
    @jwt_required
    @ns.expect(sample1_user_tag_model)
    @ns.doc(description='''대상을 해당 idx의 태그로 초대합니다.''',
            responses={200: '성공적으로 초대하였습니다.',
                       403: '권한이 없습니다.',
                       404: '존재하지 않는 대상입니다.',  # 처리 아직 안함.
                       409: '이미 보냈습니다.'})
    def post(self):
        data = request.get_json()

        user_tag = get_sample1_user_tag_by_user_tag_idx(
            get_jwt_identity()[0]['idx'], data['tag_idx'])
        if user_tag is None:
            return {}, 403
        if user_tag.invitation_allowed is False:
            return {}, 403

        data['status'] = 'waiting'
        return {}, add_sample1_user_tag_invitation(data)


@ns.route('/invitation/admin')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagInvitationAdminResource(Resource):
    @permission_required('sample1', 2)
    @jwt_required
    @ns.expect(sample1_user_tag_model)
    @ns.doc(description='''대상에 해당 idx의 태그를 넣습니다.''',
            responses={200: '성공적으로 넣었습니다.',
                       404: '존재하지 않는 대상입니다.'})
    def post(self):
        data = request.get_json()
        data['status'] = 'forced'
        return {}, add_sample1_user_tag_invitation(data)


@ns.route('/my/invitations')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagMyInvitationsResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_tag_full_list_model)
    @ns.doc(description='''자신에게 왔던 모든 '태그 초대'를 줍니다.''',
            responses={200: '성공적으로 모든 태그 초대를 주었습니다.'})
    def get(self):
        responses = get_all_sample1_user_tags_invitations_by_user_idx(
            get_jwt_identity()[0]['idx'])

        tags = []
        for response in responses:
            response.tag.__dict__['created_date'] =\
                mktime(response.created_date.timetuple())
            tags.append(response)

        return {'tags': tags}, 200


@ns.route('/my/request/<int:tag_idx>')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagMyRequestResource(Resource):
    @jwt_required
    @ns.doc(description='''해당 idx의 태그를 신청합니다.''',
            responses={200: '성공적으로 신청하였습니다.',
                       403: '신청할 수 없는 태그입니다.',  # 미구현
                       404: '존재하지 않는 태그입니다.',  # 처리 아직 안함.
                       409: '이미 보냈습니다.'})  # 미구현
    def post(self, tag_idx):
        return add_sample1_user_tag_request(
            {'tag_idx': tag_idx}, get_jwt_identity()[0]['idx]'])


# 현재 request 랑 refused 구별 x 수정해야됨
@ns.route('/my/requests')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagMyRequestsResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_tag_full_list_model)
    @ns.doc(description='''자신이 신청했던 태그 목록을 줍니다.''',
            responses={200: '성공적으로 모든 태그 목록을 주었습니다.'})
    def get(self):
        responses = get_all_sample1_user_tags_invitations_by_user_idx(
            get_jwt_identity()[0]['idx'])

        tags = []
        for response in responses:
            response.tag.__dict__['created_date'] =\
                mktime(response.created_date.timetuple())
            tags.append(response)

        return {'tags': tags}, 200


# 현재 request 랑 refused 구별 x 수정해야됨
@ns.route('/tag/<int:tag_idx>/requests')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagMyRequestsResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_tag_full_list_model)
    @ns.doc(description='''해당 idx의 태그의 모든 신청목록을 줍니다.''',
            responses={200: '성공적으로 모든 신청목록을 주었습니다.'})
    def get(self):
        responses = get_all_sample1_user_tags_invitations_by_user_idx(
            get_jwt_identity()[0]['idx'])

        tags = []
        for response in responses:
            response.tag.__dict__['created_date'] =\
                mktime(response.created_date.timetuple())
            tags.append(response)

        return {'tags': tags}, 200


@ns.route('/my/<int:tag_idx>')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagIdxResource(Resource):
    @jwt_required
    @ns.doc(description='''자신의 해당 idx의 태그를 제거합니다.''',
            responses={200: '성공적으로 제거하였습니다.',
                       403: '관리자에 의해서 부여된거라 권한이 없습니다.',  # 미구현
                       404: '해당 idx의 태그를 소유하지 않았습니다.'})  # 미구현
    def delete(self, tag_idx):
        return {}, delete_sample1_user_tag_by_user_tag_idx(
            tag_idx, get_jwt_identity()[0]['idx'])


@ns.route('/my/tags')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class sample1UserTagAllResource(Resource):
    @jwt_required
    @ns.marshal_with(sample1_tag_full_list_model)
    @ns.doc(description='''자신이 가지고 있는 모든 태그를 줍니다.''',
            responses={200: '성공적으로 출력하였습니다.',
                       404: '존재하지 않는 유접니다.'})
    def get(self):
        responses =\
            get_all_sample1_user_tags_by_user_idx(get_jwt_identity()[0]['idx'])
        tags = []
        for response in responses:
            tag = response.tag.__dict__
            tag['created_date'] = mktime(response.created_date.timetuple())
            tags.append(tag)
        return {'tags': tags}, 200
