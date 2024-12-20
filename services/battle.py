import random

class CombatMechanics:
    def __init__(self, stat, max_value=5, mechanic_type="attack"):
        """
        CombatMechanics 클래스 초기화
        :param stat: 공격력 또는 방어력 스탯
        :param max_value: 최대값 (기본값 5)
        :param mechanic_type: 기능 타입 ("attack" 또는 "defense")
        """
        self.stat = stat  # 공격력 또는 방어력 스탯
        self.max_value = max_value  # 최대값
        self.mechanic_type = mechanic_type  # "attack" 또는 "defense"

    def _pre_check(self):
        """
        사전판정을 수행: (50 + 스탯 * 10) >= 랜덤값이면 적중.
        """
        chance = 50 + self.stat * 10
        rand_value = random.randint(1, 100)

        if rand_value <= chance:
            return True, rand_value
        else:
            return False, rand_value

    def perform(self):
        """
        공격 또는 방어 수행
        :return: 결과 메시지 또는 값
        """
        hit, rand_value = self._pre_check()

        if not hit:
            action = "공격" if self.mechanic_type == "attack" else "방어"
            return action

        # 기본 값 계산: 스탯 + 주사위 값
        value = self.stat + self._calculate_dice()

        # 오버스탯 처리 (스탯이 6 이상인 경우)
        if self.stat >= 6:
            value += (self.stat - 5)

        # 특수 이벤트 처리
        if rand_value == 1:
            value = self.max_value  # 최대값 적용
        elif rand_value == 100:
            value = self.stat + self._calculate_dice()  # 본인에게 추가 피해 또는 방어

        return value

    def _calculate_dice(self):
        """
        주사위 계산: 1d(스탯 기준 주사위)
        """
        return random.randint(1, self.stat)

class Avoidance:
    def __init__(self, agility, defense):
        """
        Avoidance 클래스 초기화
        :param agility: 민첩성 (0 ~ 5의 값)
        :param defense: 방어력
        """

        self.agility = agility
        self.defense = defense

    def attempt_evade(self):
        """
        회피를 시도하는 메서드.
        :return: 결과 문자열 및 계산된 값
        """
        random_value = random.randint(1, 100)
        avoidance_threshold = self.agility * 10

        if random_value <= avoidance_threshold:
            return "회피 성공!", 0  # 성공 시 데미지가 없음

        # 회피 실패 시 랜덤 데미지 계산
        damage = random.randint(1, 100)
        if damage == 1:
            recovery = self.defense  # 체력 회복 (방어력만큼)
            return f"회피 성공! 특별 이벤트: 체력이 {recovery}만큼 회복되었습니다.", -recovery
        elif damage == 100:
            critical_damage = 2 * damage  # 치명타
            return f"회피 실패! 특별 이벤트: 치명타 발생! {critical_damage}의 데미지를 입었습니다.", critical_damage
        else:
            return f"회피 실패! {damage}의 데미지를 입었습니다.", damage

class Monster:
    def __init__(self, atk_stat, def_stat, agi_stat):
        """
        Monster 클래스 초기화
        :param atk_stat: 몬스터 공격력
        :param def_stat: 몬스터 방어력
        :param agi_stat: 몬스터 민첩성
        """
        self.atk_stat = atk_stat
        self.def_stat = def_stat
        self.agi_stat = agi_stat
        self.hp = def_stat * 5  # 체력은 방어력 * 5

        # CombatMechanics 인스턴스 생성
        self.attack_instance = CombatMechanics(atk_stat, max_value=5, mechanic_type="attack")
        self.defense_instance = CombatMechanics(def_stat, max_value=5, mechanic_type="defense")

    def attack(self):
        """
        몬스터 공격 수행
        :return: 공격값
        """
        return self.attack_instance.perform()

    def defend(self, damage):
        """
        몬스터 방어 수행
        :param damage: 플레이어의 공격값
        :return: 방어 후 남은 체력
        """
        defense_value = self.defense_instance.perform()
        net_damage = max(damage - defense_value, 0)
        self.hp -= net_damage
        if self.hp < 0:
            self.hp = 0
        return net_damage

