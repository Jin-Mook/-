from flask import Blueprint, render_template
from models import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main():
    return render_template('main.html')