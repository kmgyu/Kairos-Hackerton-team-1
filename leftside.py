from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    playrecord = {
        '2024-07-21':"이거이거함"
    }
    
    return render_template('/index.html')

@app.route('/left-test')
def leftsidetest():
    return render_template('/left-sidebar/record.html')

@app.route('/api/recent-events')
def get_recent_events():
    play_records = [
        {
            "situation": "You encountered a fork in the road.",
            "choices": "Left path (forest), Right path (mountain)",
            "result": "Chose the forest path, encountered a group of bandits."
        },
        {
            "situation": "You met an old merchant.",
            "choices": "Buy supplies, Ignore",
            "result": "Bought supplies and received a treasure map."
        }
    ]
    return jsonify(play_records)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

# 기능 기준으로 템플릿 이름 