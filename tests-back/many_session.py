from flask import Flask, session, request, jsonify
from flask_session import Session

app = Flask(__name__)

# Flask 세션 설정
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'  # 파일 시스템을 세션 저장소로 사용
Session(app)

# 기본 캐릭터 정보
DEFAULT_CHARACTER = {
    "name": "Unknown Adventurer",
    "level": 1,
    "hp": 100,
    "mp": 50,
    "inventory": []
}

@app.route('/create_character', methods=['POST'])
def create_character():
    """캐릭터 생성"""
    character_name = request.json.get('name', 'Unknown Adventurer')
    session['character'] = DEFAULT_CHARACTER.copy()  # 기본 캐릭터 복사
    session['character']['name'] = character_name
    return jsonify({"message": f"Character '{character_name}' created!", "character": session['character']}), 201

@app.route('/get_character', methods=['GET'])
def get_character():
    """현재 세션의 캐릭터 정보 조회"""
    if 'character' not in session:
        return jsonify({"error": "No character found in session. Please create one first."}), 404
    return jsonify(session['character'])

@app.route('/update_character', methods=['PATCH'])
def update_character():
    """캐릭터 정보 업데이트"""
    if 'character' not in session:
        return jsonify({"error": "No character found in session. Please create one first."}), 404

    updates = request.json  # 업데이트 내용 (예: {"hp": 80})
    character = session['character']

    for key, value in updates.items():
        if key in character:
            character[key] = value

    session['character'] = character
    return jsonify({"message": "Character updated successfully!", "character": character})

@app.route('/delete_character', methods=['DELETE'])
def delete_character():
    """캐릭터 삭제"""
    if 'character' in session:
        del session['character']
        return jsonify({"message": "Character deleted successfully!"}), 200
    return jsonify({"error": "No character found in session to delete."}), 404

@app.route('/')
def index():
    """간단한 메인 페이지"""
    return """
    <h1>Welcome to TRPG Web Game</h1>
    <p>Use the API to create and manage your character!</p>
    """

if __name__ == '__main__':
    app.run(debug=True)
