from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_cors import CORS
from sqlalchemy.dialects.mysql import INTEGER, BIGINT, CHAR, DECIMAL, DATE, DATETIME, VARCHAR, TIMESTAMP
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow
import datetime
import base64
import simplejson
from hashlib import sha256
import copy
from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools

from sqlalchemy import table, column, func, desc

import os

# Usefull links:
# https://blog.miguelgrinberg.com/post/nested-queries-with-sqlalchemy-orm
# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
# https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.func

# def create_token(api_user, api_role):
# 	'''
# 	生成token
# 	:param api_user:用户id
# 	:return: token
# 	''' 
# 	s = Serializer(current_app.config["SECRET_KEY"],expires_in=3600)
# 	tmp_dict = {"id":api_user, "role":api_role}
# 	tmp_byte = bytes('{}'.format(tmp_dict),'utf-8')
# 	token = s.dumps(copy.deepcopy(tmp_byte)).decode()
# 	return token

# def verify_token(token):
# 	'''
# 	校验token
# 	:param token: 
# 	:return: 用户信息 or None
# 	'''
# 	s = Serializer(current_app.config["SECRET_KEY"])
# 	try:
# 		data = s.loads(token)
# 	except Exception:
# 		return None
# 	if (data["role"] == 0):
# 		result = Student.query.get(data["id"])
# 	elif (data["role"] == 1):
# 		result = Teacher.query.get(data["id"])
# 	elif (data["role"] == 2):
# 		result = Admin.query.get(data["id"])
# 	return result

# def login_required(view_func):
# 	@functools.wraps(view_func)
# 	def verify_token(*args,**kwargs):
# 		try:
# 			token = request.headers["z-token"]
# 		except Exception:
# 			return jsonify(code = 4103,msg = '缺少参数token')
		
# 		s = Serializer(current_app.config["SECRET_KEY"])
# 		try:
# 			s.loads(token)
# 		except Exception:
# 			return jsonify(code = 500,msg = "登录已过期")

# 		return view_func(*args,**kwargs)

# 	return verify_token


username_to_token = {}

token_to_username = {}

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
	id = db.Column(BIGINT(20, unsigned=True), primary_key = True)
	username = db.Column(VARCHAR(64), nullable = False)
	password = db.Column(VARCHAR(64), nullable = False)
	major = db.Column(VARCHAR(64), nullable = False)
	sex = db.Column(BIGINT(20, unsigned=True), nullable = False)
	phone = db.Column(VARCHAR(64), nullable = False)

	# Constructor
	def __init__(self, id, username, password, major, sex, phone):
		self.id = id
		self.username = username
		self.password = password
		self.major = major
		self.sex = sex
		self.phone = phone

class Teacher(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), primary_key = True)
	username = db.Column(VARCHAR(64), nullable = False)
	password = db.Column(VARCHAR(64), nullable = False)
	major = db.Column(VARCHAR(64), nullable = False)

	# Constructor
	def __init__(self, id, username, password, major):
		self.id = id
		self.username = username
		self.password = password
		self.major = major

class Admin(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), primary_key = True)
	username = db.Column(VARCHAR(64), nullable = False)
	password = db.Column(VARCHAR(64), nullable = False)
	major = db.Column(VARCHAR(64), nullable = False)

	# Constructor
	def __init__(self, id, username, password, major):
		self.id = id
		self.username = username
		self.password = password
		self.major = major

class CultivationPlan(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False,  primary_key=True)
	student_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('student.id', ondelete='CASCADE'))
	teacher_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('teacher.id', ondelete='CASCADE'))

	# Constructor
	def __init__(self, id, student_id, teacher_id):
		self.id = id
		self.student_id = student_id
		self.teacher_id = teacher_id

class Choose(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False,  primary_key=True)
	student_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('student.id', ondelete='CASCADE'))
	teacher_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('teacher.id', ondelete='CASCADE'))

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
	used = db.Column(BIGINT(20, unsigned=True), nullable=False)
	capacity = db.Column(BIGINT(20, unsigned=True), nullable=False)
	course_time = db.Column(VARCHAR(64), nullable=False)
	course_length = db.Column(BIGINT(20, unsigned=True), nullable=False)
	course_exam_time = db.Column(VARCHAR(64), nullable=False)
	course_position = db.Column(VARCHAR(64), nullable=False)
	major = db.Column(VARCHAR(64), nullable=False)
	credit = db.Column(BIGINT(20, unsigned=True), nullable=False)
	chosen_true = db.Column(BIGINT(20, unsigned=True), nullable=False)
	chosen_false = db.Column(BIGINT(20, unsigned=True), nullable=False)


	def __init__(self, id, serial_no, course_name, teacher_id, used, capacity, course_time, course_length, course_exam_time, course_position, major, credit, chosen_true, chosen_false):
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
		self.chosen_true = chosen_true
		self.chosen_false = chosen_false

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
		fields = ('id', 'serial_no', 'course_name', 'teacher_id', 'used', 'capacity', 'course_time', 'course_length', 'course_exam_time', 'course_position', 'major', 'credit')

class StudentSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'username', 'password', 'major', 'sex', 'phone')

class TeacherSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'username', 'password', 'major')

class AdminSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'username', 'password', 'major')

class CultivationPlanSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'student_id', 'teacher_id')

class ChooseSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'student_id', 'teacher_id')

class ChosenCourseSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('serial_no', 'course_name', 'teacher_id', 'course_position', 'course_time', 'course_exam_time')
    
class ChosenStateSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('serial_no', 'course_name', 'teacher_id', 'course_position', 'course_time', 'course_exam_time', 'chosen')

class LoginSuccessSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('success', 'message', 'token', 'role')

class LoginFailSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('success', 'message')

class LogoutSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('success', 'message')

class UserInfoSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('username', 'major')

class UpdateCultivationPlanSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('success', 'message')

class StudentChosenSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'serial_no', 'course_name', 'course_position', 'course_time', 'course_exam_time', 'capacity', 'used')

class StudentTeacherSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'username', 'sex', 'major', 'phone')

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


@app.after_request
def change_request_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Token, Magic"
    return response

def sha256encode(arg):
    sha256_pwd = sha256(bytes('info_mgr',encoding='utf-8'))
    sha256_pwd.update(bytes(arg,encoding='utf-8'))
    return sha256_pwd.hexdigest()


# ################################################
# ######
# ######            TEST app.py
# ######
# ################################################

token = sha256encode('3170105470')
username_to_token['3170105470'] = token
token_to_username[token] = '3170105470'
token = sha256encode('3000000000')
username_to_token['3000000000'] = token
token_to_username[token] = '3000000000'
token = sha256encode('666666')
username_to_token['666666'] = token
token_to_username[token] = '666666'
token = sha256encode('99999')
username_to_token['99999'] = token
token_to_username[token] = '99999'
# db.create_all()
# db.session.add(Student('3170105470', 'zys', '123456', 'cs', '1', '18888922411'))
# db.session.add(Student('3000000000', 'wzh', '123456', 'cs', '1', '111111'))
# db.session.commit()
# # student = Student.query.filter(Student.id == '3170105470').all()
# # create_token('3000000000'.encode(), 0)

# db.session.add(Teacher('666666', 'teacher', '123456', 'math'))
# db.session.commit()
# # create_token('666666'.encode(), 1)

# db.session.add(Admin('99999', 'admin', '123456', 'cs'))
# db.session.commit()
# # create_token('99999'.encode(), 2)

# db.session.add(Course('1', '0001', 'se', '666666', '0', '70', '1:1,2', '2', '2020.6.25', 'yq', 'cs', '2', '1', '0'))
# db.session.commit()

# db.session.add(Course('2', '0002', 'sb', '666666', '0', '70', '2:3,4,5', '3', '2020.6.25', 'zjg', 'cs', '3', '1', '0'))
# db.session.commit()

# db.session.add(Choose('1', '3170105470', '666666'))
# db.session.commit()

# db.session.add(Choose('2', '3170105470', '666666'))
# db.session.commit()

# db.session.add(CultivationPlan('1', '3170105470', '666666'))
# db.session.commit()

# db.session.add(CultivationPlan('2', '3170105470', '666666'))
# db.session.commit()








@app.route('/user/current', methods=['GET'])
def getUserInfo():
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	student_info = db.session.query(Student.username, Student.major).filter(Student.id == student_id).all()
	result = user_info_schema.jsonify(student_info[0])
	print(student_info[0])
	return result

@app.route('/courses/enrolled', methods=['GET'])
def getSelectedCourse():
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	all_choose = Choose.query.filter(Choose.student_id == student_id).all()
	# all_course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time).filter(lambda i: Course.id == i.id, all_choose).all()
	all_course = []
	for i in range(len(all_choose)):
		course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time).filter(Course.id == all_choose[i].id).all()
		all_course.append(course[0])
	result = chosens_course_schema.jsonify(all_course)
	return result


@app.route('/courses/major', methods=['GET'])
def getMajorCourse():
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	student_major = db.session.query(Student.major).filter(Student.id == student_id)
	all_course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time).filter(Course.major == student_major).all()
	result = chosens_course_schema.jsonify(all_course)
	return result

@app.route('/user/courses', methods=['GET'])
def getAllCourse():
	token = request.headers['token']
	if token in token_to_username:
		user_id = token_to_username[token]
	else:
		return str(404)
	if (Student.query.filter(Student.id == user_id).all() != []):
		all_plan = CultivationPlan.query.filter(CultivationPlan.student_id == user_id).all()
		all_choose = Choose.query.filter(Choose.student_id == user_id).all()
		all_choose_id = []
		for i in range(len(all_choose)):
			all_choose_id.append(all_choose[i].id)
		all_course = []
		for i in range(len(all_plan)):
			course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time, (Course.chosen_true if (Course.id in all_choose_id) else Course.chosen_false).label('chosen')).filter(Course.id == all_plan[i].id).all()
			all_course.append(course[0])
		result = chosens_state_schema.jsonify(all_course)
	elif (Teacher.query.filter(Teacher.id == user_id).all() != []):
		all_choose = Choose.query.filter(Choose.teacher_id == user_id).all()
		all_course = []
		for i in range(len(all_choose)):
			course = db.session.query(Course.id, Course.serial_no, Course.course_name, Course.course_position, Course.course_time, Course.course_exam_time, Course.capacity, Course.used).filter(Course.id == all_choose[i].id).all()
			all_course.append(course[0])
		result = students_chosen_schema.jsonify(all_course)
	return result

