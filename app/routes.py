import os
import csv
import shutil
from flask import render_template,redirect,flash,url_for,request
from app import app
from flask_login import login_required
from app.models import Students
from flask_login import current_user,login_user
from werkzeug.urls  import url_parse
from app import db
from app.forms import RegistrationForm,UploadFile,LoginForm
from app.models import Faculty
from flask_login import logout_user
from werkzeug.utils import secure_filename


@app.route('/uploadfile',methods=['GET','POST'])
@login_required
def uploadfile():
	form = UploadFile()
	if form.validate_on_submit():
		print(1)
		file=form.upload_file.data
		file_name=secure_filename(file.filename)
		if file is None:
			flash("No file selected")
			return redirect(uploadfile)
		else:
			print(2)
			directory = os.path.join(app.config['FILE_LOCATION'])
			csv_dir = os.path.join(directory, 'csv_files')
			os.makedirs(csv_dir, exist_ok=True)
			file.save(os.path.join(csv_dir, file_name))
			for filename in os.listdir(csv_dir):
				if filename.endswith('.csv'):
					filepath = os.path.join(csv_dir, filename)
					with open(filepath) as file:
						reader = csv.DictReader(file)
						for row in reader:
							data = Students(
       			            usn=row['usn'],
       			            name=row['name'],
       			            age=row['age'],
       			            address=row['address'],
       			            phone=row['phone'],
       			            email=row['email'],
       			            yoa =row['yoa'], 
       			            specialization = row['specialization'],
       			            semester = row['semester'],
       			            section=row['section'],
       			            )
						db.session.add(data)
						db.session.commit()
						os.makedirs(os.path.join(directory, 'processed_csv_files'), exist_ok=True)
						shutil.move(filepath, os.path.join(directory, 'processed_csv_files', filename))
						flash(f'Data has been imported successfully from {filename}. CSV files moved to processed_csv_files directory.')
						return redirect(url_for('index'))
	return render_template('uploadfile.html',title='Upload File',form=form)


@app.route('/student',methods=('GET','POST'))
@login_required
def student():
	if request.method == 'POST':
		student_req=request.form['view']
		if current_user.is_authenticated:
			students_data=Students.query.filter_by(usn=f"{student_req}").first()
			return render_template('student_view.html',student_data=students_data)
		return redirect(url_for('login'))
	return render_template('student_view.html')


@app.route('/index',methods=('GET','POST'))
@login_required
def index():
	specialization_query=Students.query.group_by(Students.specialization)
	semester_query=Students.query.group_by(Students.semester)
	yoa_query=Students.query.group_by(Students.yoa)
	section_query=Students.query.group_by(Students.section)
	if request.method=='POST':
		spec_req=request.form['filterSpec']
		sem_req=request.form['filterSem']
		yoa_req=request.form['filterYOA']
		sec_req=request.form['filterSec']
		print_req=request.form['print_data']
		if spec_req and sem_req and yoa_req and sec_req:
			table_query= Students.query.filter_by(specialization=f'{spec_req}' , semester=f'{sem_req}', yoa=f'{yoa_req}', section=f'{sec_req}')
		elif spec_req and sem_req and yoa_req and not sec_req:
			table_query= Students.query.filter_by(specialization=f'{spec_req}' , semester=f'{sem_req}', yoa=f'{yoa_req}')
		elif spec_req and sem_req and not yoa_req and sec_req:
			table_query=Students.query.filter_by(specialization=f'{spec_req}' , semester=f'{sem_req}', section=f'{sec_req}')
		elif spec_req and sem_req and not yoa_req and not sec_req:
			table_query=Students.query.filter_by(specialization=f'{spec_req}' , yoa=f'{yoa_req}')
		elif spec_req and not sem_req and yoa_req and sec_req:
			table_query=Students.query.filter_by(specialization=f'{spec_req}', yoa=f'{yoa_req}', section=f'{sec_req}')
		elif spec_req and not sem_req and yoa_req and not sec_req:
			table_query= Students.query.filter_by(specialization=f'{spec_req}' , yoa=f'{yoa_req}')
		elif spec_req and not sem_req and not yoa_req and sec_req:
			table_query=Students.query.filter_by(specialization=f'{spec_req}', section=f'{sec_req}')
		elif spec_req and not sem_req and not yoa_req and not sec_req:
			table_query=Students.query.filter_by(specialization=f'{spec_req}',)
		elif not spec_req and sem_req and yoa_req and sec_req:
			table_query=Students.query.filter_by(semester=f'{sem_req}', yoa=f'{yoa_req}', section=f'{sec_req}')
		elif not spec_req and sem_req and yoa_req and not sec_req:
			table_query=Students.query.filter_by(semester=f'{sem_req}', yoa=f'{yoa_req}')
		elif not spec_req and sem_req and not yoa_req and sec_req:
			table_query=Students.query.filter_by(semester=f'{sem_req}', section=f'{sec_req}')
		elif not spec_req and sem_req and not yoa_req and not sec_req:
			table_query=Students.query.filter_by(semester=f'{sem_req}',)
		elif not spec_req and not sem_req and yoa_req and sec_req:
			table_query=Students.query.filter_by(yoa=f'{yoa_req}', section=f'{sec_req}')
		elif not spec_req and not sem_req and yoa_req and not sec_req:
			table_query=Students.query.filter_by(yoa=f'{yoa_req}',)
		elif not spec_req and not sem_req and not yoa_req and sec_req:
			table_query=Students.query.filter_by(section=f'{sec_req}')
		elif not spec_req and not sem_req and not yoa_req and not sec_req:
			table_query=Students.query
		if print_req=='yes':
			return render_template('printView.html',table_query=table_query)
		return render_template('filterView.html',table_query=table_query,specialization_query=specialization_query,semester_query=semester_query,yoa_query=yoa_query,section_query=section_query)
	return render_template('index.html',specialization_query=specialization_query,semester_query=semester_query,yoa_query=yoa_query,section_query=section_query)

@app.route('/api/data')
def data():
	query= Students.query	
    # search filter 
	search = request.args.get('search')
	print(f'{search}')
	if search:
		query = query.filter(db.or_(
            Students.usn.like(f'%{search}%'),
            Students.name.like(f'%{search}%'),
        ))
	total = query.count()

    # sorting
	sort = request.args.get('sort')
	if sort:
		order = []
		for s in sort.split(','):
			direction = s[0]
			name = s[1:]
			if name not in  ['usn','name','specialization','semester','yoa','section']:
				name = 'name'
			col = getattr(Students, name)
			if direction == '-':
				col = col.desc()
			order.append(col)
		if order:
			query = query.order_by(*order)

    # pagination
	start = request.args.get('start', type=int, default=-1)
	length = request.args.get('length', type=int, default=-1)
	if start != -1 and length != -1:
		query = query.offset(start).limit(length)

    # response
	return {
        'data': [user.to_dict() for user in query],
        'total': total,
    }

@app.route('/login',methods=('GET','POST'))
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		faculty_user = Faculty.query.filter_by(username=form.username.data).first()
		if faculty_user is None or not faculty_user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(faculty_user, remember=form.remember_me.data)
		next_page= request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		faculty_user = Faculty(username=form.username.data, email=form.email.data)
		faculty_user.set_password(form.password.data)
		db.session.add(faculty_user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/')
def home():
	return render_template('home.html')
