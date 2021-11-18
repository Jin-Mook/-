from flask import Blueprint
from models import *

bp = Blueprint('book',__name__, url_prefix='/book')

@bp.route('/<id>')
def info(id):

  book = Book_list.query.filter(Book_list.id==id).first()
  print(book.isbn)
  user = User.query.all()
  print(user[0].user_pw)

  return id
