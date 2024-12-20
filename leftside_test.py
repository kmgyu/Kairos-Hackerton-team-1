from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import models
import dotenv
import os
# import pymysql

# pymysql.install_as_MySQLdb()
dotenv.load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')

app = Flask(__name__)

# db = SQLAlchemy(app)
# SQLite 데이터베이스 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)

# 외래 키 제약 활성화
@app.before_request
def before_request():
    models.db.session.execute(text('PRAGMA foreign_keys = ON'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/left-test')
def leftsidetest():
    return render_template('left-sidebar/record.html')

@app.route('/api/recent-events')
def get_recent_events():# 세션 테이블에서 데이터 가져오기
    # print(models.db.engine)  # 테이블 목록 출력

    sessions = models.Sessions.query.all()


    # if not sessions:
    #     print("No sessions found in the database.")

    # play_records 형식으로 변환
    play_records = [
        {
            "situation": session.Situation,
            "choices": session.Choices,
            "result": session.Result
        }
        for session in sessions
    ]
    
    return jsonify(play_records)


"""
@app.route('/api/completed-quests')
def get_completed_quests():
    completed_quests = [
        {
            "title": "The Bandit Camp",
            "summary": "You cleared the bandit camp and rescued the villagers."
        },
        {
            "title": "Mystic Cave",
            "summary": "You explored the Mystic Cave and recovered the ancient artifact."
        },
        {
            "title": "Mystic Cave",
            "summary": "You explored the Mystic Cave and recovered the ancient artifact."
        },
        {
            "title": "Mystic Cave",
            "summary": "You explored the Mystic Cave and recovered the ancient artifact."
        },
        {
            "title": "Mystic Cave",
            "summary": "You explored the Mystic Cave and recovered the ancient artifact."
        }
    ]
    return jsonify(completed_quests)

@app.route('/api/current-quest')
def get_current_quest():
    current_quest = {
        "title": "The Dragon's Lair",
        "description": "You are tasked with slaying the dragon threatening the village.",
        "progress": 45
    }
    return jsonify(current_quest)
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

# 기능 기준으로 템플릿 이름 