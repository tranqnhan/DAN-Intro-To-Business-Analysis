from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/')
def index():
    return render_template('index.html')

@user_profile.route('/profile')
@login_required
def profile():
    firstname = current_user.firstname
    lastname = current_user.lastname
    credits = current_user.credits
    return render_template('login/profile.html', firstname=firstname, lastname=lastname, credits=credits)