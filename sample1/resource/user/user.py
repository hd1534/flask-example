from sample1.resource import api
from sample1.decorators import permission_required

from flask_restplus import Resource, fields, marshal
from flask_jwt_extended import create_access_token

from sample1.database.user.user import (
    add_all_user,
    get_user
)
from sample1.database.user.student import (
    add_all_student,
    get_student,
    delete_all_student
)
from flask_jwt_extended import jwt_required, get_jwt_identity

ns = api.namespace('user', description='User methods')

user_full_model = ns.model('UserModel', {
    'idx': fields.Integer(required=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'user_type': fields.String(required=True),
    'gender': fields.String(required=True)
})

student_model = ns.model('StudentModel', {
    'idx': fields.Integer(),
    'grade': fields.String(),
    'klass': fields.String(),
    'number': fields.String,
    'serial': fields.String
})

user_plus_student_model = ns.clone(
    'Student', user_full_model, {
        'student': fields.List(fields.Nested(student_model))
    }
)

full_student_model = ns.model('FullStudentModel', {
    'idx': fields.Integer(),
    'name': fields.String,
    'grade': fields.String(),
    'klass': fields.String(),
    'number': fields.String,
    'serial': fields.String,
    'photo': fields.String,
    'email': fields.String,
    "user_type": fields.String

})


@ns.route('/<user_idx>')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class AllDetsResource(Resource):

    @permission_required('admin', 1)
    @jwt_required
    @ns.marshal_with(user_plus_student_model)
    @ns.doc(description='''user_idx 로 학생 정보 출력한다,,''',
            responses={200: '학생정보를 성공적으로 출력했습니다.'})
    def get(self, user_idx):
        student = get_user(user_idx)
        return student


@ns.route('/cron/')
class UserCronResource(Resource):
    @ns.doc(responses={200: 'Successsful'})
    def get(self):
        users_data = users()
        add_all_user(users_data)
        students_data = students()
        delete_all_student()
        add_all_student(students_data)


@ns.route('/jwt/')
@ns.header('Authorization', 'JWT Token (with Bearer)', required=True)
@ns.param('Authorization', 'JWT Token (with Bearer)', 'header', required=True)
class ReadJWT(Resource):
    @jwt_required
    @ns.marshal_with(full_student_model)
    @ns.doc(description='''jwt대신까줌''',
            responses={200: '학생정보를 성공적으로 출력했습니다.'})
    def get(self):
        print(get_jwt_identity())
        if get_jwt_identity()[0]['user_type'] == 'S':
            jwt = {
                'idx': get_jwt_identity()[0]['idx'],
                'name': get_jwt_identity()[0]['name'],
                'grade': get_jwt_identity()[0]['grade'],
                'klass': get_jwt_identity()[0]['klass'],
                'number': get_jwt_identity()[0]['number'],
                'serial': get_jwt_identity()[0]['serial'],
                'email': get_jwt_identity()[0]['email'],
                "user_type": get_jwt_identity()[0]['user_type']}
        else:
            jwt = {
                'idx': get_jwt_identity()[0]['idx'],
                'name': get_jwt_identity()[0]['name'],
                'email': get_jwt_identity()[0]['email'],
                "user_type": get_jwt_identity()[0]['user_type']}
        return jwt
