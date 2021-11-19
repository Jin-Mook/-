from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import backref
db = SQLAlchemy()

# User 유저 정보에 관한 테이블
class User(db.Model):
  __tablename__ = "User"

  id                    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  user_id               = db.Column(db.String(30), nullable=False)
  user_pw               = db.Column(db.Text, nullable=False)
  nickname              = db.Column(db.String(30), nullable=False, unique=True)

  user1 = db.relationship("Book_borrow_return", backref='User')
  user2 = db.relationship("Review", backref='User')

  def __init__(self, user_id, user_pw, nickname):
    self.user_id = user_id
    self.user_pw = user_pw
    self.nickname = nickname


# Book_list 책의 종류에 대한 테이블
class Book_list(db.Model):
  __tablename__ = "Book_list"

  id                    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  book_name             = db.Column(db.String(30), primary_key=True ,nullable=False)
  publisher             = db.Column(db.String(30), nullable=False)
  author                = db.Column(db.String(50), nullable=False)
  publication_date      = db.Column(db.Date, nullable=False)
  pages                 = db.Column(db.Integer, nullable=False)
  isbn                  = db.Column(db.Integer, nullable=False)
  description           = db.Column(db.Text, nullable=False)
  link                  = db.Column(db.Text, nullable=False)
  book_img              = db.Column(db.String(10), nullable=False)

  book_list1 = db.relationship("Book_borrow_return", backref='Book_list')
  book_list2 = db.relationship("Book_remain", backref='Book_list')
  book_list3 = db.relationship("Review", backref='Book_list')

  def __init__(self, book_name, publisher, author, publication_date, pages, isbn, description, link, book_img):
    self.book_name = book_name
    self.publisher = publisher
    self.author = author
    self.publication_date = publication_date
    self.pages = pages
    self.isbn = isbn
    self.description = description
    self.link = link
    self.book_img = book_img


# Book_borrow_return 대여 반납과 관련된 테이블
class Book_borrow_return(db.Model):
  __tablename__ = 'Book_borrow_return'

  id                    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  user_id               = db.Column(db.String(30), db.ForeignKey(User.user_id), nullable=False)
  book_name             = db.Column(db.String(30), db.ForeignKey(Book_list.book_name), nullable=False)
  author                = db.Column(db.String(50), nullable=False)
  borrow_date           = db.Column(db.Date, nullable=False)
  return_date           = db.Column(db.Date, nullable=False)
  book_count            = db.Column(db.Integer, nullable=False)

  def __init__(self, user_id, book_name, author, borrow_date, return_date, book_count):
    self.user_id = user_id
    self.book_name = book_name
    self.author = author
    self.borrow_date = borrow_date
    self.return_date = return_date
    self.book_count = book_count


# Book_remain 대여 후 남은 책과 관련된 테이블
class Book_remain(db.Model):
  __tablename__ = "Book_remain"

  id                    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  book_name             = db.Column(db.String(30), db.ForeignKey(Book_list.book_name), nullable=False)
  book_remain           = db.Column(db.Integer, nullable=False, default=10)

  def __init__(self, book_name, book_remain):
    self.book_name = book_name
    self.book_remain = book_remain


# Review 책 리뷰와 관련된 테이블
class Review(db.Model):
  __tablename__ = "Review"

  id                    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  user_id               = db.Column(db.String(30), db.ForeignKey(User.user_id), nullable=False)
  book_name             = db.Column(db.String(30), db.ForeignKey(Book_list.book_name), nullable=False)
  author                = db.Column(db.String(50), nullable=False)
  isbn                  = db.Column(db.Integer)
  rating                = db.Column(db.Integer, default=0)
  review_context        = db.Column(db.Text)
  nickname              = db.Column(db.String(30), nullable=False)

  def __init__(self, user_id, book_name, author, isbn, rating, review_context, nickname):
    self.user_id = user_id
    self.book_name = book_name
    self.author = author
    self.isbn = isbn
    self.rating = rating
    self.review_context = review_context
    self.nickname = nickname