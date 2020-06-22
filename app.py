from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_cors import CORS
from sqlalchemy.dialects.mysql import INTEGER, BIGINT, CHAR, DECIMAL, DATE, DATETIME, VARCHAR, TIMESTAMP
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow
import datetime

import simplejson

from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools

from sqlalchemy import table, column, func, desc

import os

# Usefull links:
# https://blog.miguelgrinberg.com/post/nested-queries-with-sqlalchemy-orm
# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
# https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.func

def create_token(api_user, api_role):
    '''
    生成token
    :param api_user:用户id
    :return: token
    ''' 
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=3600)
    token = s.dumps({"id":api_user, "role":api_role}).decode("ascii")
    return token

def verify_token(token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except Exception:
        return None
    if (data["role"] == 0):
        result = Student.query.get(data["id"])
    elif (data["role"] == 1):
        result = Teacher.query.get(data["id"])
    elif (data["role"] == 2):
        result = Admin.query.get(data["id"])
    return result

def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            token = request.headers["z-token"]
        except Exception:
            return jsonify(code = 4103,msg = '缺少参数token')
        
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code = 500,msg = "登录已过期")

        return view_func(*args,**kwargs)

    return verify_token

# https://stackoverflow.com/questions/32419455/how-to-sum-count-subqueries-with-sqlalchemy --> count sum etc

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

# init app
app = Flask(__name__)

# API Endpoints


# Database
app.config['MYSQL_USER'] = 'nmt_fleet_manager'
#app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_PASSWORD'] = 'Fleet2019S2'
app.config['MYSQL_DB'] = 'nmt_fleet_manager'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE'] = 'nmt_fleet_manager'

#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nmt_fleet_manager:Fleet2019S2@localhost/nmt_fleet_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
mysql = MySQL(app)
CORS(app)
ma = Marshmallow(app)


# ################################################
# ######
# ######                MODELS
# ######
# ################################################
# ###### Create MySQL Tables using MySQLAlchemy
# ###############################################


# ################################################
# ######     Vehicle Class/Model
# ################################################

class Student(db.Model):
	id = db.Column(BIGINT(20), unsigned=True), primary_key = True)
	username = db.Column(VARCHAR(64)), nullable = False)
	password = db.Column(VARCHAR(64)), nullable = False)
	major = db.Column(VARCHAR(64)), nullable = False)
    sex = db.Column(BIGINT(20), unsigned=True), nullable = False)
    phone = db.Column(VARCHAR(64)), nullable = False)
	
	# Constructor
	def __init__(self, id, username, password, major, sex, phone):
		self.id = id
		self.username = username
		self.password = password
		self.major = major
        self.sex = sex
        self.phone = phone

class Teacher(db.Model):
	id = db.Column(BIGINT(20), unsigned=True), primary_key = True)
	username = db.Column(VARCHAR(64)), nullable = False)
	password = db.Column(VARCHAR(64)), nullable = False)
	major = db.Column(VARCHAR(64)), nullable = False)
	
	# Constructor
	def __init__(self, id, username, password, major):
		self.id = id
		self.username = username
		self.password = password
		self.major = major

class Admin(db.Model):
	id = db.Column(BIGINT(20), unsigned=True), primary_key = True)
	username = db.Column(VARCHAR(64)), nullable = False)
	password = db.Column(VARCHAR(64)), nullable = False)
	major = db.Column(VARCHAR(64)), nullable = False)
	
	# Constructor
	def __init__(self, id, username, password, major):
		self.id = id
		self.username = username
		self.password = password
		self.major = major

class CultivationPlan(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), nullable=False), db.ForeignKey('course.id', ondelete='CASCADE'), primary_key=True)
	student_id = db.Column(BIGINT(20), unsigned=True), db.ForeignKey('student.id', ondelete='CASCADE'))
	teacher_id = db.Column(BIGINT(20), unsigned=True), db.ForeignKey('teacher.id', ondelete='CASCADE'))
	
	# Constructor
	def __init__(self, id, student_id, teacher_id):
        self.id = id
		self.student_id = student_id
        self.teacher_id = teacher_id

