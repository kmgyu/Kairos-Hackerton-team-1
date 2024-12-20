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

@app.route('/battle_test')
def battle():
    """전투 화면"""
    battle_state = get_battle_state()
    return render_template('battle_test.html', player=battle_state, monster=battle_state)

@app.route('/battle_action', methods=['POST'])
def battle_action():
    data = request.json
    action = data.get('action')

    player = Player(atk_stat=3, def_stat=3, agi_stat=3)
    monster = Monster(atk_stat=2, def_stat=2, agi_stat=2)

    if action == 'attack':
        player_damage = player.attack()
        monster_damage = monster.defend(player_damage)
        log = f"플레이어가 {player_damage}로 공격, 몬스터는 {monster_damage} 피해를 입었습니다."
    elif action == 'defend':
        player.defend()
        log = "플레이어가 방어했습니다."
    elif action == 'avoid':
        result = player.avoid()
        log = f"플레이어가 회피 시도: {result}"
    elif action == 'dice':
        dice_roll = player.dice()
        log = f"플레이어가 주사위를 굴려 {dice_roll}이 나왔습니다."
    else:
        log = "알 수 없는 액션입니다."

    return jsonify({
        'player_hp': player.hp,
        'monster_hp': monster.hp,
        'log': log
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
