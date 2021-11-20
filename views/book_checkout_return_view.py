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
    book_img = '../.' + book.book_img

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


# 반납 페이지 => 반납해야 하는 책들의 목록을 보여준다.
@bp.route('/bookReturn/<nickname>')
def bookReturn(nickname):
  user_id = session.get('login')
  user = User.query.filter(User.user_id==user_id).first()

  # html파일에 넘겨줄 데이터를 담을 리스트
  returned_list = []
  # 반납하지 못한 책들의 정보를 가져옴
  returned_books = Book_borrow_return.query.filter(Book_borrow_return.user_id==user_id, Book_borrow_return.returned_date=='no').all()

  for returned_book in returned_books:
    # 반납이 필요한 책 정보들를 저장한다.
    book_name = returned_book.book_name
    borrow_date = returned_book.borrow_date
    return_date = returned_book.return_date
    book_count = returned_book.book_count
    book_id = returned_book.id

    # 이미지 불러오기
    book = Book_list.query.filter(Book_list.book_name==book_name).first()
    book_img = '../.' + book.book_img
    
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
    
    returned_list.append([book_img, book_name, book_count, book_ratings, borrow_date, return_date, book_id])

  return render_template('returnBook.html', returned_list=returned_list, nickname=nickname, user=user)


# 반납하기 버튼을 눌렀을때 post요청을 받는 라우트
@bp.route('/returnBook/<id>', methods=["POST"])
def returnBook(id):
  book = Book_borrow_return.query.filter(Book_borrow_return.id==id).first()
  user = User.query.filter(User.user_id==book.user_id).first()
  # 대여 관련 테이블의 return_date의 값을 원래의 borrow_date의 2주뒤로 설정되어있는 것에서
  # 현재 날짜로 바꿔주고 returned_date 값을 'yes'로 바꿔준다.
  now = date.today()
  book.return_date = now
  book.returned_date = 'yes'
  db.session.commit()

  # Book_remain테이블의 book_remain 속성의 값을 반납한 개수만큼 다시 늘려준다.
  book_remain = Book_remain.query.filter(Book_remain.book_name==book.book_name).first()
  book_remain.book_remain += book.book_count
  db.session.commit()

  return redirect(url_for('checkout_return.bookReturn', nickname=user.nickname))
