from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

class Stats:
    def __init__(self, Strength=0, Dexterity=0, Defense=0):
        self.Strength = Strength
        self.Dexterity = Dexterity
        self.Defense = Defense


class Items:
    def __init__(self, name="", quantity=0):
        self.name = name
        self.quantity = quantity


class Character:
    def __init__(self, stats=Stats(), items=Items(), name="", job="", points=10):
        self.name = name
        self.job = job
        self.stats = stats
        self.points = points
        self.items = items



# 메인 페이지
@app.route('/')
def index():
    character = Character(name="Hero", job="Warrior", stats=Stats(Strength=5, Dexterity=3, Defense=2), points=5, items=Items(name="Sword", quantity=1))
    return render_template('/right-sidebar/start_right.html', character=character)

# @app.route('/ingame_right')
# def ingame_right():
#     # user_id = session.get('user_id')
#     # if not user_id:
#     #     return jsonify({"message": "User not logged in"}), 400

#     # cursor = mysql.get_db().cursor()
#     # cursor.execute("SELECT * FROM characters WHERE user_id = %s", (user_id,))
#     # character_data = cursor.fetchone()

#     # if not character_data:
#     #     return jsonify({"message": "Character not found"}), 404

#     # # 아이템 정보 가져오기 (예시로 2개의 아이템)
#     # cursor.execute("SELECT name, quantity FROM inventory WHERE user_id = %s", (user_id,))
#     # items_data = cursor.fetchall()

#     # # 데이터 포맷팅
#     # character = {
#     #     "name": character_data[1],
#     #     "job": character_data[2],
#     #     "stats": {
#     #         "Strength": character_data[3],
#     #         "Dexterity": character_data[4],
#     #         "Defense": character_data[5]
#     #     },
#     #     "points": character_data[6],
#     #     "items": [{"name": item[0], "quantity": item[1]} for item in items_data]
#     # }

#     return render_template('ingame_right.html', character=Character)


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


@app.route('/update_stats', methods=['POST'])
def update_stats():
    data = request.json
    stat = data.get("stat")  # 수정할 스탯 이름 (e.g., "Strength")
    amount = data.get("amount")  # 변경 값 (e.g., +1, -1)

    if stat in Character.stats:
        # 포인트 배분 로직
        if amount == 1 and Character.points > 0:  # 포인트를 추가
            setattr(Character.stats, stat, getattr(Character.stats, stat) + 1)
            Character.points -= 1
        elif amount == -1 and getattr(Character.stats, stat) > 0:  # 포인트를 회수
            setattr(Character.stats, stat, getattr(Character.stats, stat) - 1)
            Character.points += 1

    return jsonify({
        "stats": Character.stats.__dict__,
        "points": Character.points
    })

@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    global Character
    # 초기 캐릭터 상태로 복원
    Character = Character.__class__()  # `Character` 객체를 다시 생성하여 초기 상태로 되돌리기
    return jsonify({
        "stats": {
            "Strength": Character.stats.Strength,
            "Dexterity": Character.stats.Dexterity,
            "Defense": Character.stats.Defense
        },
        "points": Character.points,
        "name": Character.name,
        "job": Character.job
    })

@app.route('/confirm_character', methods=['POST'])
def confirm_character():
    global Character
    data = request.json
    Character["name"] = data.get("name", Character["name"])
    Character["job"] = data.get("job", Character["job"])
    return jsonify({"message": "Character updated successfully!", "character": Character})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

# 기능 기준으로 템플릿 이름 