class Choose(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), nullable=False), db.ForeignKey('course.id', ondelete='CASCADE'), primary_key=True)
	student_id = db.Column(BIGINT(20), unsigned=True), db.ForeignKey('student.id', ondelete='CASCADE'))
	teacher_id = db.Column(BIGINT(20), unsigned=True), db.ForeignKey('teacher.id', ondelete='CASCADE'))
	
	# Constructor
	def __init__(self, id, student_id, teacher_id):
        self.id = id
		self.student_id = student_id
        self.teacher_id = teacher_id

		# asaa
		# 11111
		# afbeibfwiuebvbuiwreiub

class Course(db.Model):
    id = db.Column(BIGINT(20, unsigned=True), nullable=False, primary_key=True)
    serial_no = db.Column(VARCHAR(16), nullable=False)
    course_name = db.Column(VARCHAR(128), nullable=False)
    teacher_id = db.Column(VARCHAR(64), nullable=False)
    used = db.Column(BIGINT(20, unsigned=True), nullable=False, server_default=0)
    capacity = db.Column(BIGINT(20, unsigned=True), nullable=False)
    course_time = db.Column(BIGINT(20, unsigned=True), nullable=False)
    course_length = db.Column(BIGINT(20, unsigned=True), nullable=False, server_default=1)
    course_exam_time = db.Column(VARCHAR(64), nullable=False)
    course_position = db.Column(VARCHAR(64), nullable=False)
	major = db.Column(VARCHAR(64), nullable=False)
	credit = db.Column(BIGINT(20, unsigned=True), nullable=False)

    
    def __init__(self, id, serial_no, course_name, teacher_id, used, capacity, course_time, course_length, course_exam_time, course_position, major, credit):
        self.id = id
        self.serial_no = serial_no
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.used = used
        self.capacity = capacity
        self.course_time = course_time
        self.course_length = course_length
        self.course_exam_time = course_exam_time
        self.course_position = course_position
		self.major = major
		self.credit = credit

# ################################################
# ######
# ######                SCHEMAS
# ######
# ################################################
# ###### Create model Schemas using Marshmallow
# ###############################################

# ################################################
# ######     Vehicles
# ################################################

class CourseSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'serial_no', 'course_name', 'teacher_id', 'used', 'capacity', 'course_time', 'course_length', 'course_exam_time', 'course_position', 'major', 'credit'}

class StudentSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'username', 'password', 'major', 'sex', 'phone'}

class TeacherSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'username', 'password', 'major'}

class AdminSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'username', 'password', 'major'}

class CultivationPlanSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'student_id', 'teacher_id'}

class ChooseSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'student_id', 'teacher_id'}

class ChosenCourseSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'code', 'name', 'teacher', 'position', 'class_time', 'exam_time'}
    
class ChosenStateSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'code', 'name', 'teacher', 'position', 'class_time', 'exam_time', 'chosen'}

class LoginSuccessSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'success', 'message', 'token', 'role'}

class LoginFailSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'success', 'message'}

class LogoutSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'success', 'message'}

class UserInfoSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'username', 'major'}

class UpdateCultivationPlanSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'success', 'message'}

class StudentChosenSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'code', 'name', 'position', 'class_time', 'exam_time', 'cap', 'used'}

class StudentTeacherSchema(ma.Schema):
    class Meta:
        orderd = True
        fields = {'id', 'name', 'sex', 'major', 'phone'}

# init schemas
course_schema = CourseSchema()

student_schema = StudentSchema()

teacher_schema = TeacherSchema()

admin_schema = AdminSchema()

cultivation_schema = CultivationPlanSchema()

choose_schema = ChooseSchema()


chosen_course_schema = ChosenCourseSchema()
chosens_course_schema = ChosenCourseSchema(many=True)

chosen_state_schema = ChosenStateSchema()
chosens_state_schema = ChosenStateSchema(many=True)

student_chosen_schema = StudentChosenSchema()
students_chosen_schema = StudentChosenSchema(many=True)

login_success_schema = LoginSuccessSchema()

login_fail_schema = LoginFailSchema()

