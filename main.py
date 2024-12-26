import logging
from flask import Flask, flash, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.DEBUG)

items = ['Fernando Alonso', 'Lewis Hamilton', 'Sebastian Vettel', 'Kimi Raikkonen']

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "CLAVE SEGURA"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bd_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db = SQLAlchemy(app)
    logging.info("Conexión a la base de datos establecida correctamente")
except OperationalError as e:
    db = None
    logging.error(f"Error de conexion a la base de datos: {e.orig}")

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

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/information', methods=['GET', 'POST'])
def information():
    user_ip_information = session.get('user_ip_information')
    username = session.get('username')

    if not user_ip_information:
        user_ip_information = request.remote_addr
        session['user_ip_information'] = user_ip_information
        flash('No se ha encontrado ninguna cookie. Creando una nueva.')
        return redirect('/information')
    else:
        flash(f'Seesion encontrada. IP: {user_ip_information}, Username: {username}')

    login_form = LoginForm()

    if db is None:
        flash('No se ha podido conectar a la base de datos')
        return render_template('error.html')

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        # Comprobar si el usuario existe y si la contraseña es correcta
        if user:
            if user.password and check_password_hash(user.password, password):
                session['username'] = username
                flash('Has iniciat sessio correctament')
                return redirect('/information')
            else:
                flash('Contrasenya incorrecta')
        else:
            flash('No s\'ha trobat cap usuari')

    # Preparar el contexto con los datos
    context = {
        'ip': user_ip_information,
        'items': items,
        'login_form': login_form,
        'username': username
    }

    # Renderizar la plantilla con el contexto
    return render_template('information.html', **context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = generate_password_hash(register_form.password.data)
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado correctamente')
            return redirect('/information')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al registrar el usuario: {e}")
            flash('Error al registrar el usuario')
    
    return render_template('register.html', form=register_form)

if __name__ == '__main__':
    if db is not None:
        with app.app_context():
            try:
                db.create_all()
            except OperationalError as e:
                logging.error(f"Error creando las tablas: {e.orig}")

    # Ejecutar la aplicación
    app.run(host='0.0.0.0', port=91, debug=True)