class Player:
    def __init__(self, atk_stat, def_stat, agi_stat):
        if not (0 <= atk_stat <= 5 and 0 <= def_stat <= 5 and 0 <= agi_stat <= 5):
            raise ValueError("스탯 값은 0에서 5 사이여야 합니다.")

        self.atk_stat = atk_stat
        self.def_stat = def_stat
        self.agi_stat = agi_stat
        self.hp = def_stat * 5  # 초기 체력은 방어력 * 5

        self.items = {}  # 착용한 아이템 목록 (아이템 번호: 아이템 이름)

        # CombatMechanics 인스턴스 초기화
        self.attack_instance = CombatMechanics(atk_stat, max_value=5, mechanic_type="attack")
        self.defense_instance = CombatMechanics(def_stat, max_value=5, mechanic_type="defense")
        self.avoidance_instance = Avoidance(agi_stat, def_stat)

    def dice(self):
        """
        1부터 100까지 랜덤 값을 반환하는 메서드.
        :return: 1~100 사이의 랜덤 값
        """
        return random.randint(1, 100)

    def attack(self):
        result = self.attack_instance.perform()
        print(result)
        return result

    def defend(self):
        result = self.defense_instance.perform()
        print(result)
        return result

    def avoid(self):
        result, change = self.avoidance_instance.attempt_evade()
        self.hp -= change
        if self.hp < 0:
            self.hp = 0
        print(result)
        return result

    def take_damage(self, monster_attack):
        """
        몬스터 공격으로 피해를 입는 메서드
        :param monster_attack: 몬스터의 공격값
        :return: 최종 피해값
        """
        player_defense = self.defend()
        net_damage = max(monster_attack - player_defense, 0)
        self.hp -= net_damage
        if self.hp < 0:
            self.hp = 0
        print(f"플레이어가 {net_damage}의 피해를 입었습니다. 남은 체력: {self.hp}")
        return net_damage

    def Item_use(self, item_id, effect_value):
        if item_id not in self.items:
            print(f"아이템 번호 {item_id}는 존재하지 않습니다.")
            return

        item_name = self.items[item_id]

        if item_name.endswith("P"):
            self.atk_stat = max(0, self.atk_stat + effect_value)
            self.def_stat = max(0, self.def_stat + effect_value)
            self.agi_stat = max(0, self.agi_stat + effect_value)
            print(f"{item_name} 사용: 스탯이 {effect_value}만큼 변경되었습니다!")
        elif item_name.endswith("B"):
            self.attack_instance.max_atk += effect_value
            self.defense_instance.max_def += effect_value
            print(f"{item_name} 사용: 데미지 및 방어에 {effect_value} 보너스가 적용되었습니다!")
        else:
            print(f"{item_name}은(는) 사용 가능한 아이템이 아닙니다.")

    def add_item(self, item_id, item_name):
        if item_id in self.items:
            print(f"아이템 번호 {item_id}는 이미 존재합니다.")
        else:
            self.items[item_id] = item_name
            print(f"아이템 {item_name} (번호: {item_id})이(가) 추가되었습니다.")

    def Item_search(self):
        if not self.items:
            return "착용 중인 아이템이 없습니다."
        return "착용 중인 아이템:\n" + "\n".join([f"{item_id}: {item_name}" for item_id, item_name in self.items.items()])

    def Item_delete(self, item_id):
        """
        아이템 제거
        :param item_id: 제거할 아이템의 번호
        """
        if item_id in self.items:
            removed_item = self.items.pop(item_id)
            print(f"아이템 {removed_item} (번호: {item_id})이(가) 제거되었습니다.")
        else:
            print(f"아이템 번호 {item_id}는 존재하지 않습니다.")
