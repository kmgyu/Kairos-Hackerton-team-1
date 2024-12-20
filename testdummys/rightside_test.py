from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

class Stats:
    def __init__(self, Strength=0, Dexterity=0, Defense=0):
        self.Strength = Strength
        self.Dexterity = Dexterity
        self.Defense = Defense

    def __str__(self):
        return f"Strength: {self.Strength}, Dexterity: {self.Dexterity}, Defense: {self.Defense}"

class Items:
    def __init__(self, name="", quantity=0):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"Name: {self.name}, Quantity: {self.quantity}"

class Character:
    def __init__(self, name="", job="", stats=None, points=0, items=None):
        self.name = name
        self.job = job
        self.stats = stats if stats else Stats()
        self.points = points
        self.items = items if items else Items()

    def __str__(self):
        return (f"Character Name: {self.name}\n"
                f"Job: {self.job}\n"
                f"Stats: {self.stats}\n"
                f"Points: {self.points}\n"
                f"Items: {self.items}")




# 글로벌 변수로 캐릭터 객체
current_character = None


@app.route('/')
def index():
    global current_character

    # 처음 방문 시 캐릭터 객체가 없으면 초기화
    if not current_character:
        current_character = Character(
            name="Hero",
            job="Warrior",
            stats=Stats(Strength=5, Dexterity=3, Defense=2),
            points=5,
            items=Items(name="Sword", quantity=1)
        )
    
    return render_template('right-sidebar/start_right.html', character=current_character)


@app.route('/update_stats', methods=['POST'])
def update_stats():
    global current_character
    data = request.get_json()
    stat = data['stat']
    amount = data['amount']

    # 잔여 포인트가 0이면 더 이상 스탯을 증가시킬 수 없음
    if current_character.points <= 0 and amount > 0:
        return jsonify({"message": "No points remaining to allocate."}), 400

    # 스탯 업데이트
    if stat == "Strength":
        if current_character.stats.Strength + amount >= 0:  # Strength가 음수가 되지 않도록
            current_character.stats.Strength += amount
        else:
            return jsonify({"message": "Strength cannot be negative."}), 400
    elif stat == "Dexterity":
        if current_character.stats.Dexterity + amount >= 0:  # Dexterity가 음수가 되지 않도록
            current_character.stats.Dexterity += amount
        else:
            return jsonify({"message": "Dexterity cannot be negative."}), 400
    elif stat == "Defense":
        if current_character.stats.Defense + amount >= 0:  # Defense가 음수가 되지 않도록
            current_character.stats.Defense += amount
        else:
            return jsonify({"message": "Defense cannot be negative."}), 400

    # 포인트 업데이트
    current_character.points -= amount

    # 업데이트된 캐릭터 반환
    return jsonify({
        'stats': current_character.stats.__dict__,
        'points': current_character.points
    })



@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    global current_character
    
    # 캐릭터 초기화
    current_character = Character(
        name="Hero",
        job="Warrior",
        stats=Stats(Strength=5, Dexterity=3, Defense=2),
        points=5,
        items=Items(name="Sword", quantity=1)
    )
    
    # 초기화된 캐릭터 정보 반환
    return jsonify({
        'name': current_character.name,
        'job': current_character.job,
        'stats': current_character.stats.__dict__,
        'points': current_character.points
    })


@app.route('/confirm_character', methods=['POST'])
def confirm_character():
    global current_character  # 현재 캐릭터 객체 사용

    # 만약 current_character가 None이라면 초기화
    if not current_character:
        current_character = Character(
            name="Hero",  # 기본 이름
            job="Warrior",  # 기본 직업
            stats=Stats(Strength=5, Dexterity=3, Defense=2),  # 기본 스탯
            points=5,  # 기본 포인트
            items=Items(name="Sword", quantity=1)  # 기본 아이템
        )
    
    # 클라이언트에서 받은 데이터
    data = request.json
    name = data.get("name", current_character.name)  # 이름을 갱신 (없으면 기존 값 사용)
    job = data.get("job", current_character.job)  # 직업을 갱신 (없으면 기존 값 사용)
    
    # 캐릭터 객체 업데이트
    current_character.name = name
    current_character.job = job
    
    print(f"Character confirmed: {current_character}, {type(current_character)}")
    return jsonify({
        "message": "Character confirmed successfully.",
        "character": {
            "name": current_character.name,
            "job": current_character.job,
            "stats": vars(current_character.stats),
            "points": current_character.points,
            "items": vars(current_character.items)
        }
    })

@app.route('/ingame_right')
def ingame_right():
    return render_template('right-sidebar/ingame_right.html', character=current_character)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
