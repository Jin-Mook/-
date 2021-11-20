from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import url_for
from models import *
from datetime import date, timedelta

bp = Blueprint('checkout_return', __name__, url_prefix='/userInfo')

# 책 대여 관련 페이지
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
    returned_date = 'no'
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
    bookRemain = Book_borrow_return(user_id, book_name, author, borrow_date, return_date, value, returned_date)
    db.session.add(bookRemain)
    db.session.commit()

    return redirect(url_for('main.main'))


# 대여기록 페이지 => 반납완료된 책들만 나오는 페이지
@bp.route('/checkoutRecord/<nickname>')
def checkoutRecord(nickname):
  user_id = session.get('login')
  user = User.query.filter(User.user_id==user_id).first()
  # 데이터를 모아서 전달할 리스트 작성
  checkout_list = []
  
  checkout_books = Book_borrow_return.query.filter(Book_borrow_return.user_id==user_id, Book_borrow_return.returned_date=='yes').all()
  for checkout_book in checkout_books:
    book_name = checkout_book.book_name
    borrow_date = checkout_book.borrow_date
    return_date = checkout_book.return_date
    book_count = checkout_book.book_count

    # 이미지 정보 가져오기
    book = Book_list.query.filter(Book_list.book_name==book_name).first()
    book_img = '.' + book.book_img

    # book rating 정보 가져오기 및 평균 계산하기
    reviews = Review.query.filter(Review.book_name==book_name).all()

    total_rating = 0
    for book in reviews:
        total_rating += book.rating
    
    # 리뷰의 개수가 0인 경우
    if len(reviews) == 0:
        book_ratings = total_rating
    # 리뷰의 개수가 0이 아닌 경우
    else:
        book_ratings = total_rating / len(reviews)
    
    # checkout_list에 추가하기
    checkout_list.append([book_img, book_name, book_count, book_ratings, borrow_date, return_date])

  return render_template('checkoutRecord.html', checkout_list=checkout_list, nickname=nickname, user=user)