# from sample1.resource import api
# from sample1.etc.sample.auth import auth as d_auth
# from sample1.etc.sample.auth import life_auth as dlife_auth
# from sample1.etc.sample import redirect_url
# from sample1.database.revoked_token import RevokedToken
#
# from flask_restplus import Resource, fields, marshal
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token
# )
#
# from flask_jwt_extended import (
#     get_jwt_identity,
#     get_raw_jwt,
#     jwt_required,
#     jwt_refresh_token_required
# )
#
# import datetime
#
# ns = api.namespace('auth', description='Auth methods')
#
# auth_model = ns.model('AuthModel', {
#     'token': fields.String(required=True),
#     'refresh_token': fields.String(required=True),
# })
#
# auth_form_model = ns.model('AuthUserModel', {
#     'id': fields.String(required=True),
#     'password': fields.String(required=True)
# })
#
#
# @ns.route('/')
# class AuthResource(Resource):
#     @ns.marshal_with(auth_model)
#     @ns.expect(auth_form_model, validate=True)
#     @ns.doc(responses={200: 'Successsful',
#                        400: 'Need more parameter',
#                        404: 'Not found user'})
#     def post(self):
#         login_res = d_auth(api.payload['id'],
#                            api.payload['password'])
#         if login_res is not None:
#             if login_res.data['user_type'] is 'O':
#                 token = create_access_token(identity=login_res)
#                 refreshtoken = create_refresh_token(identity=login_res)
#                 return {'token': token,
#                         'refresh_token': refreshtoken}, 205
#             else:
#                 token = create_access_token(identity=login_res)
#                 refreshtoken = create_refresh_token(identity=login_res)
#                 return {'token': token,
#                         'refresh_token': refreshtoken}, 200
#         else:
#             return {}, 404
#
#
# @ns.route('/logout/refresh')
# @ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
# @ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
# class UserLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedToken(jti=jti)
#             revoked_token.add()
#             return {'message': 'complete revoking refresh token'}, 200
#         except:
#             return {}, 500
#
#
# @ns.route('/token/refresh')
# @ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
# @ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
# class TokenLogoutAccess(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         user = get_jwt_identity()
#         jti = get_raw_jwt()
#         access_token = create_access_token(identity=user)
#         exptime = datetime.datetime.fromtimestamp(int(jti['exp']))
#         now = datetime.datetime.now()
#         if (exptime - now).days < 10:
#             refreshtoken = create_refresh_token(identity=user)
#             return {'token': access_token,
#                     'refresh_token': refreshtoken}, 200
#         else:
#             return {'token': access_token}, 200
