from flask import render_template, url_for, redirect, flash, request
from flask_login import logout_user, login_user, current_user

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from ..email import mail_message


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_url = request.args.get('next')
            return redirect(next_url) if next_url else redirect(url_for('main.index'))
        else:
            flash('Login was unsuccessful. Kindly check on the email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email)
        user.set_password(password)
        mail_message("Welcome to Blog", "email/welcome_user", user.email, {"user":user})
        user.save()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/sign_up.html', title='Sign Up', form=form, current_user=current_user)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# @auth.route('/register',methods = ["GET","POST"])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = User(email = form.email.data, username = form.username.data,password = form.password.data)
#         db.session.add(user)
#         db.session.commit()

#         mail_message("Welcome to blog","email/welcome_user",user.email,user=user)

#         return redirect(url_for('auth.login')) form = RegistrationForm()
#         title = "New Account"
#     return render_template('auth/register.html',registration_form = form)