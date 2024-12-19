from flask import Flask, flash, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
items=['Fernando Alonso', 'Lewis Hamilton', 'Sebastian Vettel', 'Kimi Raikkonen']

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"]="CLAVE SEGURA"


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bd_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __str__(self):
        return self.username

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/index')
def index():
    
    user_ip_information = request.remote_addr
    response = make_response(redirect('/show_information'))
    session['user_ip_information'] = user_ip_information 

    return response

@app.route('/show_information', methods=['GET', 'POST'])
def show_information():
    
    user_ip_information = session.get('user_ip_information')

    username = session.get('username')

    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Has iniciat sessio correctament')
        return make_response(redirect('/index'))

    context = {
        'ip': user_ip_information,
        'items': items,
        'login_form': login_form,
        'username': username
    }
    
    return render_template('information.html', **context)

if __name__ == '__main__':

    with app.app_context():
        db.create_all()


    app.run(host='0.0.0.0', port=91, debug=True)