from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import url_for
from models import *
from datetime import date, timedelta

bp = Blueprint('checkout_return', __name__, url_prefix='/userInfo')

@bp.route('/checkout/<id>', methods=["GET", "POST"])
def checkout(id):
  book_info = Book_list.query.filter(Book_list.id==id).first()

  if request.method == "GET":
    # book의 정보를 가지고 Book_remain에서 남은 책의 정보를 가져온다.
    book_name = book_info.book_name
    book_remain = Book_remain.query.filter(Book_remain.book_name==book_name).first()

    book_remain = book_remain.book_remain

    return render_template('checkout.html', book_name=book_name, book_remain=book_remain, id_value=id)
  else:
    value = int(request.form['checkoutNum'])
    
    # 유저 아이디를 가져온다.
    user_id = session.get('login')
    # 책 정보와 날짜 정보를 가져온다
    book_name = book_info.book_name
    author = book_info.author
    borrow_date = date.today()
    return_date = borrow_date + timedelta(weeks=2)

    # Book_remain 테이블에서 해당 책의 book_remain을 value만큼 빼준다.
    book = Book_remain.query.filter(Book_remain.book_name==book_name).first()
    book.book_remain -= value
    db.session.commit()
    # Book_borrow_return 테이블에서 book_count 값을 value만큼 갖는 레이블을 추가해준다.
    bookRemain = Book_borrow_return(user_id, book_name, author, borrow_date, return_date, value)
    db.session.add(bookRemain)
    db.session.commit()

    return redirect(url_for('main.main'))