logout_schema = LogoutSchema()

user_info_schema = UserInfoSchema()

update_cultivation_plan_schema = UpdateCultivationPlanSchema()

student_teacher_schema = StudentTeacherSchema()
students_teacher_schema = StudentTeacherSchema(many=True)

# ################################################
# ######
# ######            API END POINTS
# ######
# ################################################

# ################################################
# ######             GET Methods
# ###############################################

@app.route('/user/current', methods=['GET'])
def getUserInfo():
    token = request.headers["z-token"]
    student = verify_token(token)
    student_info = Student.query.filter(Student.id == student.id)
    result = user_info_schema.jsonify((student_info.username, student_info.major))
    return result

@app.route('/courses/enrolled', methods=['GET'])
def getSelectedCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    all_choose = Choose.query.filter(Choose.student_id == student.id).all()
    all_course = db.session.query(Course.serial_no, Course.course_name, Teacher.username, Course.course_position, Course.course_time, Course.course_exam_time).filter(Course.id in all_choose.id).filter(Teacher.id == all_choose.teacher_id).all()
    result = chosens_course_schema.jsonify(all_course)
    return result


@app.route('/courses/major', methods=['GET'])
def getMajorCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    all_course = db.session.query(Course.serial_no, Course.course_name, Teacher.username, Course.course_position, Course.course_time, Course.course_exam_time).filter(Course.major == student.major).filter(Teacher.id == Course.teacher_id).all()
    result = chosens_course_schema.jsonify(all_course)
    return result

@app.route('/user/courses', methods=['GET'])
def getAllCourse():
    token = request.headers["z-token"]
    user = verify_token(token)
    if (type(user).__name__ == 'Student'):
        all_choose = Choose.query.filter(Choose.student_id == student.id).all()
        all_course = db.session.query(Course.serial_no, Course.course_name, Teacher.username, Course.course_position, Course.course_time, Course.course_exam_time, 1 if Course.id in all_choose.id else 0).filter(Teacher.id == Course.teacher_id).all()
        result = chosens_state_schema.jsonify(all_course)
    elif (type(user).__name__ == 'Teacher'):
        all_choose = Choose.query.filter(Choose.teacher_id == teacher.id).all()
        all_course = db.session.query(Choose.id, Course.serial_no, Course.course_name, Course.course_position, Course.course_time, Course.course_exam_time, Course.capacity, Course.used).filter(Course.id in all_choose.id).all()
        result = students_chosen_schema.jsonify(all_course)
    return result

@app.route('/courses/:cid/list', methods=['GET'])
def getStudentTeacherList():
    token = request.headers["z-token"]
    teacher = verify_token(token)
    all_choose = Choose.query.filter(Choose.teacher_id == teacher.id).filter(cid == Choose.id).all() 
    all_student = db.session.query(Student.id, Student.username, Student.sex, Student.major, Student.phone).filter(Student.id in all_choose.student_id).all()
    result = students_teacher_schema.jsonify(all_student)
    return result



# ################################################
# ######             POST Methods
# ###############################################

@app.route('/login', methods=['POST'])
def userLogin(id, password):
	student_id_list = Student.query.all().id
	teacher_id_list = Teacher.query.all().id
	admin_id_list = Admin.query.all().id
	if (id in student_id_list):
		role = 0
	elif (id in teacher_id_list):
		role = 1
	elif (id in admin_id_list):
		role = 2
	else:
		role = -1
		result = login_fail_schema.jsonify((False, "Invalid username or password"))
	if (role == 0):
	    correct_password = Student.query.filter(Student.id == id)
		if (correct_password == password):
			result = login_success_schema.jsonify((True, "Login Success", create_token(id, 0), 0))
		else:
			result = login_fail_schema.jsonify((False, "Invalid username or password"))
	if (role == 1):
	    correct_password = Teacher.query.filter(Teacher.id == id)
		if (correct_password == password):
			result = login_success_schema.jsonify((True, "Login Success", create_token(id, 1), 1))
		else:
			result = login_fail_schema.jsonify((False, "Invalid username or password"))
	if (role == 2):
	    correct_password = Admin.query.filter(Admin.id == id)
		if (correct_password == password):
			result = login_success_schema.jsonify((True, "Login Success", create_token(id, 2), 2))
		else:
			result = login_fail_schema.jsonify((False, "Invalid username or password"))
    return result

