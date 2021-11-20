from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from models import db, User, Book_list, Book_borrow_return, Book_remain, Review
from flask_bcrypt import Bcrypt
import pymysql
pymysql.install_as_MySQLdb()

bp = Blueprint('main', __name__, url_prefix='/')
bcrypt = Bcrypt()

# 메인 페이지 => 책의 목록과 로그인 페이지 회원가입 페이지로 갈 수 있는 링크가 있다.
@bp.route('/')
def main():
    # 데이터로 넘겨줄 정보를 담을 리스트
    book_info = []

    book_infos = Book_list.query.all()

    for data in book_infos:
        book_id = data.id
        book_title = data.book_name
        book_img = data.book_img
        # 책 제목에 해당하는 Review테이블의 rating 속성의 값들을 가져와서 평균을 내주어야한다.
        # 책 제목에 해당하는 Book_remain 테이블의 book_remain 속성의 값을 가져와야 한다.
        # book_ratings = Review.query.filter(Review.book_name==book_title).all()
        # 지금은 평점을 3으로 통일하겠다.
        reviews = Review.query.filter(Review.book_name==book_title).all()
        total_rating = 0
        for book in reviews:
            total_rating += book.rating
        
        # 리뷰의 개수가 0인 경우
        if len(reviews) == 0:
            book_ratings = total_rating
        # 리뷰의 개수가 0이 아닌 경우
        else:
            book_ratings = total_rating / len(reviews)

        # 남아있는 책도 10권으로일단 통일
        book_remain = Book_remain.query.filter(Book_remain.book_name==book_title).first()
        book_img = '.' + book_img
        book_info.append([book_img, book_title, book_ratings, book_remain.book_remain, book_id])
    

    # 로그인 된 상태라면 로그인된 유저의 정보 불러오기
    user_id = session.get('login')
    user = User.query.filter(User.user_id==user_id).first()

    return render_template('main.html', book_info=book_info, user=user)


# 회원가입 페이지
@bp.route('/regist', methods=["POST", "GET"])
def regist():
    if request.method == "GET":
        return render_template('regist.html')
    else:
        user_id = request.form['user_id']
        user_pw1 = request.form['user_pw1']
        user_pw2 = request.form['user_pw2']
        nickname = request.form['nickname']

        # 아이디 이메일 형식으로 받는 기능은 후에 추가하자
        # 비밀번호 최소 10자리 영문, 숫자, 특수문자 중 2 종류 이상 조합
        # 혹은 최소 8자리 이상 영문, 숫자, 특수문자 조합이 가능하게 만들기도 후에 추가

        # 비밀번호가 같지 않은 경우
        if user_pw1 != user_pw2:
            flash('비밀번호를 확인하세요')
            return render_template('regist.html')
        
        # user_id 가 동일한 경우
        user = User.query.filter(User.user_id==user_id).first()
        if user != None:
            flash('이미 존재하는 아이디 입니다.')
            return render_template('regist.html')

        # 비밀번호 암호화 하기
        password = bcrypt.generate_password_hash(user_pw1)
        user = User(user_id, password, nickname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.main'))


# 로그인 페이지
@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        user_id = request.form["user_id"]
        user_pw = request.form["user_pw"]

        # 입력받은 아이디가 User table에 없는 경우
        user = User.query.filter(User.user_id==user_id).first()
        if user == None:
            flash('없는 아이디 입니다.')
            return render_template('login.html')
        # 입력받은 아이디가 있는 경우
        else:
            # 비밀번호가 일치하는 경우
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['login'] = user_id
                session['nickname'] = user.nickname
                return redirect('/')
            # 비밀번호가 일치하지 않는 경우
            else:
                flash('비밀번호가 일치하지 않습니다.')
                return render_template('login.html')


# 로그아웃 페이지
@bp.route('/logout')
def logout():
    session['login'] = None
    session['nickname'] = None
    return redirect('/')
