from flask import Flask
from models import db
from views import main_view


app = Flask(__name__)
app.register_blueprint(main_view.bp)
app.secret_key = 'secretttt'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/elice_library'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

if __name__ == '__main__':
  app.run(debug=True)