@app.route('/logout', methods=['POST'])
def userLogout():
	result = logout_schema.jsonify((True, "Logout Success"))
	return result

@app.route('/user/scheme', methods=['POST'])
def cultivatePlan():
    token = request.headers["z-token"]
    student = verify_token(token)
    choose_list = request.json['classes']
    for choose in choose_list:
        # don't know whether can write like this
        course = Course.query.get(Course.serial_no == choose)
        choose_id = course.id
        choose_student = student.id
        choose_teacher = course.teacher_id
        new_choose = CultivationPlan(choose_id, choose_student, choose_teacher)
        db.session.merge(new_choose)
    
    db.session.commit()

    result = update_cultivation_plan_schema.jsonify((True, "Update training scheme success"))
    return result

@app.route('/user/courses', methods=['POST'])
def addCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    courses_list = request.json['courses']
    for course_serial_no in courses_list:
        course = Course.query.get(Course.serial_no == course_serial_no)

        # Unknown whether it's correct
        course.used += 1

        choose_id = course.id
        choose_student = student.id
        choose_teacher = course.teacher_id
        new_choose = Choose(choose_id, choose_student, choose_teacher)
        db.session.merge(new_choose)
    
    db.session.commit()

    return 204

@app.route('/courses/:cid/list', methods=['POST'])
def getStudentTeacherList():
    token = request.headers["z-token"]
    admin = verify_token(token)
    student_list = request.json['id']
    for student_id in student_list:
        course = Course.query.get(Course.id == cid)

        # Unknown whether it's correct
        course.used += 1

        choose_id = cid
        choose_student = student_id
        choose_teacher = course.teacher_id
        new_choose = Choose(choose_id, choose_student, choose_teacher)
        db.session.merge(new_choose)
    
    db.session.commit()

    return 200

# @app.route('/user/program', methods=['POST'])
# def CultivatePlan():
#     token = request.headers["z-token"]
#     student = verify_token(token)
#     choose_list = request.json['classes']
#     for choose in choose_list:
#         course = Course.query.get(Course.serial_no = choose)
#         choose_id = course.id
#         choose_student = student.id
#         choose_teacher = course.teacher_id
#         new_choose = CultivationPlan(choose_id, choose_student, choose_teacher)
#         db.session.merge(new_choose)
    
#     db.session.commit()

#     return 200

# @app.route('/user/courses/<serial_no>', methods=['POST'])
# def CultivatePlan():
#     token = request.headers["z-token"]
#     student = verify_token(token)
#     course = Course.query.get(serial_no)
#     course_id = course.id
#     course_student = student.id
#     course_teacher = course.teacher_id
#     new_course = Choose(course_id, student_id, course_teacher)
#     db.session.add(new_course)
    
#     db.session.commit()

#     return 200
	
# ################################################
# ######             PUT Methods
# ###############################################


# ################################################
# ######             DELETE Methods
# ###############################################
	
@app.route('/user/courses', methods=['DELETE'])
def deleteCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    courses_list = request.json['courses']
    for course_serial_no in courses_list:
        course = Course.query.get(Course.serial_no == course_serial_no)
        
        # Unknown whether it's correct
        course.used -= 1

        delete_course = Choose.query.get(Choose.id == course.id)
        db.session.delete(delete_choose)
	db.session.commit()
    return 204

@app.route('/courses/:cid/list', methods=['DELETE'])
def deleteCourse():
    token = request.headers["z-token"]
    admin = verify_token(token)
    student_list = request.json['id']
    for student_id in student_list:
        course = Course.query.get(Course.id == cid)
        
        # Unknown whether it's correct
        course.used -= 1

        delete_course = Choose.query.get(Choose.id == course.id and Choose.student_id == student_id)
        db.session.delete(delete_choose)
	db.session.commit()
    return 200

# Run server
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.1.105', debug=True)
