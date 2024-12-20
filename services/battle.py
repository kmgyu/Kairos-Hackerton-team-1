import random

class CombatMechanics:
    def __init__(self, stat, max_value=5, mechanic_type="attack"):
        self.stat = stat
        self.max_value = max_value
        self.mechanic_type = mechanic_type

    def _pre_check(self):
        chance = 50 + self.stat * 10
        rand_value = random.randint(1, 100)
        return rand_value <= chance, rand_value

    def perform(self):
        hit, rand_value = self._pre_check()

        if not hit:
            return 0

        value = self.stat + self._calculate_dice()

        if self.stat >= 6:
            value += (self.stat - 5)

        if rand_value == 1:
            value = self.max_value
        elif rand_value == 100:
            value = self.stat + self._calculate_dice()

        return value

    def _calculate_dice(self):
        return random.randint(1, self.stat)

class Avoidance:
    def __init__(self, agility, defense):
        self.agility = agility
        self.defense = defense

    def attempt_evade(self):
        random_value = random.randint(1, 100)
        avoidance_threshold = self.agility * 10

        if random_value <= avoidance_threshold:
            return "회피 성공!", 0

        damage = random.randint(1, 100)
        if damage == 1:
            recovery = self.defense
            return f"회피 성공! 특별 이벤트: 체력이 {recovery}만큼 회복되었습니다.", -recovery
        elif damage == 100:
            critical_damage = 2 * damage
            return f"회피 실패! 특별 이벤트: 치명타 발생! {critical_damage}의 데미지를 입었습니다.", critical_damage
        else:
            return f"회피 실패! {damage}의 데미지를 입었습니다.", damage

class Monster:
    def __init__(self, atk_stat, def_stat, agi_stat):
        self.atk_stat = atk_stat
        self.def_stat = def_stat
        self.agi_stat = agi_stat
        self.hp = def_stat * 5
        self.attack_instance = CombatMechanics(atk_stat, max_value=5, mechanic_type="attack")
        self.defense_instance = CombatMechanics(def_stat, max_value=5, mechanic_type="defense")

    def attack(self):
        return self.attack_instance.perform()

    def defend(self, damage):
        defense_value = self.defense_instance.perform()
        net_damage = max(damage - defense_value, 0)
        self.hp -= net_damage
        self.hp = max(self.hp, 0)
        return net_damage

class Player:
    def __init__(self, atk_stat, def_stat, agi_stat):
        if not (0 <= atk_stat <= 5 and 0 <= def_stat <= 5 and 0 <= agi_stat <= 5):
            raise ValueError("스탯 값은 0에서 5 사이여야 합니다.")

        self.atk_stat = atk_stat
        self.def_stat = def_stat
        self.agi_stat = agi_stat
        self.hp = def_stat * 5
        self.items = {}
        self.attack_instance = CombatMechanics(atk_stat, max_value=5, mechanic_type="attack")
        self.defense_instance = CombatMechanics(def_stat, max_value=5, mechanic_type="defense")
        self.avoidance_instance = Avoidance(agi_stat, def_stat)

    def dice(self):
        return random.randint(1, 100)

    def attack(self):
        return self.attack_instance.perform()

    def defend(self):
        return self.defense_instance.perform()

    def avoid(self):
        result, change = self.avoidance_instance.attempt_evade()
        self.hp += change
        self.hp = max(self.hp, 0)
        return result

    def take_damage(self, monster_attack):
        player_defense = self.defend()
        net_damage = max(monster_attack - player_defense, 0)
        self.hp -= net_damage
        self.hp = max(self.hp, 0)
        return net_damage

    def add_item(self, item_id, item_name):
        if item_id in self.items:
            return f"아이템 번호 {item_id}는 이미 존재합니다."
        self.items[item_id] = item_name
        return f"아이템 {item_name} (번호: {item_id})이(가) 추가되었습니다."

    def Item_search(self):
        if not self.items:
            return "착용 중인 아이템이 없습니다."
        return "착용 중인 아이템:\n" + "\n".join([f"{item_id}: {item_name}" for item_id, item_name in self.items.items()])

    def Item_delete(self, item_id):
        if item_id in self.items:
            removed_item = self.items.pop(item_id)
            return f"아이템 {removed_item} (번호: {item_id})이(가) 제거되었습니다."
        return f"아이템 번호 {item_id}는 존재하지 않습니다."