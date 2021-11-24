from flask import Blueprint, render_template, session, request, redirect, url_for
from models import *

bp = Blueprint('book',__name__, url_prefix='/book')

# 책 상세 페이지
@bp.route('/<id>')
def info(id):
  # 로그인이 되어있는 상태라면 로그인된 user의 정보를 전달해 주어야
  # bookinfo.html에서 리뷰 입력창이 열린다.
  user_id = session.get('login')
  user = User.query.filter(User.user_id==user_id).first()

  # 해당 id값의 책 정보 가져오기
  book_infos = Book_list.query.filter(Book_list.id==id).first()
  
  # 해당 책의 리뷰 목록 가져오기
  # id의 내림차순으로 가져온다. 즉 최신 리뷰목록을 우선으로 보여준다.
  reviews = Review.query.filter(Review.book_name==book_infos.book_name).order_by(Review.id.desc()).all()

  return render_template('bookinfo2.html', book_infos=book_infos, reviews=reviews, user=user, id=id)


# 리뷰 작성 라우트
@bp.route('/review/<id>', methods=["POST"])
def review(id):
  user_id = session.get('login')
  book = Book_list.query.filter(Book_list.id==id).first()
  user = User.query.filter(User.user_id==user_id).first()

  review_context = request.form['review_context']
  rating = request.form.getlist('rating')
  rating = int(rating.pop())

  review = Review(user.user_id, book.book_name, book.author, book.isbn, rating, review_context, user.nickname)
  db.session.add(review)
  db.session.commit()
  return redirect(url_for('book.info', id=id))
