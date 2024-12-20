from flask import Flask, render_template, request, jsonify

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
    data = request.get_json()  # 클라이언트에서 보낸 JSON 데이터 파싱
    name = data.get('name')
    job = data.get('job')
    strength = data.get('Strength')
    dexterity = data.get('Dexterity')
    defense = data.get('Defense')

    # 데이터 처리 (예: 캐릭터 정보 저장)
    current_character.name = name
    current_character.job = job
    current_character.stats.Strength = strength
    current_character.stats.Dexterity = dexterity
    current_character.stats.Defense = defense

    # 처리 후 결과를 JSON 형식으로 반환
    return jsonify({
        'status': 'Character confirmed',
        'name': current_character.name,
        'job': current_character.job,
        'stats': {
            'Strength': current_character.stats.Strength,
            'Dexterity': current_character.stats.Dexterity,
            'Defense': current_character.stats.Defense
        }
    })


@app.route('/printf', methods=['POST'])
def printf():
    # 요청에서 JSON 데이터 받기
    data = request.get_json()
    
    # 데이터가 없으면 400 오류 반환
    if not data or 'user_input' not in data:
        return jsonify({'message': 'No user input provided'}), 400

    user_input = data['user_input']
    
    # 받은 값을 콘솔에 출력
    print(f'User input: {user_input}')
    
    # 응답 반환
    return jsonify({'message': 'Success', 'input_received': user_input})

@app.route('/ingame_ui', methods=['GET'])
def ingame_ui():
    branch = int(request.args.get('branch', 0))  # branch 값이 없으면 기본값 0
    scripts = ['first',
               'second',
               'third',
               '4',
               '5',
               '6',
               '7']
    # current_character는 이미 서버에서 데이터를 처리하고 있어 따로 파라미터를 받지 않습니다.
    return render_template('intergration/ingame_ui.html', character=current_character, script=scripts[branch])

@app.route('/game_ending')
def game_ending():
    character = current_character  # 이미 생성된 캐릭터 객체
    play_summary = {
        'title': 'Your Adventure Title',
        'description': 'A detailed description of your adventure.',
        'progress': '50%'  # 예시로 50% 진행 중
    }
    ending_scripts = ['The final battle begins...', 'You have completed your quest.']  # 예시 스크립트
    play_log = ['Started the journey.', 'Defeated the dragon.', 'Found a hidden treasure.']  # 예시 로그

    return render_template('intergration/game_ending.html', character=character, play_summary=play_summary, ending_scripts=ending_scripts, play_log=play_log)

@app.route('/')
def index():
    
    return render_template('intergration/gamestart.html', character=current_character)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
