from flask import Flask, request, jsonify, render_template
import random

# 전투 클래스 정의 포함
from services.battle import * # 올바른 경로로 수정

app = Flask(__name__)

# 플레이어와 몬스터 초기화
player = Player(atk_stat=3, def_stat=4, agi_stat=2)  # 플레이어의 초기 스탯
monster = Monster(atk_stat=3, def_stat=3, agi_stat=1)  # 몬스터의 초기 스탯

def get_battle_state():
    """현재 전투 상태 반환"""
    return {
        "player_hp": player.hp,
        "monster_hp": monster.hp,
        "log": []
    }

@app.route('/battle')
def battle():
    """전투 화면"""
    battle_state = get_battle_state()
    return render_template('battle.html', player=battle_state, monster=battle_state)

@app.route('/battle_action', methods=['POST'])
def battle_action():
    """플레이어의 행동 처리"""
    battle_state = get_battle_state()
    action = request.json.get("action")
    log_entry = ""

    if action == "attack":
        # 플레이어 공격
        player_attack = player.attack()
        damage_dealt = monster.defend(player_attack)
        log_entry = f"Player attacks for {player_attack}! Monster defends and takes {damage_dealt} damage."

    elif action == "defend":
        # 방어 동작 (몬스터의 공격을 방어)
        monster_attack = monster.attack()
        damage_taken = player.take_damage(monster_attack)
        log_entry = f"Player defends! Monster attacks for {monster_attack}, Player takes {damage_taken} damage."

    elif action == "avoid":
        # 회피 시도
        result = player.avoid()
        log_entry = f"Player attempts to avoid: {result}"

    elif action == "dice":
        # 주사위 사용
        dice_roll = player.dice()
        log_entry = f"Player rolls a dice and gets {dice_roll}."

    else:
        return jsonify({"error": "Invalid action"}), 400

    # 상태 업데이트
    battle_state["player_hp"] = player.hp
    battle_state["monster_hp"] = monster.hp
    battle_state["log"].append(log_entry)

    # 전투 종료 확인
    if battle_state["monster_hp"] <= 0:
        log_entry = "Monster is defeated! Player wins!"
        battle_state["log"].append(log_entry)
    elif battle_state["player_hp"] <= 0:
        log_entry = "Player is defeated! Game over!"
        battle_state["log"].append(log_entry)

    return jsonify({
        "player_hp": battle_state["player_hp"],
        "monster_hp": battle_state["monster_hp"],
        "log": log_entry
    })

if __name__ == '__main__':
    app.run(debug=True)
