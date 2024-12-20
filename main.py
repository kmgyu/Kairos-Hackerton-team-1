from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import dotenv
import os
from models import db, bcrypt
from login import login_bp

dotenv.load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login.login'  # Blueprint에서 정의된 'login' 함수로 연결

# Blueprint 등록
app.register_blueprint(login_bp)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    models.db.create_all()  # 데이터베이스 테이블 생성 (필요시)
    app.run(host='0.0.0.0', port=3000)