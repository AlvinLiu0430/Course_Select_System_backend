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

def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    ''' 
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=3600)
    token = s.dumps({"id":api_user}).decode("ascii")
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
    student = Student.query.get(data["id"])
    return student

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

print("sikgbfsibvbiyusw")

class Student(db.Model):
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
        fields = {'id', 'username', 'password', 'major'}

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
        fields = {'id', 'couse_name', 'teacher_id', 'course_position', 'course_time', 'course_exam_time'}

# init schemas
course_schema = CourseSchema()

student_schema = StudentSchema()

teacher_schema = TeacherSchema()

admin_schema = AdminSchema()

cultivation_schema = CultivationPlanSchema()

choose_schema = ChooseSchema()


chosen_course_schema = ChosenCourseSchema()
chosens_course_schema = ChosenCourseSchema(many=True)

# ################################################
# ######
# ######            API END POINTS
# ######
# ################################################

# ################################################
# ######             GET Methods
# ###############################################

@app.route('/course/enrolled', methods=['GET'])
def getSelectedCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    all_choose = Choose.query.filter(Choose.student_id == student.id).all()
    all_course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time).filter(Course.id in all_choose.id).all()
    result = chosens_course_schema.jsonify(all_course)
    return result


@app.route('/course/major', methods=['GET'])
def getMajorCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    all_course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time).filter(Course.major == student.major).all()
    result = chosens_course_schema.jsonify(all_course)
    return result

@app.route('/user/courses', methods=['GET'])
def GetAllCourse():
    token = request.headers["z-token"]
    student = verify_token(token)
    all_course = db.session.query(Course.serial_no, Course.course_name, Course.teacher_id, Course.course_position, Course.course_time, Course.course_exam_time).all()
    result = chosens_course_schema.jsonify(all_course)
    return result



# ################################################
# ######             POST Methods
# ###############################################

@app.route('/user/program', methods=['POST'])
def CultivatePlan():
    token = request.headers["z-token"]
    student = verify_token(token)
    choose_list = request.json['classes']
    for choose in choose_list:
        course = Course.query.get(Course.serial_no = choose)
        choose_id = course.id
        choose_student = student.id
        choose_teacher = course.teacher_id
        new_choose = CultivationPlan(choose_id, choose_student, choose_teacher)
        db.session.merge(new_choose)
    
    db.session.commit()

    return 200

@app.route('/user/courses/<serial_no>', methods=['POST'])
def CultivatePlan():
    token = request.headers["z-token"]
    student = verify_token(token)
    course = Course.query.get(serial_no)
    course_id = course.id
    course_student = student.id
    course_teacher = course.teacher_id
    new_course = Choose(course_id, student_id, course_teacher)
    db.session.add(new_course)
    
    db.session.commit()

    return 200
	
# ################################################
# ######             PUT Methods
# ###############################################
	


# ################################################
# ######             DELETE Methods
# ###############################################
	

# Run server
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.1.105', debug=True)
