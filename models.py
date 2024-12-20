from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'userlist'
    
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

    def __repr__(self):
        return f'<Item {self.ItName} (ID: {self.ItemID})>'


class PlayerCh(db.Model):
    __tablename__ = 'PlayerCh'

    CharID = db.Column(db.String(156), primary_key=True, nullable=False)
    Username = db.Column(db.String(150), db.ForeignKey('userlist.username'), nullable=False)
    PCName = db.Column(db.String(10), nullable=False)
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)
    
    INV1 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV2 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV3 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV4 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    INV5 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    AM1 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    AM2 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)
    AM3 = db.Column(db.String(5), db.ForeignKey('Item.ItemID'), nullable=True)

    # 관계 설정
    inventory_items_1 = db.relationship('Item', foreign_keys=[INV1], backref='playerch_inv1')
    inventory_items_2 = db.relationship('Item', foreign_keys=[INV2], backref='playerch_inv2')
    inventory_items_3 = db.relationship('Item', foreign_keys=[INV3], backref='playerch_inv3')
    inventory_items_4 = db.relationship('Item', foreign_keys=[INV4], backref='playerch_inv4')
    inventory_items_5 = db.relationship('Item', foreign_keys=[INV5], backref='playerch_inv5')
    accessory_items_1 = db.relationship('Item', foreign_keys=[AM1], backref='playerch_am1')
    accessory_items_2 = db.relationship('Item', foreign_keys=[AM2], backref='playerch_am2')
    accessory_items_3 = db.relationship('Item', foreign_keys=[AM3], backref='playerch_am3')

    def __repr__(self):
        return f'<PlayerCh {self.PCName} (User: {self.Username})>'


class Mob(db.Model):
    __tablename__ = 'Mob'

    MoName = db.Column(db.String(100), primary_key=True, nullable=False)
    NameKo = db.Column(db.String(100), nullable=False)
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Mob {self.MoName} ({self.NameKo})>'


class Scenario(db.Model):
    __tablename__ = 'Scenario'

    SceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(20), nullable=False)
    Descript = db.Column(db.String(100), nullable=True)

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

    SNID = db.Column(db.String(6), primary_key=True)
    SceID = db.Column(db.Integer, db.ForeignKey('Scenario.SceID'), nullable=False)
    NType = db.Column(db.String(100), nullable=False)
    NxtNd = db.Column(db.String(6), db.ForeignKey('ScenarioNode.SNID'), nullable=True)
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


class Sessions(db.Model):
    __tablename__ = 'Sessions'

    SessionID = db.Column(db.String(10), primary_key=True)
    SceID = db.Column(db.Integer, db.ForeignKey('Scenario.SceID'), nullable=False)
    Username = db.Column(db.String(150), db.ForeignKey('userlist.username'), nullable=False)
    Situation = db.Column(db.String(500), nullable=False)
    Choices = db.Column(db.String(500), nullable=True)
    Result = db.Column(db.String(500), nullable=True)
    LogTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    scenario = db.relationship('Scenario', backref=db.backref('sessions', lazy=True))

    def __repr__(self):
        return f"<Session {self.SessionID} - Username: {self.Username}, SceID: {self.SceID}, LogTime: {self.LogTime}>"

    def to_dict(self):
        return {
            'SessionID': self.SessionID,
            'Username': self.Username,
            'SceID': self.SceID,
            'Situation': self.Situation,
            'Choices': self.Choices,
            'Result': self.Result,
            'LogTime': self.LogTime.strftime('%Y-%m-%d %H:%M:%S')
        }


class Quest(db.Model):
    __tablename__ = 'Quest'

    QuestID = db.Column(db.String(5), primary_key=True, nullable=False)
    Ntype = db.Column(db.String(20), nullable=True)
    Script = db.Column(db.String(500), nullable=True)
    ATK = db.Column(db.Integer, default=0)
    DEF = db.Column(db.Integer, default=0)
    AGI = db.Column(db.Integer, default=0)

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
