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


def isTimeAvailable(start, end):
	start_time = datetime.datetime.strptime(start, "%Y-%m-%d")
	end_time = datetime.datetime.strptime(end, "%Y-%m-%d")
	current_time = datetime.datetime.now()
	if (start_time <= current_time and current_time <= end_time):
		return True
	else:
		return False

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
	student_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('student.id', ondelete='CASCADE'), primary_key=True)
	teacher_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('teacher.id', ondelete='CASCADE'))

	# Constructor
	def __init__(self, id, student_id, teacher_id):
		self.id = id
		self.student_id = student_id
		self.teacher_id = teacher_id

class Choose(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False,  primary_key=True)
	student_id = db.Column(BIGINT(20, unsigned=True), db.ForeignKey('student.id', ondelete='CASCADE'), primary_key=True)
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


class Schedule(db.Model):
	id = db.Column(BIGINT(20, unsigned=True), nullable=False, primary_key=True)
	operation_type = db.Column(VARCHAR(64), nullable=False)
	start_time = db.Column(VARCHAR(64), nullable=False)
	end_time = db.Column(VARCHAR(64), nullable=False)

	def __init__(self, id, operation_type, start_time, end_time):
		self.id = id
		self.operation_type = operation_type
		self.start_time = start_time
		self.end_time = end_time

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
		fields = ('id', 'serial_no', 'course_name', 'teacher_id', 'used', 'capacity', 'course_time', 'course_length', 'course_exam_time', 'course_position', 'major', 'credit', 'chosen_true', 'chosen_false')

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
		fields = ('code', 'name', 'teacher', 'position', 'class_time', 'exam_time')
    
class ChosenStateSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('code', 'name', 'teacher', 'position', 'class_time', 'exam_time', 'chosen')

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
		fields = ('id', 'code', 'name', 'position', 'class_time', 'exam_time', 'cap', 'used')

class StudentTeacherSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'username', 'sex', 'major', 'phone')

class ScheduleSchema(ma.Schema):
	class Meta:
		orderd = True
		fields = ('id', 'operation_type', 'start_time', 'end_time')

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

schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)


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
		course = db.session.query(Course.serial_no.label('code'), Course.course_name.label('name'), Course.teacher_id.label('teacher'), Course.course_position.label('position'), Course.course_time.label('class_time'), Course.course_exam_time.label('exam_time')).filter(Course.id == all_choose[i].id).all()
		print(course)
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
			tmp = db.session.query(Course.id).filter(Course.id == all_plan[i].id).all()
			course = db.session.query(Course.serial_no.label('code'), Course.course_name.label('name'), Course.teacher_id.label('teacher'), Course.course_position.label('position'), Course.course_time.label('class_time'), Course.course_exam_time.label('exam_time'), (Course.chosen_true if (tmp[0].id in all_choose_id) else Course.chosen_false).label('chosen')).filter(Course.id == all_plan[i].id).all()
			all_course.append(course[0])
		result = chosens_state_schema.jsonify(all_course)
	elif (Teacher.query.filter(Teacher.id == user_id).all() != []):
		all_choose = Choose.query.filter(Choose.teacher_id == user_id).all()
		all_course = []
		for i in range(len(all_choose)):
			course = db.session.query(Course.id, Course.serial_no.label('code'), Course.course_name.label('name'), Course.course_position.label('position'), Course.course_time.label('class_time'), Course.course_exam_time.label('exam_time'), Course.capacity.label('cap'), Course.used).filter(Course.id == all_choose[i].id).all()
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

@app.route('/schedules', methods=['GET'])
def getScheduleInfo():
	token = request.headers['token']
	if token in token_to_username:
		admin_id = token_to_username[token]
	else:
		return str(404)
	data = request.get_json("schedules")
	id_list = data['id']
	all_schedule = []
	for schedule_id in id_list:
		schedule = db.session.query(Schedule.id, Schedule.operation_type, Schedule.start_time, Schedule.end_time).filter(Schedule.id == schedule_id).all()
		all_schedule.append(schedule[0])
	result = schedules_schema.jsonify(all_schedule)
	return result


# ################################################
# ######             POST Methods
# ###############################################

@app.route('/login', methods=['POST'])
def userLogin():
	student_id_list = []
	teacher_id_list = []
	admin_id_list = []
	student_list = Student.query.all()
	teacher_list = Teacher.query.all()
	admin_list = Admin.query.all()

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
	schedule_result = Schedule.query(Schedule.operation_type, Schedule.start_time, Schedule.end_time).filter(Schedule.operation_type == "培养方案制定").all()
	start = schedule_result[0].start_time
	end = schedule_result[0].end_time
	if (not isTimeAvailable(start, end)):
		return {'success': 'False', 'message': 'Not in the available set cultivation plan time!'}
	data = request.get_json("classes")
	# choose_list = request.form.get('classes')
	choose_list = data['classes']
	for choose in choose_list:
		# don't know whether can write like this
		course = db.session.query(Course.id, Course.teacher_id).filter(Course.serial_no == choose).all()
		choose_id = course[0].id
		choose_student = student_id
		choose_teacher = course[0].teacher_id
		new_choose = CultivationPlan(choose_id, choose_student, choose_teacher)
		db.session.merge(new_choose)

	db.session.commit()

	result = {'success': 'True', 'message': 'Update training scheme success'}
	return result

