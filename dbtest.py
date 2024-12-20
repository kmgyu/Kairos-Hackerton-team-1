from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import dotenv
import models
import os

dotenv.load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI  # MariaDB URI 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)

# class Quest(db.Model):
#     __tablename__ = 'Quest'

#     QuestID = db.Column(db.String(5), primary_key=True, nullable=False)
#     Ntype = db.Column(db.String(20), nullable=True)
#     Script = db.Column(db.String(500), nullable=True)
#     ATK = db.Column(db.Integer, default=0)
#     DEF = db.Column(db.Integer, default=0)
#     AGI = db.Column(db.Integer, default=0)

#     __table_args__ = (
#         CheckConstraint('ATK BETWEEN 0 AND 5', name='check_atk'),
#         CheckConstraint('DEF BETWEEN 0 AND 5', name='check_def'),
#         CheckConstraint('AGI BETWEEN 0 AND 5', name='check_agi'),
#     )

#     def __repr__(self):
#         return f'<Quest {self.QuestID} - {self.Ntype}>'

if __name__ == '__main__':
    with app.app_context():
        models.db.create_all()  # 데이터베이스 테이블 생성 (필요시)

        # DB에서 데이터 조회하여 출력
        quests = models.Quest.query.all()
        if quests:
            for quest in quests:
                print(f'QuestID: {quest.QuestID}, Ntype: {quest.Ntype}, ATK: {quest.ATK}, DEF: {quest.DEF}, AGI: {quest.AGI}')
        else:
            print("No quests found in the database.")
