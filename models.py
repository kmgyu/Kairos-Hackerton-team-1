from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False) # user id
    nickname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    

class Item(db.Model):
    __tablename__ = 'Item'

    # Primary Key (PK)
    ItemID = db.Column(db.String(5), primary_key=True, nullable=False)  # IT + 숫자 3자리 조합
    Name = db.Column(db.String(150), nullable=False)  # 아이템 이름
    ATKP = db.Column(db.Integer, default=0)  # 공격력 증가/감소값
    DEFP = db.Column(db.Integer, default=0)  # 방어력 증가/감소값
    AGIP = db.Column(db.Integer, default=0)  # 민첩성 증가/감소값
    ATKB = db.Column(db.Integer, default=0)  # 최종 공격력 보너스
    DEFB = db.Column(db.Integer, default=0)  # 최종 방어력 보너스
    AGIB = db.Column(db.Integer, default=0)  # 최종 민첩성 보너스

    def __init__(self, ItemID, Name, ATKP=0, DEFP=0, AGIP=0, ATKB=0, DEFB=0, AGIB=0):
        self.ItemID = ItemID
        self.Name = Name
        self.ATKP = ATKP
        self.DEFP = DEFP
        self.AGIP = AGIP
        self.ATKB = ATKB
        self.DEFB = DEFB
        self.AGIB = AGIB

    def __repr__(self):
        return f'<Item {self.Name} (ID: {self.ItemID})>'


class Character(db.Model):
    __tablename__ = 'Character'

    # Primary Key (PK)
    CharID = db.Column(db.String(156), primary_key=True, nullable=False)  # Username + 랜덤 숫자 6자리
    Username = db.Column(db.String(150), db.ForeignKey('User.username'), nullable=False)  # User 외래키
    Name = db.Column(db.String(10), nullable=False)  # 캐릭터 이름
    ATK = db.Column(db.Integer, default=0)  # 공격력
    DEF = db.Column(db.Integer, default=0)  # 방어력
    AGI = db.Column(db.Integer, default=0)  # 민첩성

    # 인벤토리 및 AM 슬롯
    INV1 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)  # 아이템 ID
    INV2 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV3 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV4 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV5 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    AM1 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    AM2 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    AM3 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)

    # 관계 설정 (Character - Item)
    inventory_items = relationship('Item', foreign_keys=[INV1, INV2, INV3, INV4, INV5, AM1, AM2, AM3], backref='character')

    def __repr__(self):
        return f'<Character {self.Name} (User: {self.Username})>'


class Mob(db.Model):
    __tablename__ = 'Mob'

    # Primary Key: 몬스터 이름 (PK)
    Name = db.Column(db.String(100), primary_key=True, nullable=False)
    # 몬스터의 한글 이름
    NameKo = db.Column(db.String(100), nullable=False)
    # 공격력 (기본값: 0)
    ATK = db.Column(db.Integer, default=0)
    # 방어력 (기본값: 0)
    DEF = db.Column(db.Integer, default=0)
    # 민첩성 (기본값: 0)
    AGI = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Mob {self.Name} ({self.NameKo})>'


class Scenario(db.Model):
    __tablename__ = 'Scenario'

    # Primary Key: 시나리오 아이디
    SceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 타이틀
    Title = db.Column(db.String(150), nullable=False)
    # 설명
    Description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Scenario {self.Title}>'

    def to_dict(self):
        """Scenario 인스턴스를 딕셔너리 형태로 변환"""
        return {
            'SceID': self.SceID,
            'Title': self.Title,
            'Description': self.Description
        }


class ScenarioNode(db.Model):
    __tablename__ = 'ScenarioNode'

    # Primary Key: 시나리오 노드 아이디
    SNID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Foreign Key: 시나리오 아이디
    SceID = db.Column(db.Integer, db.ForeignKey('Scenario.SceID'), nullable=False)
    # 시나리오 타입 (0: 대화, 1: 아이템 획득, 2: 몬스터 전투 등)
    Type = db.Column(db.Integer, nullable=False)
    # 다음 노드 (다음에 이어질 시나리오 노드)
    NxtNd = db.Column(db.Integer, db.ForeignKey('ScenarioNode.SNID'), nullable=True)
    # 스크립트 (해당 노드에서 보여줄 스크립트)
    Script = db.Column(db.String(500), nullable=True)

    # ForeignKey 관계 설정: 다음 노드와의 관계 설정
    next_node = db.relationship('ScenarioNode', remote_side=[SNID], backref=db.backref('previous_node', lazy='joined'))

    def __repr__(self):
        return f'<ScenarioNode {self.SNID} - SceID: {self.SceID}>'

    def to_dict(self):
        """ScenarioNode 인스턴스를 딕셔너리 형태로 변환"""
        return {
            'SNID': self.SNID,
            'SceID': self.SceID,
            'Type': self.Type,
            'NxtNd': self.NxtNd,
            'Script': self.Script
        }



class Session(db.Model):
    __tablename__ = 'Session'

    # 세션의 고유 ID (Primary Key)
    SessionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key: User 테이블의 id
    UserID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    
    # Foreign Key: Scenario 테이블의 SceID
    SceID = db.Column(db.Integer, db.ForeignKey('Scenario.SceID'), nullable=False)
    
    # 로그 아이디 (로그 기록을 위한 고유 ID)
    LogID = db.Column(db.Integer, autoincrement=True, nullable=False)
    
    # 스크립트 내용 (유저가 본 스크립트)
    Script = db.Column(db.String(500), nullable=True)
    
    # 로그 시간 (스크립트가 발생한 시간)
    LogTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 유저 정보 (ForeignKey 관계)
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    
    # 시나리오 정보 (ForeignKey 관계)
    scenario = db.relationship('Scenario', backref=db.backref('sessions', lazy=True))

    def __repr__(self):
        return f'<Session {self.SessionID} - UserID: {self.UserID}, SceID: {self.SceID}>'

    def to_dict(self):
        """Session 인스턴스를 딕셔너리 형태로 변환"""
        return {
            'SessionID': self.SessionID,
            'UserID': self.UserID,
            'SceID': self.SceID,
            'LogID': self.LogID,
            'Script': self.Script,
            'LogTime': self.LogTime
        }
