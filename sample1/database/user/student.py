from sample1.database import MYSQL as db
import datetime


class Student(db.Model):
    __tablename__ = 'student'

    idx = db.Column(db.Integer, db.ForeignKey('user.idx'),
                    primary_key=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    klass = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    serial = db.Column(db.String(10), nullable=False)
    user = db.relationship("User", back_populates="student")


def get_student(user_idx):
    return Student.query.filter_by(idx=user_idx).first()


def get_student_by_serial(user_serial):
    return Student.query.filter_by(serial=user_serial).first()


def delete_all_student():
    Student.query.delete()


def get_all_student_by_grade(grade):
    return Student.query.filter_by(grade=grade) \
        .order_by(Student.serial.asc()).all()


def add_all_student(students_data):
    for student_data in students_data:
        student = Student.query.filter_by(idx=student_data['user_id']).first()
        if student is None:
            db.session.add(Student(idx=student_data['user_id'],
                                   grade=student_data['grade'],
                                   klass=student_data['class'],
                                   number=student_data['number'],
                                   serial=student_data['serial']))
        else:
            student.idx = student_data['user_id'],
            student.grade = student_data['grade'],
            student.klass = student_data['class'],
            student.number = student_data['number'],
            student.serial = student_data['serial']
    db.session.commit()
