from flask import Flask, render_template, request, jsonify, redirect, url_for

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
    
current_character = Character(
            name="Hero",
            job="Warrior",
            stats=Stats(Strength=5, Dexterity=3, Defense=2),
            points=5,
            items=Items(name="Sword", quantity=1)
        )

@app.route('/api/current-quest')
def current_quest():
    # 처리 로직
    return jsonify({"quest": "Current Quest Data"})

@app.route('/api/recent-events')
def recent_events():
    # 처리 로직
    return jsonify({"events": "Recent Event Data"})

@app.route('/api/completed-quests')
def completed_quests():
    # 처리 로직
    return jsonify({"quests": "Completed Quest Data"})

@app.route('/update_stats', methods=['POST'])
def update_stats():
    data = request.get_json()  # 클라이언트에서 보내온 JSON 데이터 파싱
    stat = data.get('stat')  # 업데이트할 스탯
    amount = data.get('amount')  # 증가 또는 감소 값

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
    # 변경된 스탯 반환
    return jsonify({
        'stats': {
            'Strength': current_character.stats.Strength,
            'Dexterity': current_character.stats.Dexterity,
            'Defense': current_character.stats.Defense
        },
        'points': current_character.points
    })
    
@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    # 초기 스탯으로 리셋
    current_character.stats = Stats(Strength=10, Dexterity=10, Defense=10)
    current_character.points = 10
    current_character.name = ""
    current_character.job = ""

    return jsonify({
        'stats': {
            'Strength': current_character.stats.Strength,
            'Dexterity': current_character.stats.Dexterity,
            'Defense': current_character.stats.Defense
        },
        'points': current_character.points,
        'name': current_character.name,
        'job': current_character.job
    })

@app.route('/confirm_character', methods=['POST'])
def confirm_character():
    data = request.get_json()  # 클라이언트에서 보낸 데이터
    name = data.get('name')
    job = data.get('job')
    stats = data.get('stats')  # 예: {'Strength': 5, 'Dexterity': 3, 'Defense': 2}

    # 캐릭터 정보 저장
    current_character.name = name
    current_character.job = job
    current_character.stats.Strength = stats.get('Strength', 0)
    current_character.stats.Dexterity = stats.get('Dexterity', 0)
    current_character.stats.Defense = stats.get('Defense', 0)

    # URL 파라미터로 전달할 데이터 생성
    return redirect(url_for('ingame_ui', 
                            name=name, 
                            job=job, 
                            Strength=current_character.stats.Strength,
                            Dexterity=current_character.stats.Dexterity,
                            Defense=current_character.stats.Defense))


@app.route('/ingame_ui')
def ingame_ui():
    # URL 파라미터에서 값 가져오기
    current_character = Character(
            name = request.args.get('name'),
            job = request.args.get('job'),
            stats=Stats(Strength = request.args.get('Strength', type=int),  Dexterity = request.args.get('Dexterity', type=int), Defense = request.args.get('Defense', type=int)),
            items=Items(name="Sword", quantity=1)
        )

    # 게임 UI 페이지 렌더링
    return render_template('intergration/ingame_ui.html', character=current_character)


@app.route('/')
def index():
    branch = int(request.args.get('branch', 0))  # branch 값이 없으면 기본값 0
    scripts = ['first',
               'second',
               'third',
               '4',
               '5']
    return render_template('intergration/gamestart.html', character=current_character, script=scripts[branch])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
