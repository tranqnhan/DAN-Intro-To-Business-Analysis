from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Item

home = Blueprint('home', __name__)

@home.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)
