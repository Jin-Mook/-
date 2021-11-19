from flask import Blueprint, render_template, redirect, request
from models import *

bp = Blueprint('checkout_return', __name__, url_prefix='/userInfo')

@bp.route('/checkout/<id>', methods=["GET", "POST"])
def checkout(id):
  if request.method == "GET":
    book_info = Book_list.query.filter(Book_list.id==id).first()
    # book의 정보를 가지고 Book_remain에서 남은 책의 정보를 가져온다.
    book_name = book_info.book_name
    book_remain = Book_remain.query.filter(Book_remain.book_name==book_name).first()

    book_remain = book_remain.book_remain

    return render_template('checkout.html', book_name=book_name, book_remain=book_remain, id_value=id)
  else:
    return "성공했습니다"