@app.route('/courses/<cid>/list', methods=['GET'])
def getStudentTeacherListGet(cid):
	token = request.headers['token']
	if token in token_to_username:
		teacher_id = token_to_username[token]
	else:
		return str(404)
	all_choose = Choose.query.filter(Choose.teacher_id == teacher_id and cid == Choose.id).all()
	all_student = []
	for i in range(len(all_choose)):
		student = db.session.query(Student.id, Student.username, Student.sex, Student.major, Student.phone).filter(Student.id == all_choose[i].student_id).all()
		if student[0] not in all_student:
			all_student.append(student[0])
	result = students_teacher_schema.jsonify(all_student)
	return result



# ################################################
# ######             POST Methods
# ###############################################

@app.route('/login', methods=['POST'])
def userLogin(id, password):
	student_id_list = Student.query.all()[0].id
	teacher_id_list = Teacher.query.all()[0].id
	admin_id_list = Admin.query.all()[0].id
	data = request.get_json()
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
			token = sha256encode(data['id'])
			username_to_token[data['id']] = token
			token_to_username[token] = data['id']
			result = login_success_schema.jsonify((True, "Login Success", token, 0))
		else:
			result = login_fail_schema.jsonify((False, "Invalid username or password"))
	if (role == 1):
		correct_password = Teacher.query.filter(Teacher.id == id)
		if (correct_password == password):
			token = sha256encode(data['id'])
			username_to_token[data['id']] = token
			token_to_username[token] = data['id']
			result = login_success_schema.jsonify((True, "Login Success", token, 1))
		else:
			result = login_fail_schema.jsonify((False, "Invalid username or password"))
	if (role == 2):
		correct_password = Admin.query.filter(Admin.id == id)
		if (correct_password == password):
			token = sha256encode(data['id'])
			username_to_token[data['id']] = token
			token_to_username[token] = data['id']
			result = login_success_schema.jsonify((True, "Login Success", token, 2))
		else:
			result = login_fail_schema.jsonify((False, "Invalid username or password"))
	return result

@app.route('/logout', methods=['POST'])
def userLogout():
	token = request.headers['token']
	if token in token_to_username:
		username = token_to_username[token]
		del token_to_username[token]
		del username_to_token[username]
	else:
		return str(404)
	result = logout_schema.jsonify((True, "Logout Success"))
	return result

@app.route('/user/scheme', methods=['POST'])
def cultivatePlan():
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	choose_list = request.json['classes']
	for choose in choose_list:
		# don't know whether can write like this
		course = Course.query.get(Course.serial_no == choose)
		choose_id = course.id
		choose_student = student_id
		choose_teacher = course.teacher_id
		new_choose = CultivationPlan(choose_id, choose_student, choose_teacher)
		db.session.merge(new_choose)

	db.session.commit()

	result = update_cultivation_plan_schema.jsonify((True, "Update training scheme success"))
	return result

@app.route('/user/courses', methods=['POST'])
def addCourse():
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	courses_list = request.json['courses']
	for course_serial_no in courses_list:
		course = Course.query.get(Course.serial_no == course_serial_no)

		# Unknown whether it's correct
		course.used += 1

		choose_id = course.id
		choose_student = student_id
		choose_teacher = course.teacher_id
		new_choose = Choose(choose_id, choose_student, choose_teacher)
		db.session.merge(new_choose)

	db.session.commit()

	return str(204)

@app.route('/courses/:cid/list', methods=['POST'])
def getStudentTeacherListPost():
	token = request.headers['token']
	if token in token_to_username:
		admin_id = token_to_username[token]
	else:
		return str(404)
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

	return str(200)

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
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	courses_list = request.json['courses']
	for course_serial_no in courses_list:
		course = Course.query.get(Course.serial_no == course_serial_no)
		
		# Unknown whether it's correct
		course.used -= 1

		delete_course = Choose.query.get(Choose.id == course.id)
		db.session.delete(delete_course)
	db.session.commit()
	return str(204)

@app.route('/courses/:cid/list', methods=['DELETE'])
def deleteCourseList():
	token = request.headers['token']
	if token in token_to_username:
		amin_id = token_to_username[token]
	else:
		return str(404)
	student_list = request.json['id']
	for student_id in student_list:
		course = Course.query.get(Course.id == cid)
		
		# Unknown whether it's correct
		course.used -= 1

		delete_course = Choose.query.get(Choose.id == course.id and Choose.student_id == student_id)
		db.session.delete(delete_choose)
	db.session.commit()
	return str(200)

# Run server
if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='192.168.1.105', debug=True)