@app.route('/user/courses', methods=['POST'])
def addCourse():
	token = request.headers['token']
	if token in token_to_username:
		student_id = token_to_username[token]
	else:
		return str(404)
	schedule_result = Schedule.query(Schedule.operation_type, Schedule.start_time, Schedule.end_time).filter(Schedule.operation_type == "选课").all()
	start = schedule_result[0].start_time
	end = schedule_result[0].end_time
	if (not isTimeAvailable(start, end)):
		return str(204)
	data = request.get_json("courses")
	choose_list = data['courses']
	for choose_course in choose_list:
		course = db.session.query(Course.id, Course.teacher_id, Course.used).filter(Course.serial_no == choose_course).all()
		tmp = Course.query.get(course[0].id)
		tmp.used += 1
		choose_id = course[0].id
		choose_student = student_id
		choose_teacher = course[0].teacher_id
		new_choose = Choose(choose_id, choose_student, choose_teacher)
		db.session.merge(new_choose)

	db.session.commit()

	return str(200)

@app.route('/courses/<cid>/list', methods=['POST'])
def getStudentTeacherListPost(cid):
	token = request.headers['token']
	if token in token_to_username:
		admin_id = token_to_username[token]
	else:
		return str(404)
	data = request.get_json("id")
	student_id = data['id']
	course = db.session.query(Course.id, Course.serial_no, Course.teacher_id).filter(Course.serial_no == cid).all()

	tmp = Course.query.get(course[0].id)
	tmp.used += 1

	choose_id = cid
	choose_student = student_id
	choose_teacher = course[0].teacher_id
	new_choose = Choose(choose_id, choose_student, choose_teacher)
	db.session.merge(new_choose)

	db.session.commit()

	return str(200)

@app.route('/schedules', methods=['POST'])
def updateScheduleInfo():
	token = request.headers['token']
	if token in token_to_username:
		admin_id = token_to_username[token]
	else:
		return str(404)
	data = request.get_json("schedules")
	id_list = data['id']
	for schedule_id in id_list:
		schedule = db.session.query(Schedule.id, Schedule.operation_type, Schedule.start_time, Schedule.end_time).filter(Schedule.id == schedule_id).all()
		if (len(schedule) == 0):
			new_schedule = Schedule(data['id'], data['operation_type'], data['start_time'], data['end_time'])
			db.session.merge(new_schedule)
		else:
			tmp = Schedule.query.get(schedule_id)
			tmp.start_time = data['start_time']
			tmp.end_time = data['end_time']
		
	db.session.commit()
	return str(200)

	
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
	schedule_result = Schedule.query(Schedule.operation_type, Schedule.start_time, Schedule.end_time).filter(Schedule.operation_type == "退课").all()
	start = schedule_result[0].start_time
	end = schedule_result[0].end_time
	if (not isTimeAvailable(start, end)):
		return str(204)
	data = request.get_json("courses")
	courses_list = data['courses']
	for course_serial_no in courses_list:
		tmp = db.session.query(Course.id).filter(Course.serial_no == course_serial_no).all()
		
		course = Course.query.get(tmp[0].id)
		course.used -= 1

		delete_choose = Choose.query.get((course.id,student_id))
		db.session.delete(delete_choose)
	db.session.commit()
	return str(204)

@app.route('/courses/<cid>/list', methods=['DELETE'])
def deleteCourseList(cid):
	token = request.headers['token']
	if token in token_to_username:
		amin_id = token_to_username[token]
	else:
		return str(404)
	data = request.get_json("id")
	student_id = data['id']
	tmp = db.session.query(Course.id).filter(Course.serial_no == cid).all()
		
	course = Course.query.get(tmp[0].id)
	course.used -= 1

	delete_choose = Choose.query.get((course.id, student_id))
	db.session.delete(delete_choose)
	db.session.commit()
	return str(200)

@app.route('/schedules', methods=['DELETE'])
def deleteSchedule():
	token = request.headers['token']
	if token in token_to_username:
		admin_id = token_to_username[token]
	else:
		return str(404)
	data = request.get_json("ids")
	id_list = data['id']
	for schedule_id in id_list:
		delete_schedule = Schedule.query.get(schedule_id)
		db.session.delete(delete_schedule)
	db.session.commit()
	return str(200)

# Run server
if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='192.168.1.105', debug=True)
