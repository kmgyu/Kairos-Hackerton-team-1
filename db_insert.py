import os
import dotenv
from flask import Flask
from models import db, Item, Mob, PlayerCh, Quest, Scenario, ScenarioNode, Sessions, User
from datetime import datetime

dotenv.load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI  # MariaDB URI 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flask 애플리케이션 컨텍스트 설정
with app.app_context():
    # 데이터베이스 테이블 생성
    db.create_all()

    # 모든 테이블 초기화
    db.session.query(Item).delete()
    db.session.query(Mob).delete()
    db.session.query(PlayerCh).delete()
    db.session.query(Quest).delete()
    db.session.query(Scenario).delete()
    db.session.query(ScenarioNode).delete()
    db.session.query(Sessions).delete()
    db.session.query(User).delete()

    # 데이터 삽입 코드
    items = [
        Item(ItemID='IT001', ItName='철검', ATKP=0, DEFP=2, AGIP=1, ATKB=4, DEFB=2, AGIB=0),
        Item(ItemID='IT002', ItName='가죽 갑옷', ATKP=2, DEFP=1, AGIP=3, ATKB=1, DEFB=0, AGIB=2),
        Item(ItemID='IT003', ItName='마법 지팡이', ATKP=4, DEFP=0, AGIP=0, ATKB=1, DEFB=0, AGIB=2),
        Item(ItemID='IT004', ItName='용기의 방패', ATKP=0, DEFP=4, AGIP=4, ATKB=0, DEFB=0, AGIB=0),
        Item(ItemID='IT005', ItName='엘프의 부츠', ATKP=0, DEFP=2, AGIP=1, ATKB=3, DEFB=2, AGIB=4)
    ]

    mobs = [
        Mob(MoName='Dragon', NameKo='드래곤', ATK=5, DEF=5, AGI=4),
        Mob(MoName='Goblin', NameKo='고블린', ATK=2, DEF=1, AGI=1),
        Mob(MoName='Orc', NameKo='오크', ATK=4, DEF=3, AGI=2),
        Mob(MoName='Skeleton', NameKo='스켈레톤', ATK=3, DEF=4, AGI=2),
        Mob(MoName='Troll', NameKo='트롤', ATK=4, DEF=4, AGI=3)
    ]

    players = [
        PlayerCh(CharID='user1220143', Username='user1', PCName='캐릭터11', ATK=13, DEF=2, AGI=6,
                 INV1='IT003', INV2='IT004', INV3='IT003', INV4='IT004', INV5='IT005', AM1='IT002', AM2='IT005', AM3='IT005'),
        PlayerCh(CharID='user264002', Username='user2', PCName='캐릭터55', ATK=8, DEF=3, AGI=7,
                 INV1='IT002', INV2='IT001', INV3='IT005', INV4='IT003', INV5='IT002', AM1='IT004', AM2='IT002', AM3='IT005'),
        PlayerCh(CharID='user3955275', Username='user3', PCName='캐릭터34', ATK=13, DEF=3, AGI=0,
                 INV1='IT001', INV2='IT005', INV3='IT003', INV4='IT004', INV5='IT001', AM1='IT003', AM2='IT004', AM3='IT002'),
        PlayerCh(CharID='user4539436', Username='user4', PCName='캐릭터30', ATK=13, DEF=6, AGI=4,
                 INV1='IT001', INV2='IT004', INV3='IT001', INV4='IT004', INV5='IT001', AM1='IT004', AM2='IT001', AM3='IT003'),
        PlayerCh(CharID='user54389', Username='user5', PCName='캐릭터17', ATK=13, DEF=8, AGI=4,
                 INV1='IT002', INV2='IT004', INV3='IT002', INV4='IT002', INV5='IT002', AM1='IT004', AM2='IT002', AM3='IT005')
    ]

    quests = [
        Quest(QuestID='Q001', Ntype='IT001', Script='철검을 획득하였습니다! 철검을 사용하여 고블린을 처치하세요.', ATK=0, DEF=2, AGI=1),
        Quest(QuestID='Q002', Ntype='Goblin', Script='고블린이 나타났습니다! 싸워서 보상을 얻으세요.', ATK=2, DEF=1, AGI=1),
        Quest(QuestID='Q003', Ntype='0', Script='마을 사람들이 도와줄 사람을 찾고 있습니다. 마을의 노인과 대화하세요.', ATK=1, DEF=2, AGI=3),
        Quest(QuestID='Q004', Ntype='Dragon', Script='강력한 드래곤이 길을 막고 있습니다. 싸울 준비를 하세요!', ATK=5, DEF=5, AGI=4),
        Quest(QuestID='Q005', Ntype='IT003', Script='마법 지팡이를 찾아 부상당한 마법사를 치료하세요.', ATK=4, DEF=0, AGI=0)
    ]

    scenarios = [
        Scenario(SceID=1, Title='잃어버린 도시', Descript='고대의 문명을 찾아 떠나는 여정. 미지의 위험이 도사린다.'),
        Scenario(SceID=2, Title='어둠의 계약', Descript='마을 주민들이 연이어 실종되며, 불길한 그림자가 드리운다.'),
        Scenario(SceID=3, Title='황혼의 성', Descript='유령이 나타나는 폐성에서의 보물을 둘러싼 모험.'),
        Scenario(SceID=4, Title='깊은 숲의 비밀', Descript='탐험가들이 숨겨진 숲 속 마을의 비밀을 밝혀낸다.'),
        Scenario(SceID=5, Title='시간의 균열', Descript='시간이 왜곡된 세계에서의 탈출을 위한 생존 게임.')
    ]

    scenario_nodes = [
        ScenarioNode(SNID='SN001', SceID=1, NType='0', NxtNd='SN002', Script='모험의 시작! 고대 도시를 향해 출발합니다.'),
        ScenarioNode(SNID='SN002', SceID=1, NType='0', NxtNd='SN003', Script='여정 중에 낯선 여행자를 만났습니다. 그가 당신에게 정보를 줍니다.'),
        ScenarioNode(SNID='SN003', SceID=1, NType='IT001', NxtNd='SN004', Script='당신은 길가에서 빛나는 철검을 발견했습니다.'),
        ScenarioNode(SNID='SN004', SceID=1, NType='IT005', NxtNd='SN005', Script='엘프의 부츠를 발견하며 민첩성이 증가합니다.'),
        ScenarioNode(SNID='SN005', SceID=1, NType='Goblin', NxtNd='SN006', Script='고블린이 길을 막습니다! 전투 준비를 하세요.'),
        ScenarioNode(SNID='SN006', SceID=1, NType='Orc', NxtNd='SN007', Script='다음 길목에서 오크를 마주쳤습니다. 힘을 모아 싸워야 합니다.'),
        ScenarioNode(SNID='SN007', SceID=1, NType='0', NxtNd='SN008', Script='전투를 마치고, 고대 도시의 입구에 도착합니다.'),
        ScenarioNode(SNID='SN008', SceID=1, NType='IT004', NxtNd='SN009', Script='당신은 용기의 방패를 발견하고 방어력이 증가합니다.'),
        ScenarioNode(SNID='SN009', SceID=1, NType='Dragon', NxtNd='SN010', Script='고대 도시의 보물을 지키는 드래곤과의 전투가 시작됩니다.'),
        ScenarioNode(SNID='SN010', SceID=1, NType='0', NxtNd=None, Script='모든 도전을 이겨내고 고대 도시의 비밀을 밝혔습니다.')
    ]

    sessions = [
        Sessions(
            SessionID='S0001', 
            SceID=1, 
            Username='user1', 
            Situation='Character encounters a monster in the forest.',
            Choices='Fight, Run', 
            Result='Character chooses to fight.', 
            LogTime=datetime.strptime('2024-12-20 18:30:00', '%Y-%m-%d %H:%M:%S')
        ),
        Sessions(
            SessionID='S0002', 
            SceID=2, 
            Username='user2', 
            Situation='Character finds a hidden treasure.',
            Choices='Take treasure, Leave it', 
            Result='Character takes the treasure.', 
            LogTime=datetime.strptime('2024-12-20 19:00:00', '%Y-%m-%d %H:%M:%S')
        )
    ]
    users = [
        User(nickname='user1', username='user1', password='password1', email='user1@example.com'),
        User(nickname='user2', username='user2', password='password2', email='user2@example.com'),
        User(nickname='user3', username='user3', password='password3', email='user3@example.com')
    ]

