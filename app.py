from flask import Flask
from views import main_view

app = Flask(__name__)
app.register_blueprint(main_view.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/elice-library'


if __name__ == '__main__':
  app.run(debug=True)