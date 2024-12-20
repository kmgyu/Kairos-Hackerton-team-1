from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# 캐릭터 초기 데이터
Character = {
    "Strength": 10,
    "Dexterity": 8,
    "Defense": 12,
    "HP": 100,
    "Level": 1
}

# 레벨업 처리
@app.route('/level_up', methods=['POST'])
def level_up():
    Character["Level"] += 1
    Character["Strength"] += 2
    Character["Dexterity"] += 1
    Character["Defense"] += 1
    return jsonify(Character)

# 공격 처리
@app.route('/take_damage', methods=['POST'])
def take_damage():
    damage = request.json.get("damage", 0)
    Character["HP"] -= damage
    if Character["HP"] < 0:
        Character["HP"] = 0
    return jsonify(Character)

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html', character=Character)

if __name__ == '__main__':
    app.run(debug=True)
