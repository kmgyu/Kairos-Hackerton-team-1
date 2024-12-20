from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://root:ScE1234**@orion.mokpo.ac.kr:8371/kairos'  # MariaDB URI 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Quest(db.Model):
    __tablename__ = 'Quest'

    QuestID = db.Column(db.String(5), primary_key=True, nullable=False)
    Ntype = db.Column(db.String(20), nullable=True)
    Script = db.Column(db.String(500), nullable=True)
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)

    __table_args__ = (
        CheckConstraint('ATK BETWEEN 0 AND 5', name='check_atk'),
        CheckConstraint('DEF BETWEEN 0 AND 5', name='check_def'),
        CheckConstraint('AGI BETWEEN 0 AND 5', name='check_agi'),
    )

    def __repr__(self):
        return f'<Quest {self.QuestID} - {self.Ntype}>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성 (필요시)
        
        # DB에서 데이터 조회하여 출력
        quests = Quest.query.all()
        for quest in quests:
            print(f'QuestID: {quest.QuestID}, Ntype: {quest.Ntype}, ATK: {quest.ATK}, DEF: {quest.DEF}, AGI: {quest.AGI}')
