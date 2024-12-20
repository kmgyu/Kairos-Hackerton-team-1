from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    username = db.Column(db.String(150), primary_key=True)  
    nickname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Item(db.Model):
    __tablename__ = 'Item'

    ItemID = db.Column(db.String(5), primary_key=True, nullable=False) 
    ItName = db.Column(db.String(150), nullable=False)  
    ATKP = db.Column(db.Integer, default=0)
    DEFP = db.Column(db.Integer, default=0)
    AGIP = db.Column(db.Integer, default=0)
    ATKB = db.Column(db.Integer, default=0)
    DEFB = db.Column(db.Integer, default=0)
    AGIB = db.Column(db.Integer, default=0)

    def __init__(self, ItemID, ItName, ATKP=0, DEFP=0, AGIP=0, ATKB=0, DEFB=0, AGIB=0):
        self.ItemID = ItemID
        self.ItName = ItName
        self.ATKP = ATKP
        self.DEFP = DEFP
        self.AGIP = AGIP
        self.ATKB = ATKB
        self.DEFB = DEFB
        self.AGIB = AGIB

    def __repr__(self):
        return f'<Item {self.ItName} (ID: {self.ItemID})>'


class PlayerCh(db.Model):  
    __tablename__ = 'PlayerCh'

    CharID = db.Column(db.String(156), primary_key=True, nullable=False)
    Username = db.Column(db.String(150), db.ForeignKey('User.username'), nullable=False)
    PCName = db.Column(db.String(10), nullable=False) 
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)
    
    INV1 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV2 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV3 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV4 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    INV5 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    AM1 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    AM2 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)
    AM3 = db.Column(db.String(6), db.ForeignKey('Item.ItemID'), nullable=True)

    # 관계 설정
    inventory_items = db.relationship('Item', foreign_keys=[INV1, INV2, INV3, INV4, INV5, AM1, AM2, AM3], backref='character')

    def __repr__(self):
        return f'<PlayerCh {self.PCName} (User: {self.Username})>'


class Mob(db.Model):
    __tablename__ = 'Mob'

    Name = db.Column(db.String(100), primary_key=True, nullable=False) 
    NameKo = db.Column(db.String(100), nullable=False)
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Mob {self.Name} ({self.NameKo})>'


class Scenario(db.Model):
    __tablename__ = 'Scenario'

    SceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(150), nullable=False)
    Descript = db.Column(db.String(500), nullable=True) 

    def __repr__(self):
        return f'<Scenario {self.Title}>'

    def to_dict(self):
        return {
            'SceID': self.SceID,
            'Title': self.Title,
            'Descript': self.Descript
        }


class ScenarioNode(db.Model):
    __tablename__ = 'ScenarioNode'

    SNID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SceID = db.Column(db.Integer, db.ForeignKey('Scenario.SceID'), nullable=False)
    NType = db.Column(db.Integer, nullable=False) 
    NxtNd = db.Column(db.Integer, db.ForeignKey('ScenarioNode.SNID'), nullable=True)
    Script = db.Column(db.String(500), nullable=True)

    next_node = db.relationship('ScenarioNode', remote_side=[SNID], backref=db.backref('previous_node', lazy='joined'))

    def __repr__(self):
        return f'<ScenarioNode {self.SNID} - SceID: {self.SceID}>'

    def to_dict(self):
        return {
            'SNID': self.SNID,
            'SceID': self.SceID,
            'NType': self.NType,
            'NxtNd': self.NxtNd,
            'Script': self.Script
        }


class Session(db.Model):
    __tablename__ = 'Session'

    SessionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    SceID = db.Column(db.Integer, db.ForeignKey('Scenario.SceID'), nullable=False)
    LogID = db.Column(db.Integer, autoincrement=True, nullable=False)
    Script = db.Column(db.String(500), nullable=True)
    LogTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    Username = db.Column(db.String(150), db.ForeignKey('User.username'), nullable=False) 

    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    scenario = db.relationship('Scenario', backref=db.backref('sessions', lazy=True))

    def __repr__(self):
        return f'<Session {self.SessionID} - UserID: {self.UserID}, SceID: {self.SceID}>'

    def to_dict(self):
        return {
            'SessionID': self.SessionID,
            'UserID': self.UserID,
            'SceID': self.SceID,
            'LogID': self.LogID,
            'Script': self.Script,
            'LogTime': self.LogTime,
            'Username': self.Username
        }

class Quest(db.Model):
    __tablename__ = 'Quest'

    QuestID = db.Column(db.String(5), primary_key=True, nullable=False)
    Ntype = db.Column(db.String(20), nullable=True)
    Script = db.Column(db.String(500), nullable=True)
    ATK = db.Column(db.Integer, default=0, check=db.CheckConstraint('ATK BETWEEN 0 AND 5'))
    DEF = db.Column(db.Integer, default=0, check=db.CheckConstraint('DEF BETWEEN 0 AND 5'))
    AGI = db.Column(db.Integer, default=0, check=db.CheckConstraint('AGI BETWEEN 0 AND 5'))

    def __repr__(self):
        return f'<Quest {self.QuestID} - {self.Ntype}>'

    def to_dict(self):
        return {
            'QuestID': self.QuestID,
            'Ntype': self.Ntype,
            'Script': self.Script,
            'ATK': self.ATK,
            'DEF': self.DEF,
            'AGI': self.AGI
        }
