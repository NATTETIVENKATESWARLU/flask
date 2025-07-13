from flask import Flask, render_template, request, redirect, url_for, flash
#---------------------------------------------------------------------------------
# this class based form handling is not used in this example
#pip install Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#---------------------------------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#pip install Flask-SQLAlchemy

#****************************************************************************************************
app = Flask(__name__)
#add your database URI here
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Example for SQLite
#----------------------------------------------------------------------------------
# Example for mySQL, PostgreSQL, or other databases

#pip install pymysql
#pip install psycopg2-binary  # For PostgreSQL
#pip install mysqlclient  # For MySQL
#pip install mysql-connector-python  # For MySQL
#pip install sqlalchemy  # SQLAlchemy is required for Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/mydata'  # Example for MySQL

#----------------------------------------------------------------------------------
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save resources
app.config['SECRET_KEY']="mykey"
db= SQLAlchemy(app)
#---------------------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

#****************************************************************************************************
#basic route to display a welcome message
@app.route('/')
def index():
    return "<h1>Welcome to Flask</h1>"

#---------------------------------------------------------------------------------
#diplaying a user profile named 'username'
@app.route('/user/<username>')
def user_profile(username):
    return f"<h1>User Profile: {username}</h1>"
#---------------------------------------------------------------------------------

#rendering a template
@app.route('/hello')
def hello():
    return render_template('hello.html')
#---------------------------------------------------------------------------------
#jinja template with a variable

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)


@app.route('/data')
def mydata():
    data= {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    return render_template('data.html', data=data)
#---------------------------------------------------------------------------------
#custom error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
#---------------------------------------------------------------------------------
#bootstrap integration
#here we assume you have a 'base.html' template that includes Bootstrap
#and other common elements like a navigation bar url_for('static', filename='style.css')

#---------------------------------------------------------------------------------
#form handling example
@app.route('/userform', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('hello_name', name=name))
    else:
        return render_template('form.html')
#****************************************************************************************************
#class based form handling
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    #all the fields you want to add names
    #boolean field
    #date field
    #datetime field
    #file field
    #select field
    #radio field
    #text area field
    #password field
    #hidden field
    #submit field
    #multiple choice field
    #validators for the fields
    #custom validators
    #csrf token for security

#message flashing example
@app.route('/form_class', methods=['GET', 'POST'])
def form_class_example():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        flash(f'Form submitted successfully! Name: {name}', 'success')
        return redirect(url_for('hello_name', name=name))
    return render_template('form_class.html', form=form)
#---------------------------------------------------------------------------------
#database operations example
#user form handling
class UserFormDB(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.route('/userform_db', methods=['GET', 'POST'])
def user_form_db():
    form = UserFormDB()
    qurey = User.query.all()  # Fetch all users from the database
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return render_template('userform_db.html', form=form)

        # Check if username already exists (optional, if unique too)
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('userform_db.html', form=form)

        # If both checks pass, add new user
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')

        return redirect(url_for('hello_name', name=new_user.username,))

    return render_template('userform_db.html', form=form,  qurey= qurey)



if __name__ == '__main__':
    app.run(debug=True,)